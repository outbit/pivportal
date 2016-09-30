import unittest
import pivportal.cli


class TestCli(unittest.TestCase):

    def test_dn_is_valid_withinvalidchars(self):
        assert pivportal.cli.dn_is_valid("%#DW;$%&*") == False

    def test_dn_is_valid(self):
        assert pivportal.cli.dn_is_valid("test_user-123") == True

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

    def test_ip_is_valid(self):
        assert pivportal.cli.ip_is_valid("127.0.0.1") == True

    def test_ip_is_valid_badchar(self):
        assert pivportal.cli.ip_is_valid(".127.0.0.1") == False

    def test_is_duplicate_register(self):
        username = "user1"
        requestid = "1234567890123456"
        authorized = False
        auth_requests = [{ "username": username, "requestid": "2234567890123456", "authorized": authorized},]
        assert pivportal.cli.is_duplicate_register(username, requestid, auth_requests) == False

    def test_is_duplicate_register_samerequestid(self):
        username = "user1"
        requestid = "1234567890123456"
        authorized = False
        auth_requests = [{ "username": username, "requestid": requestid, "authorized": authorized},]
        assert pivportal.cli.is_duplicate_register(username, requestid, auth_requests) == True

    def test_is_duplicate_register_exact(self):
        username = "user1"
        requestid = "1234567890123456"
        authorized = False
        auth_requests = [{ "username": username, "requestid": requestid, "authorized": authorized},]
        assert pivportal.cli.is_duplicate_register(username, requestid, auth_requests) == True

    def test_request_list_invaliduser(self):
        pivportal.cli.dn_to_username = {'test_dn1': "testuser1"}
        result = pivportal.cli.app.test_client().post("/api/rest/request/list", headers={'SSL_CLIENT_S_DN': 'test_dn9'})
        assert result.status_code == 401

    def test_request_list(self):
        pivportal.cli.dn_to_username = {'test_dn1': "testuser1"}
        result = pivportal.cli.app.test_client().post("/api/rest/request/list", headers={'SSL_CLIENT_S_DN': 'test_dn1'})
        assert result.status_code == 200

    def test_request_register_badrequestid(self):
        pivportal.cli.dn_to_username = {'test_dn1': "testuser1"}
        result = pivportal.cli.app.test_client().post("/api/client/request/register", data={'username': 'testuser', 'requestid': '234567890123456'})
        print(result)
        assert result.status_code == 400

    def test_request_register_nousername(self):
        pivportal.cli.dn_to_username = {'test_dn1': "testuser1"}
        result = pivportal.cli.app.test_client().post("/api/client/request/register", data={'requestid': '234567890123456'})
        print(result)
        assert result.status_code == 400

    def test_request_register_norequestid(self):
        pivportal.cli.dn_to_username = {'test_dn1': "testuser1"}
        result = pivportal.cli.app.test_client().post("/api/client/request/register", data={'username': 'testuser'})
        assert result.status_code == 400

    def test_request_register(self):
        pivportal.cli.dn_to_username = {'test_dn1': "testuser1"}
        result = pivportal.cli.app.test_client().post("/api/client/request/register", data={'username': 'testuser', 'requestid': '1234567890123456'})
        assert result.status_code == 200
