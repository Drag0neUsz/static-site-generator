import unittest
from web_builder import extract_title

class TestWebBuilder(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello World \n\n This is a test"), "Hello World")
        self.assertRaises(Exception, extract_title, "Hello World \n\n This is a test")
        self.assertEqual(extract_title("some text\n\n# # Hello World \n\n\n This is a test"), "Hello World")
