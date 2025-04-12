#!/usr/bin/env python3

import re
import sys
from pathlib import Path

def clean_markdown(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Remove irrelevant sections
    noise_headings = ['Acknowledgements', 'License', 'Foreword', 'Credits', 'Copyright']
    for heading in noise_headings:
        text = re.sub(rf'#+\s*{heading}.*?(?=\n#+|\Z)', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Normalize all headings to max depth 3
    text = re.sub(r'######', '###', text)
    text = re.sub(r'#####', '###', text)
    text = re.sub(r'####', '##', text)
    text = re.sub(r'###', '##', text)
    text = re.sub(r'##', '#', text)

    # Collapse short lines into paragraphs
    lines = text.splitlines()
    new_lines = []
    buffer = ""
    for line in lines:
        if len(line.strip()) < 60 and not line.startswith('#'):
            buffer += " " + line.strip()
        else:
            if buffer:
                new_lines.append(buffer.strip())
                buffer = ""
            new_lines.append(line.strip())
    if buffer:
        new_lines.append(buffer.strip())

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(new_lines))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: strip-stylebook-noise.py input.md output.md")
        sys.exit(1)
    clean_markdown(sys.argv[1], sys.argv[2])
