#!/usr/bin/env python3
"""lint_prompt.py - check an agent prompt against the agent-prompt-builder rules.

Standard library only (Python 3.8+). Usage:
    python3 lint_prompt.py PROMPT_FILE [--form auto|full|phased|medium|short|start|system|runtime]
                                       [--strict] [--template] [--json]
    cat prompt.txt | python3 lint_prompt.py -

If the file contains ``` fenced blocks, each block is checked as a separate prompt.
Exit code: 0 = no errors (warnings allowed unless --strict), 1 = errors found, 2 = usage error.

Forms (auto-detected):
  full     agent task with REQUIREMENTS: all fixed blocks required
  phased   big project with PHASES / FIRST DELIVERABLE
  medium   OpenCode / Hermes / local models: GOAL, STRICT RULES, SPECIFICS, DO, RISKS, LIMITS,
           WORKING BEHAVIOUR, DONE WHEN
  short    small local model, one-shot: Task + Output (+ Rules)
  start    short "Read PLAN.md ..." start prompt
  system   system prompt for an LLM app (ROLE, no task)
  runtime  prompt run on every input ({{SLOTS}} or SCHEMA)

The checks are deterministic and conservative: they catch missing structure and known
bad patterns. They cannot prove a prompt is correct; facts still need verification.
"""
import argparse
import json
import re
import sys

BLOCKS = [
    "ROLE", "GOAL", "TASK", "STRICT RULES", "CONTEXT", "SOURCES", "SPECIFICS", "STANDARDS",
    "APPROACH", "REQUIREMENTS", "RISKS", "CONSTRAINTS", "VERIFICATION", "BEFORE YOU FINISH",
    "WORKING BEHAVIOUR", "ROLLBACK", "PROGRESS", "OUTPUT", "STOP WHEN", "UNVERIFIED",
    "OPTIONS", "EXAMPLES", "DO", "LIMITS", "DONE WHEN", "AUTHORISATION", "SCHEMA", "INPUT",
    "RULES", "CAPABILITIES", "INTERFACE", "ENVIRONMENT AND PERMISSIONS", "RESEARCH", "PHASES",
    "BOUNDARIES", "FIRST DELIVERABLE", "SUGGESTIONS",
]
# longest names first so "STOP WHEN" wins over "STOP", "DONE WHEN" over "DO"
_NAMES = sorted(BLOCKS, key=len, reverse=True)
HEADER_RE = re.compile(r"^\s*(" + "|".join(re.escape(b) for b in _NAMES) + r")\b\s*(\([^)]*\))?\s*:?", re.I)

REQUIRED = {
    "full": ["ROLE", "GOAL", "STRICT RULES", "CONTEXT", "SOURCES", "SPECIFICS", "STANDARDS", "APPROACH", "REQUIREMENTS",
             "RISKS", "CONSTRAINTS", "VERIFICATION", "BEFORE YOU FINISH", "WORKING BEHAVIOUR",
             "PROGRESS", "OUTPUT", "STOP WHEN", "UNVERIFIED"],
    "phased": ["ROLE", "GOAL", "STRICT RULES", "SPECIFICS", "STANDARDS", "APPROACH", "RISKS",
               "PHASES", "CONSTRAINTS", "FIRST DELIVERABLE", "WORKING BEHAVIOUR", "OUTPUT", "STOP WHEN"],
    "medium": ["GOAL", "STRICT RULES", "SPECIFICS", "DO", "RISKS", "LIMITS", "WORKING BEHAVIOUR",
               "DONE WHEN"],
}
ALIASES = {"GOAL": ("GOAL", "TASK"), "CONSTRAINTS": ("CONSTRAINTS", "BOUNDARIES"),
           "STRICT RULES": ("STRICT RULES", "RULES"), "DONE WHEN": ("DONE WHEN", "STOP WHEN")}
