#!/usr/bin/env bash
set -euo pipefail

PROJ="/workspaces/ChangeOnt"

# keep each CLI's state inside the project (and out of $HOME)
mkdir -p "$PROJ/.codex" "$PROJ/.gemini" "$PROJ/.claude"

# link state dirs so CLIs read/write under the repo
if [ ! -L "$HOME/.codex"  ]; then rm -rf "$HOME/.codex"  || true; ln -s "$PROJ/.codex"  "$HOME/.codex";  fi
if [ ! -L "$HOME/.gemini" ]; then rm -rf "$HOME/.gemini" || true; ln -s "$PROJ/.gemini" "$HOME/.gemini"; fi
if [ ! -L "$HOME/.claude" ]; then rm -rf "$HOME/.claude" || true; ln -s "$PROJ/.claude" "$HOME/.claude"; fi

# avoid accidental API billing; we’ll use account-login flows
unset OPENAI_API_KEY || true
unset GEMINI_API_KEY || true
unset ANTHROPIC_API_KEY || true

echo "[ai_bootstrap] linked ~/.codex ~/.gemini ~/.claude to project; API keys unset."