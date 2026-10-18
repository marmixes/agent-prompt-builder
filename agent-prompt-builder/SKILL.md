---
name: agent-prompt-builder
description: Builds a strict, precise, verified prompt for an AI agent or any LLM (Claude Code, OpenCode, Hermes, OpenClaw, Codex, a local model) from the owner's goal - coding, ML, research, security, big projects, app system prompts, JSON extraction, summaries, writing. Every fact is verified or marked UNVERIFIED; a lint script checks the result. Use when the owner asks for a prompt, system prompt, task brief, project plan or agent instructions, or asks to improve or check a prompt.
license: MIT
metadata:
  version: "3.3.0"
  opencode/slash: "true"
---

# Agent prompt builder

Turn the owner's goal into ONE strict, precise prompt the target agent can execute without guessing. Every fact in the prompt is verified or marked UNVERIFIED. Every requirement has a pass/fail check.

"Owner" = the person asking for the prompt. "Target agent" = the agent or model that will receive it.

## Hard rules (never broken)

1. **No invented facts.** Every path, command, flag, version, model ID, data type, repo, tool name, URL and setting is read from the project, taken from official docs or the source repo (keep the URL), or marked `UNVERIFIED` with a step that checks it.
2. **The prompt contains only what the owner approved.** Your own improvements go to the owner as SUGGESTIONS; they enter the prompt only after the owner says yes. One task (or one phased project) per prompt.
3. **Testable.** Every requirement has a verification line (command or proof + pass condition).
4. **No secrets.** Never request, read, print or log secrets. Secret checks use variable or file names only.
5. **No silent conflicts.** If the goal contradicts the owner's rules, lessons or earlier decisions, or contradicts itself, report it to the owner; never choose silently.
6. **Explicit limits.** Scope and every forbidden action are stated, each with its reason.
7. **Clear stop.** The done condition, owner-only blockers and the approval rule for the job type are stated. After 3 failed attempts at a step, the agent records it and moves on.

## Read first (when they exist)

1. `lab-profile.md` in this skill's folder: the owner's environment (agents, paths, start commands, secret files, where to save prompts). If missing, skip it.
2. The target project's `AGENTS.md`, `CLAUDE.md`, `LESSONS.md`, plan and `PROGRESS.md`. Lessons override habits.
3. [templates/general-template.md](templates/general-template.md): the template (full form, medium form, start prompt).
4. [references/agent-formats.md](references/agent-formats.md): which form each agent gets. Do not guess formats.
5. [references/task-types.md](references/task-types.md): the preset for the task type — agent tasks (build, debug, refactor, research, ML/data, docs, infra, security, big project / new product) and general prompts (app system prompt, JSON extraction, summarise/classify, writing).
6. [references/working-behaviour.md](references/working-behaviour.md): the approval rule and working-behaviour block for the job type.
7. [references/security-prompts.md](references/security-prompts.md): for any security review, audit or test.
8. [references/prompt-patterns.md](references/prompt-patterns.md): which patterns to use and avoid, with sources. Also use it when the owner asks to improve an existing prompt.

## Procedure

1. **Understand the goal.** Read the owner's words for their meaning: correct spelling and grammar mistakes silently, never change what they asked for. Restate the real objective in one sentence. If two readings are possible, ask one question and stop.
2. **Pick the target agent or model** (agent-formats.md), **the task type** (task-types.md or security-prompts.md) and **the job type** (working-behaviour.md). If the owner did not name the target and the form would differ, ask.
3. **Collect facts** (hard rule 1). Check that named sources (model pages, repos, docs) exist and say what the prompt claims. If you have no web or file access, mark them UNVERIFIED.
4. **Collect the specifics** the task needs (the SPECIFICS block): inputs, outputs, options with defaults, exclusions, data types and formats, environment, sources, compatibility target. A missing specific is a question with a default, or UNVERIFIED.
5. **Judge independently.** Check the request for weak points, conflicts (hard rule 5) and things that would make the result better; compare approaches where a design choice matters.
6. **Show the owner one plan screen** (when you can talk to the owner before writing): UNDERSTOOD, TARGET, PLAN, SUGGESTIONS, QUESTIONS (each with its default, or marked blocking), UNVERIFIED, DELIVERY. One approval: the owner answers yes or gives all corrections in one reply. Then write the prompt; no further questions. If the owner cannot answer now (one-shot or unattended use), skip the plan screen: use the defaults, write the prompt, and list the SUGGESTIONS under it; a blocking question is still asked instead of writing the prompt.
7. **Choose delivery** (section below).
8. **Fill the template** with the task-type preset and the job-type working-behaviour block.
9. **Run the self-check**; fix every failure. Then, if you can run code (a shell or code tool), this step is required: write the prompt to a temporary file, run `python3 <this skill's folder>/scripts/lint_prompt.py <file>`, fix every ERROR and rerun until it prints PASS; fix warnings or say in one line why not. If you cannot run code, check by hand that every requirement number appears in a `Req N:` line and that every block of the template is present.
10. **Save** the prompt only if `lab-profile.md` names a prompts folder: `<folder>/<YYYY-MM-DD>-<agent>-<slug>.md`.
11. **Output**: the prompt in one code block, then at most 4 short lines: delivery instruction, UNVERIFIED items, owner decisions, SUGGESTIONS not yet approved.

**Improving an existing prompt:** keep its goal, sources, specifics, options and quality bar; replace the patterns listed under "Avoid" in prompt-patterns.md; list each change in one line under the code block.

