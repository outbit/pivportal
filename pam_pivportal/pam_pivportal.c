#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <security/pam_appl.h>
#include <security/pam_modules.h>

#include <stdio.h>
#include <curl/curl.h>

#include <unistd.h>
#include <glib.h>


#define PIVPORTAL_CONFIG_FILE "/etc/pivportal.conf"
#define MAX_STR 255


char g_server_ip[MAX_STR] = {0};
char g_server_port[MAX_STR] = {0};
int g_server_ssl_verify_host = 0;


int read_config() {
    GKeyFile *keyfile = 0;
    GKeyFileFlags flags = 0;
    GError *error = 0;
    gchar *server_ip = 0, *server_port = 0;

    // Check If Config file exists, exit if it doesnt
    if ( 0 != access (PIVPORTAL_CONFIG_FILE, F_OK) ) {
        // No config file is ok
        return(0);
    }

    keyfile = (GKeyFile *)g_key_file_new();
    flags = G_KEY_FILE_KEEP_COMMENTS | G_KEY_FILE_KEEP_TRANSLATIONS;

    /*
    Example: /etc/pivportal.conf
     [server]
     ip=192.168.0.10
     port=442
     ssl_verify_host=0
    */
    if (!g_key_file_load_from_file(keyfile, PIVPORTAL_CONFIG_FILE, flags, &error)) {
        g_error(error->message);
        return(-1);
    }

    // Get Configuration Options
    server_ip = (gchar *)g_key_file_get_string(keyfile, "server", "ip", NULL);
    server_port = (gchar *)g_key_file_get_string(keyfile, "server", "port", NULL);
    g_server_ssl_verify_host = g_key_file_get_integer(keyfile, "server", "ssl_verify_host", NULL); // Defaults to 0 if not found in file

    if ( server_ip != 0 ) {
        memset(g_server_ip, 0, sizeof(g_server_ip));
        snprintf(g_server_ip, sizeof(g_server_ip), "%s", server_ip);
    }

    if ( server_port != 0 ) {
        memset(g_server_port, 0, sizeof(g_server_port));
        snprintf(g_server_port, sizeof(g_server_port), "%s", server_port);
    }

    return(0);
}


size_t write_curl_data(void *buffer, size_t size, size_t nmemb, void *userp)
{
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
        randomString = malloc(sizeof(char) * (length +1));

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


int register_pivportal(const char *username, const char *requestid, const char *url, long verifyHost)
{
  CURL *curl = 0;
  CURLcode res = 0;
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
      curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, verifyHost);
      curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, verifyHost);
      //curl_easy_setopt(curl, CURLOPT_SSL_VERIFYSTATUS, verifyHost); TODO, do I need this?
      curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_fields);
      curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_curl_data);
      curl_easy_setopt ( curl, CURLOPT_ERRORBUFFER, teststr_error );  // DEBUG
 
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


int status_pivportal(const char *username, const char *requestid, const char *url, long verifyHost)
{
  CURL *curl = 0;
  CURLcode res = 0;
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
      curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, verifyHost);
      curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, verifyHost);
      //curl_easy_setopt(curl, CURLOPT_SSL_VERIFYSTATUS, verifyHost); TODO, do I need this?
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
    int retval = 0;
    const char* pUsername = 0;
    char *requestid = 0;
    char request_auth_str[MAX_STR] = {0};
    char register_url_str[MAX_STR] = {0};
    char status_url_str[MAX_STR] = {0};

    // Default Values
    memset(g_server_ip, 0, sizeof(g_server_ip));
    memset(g_server_port, 0, sizeof(g_server_port));
    snprintf(g_server_ip, sizeof(g_server_ip), "%s", "127.0.0.1");
    snprintf(g_server_port, sizeof(g_server_port), "%s", "442");

    read_config();

    requestid = randstring(16);

    retval = pam_get_user(pamh, &pUsername, "Username: ");

    if (retval != PAM_SUCCESS) {
        return retval;
    }

    // Register Auth Request
    memset(register_url_str, 0, sizeof(register_url_str));
    snprintf(register_url_str, sizeof(register_url_str), "https://%s:%s/api/client/request/register", g_server_ip, g_server_port);
    retval = register_pivportal(pUsername, requestid, register_url_str, g_server_ssl_verify_host);

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

    // Verify User Authed
    memset(status_url_str, 0, sizeof(status_url_str));
    snprintf(status_url_str, sizeof(status_url_str), "https://%s:%s/api/client/request/status", g_server_ip, g_server_port);
    retval = status_pivportal(pUsername, requestid, status_url_str, g_server_ssl_verify_host);

    if (retval != 0) {
        return PAM_AUTH_ERR;
    }

    return PAM_SUCCESS;
}