# opusPromptSkill

A Claude Code skill (`/frame`) that turns a rough prompt into a well-framed brief, so Opus 5.5 plays to its strengths and avoids its known failure modes.

Based on Anthropic's [Getting the most out of Opus 5.5](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/).

## Planned

- `/frame <rough prompt>` with modes: `build`, `audit`, `review`, `design`, `doc`
- A standing CLAUDE.md block (keep going, treat answers as done, TASKS.md on long runs)
- Maybe later: `/debrief`, `/verify`

Source lives here; the skill installs to `~/.claude/skills/frame/`.
