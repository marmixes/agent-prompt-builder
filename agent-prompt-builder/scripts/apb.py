#!/usr/bin/env python3
"""apb - agent prompt builder on the command line.

Type what you need in your own words (spelling mistakes are fine). apb shows what it
understood, the best plan, any questions with default answers, and what is UNVERIFIED.
You approve once (or type corrections and answers in one line); it then writes the final
prompt, lints it, fixes lint errors itself (at most 2 rounds) and saves it.

Works with any OpenAI-compatible chat API: llama.cpp, vLLM, Ollama, LM Studio, OpenAI,
OpenRouter. Python 3.8+, standard library only.

    python3 apb.py "make my fastapi app fastr, its slow on /search"
    python3 apb.py --file goal.txt --out prompts/
    echo "goal" | python3 apb.py -

Settings (flag or environment variable):
    --base-url  APB_BASE_URL   default http://127.0.0.1:8080/v1
    --model     APB_MODEL      default "local" (llama.cpp ignores the name)
    API key     APB_API_KEY    (or OPENAI_API_KEY); read from the environment only, never printed
Exit codes: 0 prompt saved, 1 error, 3 stopped with questions that need your answer, 4 cancelled.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import lint_prompt  # noqa: E402

REFERENCES = ["SKILL.md", "templates/general-template.md", "references/agent-formats.md",
              "references/task-types.md", "references/working-behaviour.md",
              "references/prompt-patterns.md", "references/security-prompts.md"]

PLAN_INSTRUCTIONS = """You are running the agent-prompt-builder procedure as a command-line tool.
The owner's goal may contain spelling mistakes or loose wording: correct them silently and restate the real goal.
There are no project files; facts you cannot check are UNVERIFIED. Do not write the prompt yet.
Reply with exactly these sections and nothing else:

UNDERSTOOD: <the goal in one corrected sentence>
TARGET: <agent or model> | <form: full, medium, short, system or runtime>
TYPE: <task-type preset name> | <job type: read-only, code changes, infra, real devices, security, publish>
PLAN:
1. <step of the best approach>
SUGGESTIONS:
- <an improvement the owner did not ask for, with its trade-off> (added only if the owner says yes)
QUESTIONS:
- <question> [default: <the answer you will use if the owner just approves>]
- <question that has no safe default> [blocking]
UNVERIFIED:
- <assumption to check>
DELIVERY: <how the owner gives the prompt to the agent>

