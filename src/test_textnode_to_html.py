import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode
from htmlnode import HTMLNode  # Import function to test

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_normal_text(self):
        node = TextNode("Hello, world!", TextType.NORMAL, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "Hello, world!")

    def test_bold_text(self):
        node = TextNode("Bold Text", TextType.BOLD, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Bold Text</b>")

    def test_italic_text(self):
        node = TextNode("Italic Text", TextType.ITALIC, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>Italic Text</i>")

    def test_code_text(self):
        node = TextNode("print('Hello')", TextType.CODE, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>print('Hello')</code>")

    def test_link_text(self):
        node = TextNode("Click here", TextType.LINKS, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">Click here</a>')

    def test_link_without_url(self):
        node = TextNode("Click here", TextType.LINKS, None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            text_node_to_html_node("Not a TextNode")

if __name__ == "__main__":
    unittest.main()
