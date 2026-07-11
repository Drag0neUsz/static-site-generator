import re
import os
from pathlib import Path

from markdown_to_html import markdown_to_html_node

def extract_title(markdown: str) -> str:
    found_match = re.search(r"^# (.*?)\n", markdown, flags=re.MULTILINE)
    if found_match is not None:
        return found_match.group(1).strip()
    raise Exception("No title found")

def generate_page(from_path, template_path, dest_path) -> str:
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    Path(dest_path).parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)
    return page


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path) -> str:

    for file in os.listdir(dir_path_content):
        if file.endswith(".md"):
            generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file.replace(".md", ".html")))
        elif os.path.isdir(os.path.join(dir_path_content, file)):
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))

generate_pages_recursive("src/content", "template.html", "public")