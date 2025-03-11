# from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []  # Default to an empty list
        self.props = props or {}  # Ensure props is always a dictionary

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        """Convert self.props dictionary to an HTML attribute string."""
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        """Return a string representation of the HTMLNode for debugging."""
        return (f"HTMLNode(tag='{self.tag}', value='{self.value}', "
                f"children={self.children}, props={self.props})")

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        """Initialize a LeafNode with a required value. It cannot have children."""
        if value is None:
            raise ValueError("LeafNode requires a value.")

        super().__init__(tag=tag, value=value, children=[], props=props or {})

    def to_html(self):
        """Convert LeafNode to an HTML string."""
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")

        if self.tag is None:
            return self.value  # No tag, return raw text

        props_str = self.props_to_html()
        if props_str:
            return f"<{self.tag} {props_str}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        """Return a string representation of the LeafNode."""
        return f"LeafNode(tag='{self.tag}', value='{self.value}', props={self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        """Initialize a ParendNode with a required: tag and children. It doesn't take a value."""
        if tag is None:
            raise ValueError("ParentNode requires a tag.")
        if not children:
            raise ValueError("ParentNode must have at least a children.")
        
        if props is None:
            props = {}
        
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        """Convert ParentNode to an HTML string recursevely."""
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        
        if not self.children:
            raise ValueError("ParentNode must have at least a children")

        props_str = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children)

        if props_str:
            return f"<{self.tag} {props_str}>{children_html}</{self.tag}>"
        return f"<{self.tag}>{children_html}</{self.tag}>"

    def __repr__(self):
        """Return a string representation of the ParentNode."""
        return f"ParentNode(tag='{self.tag}', children={self.children}, props={self.props})"

