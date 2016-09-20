import unittest
import pivportal.cli


class TestCli(unittest.TestCase):

    def test_username_is_valid_withinvalidchars(self):
        assert pivportal.cli.username_is_valid("%#DW;") == False

    def test_username_is_valid(self):
        assert pivportal.cli.username_is_valid("test_user-123") == True
