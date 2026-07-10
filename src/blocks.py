from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block: str) -> BlockType:
    if any(block.startswith("#"*i + " ") for i in range(1, 7)):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
   
    if all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    
    lines = block.split("\n")
    i = 1
    all_lines_start_with_number = True
    for line in lines:
        if not line.startswith(f"{i}. "):
            all_lines_start_with_number = False
            break
        i += 1
    if all_lines_start_with_number:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
