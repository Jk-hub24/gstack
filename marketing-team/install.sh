#!/usr/bin/env bash
# Install the marketing team into ~/.claude so every Claude Code project on this
# machine can use it. Re-run after pulling updates.
#
#   ./marketing-team/install.sh            copy (safe default)
#   ./marketing-team/install.sh --link     symlink, edits here go live immediately
#
# Prefer the plugin route when you can (see README). This script is for machines
# where you'd rather not use the plugin marketplace.
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="${CLAUDE_HOME:-$HOME/.claude}"
MODE="copy"
[ "${1:-}" = "--link" ] && MODE="link"

mkdir -p "$DEST/agents" "$DEST/skills"

for f in "$SRC"/agents/*.md; do
  name="$(basename "$f")"
  if [ "$MODE" = "link" ]; then ln -sfn "$f" "$DEST/agents/$name"; else cp "$f" "$DEST/agents/$name"; fi
  echo "agent  $name"
done

for d in "$SRC"/skills/*/; do
  name="$(basename "$d")"
  rm -rf "$DEST/skills/$name"
  if [ "$MODE" = "link" ]; then ln -sfn "${d%/}" "$DEST/skills/$name"; else cp -R "${d%/}" "$DEST/skills/$name"; fi
  echo "skill  $name"
done

echo
echo "Installed ($MODE) into $DEST. Start a new Claude Code session, then try:"
echo "  /campaign geo-radar 40 design partners by January"
