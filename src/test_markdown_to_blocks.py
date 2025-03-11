import unittest
from markdown_to_blocks import (
    markdown_to_blocks, 
    block_to_block_type, 
    markdown_to_html_node, 
    BlockType,
)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
                self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
                self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
                self.assertEqual(block_to_block_type("```\ncode block\n```"), BlockType.CODE)
                self.assertEqual(block_to_block_type("> Quote line 1\n> Quote line 2"), BlockType.QUOTE)
                self.assertEqual(block_to_block_type("* Unordered list item 1\n* Unordered list item 2"), BlockType.UNORDERED_LIST)
                self.assertEqual(block_to_block_type("1. Ordered list item 1\n2. Ordered list item 2"), BlockType.ORDERED_LIST)
                self.assertEqual(block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)

    
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and ```code``` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
              html,
              "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        print("NODE:",node)
        html = node.to_html()
        # print("HTML:",html)
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )