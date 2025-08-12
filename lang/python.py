import io
import tokenize
from token import COMMENT, STRING
from typing import Dict, List

from handler import SourceHandler


class PythonHandler(SourceHandler):
    def __init__(self):
        super().__init__()

    def extract_comments(self, lined_file: list[str]):
        blocks = extract_comment_blocks_from_lines(lined_file)
        for b in blocks:
            end = b["end_line"]
            b["function"] = is_function_below(lined_file, end) # lined are 1 indexed because of course why not, so we pass - 1 + 1 to get the function line
        
        return blocks



def is_function_below(src_lines: List[str], test_line: int) -> bool:
    while True:
        if len(src_lines) - 1 < test_line:
            return False

        if src_lines[test_line].replace(" ", "").startswith("def"):
            return True
        elif src_lines[test_line].replace(" ", "").startswith("@"):
            print("skipping one")
            test_line += 1
            continue
        else:
            return False


def extract_triple_quoted_blocks(lined_file: List[str]) -> List[Dict]:
    source = "\n".join(lined_file)
    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    blocks = []
    for tok in tokens:
        if tok.type == STRING:
            text = tok.string
            start_line = tok.start[0]
            end_line = tok.end[0]
            # Consider triple-quoted strings spanning multiple lines
            if text.startswith(('"""', "'''")) and "\n" in text:
                blocks.append({
                    "start_line": start_line,
                    "end_line": end_line,
                    "type": "triple_quote",
                    "content": text
                })
    return blocks

def extract_hash_comment_blocks(lined_file: List[str]) -> List[Dict]:
    blocks = []
    current_block = []
    current_start = None

    for idx, line in enumerate(lined_file, 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            if current_start is None:
                current_start = idx
            current_block.append(line)
        elif stripped == "":
            # Allow blank lines inside comment blocks, so keep appending if block open
            if current_block:
                current_block.append(line)
        else:
            # Non-comment, non-blank line ends current block if any
            if current_block:
                # Remove trailing blank lines from the block content
                while current_block and current_block[-1].strip() == "":
                    current_block.pop()
                blocks.append({
                    "start_line": current_start,
                    "end_line": current_start + len(current_block) - 1,
                    "type": "hash_block",
                    "content": "\n".join(current_block)
                })
                current_block = []
                current_start = None

    # End of file, if block open, close it
    if current_block:
        while current_block and current_block[-1].strip() == "":
            current_block.pop()
        blocks.append({
            "start_line": current_start,
            "end_line": current_start + len(current_block) - 1,
            "type": "hash_block",
            "content": "\n".join(current_block)
        })
    return blocks

def extract_comment_blocks_from_lines(lined_file: List[str]) -> List[Dict]:
    hash_blocks = extract_hash_comment_blocks(lined_file)
    triple_blocks = extract_triple_quoted_blocks(lined_file)
    # Merge and sort all comment blocks by start_line
    all_blocks = hash_blocks + triple_blocks
    all_blocks.sort(key=lambda b: b['start_line'])
    return all_blocks
