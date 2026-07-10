import unittest
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
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
        node = TextNode("This is a **double** **bold text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[1].text, "double")
        self.assertEqual(new_nodes[2].text, " ")
        self.assertEqual(new_nodes[3].text, "bold text")
        self.assertEqual(new_nodes[0].type, TextType.TEXT)
        self.assertEqual(new_nodes[1].type, TextType.BOLD)
        self.assertEqual(new_nodes[2].type, TextType.TEXT)
        self.assertEqual(new_nodes[3].type, TextType.BOLD)

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
        node = TextNode("This is a _double_ _italic text_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[1].text, "double")
        self.assertEqual(new_nodes[2].text, " ")
        self.assertEqual(new_nodes[3].text, "italic text")
        self.assertEqual(new_nodes[0].type, TextType.TEXT)
        self.assertEqual(new_nodes[1].type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].type, TextType.TEXT)
        self.assertEqual(new_nodes[3].type, TextType.ITALIC)

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

class TestSplitNodesImageAndLink(unittest.TestCase):
    def test_split_nodes_image_along_link(self):
        node = TextNode("This is text with an img ![to boot dev](https://www.boot.dev) and a link to [to youtube](https://www.youtube.com/@bootdotdev), and another image ![to youtube](https://www.youtube.com/@bootdotdev) as well as a link to [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        new_nodes = split_nodes_image([node])   
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is text with an img ")
        self.assertEqual(new_nodes[0].type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[2].text, " and a link to [to youtube](https://www.youtube.com/@bootdotdev), and another image ")
        self.assertEqual(new_nodes[2].type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "to youtube")
        self.assertEqual(new_nodes[3].type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].url, "https://www.youtube.com/@bootdotdev")
        self.assertEqual(new_nodes[4].text, " as well as a link to [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(new_nodes[4].type, TextType.TEXT)
    
    def test_split_nodes_image(self):
        node = TextNode("This is text with an img ![to boot dev](https://www.boot.dev) and a link to [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with an img ")
        self.assertEqual(new_nodes[0].type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[2].text, " and a link to [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(new_nodes[2].type, TextType.TEXT)
    
    def test_split_nodes_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[0].type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "to youtube")
        self.assertEqual(new_nodes[3].type, TextType.LINK)
        self.assertEqual(new_nodes[3].url, "https://www.youtube.com/@bootdotdev")

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is just a plain text without any links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is just a plain text without any links.")
        self.assertEqual(new_nodes[0].type, TextType.TEXT)

    def test_split_nodes_image_only_image(self):
        node = TextNode("![only image](https://www.boot.dev/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "only image")
        self.assertEqual(new_nodes[0].type, TextType.IMAGE)
        self.assertEqual(new_nodes[0].url, "https://www.boot.dev/img.png")

    def test_split_nodes_link_consecutive(self):
        node = TextNode("[first link](url1)[second link](url2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "first link")
        self.assertEqual(new_nodes[0].type, TextType.LINK)
        self.assertEqual(new_nodes[0].url, "url1")
        self.assertEqual(new_nodes[1].text, "second link")
        self.assertEqual(new_nodes[1].type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "url2")

    def test_split_nodes_link_ignores_non_text_nodes(self):
        node = TextNode("`[this looks like a link](url) but is code`", TextType.CODE)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "`[this looks like a link](url) but is code`")
        self.assertEqual(new_nodes[0].type, TextType.CODE)

    def test_split_nodes_image_multiple_nodes_input(self):
        node1 = TextNode("Text with ![img1](url1) here.", TextType.TEXT)
        node2 = TextNode("Code block", TextType.CODE)
        node3 = TextNode("More text with ![img2](url2)", TextType.TEXT)
        
        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertEqual(len(new_nodes), 6)
        
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[1].text, "img1")
        self.assertEqual(new_nodes[1].type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "url1")
        self.assertEqual(new_nodes[2].text, " here.")
        
        self.assertEqual(new_nodes[3].text, "Code block")
        self.assertEqual(new_nodes[3].type, TextType.CODE)
        
        self.assertEqual(new_nodes[4].text, "More text with ")
        self.assertEqual(new_nodes[5].text, "img2")
        self.assertEqual(new_nodes[5].type, TextType.IMAGE)
        
    def test_split_nodes_link_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "")
        self.assertEqual(new_nodes[0].type, TextType.TEXT)

class TestTextToTextNodes(unittest.TestCase):
    
    def test_text_to_textnodes_happy_path(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 10)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " with an ")
        self.assertEqual(nodes[2].type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " word and a ")
        self.assertEqual(nodes[4].type, TextType.TEXT)
        self.assertEqual(nodes[5].text, "code block")
        self.assertEqual(nodes[5].type, TextType.CODE)
        self.assertEqual(nodes[6].text, " and an ")
        self.assertEqual(nodes[6].type, TextType.TEXT)
        self.assertEqual(nodes[7].text, "obi wan image")
        self.assertEqual(nodes[7].type, TextType.IMAGE)
        self.assertEqual(nodes[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(nodes[8].text, " and a ")
        self.assertEqual(nodes[8].type, TextType.TEXT)
        self.assertEqual(nodes[9].text, "link")
        self.assertEqual(nodes[9].type, TextType.LINK)
        self.assertEqual(nodes[9].url, "https://boot.dev")

    def test_text_to_textnodes_plain_text_only(self):
        text = "This is just standard text without any formatting."
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is just standard text without any formatting.")
        self.assertEqual(nodes[0].type, TextType.TEXT)

    def test_text_to_textnodes_adjacent_formats(self):
        text = "**bold**_italic_`code`"
        nodes = text_to_textnodes(text)
        print(nodes)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "bold")
        self.assertEqual(nodes[0].type, TextType.BOLD)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, "code")
        self.assertEqual(nodes[2].type, TextType.CODE)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].type, TextType.TEXT)

if __name__ == "__main__":
    unittest.main()