FIX = {
    "ROLE": "one sentence naming the expertise",
    "GOAL": "'Your task is to <action> <what> so that <result>'",
    "STRICT RULES": "the mandatory rules (or 'STRICT RULES: as in AGENTS.md, plus: ...')",
    "SPECIFICS": "inputs, outputs, options with defaults, exclusions, data types, environment, compatibility target ('n/a' where not applicable)",
    "STANDARDS": "the quality bar (style guide, docstrings, KISS, dependencies)",
    "APPROACH": "options compared against criteria, or 'one obvious approach: <it>'",
    "REQUIREMENTS": "numbered, testable requirements",
    "RISKS": "edge cases and failure modes, each covered by a test",
    "CONSTRAINTS": "scope and forbidden actions, each with a reason",
    "VERIFICATION": "one 'Req N:' line per requirement",
    "BEFORE YOU FINISH": "self-check against VERIFICATION and STANDARDS",
    "WORKING BEHAVIOUR": "the block for the job type (references/working-behaviour.md)",
    "PROGRESS": "where steps are ticked, [x] only with proof",
    "OUTPUT": "the exact deliverable and report format",
    "STOP WHEN": "the done condition",
    "CONTEXT": "verified facts with sources and why the job matters",
    "SOURCES": "the repos/docs to use, or 'SOURCES: none needed'",
    "UNVERIFIED": "assumptions to check first, or 'UNVERIFIED: none'",
    "PHASES": "each phase with deliverable and verification criteria",
    "FIRST DELIVERABLE": "what phase 1 delivers before asking for approval",
    "DO": "numbered steps, each with '→ check: <command> → expect: <result>'",
    "LIMITS": "what may change and what must not, with reasons",
    "DONE WHEN": "the done condition",
}
XML_TAGS = {"example", "examples", "document", "documents", "source", "document_content", "file",
            "instructions", "context", "input", "output"}

HYPE = [
    "world-leading", "world-class", "world class", "flawless", "brilliant", "absolute best",
    "best in the world", "genius", "rockstar", "10x engineer", "perfect code",
]
IDENTITY_RE = re.compile(
    r"\byou are (claude|chatgpt|gpt[-\w.]*|gemini|llama|qwen|mistral|deepseek|a large language model|an ai language model)\b",
    re.I)
NO_CAVEATS_RE = re.compile(
    r"\bnever (include|add|give) (any )?(caveats|disclaimers)|\bnever explain\b|\bdo not explain anything\b", re.I)
RITUAL_RE = re.compile(
    r"think step[- ]by[- ]step|mentally walk through|walk through \d+ steps|consider (three|3|several) approaches and mentally",
    re.I)
SECRET_ASK_RE = re.compile(
    r"\b(cat|print|echo|show|display|paste|send|output|reveal|read)\b(?!\s*:)[^\n]{0,50}"
    r"(\.env\b|api[_ -]?keys?\b|secret(s)?\b|password(s)?\b|(api|access|auth|bot|bearer|github|refresh)[ _-]?tokens?\b|private key|\.key\b)",
    re.I)
NEGATION_RE = re.compile(r"\b(never|do not|don't|must not|no |not |without|only (the )?(variable|file) names?|names only)", re.I)
CAPS_RE = re.compile(r"\b(MUST|NEVER|ALWAYS|CRITICAL|IMPORTANT|MANDATORY)\b")
THOROUGH_RE = re.compile(r"\bbe thorough\b", re.I)
IF_IN_DOUBT_RE = re.compile(r"\bif in doubt,? use\b", re.I)
EVERYTHING_RE = re.compile(r"\b(fix|improve|do|refactor) everything\b", re.I)
ENDLESS_RE = re.compile(r"\bif (it|the result) can be improved,? you (must|should) improve", re.I)
NUM_ITEM_RE = re.compile(r"^\s*(\d+)[.)]\s+\S")
REQ_REF_RE = re.compile(r"\bReq(?:uirement)?s?\s*(\d+)(?:\s*[-–—]\s*(\d+))?", re.I)
PLACEHOLDER_RE = re.compile(r"</?([A-Za-z][^<>\n]{0,80})>")


