# Lab profile (template)

Copy this file to `lab-profile.md` in the same folder and fill it in.
`lab-profile.md` is personal: do not commit it (it is in `.gitignore`).
Write names and paths only. Never write secret values here.

## Agents
<!-- Which agents you use and where they run -->
- Claude Code: <machine / container>
- OpenCode: <machine / container, model>
- Hermes: <machine / container, model>
- Local model: <server, e.g. llama.cpp at http://host:port/v1>

## Start commands
<!-- Exact commands to start each agent -->
- Claude Code: `<command>`
- OpenCode: `<command>`

## Machines and paths
<!-- Where commands run; how paths differ between host and container -->
- Host: <name>, projects at `<path>`
- Container: <name>, projects at `<path>`

## Secret files (never read or print)
- `<path>/.env`
- `<path>/config.yaml` (key lines)

## Prompts folder (optional)
<!-- If set, every prompt is saved here -->
- `<path>/prompts`

## Rules and lessons files
- `<path>/LESSONS.md`

## Notes
- <anything else every prompt must respect>
