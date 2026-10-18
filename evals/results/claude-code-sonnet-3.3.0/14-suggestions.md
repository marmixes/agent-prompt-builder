```
ROLE: You are a senior Python web engineer experienced in Flask, account authentication flows and transactional email.

GOAL: Your task is to add a password reset by email to my existing Flask app so that a user who forgot their password can request a reset link by email, open it, set a new password, and log in with it, with every REQUIREMENT passing its VERIFICATION check.

STRICT RULES (mandatory; if you cannot follow one, stop and report which one)
1. Do exactly the GOAL; change nothing outside SCOPE.
2. Before changing anything, record the current state (Python and Flask versions, installed extensions, test results, git status) and report it.
3. Research before deciding: read the app's files and the SOURCES first; never make a claim about a file you have not read.
4. Every requirement must pass its VERIFICATION check; show the command, exit code and key output line.
5. Never guess and never promise what you cannot verify: report it as UNVERIFIED.
6. Never mark a step done without proof.
7. Never read or print secrets (.env files, SMTP passwords, SECRET_KEY values); refer to them by variable name only; never touch other projects, services or settings outside SCOPE.
8. Stop exactly at STOP WHEN; no extra work and no unrequested changes.

CONTEXT
- The app is an existing Flask application; its location, structure, user model, authentication method, database and email setup were not available when this prompt was written (UNVERIFIED until you read the project).
- Why it matters: the reset flow must reuse the app's own user model, password hashing and email configuration instead of adding parallel ones.

SOURCES (use these; do not substitute others)
- https://flask.palletsprojects.com/ — Flask documentation (routes, templates, config, testing); confirm the installed version's docs.
- https://itsdangerous.palletsprojects.com/ — itsdangerous (installed with Flask) for signed, expiring tokens: URLSafeTimedSerializer.dumps and loads(max_age=...), SignatureExpired and BadSignature exceptions. UNVERIFIED: confirm the API on the installed version.
- The app's own documentation, README, and any existing email or auth code, if present.

SPECIFICS
- Inputs: the user's email address (form field), the reset token from the link, the new password (form field, entered twice).
- Outputs: a "forgot password" page, a reset page, an email containing the reset link, and updated password hash in the existing user store.
- Options: token lifetime: how long a link works [default: 3600 seconds]; sender address: From header of the email [default: the app's existing mail sender if one exists, otherwise a config key MAIL_DEFAULT_SENDER, UNVERIFIED]; minimum password length: [default: the app's existing rule, otherwise 8]; URL paths: [default: /forgot-password and /reset-password/ followed by the token (Flask route variable named token)].
- Exclusions: login, registration and any existing routes stay unchanged; no new user fields unless required; no changes to the app's frontend styling beyond reusing its base template.
- Data types / formats: token is a URL-safe string signed with the app's secret key (UNVERIFIED: confirm the key is configured through app.config["SECRET_KEY"]); passwords stored with the same hashing the app already uses (UNVERIFIED: read it); email is plain text, optionally with an HTML part.
- Environment: UNVERIFIED — OS, Python version, Flask version, database and mail library are read from the project; run all commands in the project folder.
- Compatibility target: the Python and Flask versions already used by the project; no upgrades.

STANDARDS
- PEP 8, PEP 257 docstrings for every new function and class, type hints; KISS; reliable, safe, fast, efficient; production-ready and maintainable; follow the project's existing structure and naming; no new dependencies outside the approved list.

APPROACH
- Compare stateless signed tokens (itsdangerous) with tokens stored in the database against simplicity, security, and fit with the project's existing code; pick one and state why in one line before starting.

REQUIREMENTS
1. A "forgot password" page accepts an email address and, if an account with that address exists, sends an email containing a reset link.
2. The reset link opens a page where the user enters a new password twice; a valid link with matching passwords updates the stored password hash and the user can log in with the new password.
3. A link older than the token lifetime, a modified link, and a malformed link are all rejected with a clear message and change nothing.
4. The new password is stored hashed with the app's existing method, never in plain text, and the token and password never appear in logs.
5. Mail sending uses the project's existing mail setup, or standard-library smtplib with settings read from configuration (names listed in the README), and failures show a generic error without crashing the app.
6. New code has automated tests covering Req 1 to 5, and the project's full existing test suite still passes.
7. The README (or the project's docs) states the new routes, the new configuration keys by name, and how to test the flow locally.

RISKS
- Wrong or missing SECRET_KEY makes tokens forgeable or invalid → covered by Req 3 (tampered-token test) and the baseline check of the config.
- Email send fails or the mail server is unreachable → covered by Req 5 (test with a failing sender).
- Existing login behaviour breaks → covered by Req 6 (full test suite before and after).
- Reset link leaks through logs → covered by Req 4 (log check).
- No existing test setup → covered by Req 6 (create tests with pytest only if the project has no test runner; report it).

CONSTRAINTS
- Scope: the project's Flask app package, its templates, its tests folder, its configuration example file and README; nothing else.
- Do not: send real emails during tests — because tests must be repeatable and must not contact real users; use a mock or Flask-Mail's testing mode / an in-memory outbox.
- Do not: edit existing tests to make them pass — because they are the check; report any you believe are wrong.
- Do not: change the user table schema or run migrations without my yes — because it alters stored data.
- Dependencies: none new by default; if the project has no mail library, use smtplib from the standard library.

VERIFICATION (one line per requirement)
- Req 1: pytest test posting a known and an unknown email to the forgot page, with the mail outbox mocked → one email with a reset link for the known address; the page responds 200 or a redirect in both cases.
- Req 2: pytest test following the emailed link, submitting a new password twice, then logging in → login with the new password succeeds, with the old password fails.
- Req 3: pytest tests with an expired token (use max_age=0 or a patched clock), an altered token and a malformed string → each returns the rejection message and the password hash is unchanged.
- Req 4: pytest assertion that the stored value differs from the plain password and verifies with the app's hash check; `grep` of captured test logs for the token and password → no match.
- Req 5: pytest test with the sender raising an exception → response shows the generic error, status is not 500, and the app keeps running.
- Req 6: run the project's test command (UNVERIFIED: read it from the project) before and after → same existing tests pass, new tests pass, exit code 0.
- Req 7: read the docs diff → routes, config key names and local test steps are all listed.

WORKING BEHAVIOUR (code in one project)
1. Read my messages for meaning: interpret spelling or grammar mistakes without changing what I asked.
2. This approval covers the whole plan in this prompt; work without asking again, only on branch `feature/password-reset`, never on main.
3. If you see a better way, propose it with its trade-offs; apply it only after my yes.
4. If a check fails: trace, debug, fix, retest; after 3 failed attempts at a step, record it as [!] and move on.
5. Ask me only for: a new dependency, anything outside SCOPE, deleting files, a database migration.
6. Budget: 90 minutes, at most 3 attempts per failing step.
7. At the end: an independent review (fresh reviewer, no prior context), then the report.

BEFORE YOU FINISH
- Check every requirement against VERIFICATION and the work against STANDARDS; criticise your own result, fix every flaw found; report anything not checked as UNVERIFIED.

PROGRESS
- Track steps in PROGRESS.md with [ ] todo, [~] in progress, [x] done, [!] failed, [?] blocked; [x] only with command, exit code and key output line. Do not commit PROGRESS.md.

OUTPUT: the diff on the branch, a list of new routes and configuration keys, the test report (command, exit code, key line) before and after, then the limitations.

STOP WHEN: Req 1 to 7 pass their verification, the independent review is done, and the report is sent.

UNVERIFIED: app location and structure; user model and password hashing; existing mail setup; test command; SECRET_KEY configuration; Flask and itsdangerous API on the installed versions.
```
Delivery: paste as the first message in Claude Code, started in the Flask project folder.
UNVERIFIED: everything about your app (structure, user model, hashing, mail setup, test command); library APIs (web fetch was blocked, not checked).
Suggestions, not in the prompt (say yes to add): same response for unknown and known emails (no account enumeration); rate limit on reset requests; single-use links (bind the token to the current password hash); end other sessions after a reset; email notice that the password changed; CSRF protection on both forms if not already present.
