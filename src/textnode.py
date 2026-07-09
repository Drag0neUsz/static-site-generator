from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text (plain)"
    BOLD = "**Bold text**"
    ITALIC = "_Italic text_"
    CODE = "`Code text`"
    LINK = "[anchor text](url)"
    IMAGE = "![alt text](url)"
    
class TextNode:
    def __init__(self, text: str, type: TextType, url: str = None):
        self.text = text
        self.type = type
        self.url = url
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.type == other.type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.type}, {self.url})"

    def text_node_to_html_node(text_node: TextNode) -> LeafNode:
        match text_node.type:
            case TextType.TEXT:
                return LeafNode(None, text_node.text)
            case TextType.BOLD:
                return LeafNode("b", text_node.text)
            case TextType.ITALIC:
                return LeafNode("i", text_node.text)
            case TextType.CODE:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            case TextType.IMAGE:
                return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            case _:
                raise ValueError(f"Unsupported text type: {text_node.type}")