#include "pam_pivportal.h"


char g_server_ips[MAX_SERVERS][MAX_STR] = {0};
char g_server_ips_len = 0;
char g_server_port[MAX_STR] = {0};
char g_client_ssl_cert[MAX_STR] = {0};
int g_server_ssl_verify_host = 0;


int read_config() {
    GKeyFile *keyfile = (GKeyFile*)0;
    GKeyFileFlags flags = (GKeyFileFlags)0;
    GError *error = (GError*)0;
    gchar **server_ips = NULL;
    gsize server_ips_len = 0;
    gchar *server_port = NULL, *client_ssl_cert = NULL;
    int x = 0;

    // Check If Config file exists, exit if it doesnt
    if ( 0 != access (PIVPORTAL_CONFIG_FILE, F_OK) ) {
        // No config file is ok
        return(0);
    }

    keyfile = (GKeyFile *)g_key_file_new();
    flags = (GKeyFileFlags)(G_KEY_FILE_KEEP_COMMENTS | G_KEY_FILE_KEEP_TRANSLATIONS);

    /*
    Example: /etc/pivportal.conf
     [server]
     host=192.168.0.10,192.168.0.11
     port=442
     client_ssl_cert=/etc/ssl/certs/pivportalClient.pem
     ssl_verify_host=0
    */
    if (!g_key_file_load_from_file(keyfile, PIVPORTAL_CONFIG_FILE, flags, &error)) {
        g_error(error->message);
        return(-1);
    }

    // Get Configuration Options
    server_ips = (gchar **)g_key_file_get_string_list(keyfile, "server", "hosts", &server_ips_len, NULL);
    server_port = (gchar *)g_key_file_get_string(keyfile, "server", "port", NULL);
    client_ssl_cert = (gchar *)g_key_file_get_string(keyfile, "server", "client_ssl_cert", NULL);
    g_server_ssl_verify_host = g_key_file_get_integer(keyfile, "server", "ssl_verify_host", NULL); // Defaults to 0 if not found in file

    if ( (server_ips_len != 0) && (server_ips != 0) ) {
        for (x = 0; x < server_ips_len; x++) {
            if ( x >= MAX_SERVERS ) {
                // Exceeding Max Server
                break;
            }
            memset(g_server_ips[x], 0, sizeof(g_server_ips[x]));
            snprintf(g_server_ips[x], sizeof(g_server_ips[x]), "%s", server_ips[x]);
            g_server_ips_len = server_ips_len;
        }
    }

    if ( server_port != 0 ) {
        memset(g_server_port, 0, sizeof(g_server_port));
        snprintf(g_server_port, sizeof(g_server_port), "%s", server_port);
    }

    if ( client_ssl_cert != 0 ) {
        memset(g_client_ssl_cert, 0, sizeof(g_client_ssl_cert));
        snprintf(g_client_ssl_cert, sizeof(g_client_ssl_cert), "%s", client_ssl_cert);
    }

    if (server_ips)
        g_strfreev(server_ips);
    if (server_port)
        free (server_port);
    if (client_ssl_cert)
        free(client_ssl_cert);

    return(0);
}


size_t write_curl_data(void *buffer, size_t size, size_t nmemb, void *userp) {
   return size * nmemb;
}


char *randstring(size_t length) {
    static char charset[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    char *randomString = NULL;
    int n = 0;
    int key = 0;
    int seed = time(NULL);

    srand(seed);

    if (length) {
        randomString = (char*)malloc(sizeof(char) * (length +1));

        if (randomString) {            
            for (n = 0;n < length;n++) {            
                key = rand() % (int)(sizeof(charset) -1);
                randomString[n] = charset[key];
            }
            randomString[length] = '\0';
        }
    }

    return randomString;
}


int register_pivportal(const char *username, const char *requestid, const char *url, const char *client_ssl_cert, long verifyHost) {
  CURL *curl = (CURL*)0;
  CURLcode res = (CURLcode)0;
  char post_fields[MAX_STR] = {0};
  int ret = 1;
  long status_code = 401;
  int retval = 0;

  // Debug stuff
  /*
  char teststr[255] = {}; // DEBUG
  */
  char teststr_error[MAX_STR] = {}; // DEBUG
  memset(teststr_error, 0, sizeof(teststr_error));

  // Build Post
  memset(post_fields, 0, sizeof(post_fields));
  snprintf(post_fields, sizeof(post_fields), "username=%s&requestid=%s", username, requestid);
 
  curl_global_init(CURL_GLOBAL_ALL);
 
  curl = curl_easy_init();

  if (curl) {
      curl_easy_setopt(curl, CURLOPT_URL, url);
      curl_easy_setopt(curl, CURLOPT_POST, 1);
      curl_easy_setopt(curl, CURLOPT_USE_SSL, 1);
      curl_easy_setopt(curl, CURLOPT_TIMEOUT, 15L);
      curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, verifyHost);
      curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, verifyHost);
      curl_easy_setopt(curl, CURLOPT_SSLCERT, client_ssl_cert);
      curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_fields);
      curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_curl_data);
      //curl_easy_setopt ( curl, CURLOPT_ERRORBUFFER, teststr_error );  // DEBUG
 
      res = curl_easy_perform(curl);

      curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &status_code);

      // DEBUG
      /*
      memset(teststr, 0, sizeof(teststr));
      snprintf(teststr, sizeof(teststr), "DEBUG: ret=%d, status_code=%Ld\n", ret, status_code);
      fputs(teststr, stderr);
      */
      fputs(teststr_error, stderr);
      // END DEBUG

      if ( /*ret != CURLE_OK || */status_code != 200 ) { // TODO: the ret value is 1 for some reason, thats bad
          retval = 1;
      }
 
      curl_easy_cleanup(curl);
  }

  curl_global_cleanup();

  return retval;
}


