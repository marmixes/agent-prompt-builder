# General prompt template

One template for every agent job. Fill every `<...>`; write `n/a` for a SPECIFICS line that does not apply. A small job keeps every block with one or two lines each; a big job uses more lines. ROLLBACK, PHASES and FIRST DELIVERABLE appear only when the job needs them; every other block is always present.

Check a filled prompt with: `python3 scripts/lint_prompt.py <file>` (this template itself passes with `--template`).

## Full form (Claude Code, Codex and other strong agents)

```
ROLE: You are a senior <domain> engineer experienced in <specific area>.

GOAL: Your task is to <action> <what> so that <result that VERIFICATION checks>.

STRICT RULES (mandatory; if you cannot follow one, stop and report which one)
1. Do exactly the GOAL; change nothing outside SCOPE.
2. Before changing anything, record the current state (versions, config, test results) and report it.
3. Research before deciding: read the files and the SOURCES first; never make a claim about a file you have not read.
4. Every requirement must pass its VERIFICATION check; show the command, exit code and key output line.
5. Never guess and never promise what you cannot verify: report it as UNVERIFIED.
6. Never mark a step done without proof.
7. Never read or print secrets; never touch other projects, services or settings outside SCOPE.
8. Stop exactly at STOP WHEN; no extra work and no unrequested changes.

CONTEXT
- <verified fact> (source: <file or URL>)
- Why it matters: <one line>

SOURCES (use these; do not substitute others)
- <repo / docs / model page URL> — <what to use it for>

SPECIFICS
- Inputs: <exact inputs, formats, locations>
- Outputs: <exact outputs, formats, locations>
- Options: <name>: <meaning> [default: <value>]
- Exclusions: <what stays unchanged / out of scope>
- Data types / formats: <exact types>
- Environment: <machine, container, OS, user, versions>
- Compatibility target: <runtime / API / version the result must work with>

STANDARDS
- <e.g. PEP 8, PEP 257 docstrings for every class and method, type hints; KISS; reliable, safe, fast, efficient; production-ready and maintainable; no new dependencies outside the approved list>

APPROACH
- Compare <2–3 options> against <criteria>; pick one and state why in one line before starting.

REQUIREMENTS
1. <one testable requirement>
2. <...>

RISKS
- <weakness, edge case or failure mode> → covered by <test / requirement>

CONSTRAINTS
- Scope: <files / folders / settings allowed to change>
- Do not: <forbidden action> — because <reason>
- Dependencies: <none / approved list with licence>

VERIFICATION (one line per requirement)
- Req 1: <command or proof> → <pass condition>
- Req 2: <...>

WORKING BEHAVIOUR (<job type: read-only | code in one project | infra | real devices | security | publish>)
1. Read my messages for meaning: interpret spelling or grammar mistakes without changing what I asked.
2. <approval rule for this job type, e.g. "This approval covers the whole plan; work without asking again.">
3. If you see a better way, propose it with its trade-offs; apply it only after my yes.
4. If a check fails: trace, debug, fix, retest; after 3 failed attempts at a step, record it as [!] and move on.
5. Ask me only for: <owner-only blockers: new dependency, outside SCOPE, deleting, high-risk or real-world actions>.
6. Budget: <max time / attempts>.
7. At the end: an independent review (fresh reviewer, no prior context), then the report.

ROLLBACK (infra and real devices only)
- <how to undo each change; written before the change is made>

PHASES (big projects only)
1. Research and design (read-only) → FIRST DELIVERABLE → my approval.
2. Implementation → verification: <criteria>.
3. Review and real tests → verification: <criteria>.
4. Release preparation → publishing needs a separate yes.

FIRST DELIVERABLE (big projects only)
- <stack comparison with reasons, architecture, MVP, risks, milestones with verification criteria, your independent assessment and suggested improvements>; then ask for one approval and do not start phase 2 before it.

BEFORE YOU FINISH
- Check every requirement against VERIFICATION and the work against STANDARDS; criticise your own result, fix every flaw found; report anything not checked as UNVERIFIED.

PROGRESS
- Track steps in <file> with [ ] todo, [~] in progress, [x] done, [!] failed, [?] blocked; [x] only with command, exit code and key output line.

OUTPUT: <exact deliverable and report format>, then the limitations.

STOP WHEN: <done condition>.

UNVERIFIED: <assumptions to check first>
```

## Medium form (OpenCode, Hermes, OpenClaw, local models)

Same rules, fewer words: local models follow short, strict prompts better. Split big jobs into several medium prompts.

```
GOAL: Your task is to <action> <what> so that <result>.

STRICT RULES (mandatory; if you cannot follow one, stop and report which one)
1. Do only the GOAL; change nothing outside LIMITS; record the current state first.
2. Read before claiming; prove every step (command, exit code, key line); never guess, report UNVERIFIED.
3. Never touch secrets; stop at DONE WHEN.

SPECIFICS
- Inputs: <...> · Outputs: <...> · Options: <name> [default: <value>] · Exclusions: <...> · Environment: <...>

DO
1. <step> → check: <command> → expect: <result>
2. <step> → check: <command> → expect: <result>

RISKS
- <failure mode> → check: <command>

LIMITS
- Only change: <files / folders>
- Do not: <action> — because <reason>

WORKING BEHAVIOUR (<job type>)
- <approval rule>; if a check fails: debug, fix, retest (max 3 tries); ask me only for <blockers>; budget <time>.

DONE WHEN: <condition>. If blocked: <what to report>.
UNVERIFIED: <items to check first>
```

## Start prompt (for a plan saved in a file)

```
Read PLAN.md and PROGRESS.md, then continue from the first step not marked [x].
Follow AGENTS.md / CLAUDE.md. Report in the OUTPUT format of PLAN.md.
```

## Avoiding double rules

If the agent's own rules file (AGENTS.md, CLAUDE.md) already contains the STRICT RULES, write `STRICT RULES: as in AGENTS.md, plus:` followed only by this job's extra rules.
