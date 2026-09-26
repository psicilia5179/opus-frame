#!/usr/bin/env bash
# Link the skills into ~/.claude/skills and install the CLAUDE.md block.
# Safe to rerun: links are refreshed and the block is replaced between its markers.
set -euo pipefail

repo="$(cd "$(dirname "$0")" && pwd)"
skills="$HOME/.claude/skills"
claude_md="$HOME/.claude/CLAUDE.md"
block="$repo/claude-md/opus-block.md"

mkdir -p "$skills"
for s in opus-frame opus-verify; do
  ln -sfn "$repo/$s" "$skills/$s"
  echo "linked $skills/$s"
done

touch "$claude_md"
cp "$claude_md" "$claude_md.bak-opus-skills-$(date -u +%Y%m%dT%H%M%SZ)"
python3 - "$claude_md" "$block" <<'EOF'
import re, sys
path, block_path = sys.argv[1], sys.argv[2]
text, block = open(path).read(), open(block_path).read().strip() + "\n"
pattern = re.compile(r"<!-- opus-skills:start.*?<!-- opus-skills:end -->\n?", re.S)
if pattern.search(text):
    text = pattern.sub(lambda _: block, text)
else:
    text = text.rstrip("\n") + ("\n\n" if text.strip() else "") + block
open(path, "w").write(text)
EOF
echo "installed block into $claude_md"
