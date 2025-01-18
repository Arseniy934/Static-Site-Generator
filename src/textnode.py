from enum import Enum
from htmlnode import LeafNode
import re
class TextType(Enum):
    plain_text = "plain"
    bold_text = "bold"
    italic_text = "italic"
    code_text = "code"
    url_text = "url"
    image = "image"

class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self,other):
        if not isinstance(other,TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    def __repr__(self):
        return f"TextNode({self.text},{self.text_type.value},{self.url})"
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.plain_text:
        return LeafNode(None, text_node.text, None)
    elif text_node.text_type == TextType.bold_text:
        return LeafNode("b", text_node.text, None)
    elif text_node.text_type == TextType.italic_text:
        return LeafNode("i", text_node.text, None)
    elif text_node.text_type == TextType.code_text:
        return LeafNode("code", text_node.text, None)
    elif text_node.text_type == TextType.url_text:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.image:
        # Для изображений значение (value) не требуется
        return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Неверный тип текста")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.plain_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            # Если форматирующие символы не закрыты, считаем весь текст обычным текстом
            new_nodes.append(TextNode(old_node.text, TextType.plain_text))
            continue
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.plain_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    a = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return a

def extract_markdown_links(text):
    a = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return a

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.plain_text:
            result.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            result.append(node)
            continue
        for alt_text, url in images:
            sections = node.text.split(f"![{alt_text}]({url})", 1)
            if sections[0] != "":
                result.append(TextNode(sections[0],TextType.plain_text))
            result.append(TextNode(alt_text,TextType.image,url))
            node.text = sections[1]
        if node.text != "":
            result.append(TextNode(node.text, TextType.plain_text))
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            result.append(node)
            continue
        for text, url in links:
            sections = node.text.split(f"[{text}]({url})", 1)
            if sections[0] != "":
                result.append(TextNode(sections[0],TextType.plain_text))
            result.append(TextNode(text,TextType.url_text,url))
            node.text = sections[1]
        if node.text != "":
            result.append(TextNode(node.text, TextType.plain_text))
    return result

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.plain_text)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.bold_text)
    nodes = split_nodes_delimiter(nodes, "*", TextType.italic_text)
    nodes = split_nodes_delimiter(nodes, "`", TextType.code_text)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = [node for node in nodes if node.text.strip() != ""]
    return nodes


