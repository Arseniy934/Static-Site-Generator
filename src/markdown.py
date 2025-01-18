from htmlnode import ParentNode, LeafNode
from textnode import TextNode, text_node_to_html_node, text_to_textnodes
import os

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block != ""]
    return blocks


def block_to_block_type(block):
    if block.startswith("#"):
        if len(block) > 1 and block[1] == " ":
            return "heading"
        for i in range(2, 7):
            if block.startswith("#" * i) and len(block) > i and block[i] == " ":
                return "heading"
    if block.startswith("'''") and block.endswith("'''"):
        return "code"
    lines = block.split("\n")
    if all(line.startswith('>') for line in lines):
        return "quote"
    if all(line.startswith('-') or line.startswith('*') for line in lines):
        return "unordered_list"
    if all(line.split(". ")[0].isdigit() and int(line.split(". ")[0]) == i + 1 for i, line in enumerate(lines)):
        return "ordered_list"
    return "paragraph"


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        if text_node.text.strip() == "":
            continue  # Пропускаем пустые TextNode
        htmlnode = text_node_to_html_node(text_node)
        if htmlnode.value is None:
            print(f"Предупреждение: создан LeafNode без значения для текста: {text_node.text}")
        children.append(htmlnode)
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == "heading":
            level = block.count("#")
            tag = f"h{level}"
            text = block.lstrip("#").strip()
            children = text_to_children(text)
            html_nodes.append(ParentNode(tag, children))

        elif block_type == "paragraph":
            children = text_to_children(block)
            html_nodes.append(ParentNode("p", children))

        elif block_type == "quote":
            lines = block.split("\n")
            text = " ".join(line.lstrip(">").strip() for line in lines)
            children = text_to_children(text)
            html_nodes.append(ParentNode("blockquote", children))

        elif block_type == "unordered_list":
            lines = block.split("\n")
            list_items = []
            for line in lines:
                text = line.lstrip("*").lstrip("-").strip()
                children = text_to_children(text)
                list_items.append(ParentNode("li", children))
            html_nodes.append(ParentNode("ul", list_items))

        elif block_type == "ordered_list":
            lines = block.split("\n")
            list_items = []
            for line in lines:
                text = line.split(". ", 1)[1]
                children = text_to_children(text)
                list_items.append(ParentNode("li", children))
            html_nodes.append(ParentNode("ol", list_items))

        elif block_type == "code":
            # Удаляем тройные кавычки и указание языка
            lines = block.split("\n")
            if lines[0].startswith("'''") and lines[-1].endswith("'''"):
                # Удаляем первую и последнюю строки (тройные кавычки)
                code_content = "\n".join(lines[1:-1]).strip()
            else:
                code_content = block.strip("'''").strip()
            children = text_to_children(code_content)
            html_nodes.append(ParentNode("pre", [ParentNode("code", children)]))

        else:
            children = text_to_children(block)
            html_nodes.append(ParentNode("p", children))

    return ParentNode("div", html_nodes)
def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("#").strip()
    raise ValueError("Заголовок h1 не найден в Markdown-тексте.")

def generate_page(from_path, template_path, dest_path):
    print(f"Создаём страницу с {from_path} по {dest_path} с помощью {template_path}")

    # Чтение Markdown-файла
    with open(from_path, "r", encoding="utf-8") as md_file:
        markdown = md_file.read()

    # Чтение шаблона
    with open(template_path, "r", encoding="utf-8") as template_file:
        template = template_file.read()

    # Преобразование Markdown в HTML
    html_content = markdown_to_html_node(markdown).to_html()

    # Извлечение заголовка
    title = extract_title(markdown)

    # Замена плейсхолдеров в шаблоне
    html_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Создание целевого каталога, если он не существует
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Сохранение результата
    with open(dest_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_page)

    print(f"Страница успешно создана: {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    # Создаем целевой каталог, если он не существует
    os.makedirs(dest_dir_path, exist_ok=True)

    # Обход каталога
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        dest_entry_path = os.path.join(dest_dir_path, entry)

        if os.path.isdir(entry_path):
            # Если это каталог, рекурсивно обрабатываем его
            generate_pages_recursive(entry_path, template_path, dest_entry_path)
        elif entry.endswith(".md"):
            # Если это Markdown-файл, создаем HTML-файл
            dest_html_path = os.path.splitext(dest_entry_path)[0] + ".html"
            generate_page(entry_path, template_path, dest_html_path)
            print(f"Создана страница: {dest_html_path}")