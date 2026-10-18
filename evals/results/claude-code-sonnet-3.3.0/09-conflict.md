I have not written the prompt yet: your request conflicts with your project rules.

- Your CLAUDE.md says: "No Docker in this project."
- Your request: add a Docker setup.

Claude Code reads CLAUDE.md on every run, so a prompt that adds Docker would either be refused by the agent or break your rule. I will not choose between them for you.

Which do you want? Reply with one letter.

A. Keep the rule. I write a prompt for the same goal without Docker (for example a Python venv or a plain run script, or a Podman/devcontainer alternative if you allow it). Tell me what the Docker setup was for (deployment, a reproducible dev environment, CI?).
B. Change the rule. You edit CLAUDE.md (or I include a step in the prompt that asks you to approve changing that line first). Then I write the Docker prompt. This is a change to your project rules, so it needs your explicit yes.
C. Make an exception for one task. I write the Docker prompt with a line saying "the CLAUDE.md Docker ban is lifted for this task only, by the owner's decision", and the rule stays for everything else.

I need these facts for A, B or C: the language and entry point of the project, where it should run (dev machine, server, CI), and whether it needs a database or other services. I will mark anything I do not get as UNVERIFIED.