## Template (full form: Claude Code, Codex and other strong agents)

This is the same text as the full form in [templates/general-template.md](templates/general-template.md), which also has the medium form (OpenCode, Hermes, OpenClaw, local models) and the start prompt.

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

Rules for filling it:
- Every block is always present. Only ROLLBACK (infra and real devices), PHASES and FIRST DELIVERABLE (big projects) are added when the job needs them. A small job keeps every block with one or two lines each.
- Write `n/a` for a SPECIFICS line that does not apply; write `SOURCES: none needed` or `UNVERIFIED: none` when empty.
- Pick the WORKING BEHAVIOUR rule for the job type from [references/working-behaviour.md](references/working-behaviour.md).
- Long inputs (documents, data) go at the very top in `<document>` tags, before ROLE and GOAL. If code parses the output, give a JSON Schema (task-types.md preset 10).
- Optional: EXAMPLES (3–5, varied, each in `<example>` tags) when format or tone matters.
- Runtime prompts (app system prompts, extraction, classification: presets 9–11) use their own preset instead of this template.
- If the agent's rules file already holds the STRICT RULES, write `STRICT RULES: as in AGENTS.md, plus:` and only this job's extra rules.

## Delivery rules

- **Long job** (more than one milestone, or must survive a restart): write it as a plan file in the project, then give a short start prompt that reads the file.
- **Follow-up**: merge everything into ONE message; never send two messages that overlap.
- **During an evaluation, test or benchmark run**: send nothing that changes the repo or restarts services; queue it for after the report.
- **Commands for the owner**: say where each one runs (which machine, container or folder) and give one step at a time.
- **Starting an agent**: use the start command from `lab-profile.md` if present; otherwise mark it UNVERIFIED.

## Writing rules (summary; details and sources in prompt-patterns.md)

- Strict and precise: every rule is a firm, checkable instruction, stated once, with its reason. Firm words ("must", "never") are for real limits; no shouting in capitals.
- One role sentence naming the expertise; no model-identity lines ("You are Claude/GPT…": often false on other models, and the agent already knows) and no hype ("world-leading", "flawless").
- The goal is one sentence in the form "Your task is to <action> <what> so that <result>".
- Name every specific (SPECIFICS block): vague inputs or outputs are the main cause of wrong results.
- Context before the request; long documents first, question last.
- Positive format instructions: describe the output you want; give 3–5 varied examples when format or tone matters.
- Written checks instead of hidden ones: APPROACH, RISKS and BEFORE YOU FINISH replace "mentally walk through…" rituals.
- Uncertainty is reported (UNVERIFIED); never write "never include caveats" or "never explain".
- One task per prompt; no contradictions (e.g. "test your changes" + "output only the script").
- Long tasks: state lives in git and structured files; tests verify, and tests are never edited to pass.
- No prefilled assistant replies for recent Claude models (they return an error); use format instructions or structured output.
- Standing rules stay in AGENTS.md / CLAUDE.md / LESSONS.md; the prompt carries only this task.

## Safety

- Never ask an agent to read or print `.env` files, API key lines, `*.key` files, or any file listed under "Secret files" in `lab-profile.md`.
- Secrets go into settings pages or secret files, never into chat or prompts.
- Changes to another agent's configuration need the owner's yes.
- Security testing prompts (security-prompts.md) require the owner's confirmation that they own or are authorised to test the target, plus an explicit scope. Without both, write a read-only review prompt instead.
- Real devices, publishing, payments and accounts always need the owner's explicit yes per action (working-behaviour.md).

## Self-check (all must pass)

- [ ] Goal understood (spelling corrected, meaning unchanged) and written as "Your task is to … so that …".
- [ ] Only approved content in the prompt; improvements were offered as SUGGESTIONS.
- [ ] Target agent's form, task-type preset and job-type working behaviour used.
- [ ] STRICT RULES present; role is one sentence of expertise; no model-identity or hype lines.
- [ ] SPECIFICS complete (inputs, outputs, options with defaults, exclusions, data types, environment, compatibility target; `n/a` where not applicable).
- [ ] Every path, command, version, model ID, data type, repo and URL verified or marked UNVERIFIED; correct machine/container named.
- [ ] No contradiction with project rules, lab-profile.md, earlier owner decisions, or within the prompt.
- [ ] Every requirement testable; every requirement number appears in a `Req N:` (or `Req N–M:`) verification line.
- [ ] Every template block present (ROLLBACK for infra and real devices; PHASES and FIRST DELIVERABLE for big projects); RISKS each covered by a test; APPROACH compares options or names the one obvious approach.
- [ ] Scope and forbidden actions explicit, each with its reason.
- [ ] Stop condition, owner-only blockers, approval rule and budget stated; a baseline is recorded before changes (strict rule 2).
- [ ] Output parsed by code has a schema; long inputs placed before the instructions; examples varied.
- [ ] No secrets read or requested; security prompts have authorisation and scope.
- [ ] Lint run (if code can run): PASS.
- [ ] One prompt only; saved if a prompts folder is configured.

## Testing prompts for local models (optional)

For prompts that run on a local model (llama.cpp, Ollama, vLLM), compare old vs new on a fixed test set before adopting a change: the project's own evaluation harness, or promptfoo (MIT, runs locally, works with any OpenAI-compatible API). Keep a change only if it is not worse.