def split_blocks(text):
    """Return [(start_line, prompt_text)] - fenced blocks if any, else the whole text."""
    lines = text.splitlines()
    blocks, cur, start, inside, fence = [], [], 0, False, None
    for i, line in enumerate(lines, 1):
        m = re.match(r"^\s*(```+|~~~+)", line)
        if m and not inside:
            inside, fence, cur, start = True, m.group(1)[:3], [], i + 1
            continue
        if inside and line.strip().startswith(fence):
            inside = False
            blocks.append((start, "\n".join(cur)))
            continue
        if inside:
            cur.append(line)
    return blocks if blocks else [(1, text)]


def header_of(line):
    """Block name if the line is a block header, else None."""
    m = HEADER_RE.match(line)
    if not m:
        return None
    name = m.group(1).upper()
    raw = line.strip()
    if name == "DO" and re.match(r"^\s*do\s+not\b", line, re.I):
        return None
    if name == "INPUT" and not raw[:5].isupper():
        return None  # "Input: ..." inside SPECIFICS / short form is a line, not a block
    # a header is written in capitals, or as "Name:" at the start of the line
    if raw[: len(name)].isupper() or re.match(r"^\s*" + re.escape(m.group(1)) + r"\s*(\([^)]*\))?\s*:", line, re.I):
        return name
    return None


def sections(lines):
    """Map block name -> list of (line_no, text); the header line is the first entry."""
    out, cur = {}, None
    for no, line in lines:
        name = header_of(line)
        if name:
            cur = name
            out.setdefault(cur, []).append((no, line))
            continue
        if cur:
            out[cur].append((no, line))
    return out


def detect_form(secs, text=""):
    keys = set(secs)
    if not keys and len(text.strip().splitlines()) <= 6 and re.search(r"\bread\s+\S+\.md\b", text, re.I):
        return "start"
    if "ROLE" in keys and not ({"TASK", "GOAL", "VERIFICATION", "STOP WHEN", "DONE WHEN", "REQUIREMENTS"} & keys):
        return "system"
    if not ({"STOP WHEN", "DONE WHEN", "PROGRESS", "WORKING BEHAVIOUR"} & keys) and (
            "SCHEMA" in keys or re.search(r"\{\{\s*\w+\s*\}\}", text)):
        return "runtime"
    if "REQUIREMENTS" in keys:
        return "full"
    if {"PHASES", "FIRST DELIVERABLE"} & keys:
        return "phased"
    if {"DO", "LIMITS"} & keys:
        return "medium"
    return "short"


def has(secs, name):
    return any(a in secs for a in ALIASES.get(name, (name,)))


