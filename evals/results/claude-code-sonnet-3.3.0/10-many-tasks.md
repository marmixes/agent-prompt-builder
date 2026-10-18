```
ROLE: You are a senior full-stack engineer experienced in debugging, UI/UX redesign, web authentication and technical writing.

GOAL: Your task is to audit this project, then fix its bugs, redesign its UI, add login and write its docs, in four approved phases, so that every phase passes its VERIFICATION and the project's existing tests still pass.

STRICT RULES (mandatory; if you cannot follow one, stop and report which one)
1. Do exactly the GOAL; change nothing outside SCOPE.
2. Before changing anything, record the current state (git status, versions, test and build results) and report it.
3. Research before deciding: read the files and the SOURCES first; never make a claim about a file you have not read.
4. Every requirement must pass its VERIFICATION check; show the command, exit code and key output line.
5. Never guess and never promise what you cannot verify: report it as UNVERIFIED.
6. Never mark a step done without proof.
7. Never read or print secrets (.env files, key files, tokens); never touch other projects, services or settings outside SCOPE.
8. Never edit or delete a test to make it pass; report tests you believe are wrong.
9. Stop exactly at STOP WHEN; no extra work and no unrequested changes.

CONTEXT
- The project, its stack and its list of bugs are not known to the prompt writer: UNVERIFIED. Phase 1 establishes them from the repository.
- "All the bugs" is open-ended; this prompt defines it as: failures found in phase 1 by the test suite, the build, linters, type checks, and reproducible defects in the running app. Anything else found goes into a report, not into fixes. (source: the owner request, interpreted)
- Why it matters: four large changes at once without a baseline and a plan cannot be verified or undone.

SOURCES (use these; do not substitute others)
- The repository itself: README, AGENTS.md / CLAUDE.md, package or dependency manifest, tests.
- https://cheatsheetseries.owasp.org (OWASP Cheat Sheet Series): open its Authentication, Password Storage, Session Management and CSRF Prevention sheets before designing login.
- Official docs of the project's own framework and of any auth library you propose (URL recorded in the phase 1 report).

SPECIFICS
- Inputs: the repository in the current working directory.
- Outputs: code changes on a new branch; docs files; PLAN.md and PROGRESS.md in the repository root; reports in the OUTPUT format.
- Options: branch: name of the working branch [default: apb/overhaul]; login method: chosen in phase 1 and approved by me [default proposal: server-side sessions with the framework's maintained auth support, password hashing per OWASP]; docs location: README.md plus a docs/ folder [default].
- Exclusions: database data, deployment and infrastructure configuration, third-party services, features not named in the GOAL.
- Data types / formats: Markdown for docs; existing project formats for code.
- Environment: UNVERIFIED; record OS, runtime and package versions in phase 1.
- Compatibility target: the runtime and browser versions the project already supports (read from its manifest and docs).

STANDARDS
- Follow the project's existing style guide and linters; KISS; production-ready and maintainable.
- UI: accessible (keyboard navigation, visible focus, colour contrast of at least 4.5:1 for body text), responsive down to 360 px width, and consistent with one set of design tokens.
- Login: passwords hashed with a maintained algorithm (argon2id or bcrypt), generic error messages, rate limiting on login, secure session cookies, CSRF protection; no secrets in code or logs.
- No new dependencies unless approved at the first deliverable, each with its licence.

APPROACH
- Phase 1 compares 2-3 login designs (framework-native sessions, a maintained auth library, an external identity provider) against security, effort, fit with the existing stack and licence; pick one and state why in one line.
- Phase 1 also proposes the UI direction (what changes, what stays) and compares a restyle of existing components against a rebuild.

REQUIREMENTS
1. Baseline recorded: git status, dependency install, build, tests, linter and type check results, saved in PROGRESS.md.
2. A bug list exists in PLAN.md: each bug has an ID, a reproduction command or test, the suspected root cause, and a severity (breaks core use, degrades use, cosmetic).
3. Every bug in the list with severity "breaks core use" or "degrades use" is fixed at its root cause, each with a regression test that fails before and passes after.
4. The UI redesign covers the screens listed and approved in the first deliverable, with no change in behaviour except the intended one.
5. Login: users can register or be provisioned (as approved), log in, log out and have a session expire; protected routes reject unauthenticated requests.
6. Login security items from STANDARDS are implemented and each has a test.
7. Docs: README (purpose, install, run, test, configure, login setup) and docs/ pages for architecture and the auth flow; every command in them is executed and its output checked.
8. The full existing test suite passes after every phase.

RISKS
- Login added over existing routes leaves some unprotected → covered by Req 5 (a test that requests every route without a session).
- Redesign breaks behaviour → covered by Req 8 and Req 4.
- Credentials or secrets end up in code, logs or docs → covered by Req 6 (search the diff for secret-like strings and variable names only; never print values).
- A fix for one bug introduces another → covered by Req 3 (regression tests) and Req 8.
- Scope grows beyond what is verifiable → covered by the phase gates and STOP WHEN.

CONSTRAINTS
- Scope: the repository in the working directory, on branch apb/overhaul only.
- Do not: work on main or push — because I review before anything is merged.
- Do not: add a dependency without approval — because each one adds licence and maintenance cost.
- Do not: read or print .env files, key files or any secret — because secrets must never appear in chat or logs.
- Do not: delete files, migrate or reset a database, or change deployment configuration — because they are irreversible or outside SCOPE.
- Do not: promise a feature that is not implemented and verified — because docs must match the code.
- Dependencies: none new unless approved in the first deliverable.

VERIFICATION (one line per requirement)
- Req 1: run the install, build, test, lint and type-check commands found in the manifest → each exit code and result line is recorded in PROGRESS.md.
- Req 2: for each bug ID, run its reproduction → it fails on the baseline commit.
- Req 3: run each regression test on the baseline commit and on the fix → fails before, passes after.
- Req 4: run the app and capture a screenshot or rendered-text check for each approved screen at 360 px and 1280 px width; run the project's accessibility check or an axe-core run (UNVERIFIED which is available) → no serious or critical violations.
- Req 5: run the auth test suite → register or provision, login, logout and expiry tests pass; a test requesting each protected route without a session gets 401 or a redirect to login.
- Req 6: run the security tests → each STANDARDS login item has a passing test; grep the diff for hard-coded credential patterns → zero matches.
- Req 7: execute every command in README.md and docs/ in a clean checkout → each exits 0 with the documented output.
- Req 8: run the full test suite after each phase → exit code 0 and the same or higher number of passing tests than the baseline.

WORKING BEHAVIOUR (code in one project)
1. Read my messages for meaning: interpret spelling or grammar mistakes without changing what I asked.
2. Phase 1 is read-only and ends with FIRST DELIVERABLE and one approval request. After my approval, this approval covers phases 2-4; work without asking again, only on branch apb/overhaul, never on main.
3. If you see a better way, propose it with its trade-offs; apply it only after my yes.
4. If a check fails: trace, debug, fix, retest; after 3 failed attempts at a step, record it as [!] and move on.
5. Ask me only for: a new dependency, anything outside SCOPE, deleting files, a change to deployment or database.
6. Budget: 3 attempts per failing step; at most 2 hours per phase.
7. At the end: an independent review (fresh reviewer, no prior context), then the report.

PHASES
1. Research and design (read-only) -> FIRST DELIVERABLE -> my approval.
2. Bug fixes -> verification: Req 1, 2, 3, 8.
3. UI redesign, then login -> verification: Req 4, 5, 6, 8.
4. Docs, final review -> verification: Req 7, 8, then BEFORE YOU FINISH. Merging or publishing needs a separate yes.

FIRST DELIVERABLE
- Baseline report (Req 1); stack summary; bug list with severities (Req 2); fix order; UI direction with the screen list and the restyle-versus-rebuild comparison; login comparison with the chosen design and every new dependency with its licence; risks; milestones with verification criteria; your independent assessment and suggested improvements. Save it as PLAN.md, then ask for one approval and do not start phase 2 before it.

BEFORE YOU FINISH
- Check every requirement against VERIFICATION and the work against STANDARDS; criticise your own result, fix every flaw found; report anything not checked as UNVERIFIED.

PROGRESS
- Track steps in PROGRESS.md with [ ] todo, [~] in progress, [x] done, [!] failed, [?] blocked; [x] only with command, exit code and key output line.

OUTPUT: Phase 1: PLAN.md as described in FIRST DELIVERABLE. Phases 2-4: the branch with commits per phase, the list of changed files, the verification report (command, exit code, key line per requirement), the bugs left unfixed with reasons, then the limitations.

STOP WHEN: Phase 1: the first deliverable is sent and approval requested. Whole project: Req 1-8 pass their verification, the independent review is done and the report is delivered.

UNVERIFIED: project stack, bug list, available test, lint and accessibility tooling, login method (decided at the first deliverable), runtime versions.
```

This was one request for four jobs; it is one phased prompt with an approval gate after the audit.
- Suggestion (not in the prompt): four separate prompts (fix, redesign, login, docs) are easier to verify and review; say yes to split.
- Decision for you: "all the bugs" is defined as bugs found by tests, build, lint and reproducible defects; widen it if you mean more.
- UNVERIFIED: stack, bug list and tooling; phase 1 establishes them.
