# opusPromptSkill

A Claude Code skill (`/frame`) that turns a rough prompt into a well-framed brief, so Opus 5.5 plays to its strengths and avoids its known failure modes.

Based on Anthropic's [Getting the most out of Opus 5.5](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/) and [Theo's breakdown of it](https://youtu.be/ejjBbaq9RmY).

## Built

- `/frame [mode] <rough prompt>` shows a brief for you to run, with modes: `build`, `audit`, `review`, `design`, `doc` (inferred when omitted)
  - Every brief names a finish line, a "don't" list, the permissions granted up front, and a suggested effort level (high or xhigh, never Max)
  - `review` writes a plain-text brief that also works in Codex, the second reviewer
  - Test prompts and a grading script live in `frame/evals/`

- `/verify [target]` checks each claim in a report, diff, review, doc, or Claude's last answer against evidence
  - Every claim is marked wrong, unconfirmed, or confirmed, with `file:line` or command output; read-only, never fixes
  - Test fixture with planted claims and ground truth lives in `verify/evals/`

## Planned

- A standing global CLAUDE.md block in `~/.claude/CLAUDE.md` (keep going, treat answers as done, TASKS.md on long runs)
- Maybe later: `/debrief`

## Tips

- Opus 5.5 defaults to medium effort. Raise it for long runs, e.g. `claude --effort high`.
- Flagged messages can move to an older model mid-run. After a long run, check `/model`, or turn off automatic switching in settings.

Source lives in `frame/` and `verify/`; install with `ln -s "$PWD/frame" ~/.claude/skills/frame` and `ln -s "$PWD/verify" ~/.claude/skills/verify`.
