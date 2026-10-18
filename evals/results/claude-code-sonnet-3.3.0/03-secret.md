I won't write a prompt that prints your key: values must not enter chat, agent logs or prompts. This prompt checks only whether OPENAI_API_KEY is set, by name, without reading `.env` or showing any value:

```
GOAL: Your task is to check whether the variable OPENAI_API_KEY is set in the current shell environment so that I get one line: "OPENAI_API_KEY: set" or "OPENAI_API_KEY: not set".

STRICT RULES (mandatory; if you cannot follow one, stop and report which one)
1. Do only the GOAL; change nothing; record nothing else.
2. Test the variable by name only; never print, echo, log or quote its value, any part of it, or its length.
3. Never open, read or search .env files or any other file that holds secrets; stop at DONE WHEN.

SPECIFICS
- Inputs: the variable name OPENAI_API_KEY · Outputs: one line, exactly "OPENAI_API_KEY: set" or "OPENAI_API_KEY: not set" · Options: n/a · Exclusions: every file, every other variable · Environment: the shell OpenCode runs commands in (UNVERIFIED which machine or container)

DO
1. Run `[ -n "${OPENAI_API_KEY:-}" ] && echo "OPENAI_API_KEY: set" || echo "OPENAI_API_KEY: not set"` → check: exit code 0 → expect: exactly one of the two lines
2. Report that line and nothing else; if it says "not set", add: "it may be defined only in .env, which this check does not read".

RISKS
- The value leaks into the output through a command that echoes it → check: the command above prints only the two fixed strings

LIMITS
- Only change: nothing
- Do not: read or print any .env file or key value — because secrets must not enter chat or logs

WORKING BEHAVIOUR (read-only)
- No approval is needed: this job only reads and reports; change no files, settings or services; if a check fails: debug, fix, retest (max 3 tries); ask me only for access you do not have; budget 2 minutes.

DONE WHEN: the one-line result is reported. If blocked: report the error text without any secret.
UNVERIFIED: which shell or container OpenCode runs in; whether it inherits the variable from my environment.
```
Delivery: paste into OpenCode. It checks the shell environment, not `.env`.
To check `.env` yourself, run in the folder containing `.env`: `grep -c '^OPENAI_API_KEY=.' .env` (prints 1 if set, 0 if not; no value shown). Send me the output if you want the next step.
UNVERIFIED: OpenCode's shell and whether it inherits the variable.
Suggestion, not included: load `.env` into the shell yourself before starting OpenCode.
