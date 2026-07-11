from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode, HTMLNode
from copy import copy_files
import os
from web_builder import generate_pages_recursive
import sys

def main():
    basepath = sys.argv[0] if len(sys.argv) > 0 else "/"

    wd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    copy_files(wd + "/static", wd + "/public")
    generate_pages_recursive(wd + "/src/content", wd + "/template.html", wd + "/docs", basepath)

if __name__ == "__main__":
    main()