import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        """Test that two identical TextNode objects are equal, no URL."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_equal_nodes(self):
        """Test that two identical TextNode objects are equal."""
        node1 = TextNode("Hello", TextType.BOLD, "https://example.com")
        node2 = TextNode("Hello", TextType.BOLD, "https://example.com")
        self.assertEqual(node1, node2)

    def test_different_text_type(self):
        """Test that nodes with different text types are not equal."""
        node1 = TextNode("Hello", TextType.BOLD, "https://example.com")
        node2 = TextNode("Hello", TextType.ITALIC, "https://example.com")
        self.assertNotEqual(node1, node2)

    def test_different_urls(self):
        """Test that nodes with different URLs are not equal."""
        node1 = TextNode("Hello", TextType.BOLD, "https://example.com")
        node2 = TextNode("Hello", TextType.BOLD, "https://another.com")
        self.assertNotEqual(node1, node2)

    def test_url_none(self):
        """Test that nodes with None as URL still behave correctly."""
        node1 = TextNode("Hello", TextType.BOLD, None)
        node2 = TextNode("Hello", TextType.BOLD, None)
        self.assertEqual(node1, node2)

    def test_different_text(self):
        """Test that nodes with different text content are not equal."""
        node1 = TextNode("Hello", TextType.BOLD, "https://example.com")
        node2 = TextNode("Hi", TextType.BOLD, "https://example.com")
        self.assertNotEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()
