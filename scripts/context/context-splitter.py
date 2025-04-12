#!/usr/bin/env python3

import re
import sys
from pathlib import Path

def split_by_heading(input_file, output_dir, heading_level='#', max_tokens=3500):
    try:
        import tiktoken
        enc = tiktoken.get_encoding('cl100k_base')
    except ImportError:
        print("⚠️ Requires `tiktoken` for token counting. Install via `pip install tiktoken`.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    sections = re.split(rf'(^{heading_level} .+?$)', text, flags=re.MULTILINE)
    combined = []
    for i in range(1, len(sections), 2):
        header = sections[i].strip()
        body = sections[i+1].strip() if i+1 < len(sections) else ""
        combined.append(f"{header}\n{body}")

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for i, chunk in enumerate(combined):
        tokens = len(enc.encode(chunk))
        if tokens > max_tokens:
            print(f"⚠️ Chunk {i} exceeds {max_tokens} tokens ({tokens}) — consider manual split.")
        out_file = Path(output_dir) / f"{i+1:02d}-{chunk.splitlines()[0].strip('# ').lower().replace(' ', '-')[:50]}.md"
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(chunk)
        print(f"✅ Saved: {out_file} ({tokens} tokens)")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: context-splitter.py input.md output_dir/")
        sys.exit(1)
    split_by_heading(sys.argv[1], sys.argv[2])
