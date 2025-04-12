#!/usr/bin/env python3

import sys
from pathlib import Path

TEMPLATE = """---
title: "{title}"
source: "AP Stylebook"
tags: []
level: "reference"
---

## Conceptual Definition

_TODO: Summarize the concept in 1–2 sentences._

## Core Principles

- TODO
- TODO

## Implementation Patterns

- TODO

## Anti-Patterns

- TODO

## Reasoning Principles

- TODO

## Related Concepts

- TODO
"""

def scaffold_module(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    title = lines[0].strip("#\n ")
    content = TEMPLATE.format(title=title)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
        f.write("\n\n")
        f.writelines(lines[1:])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: scaffold-context-modules.py input.md output.md")
        sys.exit(1)
    scaffold_module(sys.argv[1], sys.argv[2])
