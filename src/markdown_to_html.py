from functions import markdown_to_blocks
from blocks import block_to_block_type, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from functions import text_to_textnodes
import re

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    html_node = ParentNode("div", [])
    
    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                nodes = text_to_textnodes(block)
                children = [node.text_node_to_html_node() for node in nodes]
                html_node.children.append(ParentNode("p", children))

            case BlockType.HEADING:
                level = 0
                for char in block:
                    if char == '#':
                        level += 1
                    else:
                        break
                clean_text = block[level + 1:] 
                nodes = text_to_textnodes(clean_text)
                children = [node.text_node_to_html_node() for node in nodes]
                html_node.children.append(ParentNode(f"h{level}", children))

            case BlockType.CODE:
                # Obcinamy backticki z początku i końca (oraz ewentualne nowelinie)
                clean_code = block.strip('`').strip('\n')
                html_node.children.append(ParentNode("pre", [LeafNode("code", clean_code)]))

            case BlockType.QUOTE:
                # Czyścimy każdą linijkę osobno, tak jak rozmawialiśmy wcześniej
                lines = block.split('\n')
                clean_lines = [line.lstrip("> ") for line in lines]
                clean_content = "\n".join(clean_lines)
                
                nodes = text_to_textnodes(clean_content)
                children = [node.text_node_to_html_node() for node in nodes]
                html_node.children.append(ParentNode("blockquote", children))

            case BlockType.UNORDERED_LIST:
                list_items = []
                for line in block.split('\n'):
                    clean_text = line.split(" ", 1)[1]
                    nodes = text_to_textnodes(clean_text)
                    children = [node.text_node_to_html_node() for node in nodes]
                    list_items.append(ParentNode("li", children))
                html_node.children.append(ParentNode("ul", list_items))
                
            case BlockType.ORDERED_LIST:
                list_items = []
                for line in block.split('\n'):
                    clean_text = line.split(" ", 1)[1]
                    nodes = text_to_textnodes(clean_text)
                    children = [node.text_node_to_html_node() for node in nodes]
                    list_items.append(ParentNode("li", children))
                html_node.children.append(ParentNode("ol", list_items))
    # print(block_type)
    # print(html_node.to_html())
    return html_node

