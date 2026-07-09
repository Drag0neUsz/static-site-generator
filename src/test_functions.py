import unittest
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[0].type, TextType.TEXT)
        self.assertEqual(new_nodes[1].type, TextType.CODE)
        self.assertEqual(new_nodes[2].type, TextType.TEXT)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is a **bold text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[1].text, "bold text")
        self.assertEqual(new_nodes[0].type, TextType.TEXT)
        self.assertEqual(new_nodes[1].type, TextType.BOLD)

    def test_split_nodes_delimiter_bold_double(self):
        node = TextNode("This is a **double****bold text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[1].text, "double")
        self.assertEqual(new_nodes[2].text, "bold text")
        self.assertEqual(new_nodes[0].type, TextType.TEXT)
        self.assertEqual(new_nodes[1].type, TextType.BOLD)
        self.assertEqual(new_nodes[2].type, TextType.BOLD)

    def test_split_nodes_delimiter_bold_double_invalid(self):
        node = TextNode("This is a **double**bold text**", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is an _italic text_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is an ")
        self.assertEqual(new_nodes[1].text, "italic text")
        self.assertEqual(new_nodes[0].type, TextType.TEXT)
        self.assertEqual(new_nodes[1].type, TextType.ITALIC)
    
    def test_split_nodes_delimiter_italic_double(self):
        node = TextNode("This is a _double__italic text_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[1].text, "double")
        self.assertEqual(new_nodes[2].text, "italic text")
        self.assertEqual(new_nodes[0].type, TextType.TEXT)
        self.assertEqual(new_nodes[1].type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].type, TextType.ITALIC)

    def test_split_nodes_delimiter_italic_invalid(self):
        node = TextNode("This is a _double_italic text_", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], ("rick roll", "https://i.imgur.com/aKaOqIh.gif"))
        self.assertEqual(images[1], ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"))
    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)
    def test_extract_markdown_images_with_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"))

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0], ("to boot dev", "https://www.boot.dev"))
        self.assertEqual(links[1], ("to youtube", "https://www.youtube.com/@bootdotdev"))
    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 0)
    def test_extract_markdown_links_with_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("to youtube", "https://www.youtube.com/@bootdotdev"))

if __name__ == "__main__":
    unittest.main()