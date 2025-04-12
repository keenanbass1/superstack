#!/usr/bin/env bash

# -----------------------------------------
# dev-prompt-launcher.sh
# A fuzzy search tool for prompt templates
# -----------------------------------------

TEMPLATE_DIR="/mnt/c/Users/keena/Desktop/dev/superstack/templates/prompts"

if ! command -v fzf &> /dev/null; then
  echo "❌ fzf is not installed. Install with: sudo apt install fzf"
  exit 1
fi

if [[ ! -d "$TEMPLATE_DIR" ]]; then
  echo "❌ Prompt templates not found at $TEMPLATE_DIR"
  exit 1
fi

echo "🔍 Scanning $TEMPLATE_DIR for prompt templates..."

selected=$(find "$TEMPLATE_DIR" -type f -name "*.md" | fzf --preview 'bat --style=numbers --color=always --line-range :40 {}')

if [[ -z "$selected" ]]; then
  echo "❌ No prompt selected."
  exit 1
fi

if command -v wl-copy &> /dev/null; then
  cat "$selected" | wl-copy
  echo "✅ Prompt copied to clipboard using wl-copy"
elif command -v clip.exe &> /dev/null; then
  cat "$selected" | clip.exe
  echo "✅ Prompt copied to clipboard using clip.exe (WSL)"
else
  echo "⚠️ No clipboard tool found (tried wl-copy, clip.exe)"
  echo "📄 Prompt path: $selected"
fi

echo "📄 Selected: $(basename "$selected")"
