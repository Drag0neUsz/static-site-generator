from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode, HTMLNode
from copy import copy_files
import os
from web_builder import generate_pages_recursive

def main():
    text_node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    print(text_node)
    node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)

    print(node.to_html())  
    wd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    copy_files(wd + "/static", wd + "/public")
    generate_pages_recursive(wd + "/src/content", wd + "/template.html", wd + "/public")

if __name__ == "__main__":
    main()