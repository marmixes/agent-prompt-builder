```
ROLE: You are a senior Python backend engineer experienced in FastAPI and pytest.

GOAL: Your task is to add a GET /health endpoint to the FastAPI app in app/main.py, with one test, so that the endpoint returns HTTP 200 and the JSON body {"status":"ok"} and the test passes.

STRICT RULES (mandatory; if you cannot follow one, stop and report which one)
1. Do exactly the GOAL; change nothing outside SCOPE.
2. Before changing anything, record the current state (Python and FastAPI versions, existing test results) and report it.
3. Research before deciding: read the files and the SOURCES first; never make a claim about a file you have not read.
4. Every requirement must pass its VERIFICATION check; show the command, exit code and key output line.
5. Never guess and never promise what you cannot verify: report it as UNVERIFIED.
6. Never mark a step done without proof.
7. Never read or print secrets; never touch other projects, services or settings outside SCOPE.
8. Stop exactly at STOP WHEN; no extra work and no unrequested changes.

CONTEXT
- The app entry point is app/main.py (source: owner's message).
- Why it matters: a health endpoint lets monitoring and deploy checks confirm the app is running.
- FastAPI's documented test method is TestClient from fastapi.testclient, which needs httpx installed (source: https://fastapi.tiangolo.com/tutorial/testing/).

SOURCES (use these; do not substitute others)
- https://fastapi.tiangolo.com/tutorial/testing/ — how to write the test with TestClient and pytest.

SPECIFICS
- Inputs: GET request to /health, no parameters, no authentication.
- Outputs: HTTP 200, JSON body exactly {"status":"ok"}.
- Options: n/a
- Exclusions: all existing routes, models, settings and tests stay unchanged.
- Data types / formats: response body is a JSON object with one key "status" whose value is the string "ok".
- Environment: the project's existing Python environment; the FastAPI instance name in app/main.py is UNVERIFIED (read the file).
- Compatibility target: the FastAPI and Python versions already installed in the project.

STANDARDS
- Follow the code style already used in app/main.py; PEP 8; type hints; a short docstring on the endpoint function and on the test; KISS; no new dependencies without approval.

APPROACH
- One obvious approach: add a route decorator on the existing FastAPI instance in app/main.py and a pytest test using TestClient, placed where the project's existing tests live (or tests/test_health.py if none exist).

REQUIREMENTS
1. GET /health returns status 200.
2. The JSON body of GET /health equals {"status":"ok"} exactly.
3. A test in the project's test folder asserts requirements 1 and 2 using TestClient.
4. All previously existing tests still pass.

RISKS
- httpx missing, so TestClient fails to import → covered by Req 3 (report the import error; do not install without approval).
- The route conflicts with an existing /health route or a catch-all route → covered by Req 2.
- The test passes only because it was written to match a wrong implementation → covered by Req 3 (the test asserts the literal expected body and status).

CONSTRAINTS
- Scope: app/main.py and one new or existing test file in the project's test folder.
- Do not: edit or delete existing tests — because they define current behaviour.
- Do not: add authentication, logging, dependency checks or extra fields to the response — because the GOAL asks for the fixed body only.
- Dependencies: none new; if httpx is missing, ask the owner.

VERIFICATION (one line per requirement)
- Req 1: run the new test with pytest (for example `python -m pytest -q -k health`) → exit code 0 and the test asserting status 200 passes.
- Req 2: same test run → the assertion `response.json() == {"status": "ok"}` passes.
- Req 3: `git diff --stat` (or file listing if not a git repo) → shows the new test using TestClient against /health.
- Req 4: full suite `python -m pytest -q` → exit code 0, same or higher pass count than the baseline.

WORKING BEHAVIOUR (code in one project)
1. Read my messages for meaning: interpret spelling or grammar mistakes without changing what I asked.
2. This approval covers the whole plan in this prompt; work without asking again, on a new branch if the project uses git, never on main.
3. If you see a better way, propose it with its trade-offs; apply it only after my yes.
4. If a check fails: trace, debug, fix, retest; after 3 failed attempts at a step, record it as [!] and move on.
5. Ask me only for: a new dependency, anything outside SCOPE, deleting files.
6. Budget: 30 minutes, 3 attempts per step.
7. At the end: an independent review (fresh reviewer, no prior context), then the report.

BEFORE YOU FINISH
- Check every requirement against VERIFICATION and the work against STANDARDS; criticise your own result, fix every flaw found; report anything not checked as UNVERIFIED.

PROGRESS
- Track steps in your replies (no file; the job is small) with [ ] todo, [~] in progress, [x] done, [!] failed, [?] blocked; [x] only with command, exit code and key output line.

OUTPUT: the diff of app/main.py and the test file, the baseline and final test output (command, exit code, key line), then the limitations.

STOP WHEN: Req 1-4 pass and the report is delivered.

UNVERIFIED: the FastAPI instance name in app/main.py; whether pytest and httpx are installed; the project's test folder and test command.
```
Delivery: paste into Claude Code, started in the project root.
UNVERIFIED: FastAPI instance name, pytest/httpx installed, test folder (the agent checks them first).
Owner decision: none blocking; defaults used (new branch if git, 30 min budget).
Suggestion, not included: a readiness check (database etc.) later, as a separate task.
