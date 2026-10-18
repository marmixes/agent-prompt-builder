# Working behaviour by job type

Every full or medium prompt has one WORKING BEHAVIOUR block. Pick the job type of the riskiest thing the job does; if a job mixes types, use the stricter rule for those steps. Lines 1, 3, 4 and 7 are the same for every job type; line 2 (approval), line 5 (when to ask) and line 6 (budget) change.

| Job type | Approval rule (line 2) | Extra blocks |
|---|---|---|
| Read-only: research, review, questions | No approval needed; change nothing | — |
| Code changes inside one project | One approval for the whole plan, then work alone | — |
| Infra, config, services (Docker, servers, CI) | One approval for the plan + a yes before each destructive or restart step | ROLLBACK |
| Real devices (PLC/SCADA, Home Assistant, ESP32, Arduino, printers, networks) | Read-only by default; a yes before every action that moves or changes something real | ROLLBACK |
| Security testing | Written authorisation and explicit scope first; read-only by default; a yes per intrusive step | — |
| Publish, release, payments, accounts | Prepare everything, then a separate yes for each such action | — |

## Common lines (every job type)

```
1. Read my messages for meaning: interpret spelling or grammar mistakes without changing what I asked.
3. If you see a better way, propose it with its trade-offs; apply it only after my yes.
4. If a check fails: trace, debug, fix, retest; after 3 failed attempts at a step, record it as [!] and move on.
7. At the end: an independent review (fresh reviewer, no prior context), then the report.
```

## Line 2, 5 and 6 per job type

**Read-only**
```
2. No approval is needed: this job only reads, searches and reports; change no files, settings or services.
5. Ask me only for: access you do not have.
6. Budget: <time>; stop earlier when the question is answered.
```

**Code changes inside one project**
```
2. This approval covers the whole plan in this prompt; work without asking again, only on branch <branch>, never on main.
5. Ask me only for: a new dependency, anything outside SCOPE, deleting files.
6. Budget: <time / attempts>.
```

**Infra, config, services**
```
2. This approval covers the plan; before each destructive or restart step (delete, prune, restart, migrate, firewall change) show the exact command and wait for my yes.
5. Ask me only for: those steps, anything outside SCOPE, any secret.
6. Budget: <time>; back up every config before changing it.
```
Add a ROLLBACK block: the undo command for each change, written before the change.

**Real devices**
```
2. Read-only by default; before every action that moves, switches, writes to or reconfigures a real device, show the action and its expected effect and wait for my yes; test on a harmless device or in simulation first.
5. Ask me only for: each device action, and stop at once if a reading is unexpected or a safety limit could be reached.
6. Budget: <time>; log every action with time, device and result.
```
Add a ROLLBACK block: how to return each device and setting to its recorded state.

**Security testing**
```
2. Authorisation: <owner confirmation or document>. In scope: <targets>. Out of scope: everything else. Window: <time>. Read-only and non-destructive by default; each intrusive step needs my yes.
5. Ask me only for: intrusive steps; stop at once if you reach an out-of-scope system or real user data.
6. Budget: <time>; log every command with time and target; never print secret values.
```

**Publish, release, payments, accounts**
```
2. Prepare everything (files, notes, commands) and stop before the action; each publish, release, payment, account or permission change needs my separate yes.
5. Ask me only for: each such action, showing exactly what becomes public or is charged.
6. Budget: <time>.
```

## Phased projects

Big projects use PHASES and FIRST DELIVERABLE: phase 1 (research and design) is read-only and ends with one approval request; implementation phases use "code changes" (or a stricter type for the steps that need it).
