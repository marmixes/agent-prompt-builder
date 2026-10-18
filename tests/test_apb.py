"""Tests for agent-prompt-builder/scripts/apb.py against a fake OpenAI-compatible server.

Run from the repo root:  python3 -m unittest discover -s tests -v
"""
import io
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "agent-prompt-builder", "scripts")
sys.path.insert(0, SCRIPTS)
import apb  # noqa: E402

PLAN = """UNDERSTOOD: Add a GET /health endpoint to the FastAPI app.
SUGGESTIONS: none
TARGET: Claude Code | full
TYPE: Build
PLAN:
1. Add the endpoint and a test.
QUESTIONS:
- Which port? [default: 8000]
UNVERIFIED:
- port 8000
DELIVERY: one message to Claude Code."""

PLAN_BLOCKING = PLAN.replace("- Which port? [default: 8000]", "- What does 'faster' mean for you? [blocking]")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from test_lint import GOOD_FULL  # noqa: E402

GOOD = "```\n" + GOOD_FULL + "```"
BAD = GOOD.replace("- Req 2: hashes unchanged after --dry-run", "")


class Fake(BaseHTTPRequestHandler):
    replies = []
    seen = []

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        Fake.seen.append({"body": body, "auth": self.headers.get("Authorization")})
        if not Fake.replies:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"no more replies")
            return
        content = Fake.replies.pop(0)
        out = json.dumps({"choices": [{"message": {"role": "assistant", "content": content}}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *a):
        pass


class TestApb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), Fake)
        cls.url = f"http://127.0.0.1:{cls.server.server_port}/v1"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        Fake.replies, Fake.seen = [], []
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def cfg(self, *extra):
        return apb.parse_args(["--base-url", self.url, "--out", self.tmp.name, *extra])

    def test_one_approval_lint_fix_and_save(self):
        Fake.replies = [PLAN, BAD, GOOD]
        answers = iter(["y"])
        lines = []
        code, reply = apb.build(self.cfg(), "add helth endpoint to my fastapi app", ask=lambda _: next(answers),
                                out=lines.append)
        self.assertEqual(code, 0)
        self.assertIn("Req 2", reply)
        self.assertEqual(len(Fake.seen), 3)  # plan, write, one fix round
        self.assertTrue(any("lint found 1 error" in l for l in lines))
        saved = os.listdir(self.tmp.name)
        self.assertEqual(len(saved), 1)
        with open(os.path.join(self.tmp.name, saved[0]), encoding="utf-8") as fh:
            self.assertIn("lint PASS", fh.read())
        # the skill is sent as the system message, the goal in the first user message
        first = Fake.seen[0]["body"]["messages"]
        self.assertEqual(first[0]["role"], "system")
        self.assertIn("Hard rules", first[0]["content"])
        self.assertIn("templates/general-template.md", first[0]["content"])
        self.assertIn("SUGGESTIONS:", first[1]["content"])
        self.assertIn("add helth endpoint", first[1]["content"])

    def test_corrections_are_passed_in_one_line(self):
        Fake.replies = [PLAN, GOOD]
        apb.build(self.cfg(), "goal", ask=lambda _: "port is 9000, target OpenCode", out=lambda *_: None)
        last_user = Fake.seen[1]["body"]["messages"][-1]["content"]
        self.assertIn("port is 9000, target OpenCode", last_user)

    def test_cancel(self):
        Fake.replies = [PLAN]
        code, _ = apb.build(self.cfg(), "goal", ask=lambda _: "n", out=lambda *_: None)
        self.assertEqual(code, 4)
        self.assertEqual(os.listdir(self.tmp.name), [])

    def test_yes_stops_on_blocking_question(self):
        Fake.replies = [PLAN_BLOCKING]
        lines = []
        code, _ = apb.build(self.cfg("--yes"), "make my app faster", out=lines.append)
        self.assertEqual(code, 3)
        self.assertTrue(any("[blocking]" in l for l in lines))
        self.assertEqual(len(Fake.seen), 1)

    def test_interactive_blocking_question_needs_answer(self):
        Fake.replies = [PLAN_BLOCKING, GOOD]
        answers = iter(["y", "the /search endpoint, under 1 s"])
        code, _ = apb.build(self.cfg(), "make my app faster", ask=lambda _: next(answers), out=lambda *_: None)
        self.assertEqual(code, 0)
        self.assertIn("under 1 s", Fake.seen[1]["body"]["messages"][-1]["content"])

    def test_lint_still_failing_after_rounds_exits_1(self):
        Fake.replies = [PLAN, BAD, BAD, BAD]
        code, _ = apb.build(self.cfg("--yes"), "goal", out=lambda *_: None)
        self.assertEqual(code, 1)
        self.assertEqual(len(Fake.seen), 4)  # plan + write + 2 fix rounds

    def test_think_tags_are_stripped(self):
        Fake.replies = ["<think>hidden reasoning</think>" + PLAN, GOOD]
        lines = []
        apb.build(self.cfg("--yes"), "goal", out=lines.append)
        self.assertFalse(any("hidden reasoning" in l for l in lines))

    def test_api_key_sent_but_never_printed(self):
        Fake.replies = [PLAN, GOOD]
        env = dict(os.environ, APB_API_KEY="sk-test-SECRET-123")
        p = subprocess.run([sys.executable, "-I", os.path.join(SCRIPTS, "apb.py"), "--yes",
                            "--base-url", self.url, "--out", self.tmp.name, "add health endpoint"],
                           capture_output=True, text=True, env=env, timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(Fake.seen[0]["auth"], "Bearer sk-test-SECRET-123")
        self.assertNotIn("SECRET-123", p.stdout + p.stderr)
        for f in os.listdir(self.tmp.name):
            with open(os.path.join(self.tmp.name, f), encoding="utf-8") as fh:
                self.assertNotIn("SECRET-123", fh.read())

    def test_server_error_is_reported(self):
        Fake.replies = []
        p = subprocess.run([sys.executable, "-I", os.path.join(SCRIPTS, "apb.py"), "--yes",
                            "--base-url", self.url, "--out", self.tmp.name, "goal"],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 1)
        self.assertIn("HTTP 500", p.stderr)

    def test_unreachable_server(self):
        p = subprocess.run([sys.executable, "-I", os.path.join(SCRIPTS, "apb.py"), "--yes", "--timeout", "5",
                            "--base-url", "http://127.0.0.1:9/v1", "--out", self.tmp.name, "goal"],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 1)
        self.assertIn("cannot reach", p.stderr)


if __name__ == "__main__":
    unittest.main()
