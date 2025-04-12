#!/usr/bin/env python3

import sys
from pathlib import Path

def count_tokens(file_path):
    try:
        import tiktoken
        enc = tiktoken.get_encoding('cl100k_base')
    except ImportError:
        print("⚠️ Requires `tiktoken`. Install with `pip install tiktoken`.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    tokens = enc.encode(text)
    print(f"{file_path}: {len(tokens)} tokens")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: token-counter.py file1.md [file2.md ...]")
        sys.exit(1)
    for path in sys.argv[1:]:
        count_tokens(path)
