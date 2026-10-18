#!/usr/bin/env python3
"""run_apb.py - run the 12 eval cases through apb.py (auto-approve) and save the replies.

    APB_BASE_URL=http://127.0.0.1:8080/v1 python3 evals/run_apb.py <run-name>
    python3 evals/check_evals.py evals/results/<run-name>

Same settings as apb.py (APB_BASE_URL, APB_MODEL, APB_API_KEY). A case where apb stops
with questions that have no safe default is saved as those questions.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "agent-prompt-builder", "scripts"))
import apb  # noqa: E402


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    run = argv[1]
    out_dir = os.path.join(HERE, "results", run)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(HERE, "cases.json"), encoding="utf-8") as fh:
        cases = json.load(fh)
    cfg = apb.parse_args(["--yes", "--out", os.path.join(out_dir, ".prompts"), *argv[2:]])
    for case in cases:
        print(f"== {case['id']}", flush=True)
        try:
            code, text = apb.build(cfg, case["request"], out=lambda *_: None)
        except apb.ApiError as e:
            print(f"   error: {e}")
            continue
        if code == 3:
            qs = [q.replace("[blocking]", "").strip() for q in apb.parse_plan(text)["blocking"]]
            text = "Before I write this prompt I need your answer:\n" + "\n".join("- " + q for q in qs)
        with open(os.path.join(out_dir, case["id"] + ".md"), "w", encoding="utf-8") as fh:
            fh.write((text or "") + "\n")
        print(f"   exit {code}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