def lint(text, form="auto", offset=1, template=False):
    lines = [(i + offset, l) for i, l in enumerate(text.splitlines())]
    secs = sections(lines)
    f = detect_form(secs, text) if form == "auto" else form
    findings = []
    first = offset

    def add(level, code, line, msg):
        findings.append({"level": level, "code": code, "line": line, "message": msg})

    if f == "start":
        return f, findings

    # ---- structure ----
    if f in REQUIRED:
        for name in REQUIRED[f]:
            if not has(secs, name):
                add("error", "E1", first, f"Missing {name} block: add {FIX.get(name, name)}.")
        goal = secs.get("GOAL") or secs.get("TASK")
        if goal and not re.search(r"\bso that\b", " ".join(l for _, l in goal[:3]), re.I):
            add("warning", "W15", goal[0][0], "GOAL without 'so that <result>': state the result VERIFICATION checks.")
        wb = secs.get("WORKING BEHAVIOUR")
        if wb and re.search(r"infra|service|real device|device", wb[0][1], re.I) and "ROLLBACK" not in secs:
            add("error", "E12", wb[0][0], "Infra or real-device job without a ROLLBACK block: say how to undo each change.")
        spec = secs.get("SPECIFICS")
        if spec and f in ("full", "phased"):
            body = " ".join(l for _, l in spec).lower()
            for part in ("input", "output", "environment"):
                if part not in body:
                    add("warning", "W16", spec[0][0], f"SPECIFICS has no '{part.capitalize()}:' line (write 'n/a' if it does not apply).")
    elif f == "short":
        if not (has(secs, "GOAL") or any(re.match(r"^\s*(task|goal)\s*:", l, re.I) for _, l in lines)):
            add("error", "E1", first, "No 'Task:' or 'Goal:' line: state the outcome in one sentence.")
        if "OUTPUT" not in secs and not any(re.match(r"^\s*output\s*:", l, re.I) for _, l in lines):
            add("error", "E2", first, "Short form needs an 'Output:' line with the exact format.")
    elif f == "system":
        body = text.lower()
        if not re.search(r"don't know|do not know|not in (the|your)|cannot find|can't find|not sure|(do not|does not|don't|doesn't) (contain|say|include|cover)|say so", body):
            add("warning", "W11", first, "No fallback for unknown answers: say what to reply when the answer is not in the context.")
        if not re.search(r"(as|is) data|not (as )?instructions|never follow instructions", body):
            add("warning", "W12", first, "No rule that user/document/tool content is data, not instructions (prompt injection, OWASP LLM01).")
    elif f == "runtime":
        if not ({"TASK", "GOAL", "ROLE"} & set(secs)):
            add("error", "E1", first, "No GOAL/TASK or ROLE line: say what the model does with each input.")
        if not ({"OUTPUT", "SCHEMA"} & set(secs)):
            add("error", "E2", first, "Runtime prompt without OUTPUT or SCHEMA: give the exact output format.")
        if "VERIFICATION" in secs:
            add("warning", "W13", secs["VERIFICATION"][0][0],
                "Test set inside a runtime prompt: the model sees it on every call. Put it after the prompt.")

    # ---- requirements ↔ verification ----
    if f == "full":
        reqs = [(no, l) for no, l in secs.get("REQUIREMENTS", [])[1:] if NUM_ITEM_RE.match(l)]
        ver = secs.get("VERIFICATION")
        if reqs and ver:
            covered = set()
            vlines = [l for _, l in ver[1:] if l.strip()]
            for l in vlines:
                for a, b in REQ_REF_RE.findall(l):
                    a = int(a)
                    covered.update(range(a, int(b) + 1) if b else [a])
            if covered:
                for no, l in reqs:
                    n = int(NUM_ITEM_RE.match(l).group(1))
                    if n not in covered:
                        add("error", "E3", no, f"Requirement {n} has no 'Req {n}:' line in VERIFICATION.")
            elif len(vlines) < len(reqs):
                add("error", "E3", ver[0][0], f"{len(reqs)} requirements but only {len(vlines)} verification line(s).")
    if f == "medium":
        for no, l in secs.get("DO", [])[1:]:
            if NUM_ITEM_RE.match(l) and not re.search(r"\bcheck\b|\bexpect\b|→|->", l, re.I):
                add("warning", "W6", no, "DO step without a check: add '→ check: <command> → expect: <result>'.")
    if f in ("phased", "full") and "PHASES" in secs:
        ph = secs.get("PHASES", [])
        steps = [(no, l) for no, l in ph[1:] if NUM_ITEM_RE.match(l) or re.match(r"^\s*-?\s*phase\b", l, re.I)]
        for no, l in steps:
            if not re.search(r"verif|check|test|proof|criteria|deliverable|approval|\byes\b", l, re.I):
                add("warning", "W17", no, "Phase without verification criteria: say how its result is checked.")

    # ---- line patterns ----
    seen = {}
    for no, l in lines:
        s = l.strip()
        if not s:
            continue
        if IDENTITY_RE.search(l):
            add("error", "E5", no, "Model-identity line: often false on other models; replace with one expertise ROLE sentence.")
        if NO_CAVEATS_RE.search(l):
            add("error", "E6", no, "Forbids caveats/explanations: this hides errors. Ask to report what was not verified.")
        if SECRET_ASK_RE.search(l) and not NEGATION_RE.search(l):
            add("error", "E4", no, "Looks like it asks to read, print or send a secret. Check by variable or file name only.")
        if ENDLESS_RE.search(l):
            add("error", "E7", no, "Open-ended 'improve if possible': no stop condition. Use measurable STOP WHEN criteria.")
        if not template and f not in ("runtime",):
            for m in PLACEHOLDER_RE.finditer(l):
                tag = m.group(1).split()[0].strip("/").lower()
                if tag not in XML_TAGS:
                    add("error", "E11", no, f"Unfilled placeholder '{m.group(0)}': fill it, or mark the value UNVERIFIED.")
        low = l.lower()
        for h in HYPE:
            if h in low:
                add("warning", "W2", no, f"Hype word '{h}': replace with a concrete STANDARDS item.")
        if RITUAL_RE.search(l):
            add("warning", "W4", no, "Hidden reasoning ritual: write it as APPROACH / RISKS / BEFORE YOU FINISH checks instead.")
        if THOROUGH_RE.search(l):
            add("warning", "W8", no, "'Be thorough': say what thoroughness means for this task.")
        if IF_IN_DOUBT_RE.search(l):
            add("warning", "W7", no, "'If in doubt, use <tool>' causes over-use: say when the tool is appropriate.")
        if EVERYTHING_RE.search(l):
            add("warning", "W9", no, "'... everything': one task per prompt.")
        if not header_of(l):
            caps = CAPS_RE.findall(l)
            if caps:
                add("warning", "W1", no, f"Shouting ({', '.join(sorted(set(caps)))}): use calm, firm wording with a reason.")
        if re.match(r"^\s*-?\s*do not\b", l, re.I) and not re.search(r"because|—|--|\bas\b|\bsince\b|\bso that\b", l, re.I):
            add("warning", "W3", no, "'Do not' without a reason: add '— because <reason>'.")
        if len(s) > 25 and not header_of(l):
            key = re.sub(r"\s+", " ", s.lower())
            if key in seen:
                add("warning", "W10", no, f"Same instruction repeated (first at line {seen[key]}): state it once.")
            else:
                seen[key] = no

    for no, l in secs.get("CONTEXT", [])[1:]:
        s = l.strip()
        if s.startswith("-") and not re.search(r"source|why it matters|\(owner|owner's|UNVERIFIED|https?://", s, re.I):
            add("warning", "W5", no, "CONTEXT fact without a source: add '(source: <file or URL>)' or mark UNVERIFIED.")

    n = sum(1 for _, l in lines if l.strip())
    if f == "full" and n > 160:
        add("warning", "W14", first, f"{n} lines: long for one task; split it, or use the phased form with a plan file.")
    if f == "medium" and n > 60:
        add("warning", "W14", first, f"{n} lines: long for a mid-size or local model; split the job into smaller prompts.")
    return f, findings


