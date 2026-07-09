from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_texts = node.text.split(delimiter)
        temp: list[TextNode] = []
        # I guess if we have valid syntax then there should always be an odd number of split results
        if len(split_texts)%2 == 0:
            raise Exception("Invalid markdown syntax")
        else:
            #keeping track of the sections inside delimiters, they will always interchange with those outside
            counter = 0 if node.text[0] == delimiter else 1
            for split_text in split_texts:
                if split_text != "": temp.append(TextNode(split_text, [text_type, TextType.TEXT][counter%2]))
                counter += 1
            new_nodes.extend(temp)
    return new_nodes


def extract_markdown_images(text: str) -> list[str]:
    images = []
    for match in re.findall(r'\!\[(.*?)\]\((.*?)\)', text):
        images.append((match[0], match[1]))
    return images

def extract_markdown_links(text: str) -> list[str]:
    links = []
    for match in re.findall(r'(?<!!)\[(.*?)\]\((.*?)\)', text):
        links.append((match[0], match[1]))
    return links



