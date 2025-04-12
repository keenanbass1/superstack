#!/usr/bin/env bash

# -------------------------------------------------------
# Superstack Tool: Convert EPUB to Claude-Friendly Markdown
# Handles WSL/Windows paths and auto-detects output directory
# -------------------------------------------------------

set -e

# Function to convert Windows-style path to WSL path if needed
convert_path() {
  local input_path="$1"
  if [[ "$input_path" =~ ^[A-Za-z]:\\ ]]; then
    # Windows-style path like C:\Users\
    wslpath -u "$input_path"
  else
    echo "$input_path"
  fi
}

# Default paths
DEFAULT_OUTPUT_DIR="/mnt/c/Users/keena/Desktop/dev/sandbox-ai/converted"
INPUT="$(convert_path "$1")"
OUTPUT_DIR="$(convert_path "${2:-$DEFAULT_OUTPUT_DIR}")"

if [[ -z "$INPUT" ]]; then
  echo "❌ Usage: convert-epub-to-md.sh [input-file] [optional-output-dir]"
  echo "👉 Input should be an .epub file located in or mounted under /mnt/c/... or ~/dev/..."
  exit 1
fi

# Validate file exists
if [[ ! -f "$INPUT" ]]; then
  echo "❌ Input file not found: $INPUT"
  exit 1
fi

# Validate pandoc is installed
if ! command -v pandoc &> /dev/null; then
  echo "❌ pandoc not found. Please install pandoc in your WSL environment."
  exit 1
fi

# Prep paths
FILENAME=$(basename -- "$INPUT")
BASENAME="${FILENAME%.*}"
mkdir -p "$OUTPUT_DIR"
OUTFILE="$OUTPUT_DIR/$BASENAME.md"

echo "🔄 Converting $INPUT → $OUTFILE"

# Convert to Markdown
pandoc "$INPUT" \
  --from=epub \
  --to=gfm \
  --wrap=preserve \
  --extract-media="$OUTPUT_DIR/media" \
  -o "$OUTFILE"

echo "✅ Raw Markdown saved to $OUTFILE"

# Basic Cleanup
echo "🧼 Cleaning up output..."
sed -i '/^<!--.*-->$/d' "$OUTFILE"                # Remove HTML comments
sed -i 's/ / /g' "$OUTFILE"                       # Replace non-breaking spaces
sed -i 's/^\s*$/\n/g' "$OUTFILE"                 # Normalize blank lines
sed -i 's/^\*\*\*\*/---/g' "$OUTFILE"          # Convert HR styles

# Header normalization
sed -i 's/^######\s*/##### /g' "$OUTFILE"
sed -i 's/^#####\s*/#### /g' "$OUTFILE"
sed -i 's/^####\s*/### /g' "$OUTFILE"
sed -i 's/^###\s*/## /g' "$OUTFILE"
sed -i 's/^##\s*/# /g' "$OUTFILE"

echo "📁 Media (if any) extracted to: $OUTPUT_DIR/media/"
echo "✨ Ready for Claude module extraction."
