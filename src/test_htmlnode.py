import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("div", "This is a div", props={"class": "container"})
        self.assertEqual(node.props_to_html(), " class=\"container\"")
    def test_props_to_html2(self):
        node = HTMLNode("div", "This is a div", props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), " class=\"container\" id=\"main\"")
    def test_eq(self):
        node = HTMLNode("div", "This is a div", props={"class": "container"})
        node2 = HTMLNode("div", "This is a div", props={"class": "container"})
        self.assertEqual(node, node2)
    def test_neq(self):
        node = HTMLNode("div", "This is a div", props={"class": "container"})
        node2 = HTMLNode("div", "This is a div", props={"class": "container2"})
        self.assertNotEqual(node, node2)
   
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    def test_eq(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("p", "Hello, world!")
        self.assertEqual(node, node2)
    def test_neq(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("p", "Hello, world!2")
        self.assertNotEqual(node, node2)


class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")
    def test_to_html_with_props(self):
        parent_node = ParentNode("div", [], {"class": "container"})
        self.assertEqual(parent_node.to_html(), "<div class=\"container\"></div>")
    def test_to_html_with_multiple_children_props(self):
        child_node = LeafNode("span", "child", {"class": "child"})
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(parent_node.to_html(), "<div class=\"container\"><span class=\"child\">child</span></div>")


if __name__ == "__main__":
    unittest.main()