#!/usr/bin/env bash

# --------------------------------------------
# extract-md-to-context.sh
# Converts a Markdown file into Claude-ready context modules
# Assumes the file is already Markdown (from EPUB or elsewhere)
# --------------------------------------------

set -e

INPUT_MD="$1"
CHUNK_DIR="${2:-./chunks}"
MODULE_DIR="${3:-./modules}"

if [[ -z "$INPUT_MD" ]]; then
  echo "Usage: extract-md-to-context.sh input.md [chunk-dir] [module-dir]"
  exit 1
fi

echo "📄 Input file: $INPUT_MD"
echo "📁 Chunk output dir: $CHUNK_DIR"
echo "📁 Module output dir: $MODULE_DIR"

# Step 1: Strip noise
CLEANED="${INPUT_MD%.md}-clean.md"
echo "🧼 Cleaning Markdown..."
python3 strip-stylebook-noise.py "$INPUT_MD" "$CLEANED"

# Step 2: Split into chunks
echo "✂️ Splitting into Claude-sized chunks..."
python3 context-splitter.py "$CLEANED" "$CHUNK_DIR"

# Step 3: Scaffold modules
echo "🧱 Scaffolding Claude-ready modules..."
mkdir -p "$MODULE_DIR"
for f in "$CHUNK_DIR"/*.md; do
  out="$MODULE_DIR/$(basename "$f")"
  python3 scaffold-context-modules.py "$f" "$out"
done

echo "✅ All done! Context modules saved to: $MODULE_DIR"
