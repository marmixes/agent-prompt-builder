#!/usr/bin/env python3
"""check_evals.py - grade an agent's answers to the fixed eval requests.

Standard library only. Usage (from the repo root):
    python3 evals/check_evals.py evals/results/<run-name>

The results folder holds one file per case, named <case id>.md, with the agent's full
reply to that request (see evals/README.md). Exit code 0 = all cases pass.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "agent-prompt-builder", "scripts"))
import lint_prompt as lp  # noqa: E402

FENCE_RE = re.compile(r"^\s*```", re.M)


def has_block(text):
    return len(FENCE_RE.findall(text)) >= 2


def check_prompt(case, text):
    if not has_block(text):
        return False, "no prompt code block"
    blocks = lp.split_blocks(text)
    _, prompt = max(blocks, key=lambda b: len(b[1]))  # the main prompt is the longest block
    mode = case.get("lint")
    if mode:
        _, fs = lp.lint(prompt)
        bad = [f for f in fs if f["level"] == "error" or mode == "strict"]
        if bad:
            return False, "lint: " + ", ".join(sorted({f["code"] for f in bad}))
    return True, "prompt ok"


def check_question(text):
    if has_block(text):
        return False, "gave a prompt instead of a question"
    if "?" not in text and not re.search(r"\b(I need|please (confirm|send|tell)|confirm (that|whether)|tell me|send me|before I write)", text, re.I):
        return False, "no question asked"
    return True, "question ok"


def grade(case, text):
    exp = case["expect"]
    if exp == "prompt":
        ok, why = check_prompt(case, text)
    elif exp == "question":
        ok, why = check_question(text)
    else:  # prompt_or_question
        ok, why = check_question(text)
        if not ok:
            ok, why = check_prompt(case, text)
    if not ok:
        return False, why
    low = text.lower()
    for s in case.get("include_all", []):
        if s.lower() not in low:
            return False, f"missing '{s}'"
    anys = case.get("include_any", [])
    if anys and not any(s.lower() in low for s in anys):
        return False, "missing one of " + ", ".join(repr(s) for s in anys)
    for rx in case.get("exclude_regex", []):
        if re.search(rx, text, re.I):
            return False, f"contains forbidden pattern {rx}"
    return True, why


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    folder = argv[1]
    with open(os.path.join(HERE, "cases.json"), encoding="utf-8") as fh:
        cases = json.load(fh)
    passed = 0
    for case in cases:
        path = os.path.join(folder, case["id"] + ".md")
        if not os.path.exists(path):
            print(f"MISSING {case['id']}")
            continue
        with open(path, encoding="utf-8") as fh:
            ok, why = grade(case, fh.read())
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'}    {case['id']}: {why}")
    print(f"{passed}/{len(cases)} passed")
    return 0 if passed == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
