#!/usr/bin/env bash

# ------------------------------------------------------
# extract-epub-to-context.sh
# Converts an EPUB book all the way to Claude-ready modules
# ------------------------------------------------------

set -e

EPUB_PATH="$1"
BASENAME=$(basename -- "$EPUB_PATH" .epub)
WORK_DIR="${2:-./extracted/$BASENAME}"
RAW_MD="$WORK_DIR/$BASENAME.md"
CLEAN_MD="$WORK_DIR/${BASENAME}-clean.md"
CHUNK_DIR="$WORK_DIR/chunks"
MODULE_DIR="$WORK_DIR/modules"

if [[ -z "$EPUB_PATH" ]]; then
  echo "Usage: extract-epub-to-context.sh book.epub [output-dir]"
  exit 1
fi

echo "📚 Processing: $EPUB_PATH"
echo "📁 Output base: $WORK_DIR"

mkdir -p "$WORK_DIR"

# Step 1: Convert EPUB to Markdown
echo "🔄 Converting EPUB to raw markdown..."
./convert-epub-to-md.sh "$EPUB_PATH" "$WORK_DIR"

# Step 2: Clean Markdown
echo "🧼 Cleaning markdown..."
python3 strip-stylebook-noise.py "$RAW_MD" "$CLEAN_MD"

# Step 3: Split into chunks
echo "✂️ Splitting cleaned markdown..."
python3 context-splitter.py "$CLEAN_MD" "$CHUNK_DIR"

# Step 4: Scaffold modules
echo "🧱 Scaffolding Claude-ready modules..."
mkdir -p "$MODULE_DIR"
for f in "$CHUNK_DIR"/*.md; do
  out="$MODULE_DIR/$(basename "$f")"
  python3 scaffold-context-modules.py "$f" "$out"
done

echo "✅ Complete! Final modules: $MODULE_DIR"