def main(argv=None):
    p = argparse.ArgumentParser(description="Lint an agent prompt against the agent-prompt-builder rules.")
    p.add_argument("file", help="prompt file, or - for stdin")
    p.add_argument("--form", default="auto",
                   choices=["auto", "full", "phased", "medium", "short", "start", "system", "runtime"])
    p.add_argument("--strict", action="store_true", help="warnings also fail")
    p.add_argument("--template", action="store_true", help="allow unfilled <placeholders> (for templates)")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    a = p.parse_args(argv)
    try:
        text = sys.stdin.read() if a.file == "-" else open(a.file, encoding="utf-8").read()
    except OSError as e:
        print(f"cannot read {a.file}: {e}", file=sys.stderr)
        return 2
    results, failed = [], False
    for start, block in split_blocks(text):
        form, fs = lint(block, a.form, start, a.template)
        results.append({"start_line": start, "form": form, "findings": fs})
        if any(x["level"] == "error" for x in fs) or (a.strict and fs):
            failed = True
    if a.json:
        print(json.dumps({"ok": not failed, "prompts": results}, indent=2))
    else:
        for r in results:
            errs = sum(1 for x in r["findings"] if x["level"] == "error")
            warns = len(r["findings"]) - errs
            print(f"prompt at line {r['start_line']} ({r['form']} form): {errs} error(s), {warns} warning(s)")
            for x in r["findings"]:
                print(f"  {x['level'].upper():7} {x['code']} line {x['line']}: {x['message']}")
        print("PASS" if not failed else "FAIL")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
