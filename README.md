# opusPromptSkill

A Claude Code skill (`/frame`) that turns a rough prompt into a well-framed brief, so Opus 5.5 plays to its strengths and avoids its known failure modes.

Based on Anthropic's [Getting the most out of Opus 5.5](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/) and [Theo's breakdown of it](https://youtu.be/ejjBbaq9RmY).

## Planned

- `/frame <rough prompt>` shows a brief for you to run, with modes: `build`, `audit`, `review`, `design`, `doc`
  - Every brief names a finish line, a "don't" list, the permissions granted up front, and a suggested effort level (high or xhigh, never Max)
  - `review` writes a plain-text brief that also works in Codex, the second reviewer
- `/verify`: a second pass that checks each claim or change against evidence
- A standing global CLAUDE.md block in `~/.claude/CLAUDE.md` (keep going, treat answers as done, TASKS.md on long runs)
- Maybe later: `/debrief`

## Tips

- Opus 5.5 defaults to medium effort. Raise it for long runs, e.g. `claude --effort high`.
- Flagged messages can move to an older model mid-run. After a long run, check `/model`, or turn off automatic switching in settings.

Source lives here; the skill installs to `~/.claude/skills/frame/`.
