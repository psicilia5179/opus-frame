#!/usr/bin/env bash
# Link the skills into ~/.claude/skills. With --claude-md, also install the CLAUDE.md block.
# Safe to rerun: links are refreshed and the block is replaced between its markers.
set -euo pipefail

with_block=0
case "${1:-}" in
  "") ;;
  --claude-md) with_block=1 ;;
  *) echo "usage: $0 [--claude-md]" >&2; exit 2 ;;
esac

repo="$(cd "$(dirname "$0")" && pwd)"
skills="$HOME/.claude/skills"
claude_md="$HOME/.claude/CLAUDE.md"
block="$repo/claude-md/opus-block.md"

# Link each skill so `git pull` updates it. Where symlinks aren't available (Git Bash on
# Windows without Developer Mode copies instead of linking), fall back to a real copy.
install_skill() {
  local src="$repo/$1" dst="$skills/$1"
  if [ -L "$dst" ]; then
    rm "$dst"
  elif [ -e "$dst" ]; then
    # Only replace an earlier copy of this same skill, never someone else's folder.
    if ! grep -qx "name: $1" "$dst/SKILL.md" 2>/dev/null; then
      echo "refusing to replace $dst: it isn't an earlier copy of $1" >&2
      exit 1
    fi
    rm -rf "$dst"
  fi
  if ln -s "$src" "$dst" 2>/dev/null && [ -L "$dst" ]; then
    echo "linked $dst"
  else
    rm -rf "$dst"
    cp -R "$src" "$dst"
    echo "copied $dst (symlinks unavailable here: rerun this script after git pull)"
  fi
}

mkdir -p "$skills"
for s in opus-frame opus-verify; do
  install_skill "$s"
done

[ "$with_block" = 1 ] || exit 0

py=""
for c in python3 python; do
  if "$c" -c "" >/dev/null 2>&1; then py="$c"; break; fi
done
[ -n "$py" ] || { echo "needs Python 3 for --claude-md" >&2; exit 1; }

touch "$claude_md"
cp "$claude_md" "$claude_md.bak-opus-skills-$(date -u +%Y%m%dT%H%M%SZ)"
"$py" - "$claude_md" "$block" <<'EOF'
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