Write "SUGGESTIONS: none", "QUESTIONS: none" or "UNVERIFIED: none" when empty. Mark a question [blocking] only when any guess
could produce the wrong prompt: two different readings of the goal, a conflict with the owner's rules,
a security test without confirmed authorisation and scope, or a request that breaks a hard rule
(then say which rule, and what you can write instead)."""

WRITE_INSTRUCTIONS = """Now write the final reply, following SKILL.md: the prompt in ONE fenced code block,
then at most 3 lines (delivery, UNVERIFIED items, owner decisions). Use the form from
templates/general-template.md that fits the target (full form for strong agents, medium form for OpenCode,
Hermes, OpenClaw and local models) with EVERY block, the WORKING BEHAVIOUR lines for the job type, and
ROLLBACK for infra or real-device jobs. Use the approved plan and the owner's answers; for questions the
owner did not answer, use the stated default. Include only the suggestions the owner accepted. Every
requirement needs a 'Req N:' line in VERIFICATION. Fill every <placeholder>; unknown values are marked
UNVERIFIED. If the request breaks a hard rule, write the safe alternative the plan named."""

FIX_INSTRUCTIONS = """The lint found these problems in your prompt:
{findings}
Fix all ERROR items (and warnings where sensible) and send the whole corrected reply again, same format."""


class ApiError(Exception):
    pass


def load_skill():
    parts = []
    for rel in REFERENCES:
        path = os.path.join(SKILL_DIR, rel)
        try:
            with open(path, encoding="utf-8") as fh:
                parts.append(f"<file path=\"{rel}\">\n{fh.read()}\n</file>")
        except OSError:
            continue  # a missing reference is not fatal
    if not parts:
        raise ApiError(f"cannot read SKILL.md in {SKILL_DIR}")
    return "You follow this skill exactly.\n\n" + "\n\n".join(parts)


def chat(cfg, messages):
    body = {"model": cfg.model, "messages": messages, "max_tokens": cfg.max_tokens}
    if cfg.temperature is not None:
        body["temperature"] = cfg.temperature
    req = urllib.request.Request(cfg.base_url.rstrip("/") + "/chat/completions",
                                 data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    if cfg.api_key:
        req.add_header("Authorization", "Bearer " + cfg.api_key)
    try:
        with urllib.request.urlopen(req, timeout=cfg.timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        raise ApiError(f"API returned HTTP {e.code}: {detail}") from None
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise ApiError(f"cannot reach {cfg.base_url}: {e}") from None
    except ValueError:
        raise ApiError("API reply is not JSON") from None
    try:
        text = data["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        raise ApiError("API reply has no choices[0].message.content") from None
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()  # reasoning models
    if not text:
        raise ApiError("model returned an empty reply")
    return text


def section(text, name):
    m = re.search(rf"^{name}:[ \t]*(.*?)(?=^\s*[A-Z][A-Z ]+:|\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def parse_plan(text):
    q = section(text, "QUESTIONS")
    questions = [] if q.lower() in ("", "none") else [
        l.strip()[1:].strip() for l in q.splitlines() if l.strip().startswith("-")]
    return {"understood": section(text, "UNDERSTOOD"),
            "questions": questions,
            "blocking": [x for x in questions if "[blocking]" in x.lower()]}


def main_prompt(reply):
    blocks = lint_prompt.split_blocks(reply)
    if len(blocks) == 1 and blocks[0][0] == 1 and "```" not in reply:
        return None
    return max(blocks, key=lambda b: len(b[1]))[1]


def slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:50] or "prompt"


def build(cfg, goal, ask=input, out=print):
    system = load_skill()
    msgs = [{"role": "system", "content": system},
            {"role": "user", "content": PLAN_INSTRUCTIONS + "\n\nOWNER'S GOAL:\n" + goal}]
    plan_text = chat(cfg, msgs)
    plan = parse_plan(plan_text)
    out("\n" + plan_text + "\n")
    msgs.append({"role": "assistant", "content": plan_text})

    if cfg.yes:
        if plan["blocking"]:
            out("Stopped: these questions need your answer (no safe default):")
            for q in plan["blocking"]:
                out("  - " + q)
            return 3, plan_text
        answer = "y"
    else:
        answer = ask("Approve? [y] yes / type corrections or answers in one line / [n] cancel: ").strip()
        if answer.lower() in ("n", "no", "cancel"):
            out("Cancelled.")
            return 4, None
        if plan["blocking"] and answer.lower() in ("", "y", "yes"):
            out("These questions have no safe default; answer them in one line:")
            for q in plan["blocking"]:
                out("  - " + q)
            answer = ask("Answers: ").strip()
            if not answer:
                return 3, plan_text
    owner = "Approved; use the defaults." if answer.lower() in ("", "y", "yes") else \
        "Approved with these corrections and answers: " + answer
    msgs.append({"role": "user", "content": owner + "\n\n" + WRITE_INSTRUCTIONS})

    reply = chat(cfg, msgs)
    for round_no in range(cfg.fix_rounds + 1):
        prompt = main_prompt(reply)
        if prompt is None:
            break  # the model answered without a prompt (e.g. a refusal or a question)
        form, findings = lint_prompt.lint(prompt)
        errors = [f for f in findings if f["level"] == "error"]
        if not errors or round_no == cfg.fix_rounds:
            break
        listing = "\n".join(f"- {f['level'].upper()} {f['code']}: {f['message']}" for f in findings)
        out(f"lint found {len(errors)} error(s); asking the model to fix them (round {round_no + 1})")
        msgs += [{"role": "assistant", "content": reply},
                 {"role": "user", "content": FIX_INSTRUCTIONS.format(findings=listing)}]
        reply = chat(cfg, msgs)

    prompt = main_prompt(reply)
    status = "no prompt in reply"
    if prompt is not None:
        _, findings = lint_prompt.lint(prompt)
        errs = sum(1 for f in findings if f["level"] == "error")
        status = "lint PASS" if errs == 0 else f"lint FAIL ({errs} error(s) left)"
    os.makedirs(cfg.out, exist_ok=True)
    path = os.path.join(cfg.out, f"{dt.date.today().isoformat()}-{slug(plan['understood'] or goal)}.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"<!-- goal: {goal.strip()[:300]} -->\n<!-- {status} -->\n\n{reply}\n")
    out("\n" + reply + "\n")
    out(f"saved: {path} ({status})")
    return (1 if status.startswith("lint FAIL") else 0), reply


def parse_args(argv):
    p = argparse.ArgumentParser(description="Build an accurate agent prompt from your goal (one approval).")
    p.add_argument("goal", nargs="*", help="your goal in your own words, or - to read stdin")
    p.add_argument("--file", help="read the goal from this file")
    p.add_argument("--base-url", default=os.environ.get("APB_BASE_URL", "http://127.0.0.1:8080/v1"))
    p.add_argument("--model", default=os.environ.get("APB_MODEL", "local"))
    p.add_argument("--out", default=os.environ.get("APB_OUT", "prompts"), help="folder for saved prompts")
    p.add_argument("--temperature", type=float, default=None)
    p.add_argument("--max-tokens", type=int, default=8192)
    p.add_argument("--timeout", type=int, default=600, help="seconds per API call")
    p.add_argument("--fix-rounds", type=int, default=2, help="max lint-fix rounds")
    p.add_argument("--yes", action="store_true", help="approve automatically; stop if a question has no default")
    a = p.parse_args(argv)
    a.api_key = os.environ.get("APB_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""
    return a


def main(argv=None):
    cfg = parse_args(sys.argv[1:] if argv is None else argv)
    if cfg.file:
        with open(cfg.file, encoding="utf-8") as fh:
            goal = fh.read()
    elif cfg.goal == ["-"]:
        goal = sys.stdin.read()
    else:
        goal = " ".join(cfg.goal)
    if not goal.strip():
        print("Give a goal: apb.py \"what you need\" (see --help)", file=sys.stderr)
        return 1
    try:
        code, _ = build(cfg, goal)
        return code
    except ApiError as e:
        print("error: " + str(e), file=sys.stderr)
        return 1
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.", file=sys.stderr)
        return 4


if __name__ == "__main__":
    sys.exit(main())
