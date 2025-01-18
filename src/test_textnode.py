import unittest

from htmlnode import *
from textnode import *
from markdown import *

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_heading(self):
        markdown = "# Heading 1"
        html_node = markdown_to_html_node(markdown)
        expected_html = "<div><h1>Heading 1</h1></div>"
        self.assertEqual(html_node.to_html(), expected_html)

    def test_paragraph(self):
        markdown = "This is a paragraph."
        html_node = markdown_to_html_node(markdown)
        expected_html = "<div><p>This is a paragraph.</p></div>"
        self.assertEqual(html_node.to_html(), expected_html)

    def test_quote(self):
        markdown = "> This is a quote."
        html_node = markdown_to_html_node(markdown)
        expected_html = "<div><blockquote>This is a quote.</blockquote></div>"
        self.assertEqual(html_node.to_html(), expected_html)

    def test_unordered_list(self):
        markdown = "* Item 1\n* Item 2"
        html_node = markdown_to_html_node(markdown)
        expected_html = "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>"
        self.assertEqual(html_node.to_html(), expected_html)

    def test_ordered_list(self):
        markdown = "1. First item\n2. Second item"
        html_node = markdown_to_html_node(markdown)
        expected_html = "<div><ol><li>First item</li><li>Second item</li></ol></div>"
        self.assertEqual(html_node.to_html(), expected_html)

    def test_code_block(self):
        markdown = "'''python\nprint('Hello, world!')\n'''"
        html_node = markdown_to_html_node(markdown)
        expected_html = "<div><pre><code>print('Hello, world!')</code></pre></div>"
        self.assertEqual(html_node.to_html(), expected_html)




if __name__ == "__main__":
    unittest.main()