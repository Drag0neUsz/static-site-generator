class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError("Subclasses must implement this method")

    def props_to_html(self):
        if self.props is None:
            return ""
        return " "+" ".join([f"{key}=\"{value}\"" for key, value in self.props.items()])

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str = None, props: dict[str, str] = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Value is required for leaf nodes")
        if self.tag is None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        if self.children is None:
            raise ValueError("Children are required for parent nodes")
        if self.tag is None:
            raise ValueError("Tag is required for parent nodes")

        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"