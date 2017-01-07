import unittest
import json
import pivportal.security
import pivportal.rest


class TestCli(unittest.TestCase):

    def setUp(self):
        from flask_redis import FlaskRedis
        from mockredis import MockRedis
        class MockRedisWrapper(MockRedis):
            '''A wrapper to add the `from_url` classmethod'''
            @classmethod
            def from_url(cls, *args, **kwargs):
                return cls()
        pivportal.rest.redis_store = FlaskRedis.from_custom_provider(MockRedisWrapper)
        pivportal.rest.redis_store.init_app(pivportal.rest.app)

    def test_dn_is_valid_withinvalidchars(self):
        assert pivportal.security.dn_is_valid("%#DW;$%&*") == False

    def test_dn_is_valid(self):
        assert pivportal.security.dn_is_valid("test_user-123") == True

    def test_username_is_valid_withinvalidchars(self):
        assert pivportal.security.username_is_valid("%#DW;") == False

    def test_username_is_valid(self):
        pivportal.security.dn_to_username = {'test_dn1': "test_user-123"}
        assert pivportal.security.username_is_valid("test_user-123") == True

    def test_requestid_is_valid(self):
        assert pivportal.security.requestid_is_valid("1234567890123456") == True

    def test_requestid_is_valid_bad(self):
        assert pivportal.security.requestid_is_valid("11234567890123456") == False

    def test_requestid_is_valid_badchar(self):
        assert pivportal.security.requestid_is_valid("^1234567890123456") == False

    def test_ip_is_valid(self):
        assert pivportal.security.ip_is_valid("127.0.0.1") == True

    def test_ip_is_valid_badchar(self):
        assert pivportal.security.ip_is_valid(".127.0.0.1") == False

    def test_is_duplicate_register(self):
        username = "user1"
        requestid = "1234567890123456"
        authorized = False
        auth_requests = {"2234567890123456": json.dumps({ "username": username, "authorized": authorized})}
        assert pivportal.security.is_duplicate_register(username, requestid, auth_requests) == False

    def test_is_duplicate_register_samerequestid(self):
        username = "user1"
        requestid = "1234567890123456"
        authorized = False
        auth_requests = {requestid: json.dumps({ "username": username, "authorized": authorized})}
        assert pivportal.security.is_duplicate_register(username, requestid, auth_requests) == True

    def test_is_duplicate_register_exact(self):
        username = "user1"
        requestid = "1234567890123456"
        authorized = False
        auth_requests = {requestid: json.dumps({ "username": username, "authorized": authorized})}
        assert pivportal.security.is_duplicate_register(username, requestid, auth_requests) == True

    def test_user_auth(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        result = pivportal.rest.app.test_client().post("/api/rest/user/login", headers={'SSL_CLIENT_S_DN': 'test_dn1'})
        assert result.status_code == 200

    def test_user_info(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        token_raw = pivportal.rest.app.test_client().post("/api/rest/user/login", headers={'SSL_CLIENT_S_DN': 'test_dn1'})
        token = "%s %s" % ("Authorization", json.loads(token_raw.get_data())["token"])
        result = pivportal.rest.app.test_client().post("/api/rest/user/info", headers={'SSL_CLIENT_S_DN': 'test_dn1', "Authorization": token})
        assert result.status_code == 200

    def test_request_list_invaliduser(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        result = pivportal.rest.app.test_client().post("/api/rest/request/list", headers={'SSL_CLIENT_S_DN': 'test_dn9'})
        assert result.status_code == 401

    def test_request_list(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        token_raw = pivportal.rest.app.test_client().post("/api/rest/user/login", headers={'SSL_CLIENT_S_DN': 'test_dn1'})
        token = "%s %s" % ("Authorization", json.loads(token_raw.get_data())["token"])
        result = pivportal.rest.app.test_client().post("/api/rest/request/list", headers={'SSL_CLIENT_S_DN': 'test_dn1', "Authorization": token})
        assert result.status_code == 200

    def test_request_list_with_requests(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        result = pivportal.rest.app.test_client().post("/api/client/request/register", data={'username': 'testuser1', 'requestid': '0204067090123451'})
        token_raw = pivportal.rest.app.test_client().post("/api/rest/user/login", headers={'SSL_CLIENT_S_DN': 'test_dn1'})
        token = "%s %s" % ("Authorization", json.loads(token_raw.get_data())["token"])
        result = pivportal.rest.app.test_client().post("/api/rest/request/list", headers={'SSL_CLIENT_S_DN': 'test_dn1', "Authorization": token})
        assert result.status_code == 200 and len(json.loads(result.get_data())) == 1

    def test_request_register_usernotfound(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        result = pivportal.rest.app.test_client().post("/api/client/request/register", data={'username': 'unknownuser', 'requestid': '234567890123456'})
        print(result)
        assert result.status_code == 400

    def test_request_register_badrequestid(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        result = pivportal.rest.app.test_client().post("/api/client/request/register", data={'username': 'testuser1', 'requestid': '234567890123456'})
        print(result)
        assert result.status_code == 400

    def test_request_register_nousername(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        result = pivportal.rest.app.test_client().post("/api/client/request/register", data={'requestid': '234567890123456'})
        print(result)
        assert result.status_code == 400

    def test_request_register_norequestid(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        result = pivportal.rest.app.test_client().post("/api/client/request/register", data={'username': 'testuser1'})
        assert result.status_code == 400

    def test_request_register(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        result = pivportal.rest.app.test_client().post("/api/client/request/register", data={'username': 'testuser1', 'requestid': '1234567890123456'})
        assert result.status_code == 200

    def test_request_status_notauthed(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        pivportal.rest.app.test_client().post("/api/client/request/register", data={'username': 'testuser1', 'requestid': '1234567890123456'})
        result = pivportal.rest.app.test_client().post("/api/client/request/status", data={'username': 'testuser1', 'requestid': '1234567890123456'})
        assert result.status_code == 401

    def test_request_status(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        # Register request
        pivportal.rest.app.test_client().post("/api/client/request/register", data={'username': 'testuser1', 'requestid': '1234567890123456'})

        # Login and auth request
        token_raw = pivportal.rest.app.test_client().post("/api/rest/user/login", headers={'SSL_CLIENT_S_DN': 'test_dn1'})
        print(token_raw)
        token = "%s %s" % ("Authorization", json.loads(token_raw.get_data())["token"])
        result_auth = pivportal.rest.app.test_client().post("/api/rest/request/auth", headers={'SSL_CLIENT_S_DN': 'test_dn1', "Authorization": token}, data=json.dumps({'username': 'testuser1', 'requestid': '1234567890123456', 'authorized': True, 'client_ip': "127.0.0.1"}), content_type='application/json')
        print(result_auth)

        # Status on request
        result_status = pivportal.rest.app.test_client().post("/api/client/request/status", data={'username': 'testuser1', 'requestid': '1234567890123456'})
        print(result_status)
        assert result_status.status_code == 200

    def test_request_auth(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        token_raw = pivportal.rest.app.test_client().post("/api/rest/user/login", headers={'SSL_CLIENT_S_DN': 'test_dn1'})
        print(token_raw)
        token = "%s %s" % ("Authorization", json.loads(token_raw.get_data())["token"])
        result = pivportal.rest.app.test_client().post("/api/rest/request/auth", headers={'SSL_CLIENT_S_DN': 'test_dn1', "Authorization": token}, data=json.dumps({'username': 'testuser1', 'requestid': '1234567890123456', 'authorized': True, 'client_ip': "127.0.0.1"}), content_type='application/json')
        assert result.status_code == 200

    def test_token_required_invalidtoken(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        token = "%s %s" % ("Authorization", "badtoken123")
        result = pivportal.rest.app.test_client().post("/api/rest/request/auth", headers={'SSL_CLIENT_S_DN': 'test_dn1', "Authorization": token}, data=json.dumps({'username': 'testuser1', 'requestid': '1234567890123456', 'authorized': True, 'client_ip': "127.0.0.1"}), content_type='application/json')
        assert result.status_code == 401

    def test_valid_client_cert_required_missingclientdnheader(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1"}
        token_raw = pivportal.rest.app.test_client().post("/api/rest/user/login", headers={'SSL_CLIENT_S_DN': 'test_dn1'})
        print(token_raw)
        token = "%s %s" % ("Authorization", json.loads(token_raw.get_data())["token"])
        result = pivportal.rest.app.test_client().post("/api/rest/request/auth", headers={"Authorization": token}, data=json.dumps({'username': 'testuser1', 'requestid': '1234567890123456', 'authorized': True, 'client_ip': "127.0.0.1"}), content_type='application/json')
        assert result.status_code == 401

    def test_valid_client_cert_required_notvaliduser(self):
        pivportal.security.dn_to_username = {}
        result = pivportal.rest.app.test_client().post("/api/rest/user/login", headers={'SSL_CLIENT_S_DN': 'test_dn1'})
        assert result.status_code == 401

    def test_valid_client_cert_required_invalidusername(self):
        pivportal.security.dn_to_username = {'test_dn1': "testuser1.$#@#"}
        result = pivportal.rest.app.test_client().post("/api/rest/user/login", headers={'SSL_CLIENT_S_DN': 'testuser1.$#@#'})
        assert result.status_code == 400