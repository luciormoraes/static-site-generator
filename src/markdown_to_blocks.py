import re
from enum import Enum
from htmlnode import ParentNode, LeafNode
from split import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    block_results = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        block_results.append(block)
    return block_results

def block_to_block_type(block):
    lines = block.split("\n")

    # Check for heading
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # Check for code block (triple backticks)
    if len(lines) > 1 and lines[0].startswith("`") and lines[-1].startswith("`"):
        return BlockType.CODE

    # Check for quote (all lines should start with ">")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Check for unordered list (* or -)
    if all(line.startswith(("* ", "- ")) for line in lines):
        return BlockType.UNORDERED_LIST

    # Check for ordered list (lines should start with "1. ", "2. ", etc.)
    if all(re.match(r"^\d+\.\s", line) for line in lines):
        return BlockType.ORDERED_LIST

    # Default to paragraph
    return BlockType.PARAGRAPH


# def markdown_to_html_node(markdown):
#     blocks = markdown_to_blocks(markdown)
#     html_blocks = []
#     for block in blocks:
#         block_type = block_to_block_type(block)
#         if block_type == BlockType.PARAGRAPH:
#             html_blocks.append(f"<p>{block}</p>")
#         elif block_type == BlockType.HEADING:
#             heading_level = block.count("#")
#             html_blocks.append(f"<h{heading_level}>{block[heading_level+1:]}</h{heading_level}>")
#         elif block_type == BlockType.CODE:
#             code_lines = block.split("\n")[1:-1]
#             code_block = "\n".join(code_lines)
#             html_blocks.append(f"<pre><code>{code_block}</code></pre>")
#         elif block_type == BlockType.QUOTE:
#             quote_lines = [line[2:] for line in block.split("\n")]
#             quote_block = "<br>".join(quote_lines)
#             html_blocks.append(f"<blockquote>{quote_block}</blockquote>")
#         elif block_type == BlockType.UNORDERED_LIST:
#             list_items = [f"<li>{line[2:]}</li>" for line in block.split("\n")]
#             list_block = "".join(list_items)
#             html_blocks.append(f"<ul>{list_block}</ul>")
#         elif block_type == BlockType.ORDERED_LIST:
#             list_items = [f"<li>{line[3:]}</li>" for line in block.split("\n")]
#             list_block = "".join(list_items)
#             html_blocks.append(f"<ol>{list_block}</ol>")
#     return "\n".join(html_blocks)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


# def code_to_html_node(block):
#     if not block.startswith("```") or not block.endswith("```"):
#         raise ValueError("Invalid code block")
#     text = block[4:-3]
#     children = text_to_children(text)
#     code = ParentNode("code", children)
#     return ParentNode("pre", [code])
def code_to_html_node(block):
    if not (block.startswith("```") and block.endswith("```")):
        raise ValueError("Invalid code block")

    # Extract raw text and preserve it without parsing Markdown formatting
    text = block[4:-3]

    # Use a single LeafNode to prevent further parsing of inline Markdown
    code_node = ParentNode("code", [LeafNode(None, text)])

    return ParentNode("pre", [code_node])



def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)