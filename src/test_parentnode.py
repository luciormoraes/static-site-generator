import unittest
from src.htmlnode import ParentNode, LeafNode  

class TestParentNode(unittest.TestCase):

    def test_parentnode_with_children(self):
        """Test rendering a ParentNode with nested LeafNodes."""
        child1 = LeafNode(tag="b", value="Bold")
        child2 = LeafNode(tag="i", value="Italic")
        parent = ParentNode(tag="p", children=[child1, child2])
        self.assertEqual(parent.to_html(), "<p><b>Bold</b><i>Italic</i></p>")

    def test_parentnode_with_props(self):
        """Test rendering a ParentNode with attributes."""
        child = LeafNode(tag="span", value="Hello")
        parent = ParentNode(tag="div", children=[child], props={"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><span>Hello</span></div>')

    def test_parentnode_no_tag_error(self):
        """Test error when ParentNode has no tag."""
        with self.assertRaises(ValueError):
            ParentNode(tag=None, children=[LeafNode(tag="p", value="Text")])

    def test_parentnode_no_children_error(self):
        """Test error when ParentNode has no children."""
        with self.assertRaises(ValueError):
            ParentNode(tag="p", children=[])

if __name__ == "__main__":
    unittest.main()

