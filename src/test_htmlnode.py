import unittest
from htmlnode import HTMLNode, LeafNode  # Assuming your file is in src/htmlnode.py
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html_single(self):
        """Test props_to_html with a single attribute."""
        node = HTMLNode(tag="a", props={"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), 'href="https://example.com"')

    def test_props_to_html_multiple(self):
        """Test props_to_html with multiple attributes."""
        node = HTMLNode(tag="img", props={"src": "image.png", "alt": "An image"})
        self.assertEqual(node.props_to_html(), 'src="image.png" alt="An image"')

    def test_props_to_html_empty(self):
        """Test props_to_html when no attributes are provided."""
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), '')  # Should return an empty string


class TestLeafNode(unittest.TestCase):

    def test_leafnode_with_tag(self):
        """Test rendering with a tag."""
        node = LeafNode(tag="p", value="This is a paragraph.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")

    def test_leafnode_without_tag(self):
        """Test rendering raw text when tag is None."""
        node = LeafNode(tag=None, value="Plain text")
        self.assertEqual(node.to_html(), "Plain text")

    def test_leafnode_with_props(self):
        """Test rendering with attributes."""
        node = LeafNode(tag="a", value="Click here", props={"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click here</a>')

    def test_leafnode_no_value_error(self):
        """Test that a LeafNode without a value raises an error."""
        with self.assertRaises(ValueError):
            LeafNode(tag="p", value=None)

if __name__ == "__main__":
    unittest.main()