int status_pivportal(const char *username, const char *requestid, const char *url, const char *client_ssl_cert, long verifyHost) {
  CURL *curl = (CURL*)0;
  CURLcode res = (CURLcode)0;
  char post_fields[MAX_STR] = {0};
  int ret = 1;
  long status_code = 401;
  int retval = 0;

  // Build Post
  memset(post_fields, 0, sizeof(post_fields));
  snprintf(post_fields, sizeof(post_fields), "username=%s&requestid=%s", username, requestid);
 
  curl_global_init(CURL_GLOBAL_ALL);
 
  curl = curl_easy_init();

  if (curl) {
      curl_easy_setopt(curl, CURLOPT_URL, url);
      curl_easy_setopt(curl, CURLOPT_POST, 1);
      curl_easy_setopt(curl, CURLOPT_USE_SSL, 1);
      curl_easy_setopt(curl, CURLOPT_TIMEOUT, 15L);
      curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, verifyHost);
      curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, verifyHost);
      curl_easy_setopt(curl, CURLOPT_SSLCERT, client_ssl_cert);
      curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_fields);
      curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_curl_data);
 
      res = curl_easy_perform(curl);

      curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &status_code);

      if ( /*ret != CURLE_OK || */ status_code != 200 ) {  // TODO: the ret value is 1 for some reason, thats bad
          retval = 1;
      }
 
      curl_easy_cleanup(curl);
  }

  curl_global_cleanup();

  return retval;
}


PAM_EXTERN int pam_sm_setcred( pam_handle_t *pamh, int flags, int argc, const char **argv ) {
    return PAM_SUCCESS;
}


PAM_EXTERN int pam_sm_acct_mgmt(pam_handle_t *pamh, int flags, int argc, const char **argv) {
    return PAM_SUCCESS;
}


PAM_EXTERN int pam_sm_authenticate( pam_handle_t *pamh, int flags,int argc, const char **argv ) {
    int retval = 0, x = 0;
    const char* pUsername = 0;
    char *requestid = 0;
    char request_auth_str[MAX_STR] = {0};
    char register_url_str[MAX_STR] = {0};
    char status_url_str[MAX_STR] = {0};

    // Default Values
    g_server_ips_len = 1;
    memset(g_server_ips[0], 0, sizeof(g_server_ips[0]));
    memset(g_server_port, 0, sizeof(g_server_port));
    memset(g_client_ssl_cert, 0, sizeof(g_client_ssl_cert));
    snprintf(g_server_ips[0], sizeof(g_server_ips[0]), "%s", "127.0.0.1");
    snprintf(g_server_port, sizeof(g_server_port), "%s", "442");
    snprintf(g_client_ssl_cert, sizeof(g_client_ssl_cert), "%s", "/etc/ssl/certs/pivportalClient.pem");

    read_config();

    requestid = randstring(16);

    retval = pam_get_user(pamh, &pUsername, "Username: ");

    if (retval != PAM_SUCCESS) {
        return retval;
    }

    for (x = 0; x < g_server_ips_len; x++) {
        if ( x >= MAX_SERVERS ) {
            // Exceeding Max Server
            break;
        }
        // Register Auth Request
        memset(register_url_str, 0, sizeof(register_url_str));
        snprintf(register_url_str, sizeof(register_url_str), "https://%s:%s/api/client/request/register", g_server_ips[x], g_server_port);
        retval = register_pivportal(pUsername, requestid, register_url_str, g_client_ssl_cert, g_server_ssl_verify_host);
        if (retval == 0) {
            // Success
            break;
        }
    }
    if (retval != 0) {
        return PAM_AUTH_ERR;
    }

    // Wait For User To Auth
    memset(request_auth_str, 0, sizeof(request_auth_str));
    snprintf(request_auth_str, sizeof(request_auth_str), "Request ID: %s\n", requestid);
    printf("\n\n");
    printf("%s", request_auth_str);
    printf("Press Enter After Authorizing This Request\n");
    getchar();
    printf("\n");

    for (x = 0; x < g_server_ips_len; x++) {
        if ( x >= MAX_SERVERS ) {
            // Exceeding Max Server
            break;
        }
        // Verify User Authed
        memset(status_url_str, 0, sizeof(status_url_str));
        snprintf(status_url_str, sizeof(status_url_str), "https://%s:%s/api/client/request/status", g_server_ips[x], g_server_port);
        retval = status_pivportal(pUsername, requestid, status_url_str, g_client_ssl_cert, g_server_ssl_verify_host);
        if (retval == 0) {
            // Success
            break;
        }
    }
    if (retval != 0) {
        return PAM_AUTH_ERR;
    }

    return PAM_SUCCESS;
}