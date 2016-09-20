import unittest
import pivportal.cli


class TestCli(unittest.TestCase):

    def test_username_is_valid_withinvalidchars(self):
        assert pivportal.cli.username_is_valid("%#DW;") == False

    def test_username_is_valid(self):
        assert pivportal.cli.username_is_valid("test_user-123") == True

    def test_requestid_is_valid(self):
        assert pivportal.cli.requestid_is_valid("1234567890123456") == True

    def test_requestid_is_valid_bad(self):
        assert pivportal.cli.requestid_is_valid("11234567890123456") == False

    def test_requestid_is_valid_badchar(self):
        assert pivportal.cli.requestid_is_valid("^1234567890123456") == False
