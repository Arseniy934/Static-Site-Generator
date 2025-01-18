
class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if self.props is None:
            return ""
        if self.props == {}:
            return ""
        a = []
        for key,value in self.props.items():
            a.append(f'{key}="{value}"')
        return " " + " ".join(a)
    def __repr__(self):
        return f"HTMLNode(tag={self.tag},value={self.value},children={self.children},props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag == "img":
            # Для тега <img> значение (value) не требуется
            return f"<{self.tag}{self.props_to_html()}>"
        if self.value is None:
            raise ValueError(f"LeafNode требует значение (value). Текущий тег: {self.tag}")
        elif not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,None,children,props)
    def to_html(self):
        if not self.tag:
            raise ValueError("TAG IS NONE...")
        elif not isinstance(self.children, list):
            raise ValueError("CHILDREN IS NONE...")
        elif not self.children:
            return f"<{self.tag}></{self.tag}>"
        else:
            a = ""
            for i in self.children:
                a += i.to_html()
            return f"<{self.tag}>{a}</{self.tag}>"

