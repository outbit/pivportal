#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <security/pam_appl.h>
#include <security/pam_modules.h>

#include <stdio.h>
#include <curl/curl.h>
 

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


int register_pivportal(const char *username, const char *requestid, const char *url)
{
  CURL *curl;
  CURLcode res;
  char post_fields[255] = {};
  int ret = 1;
  long status_code = 401;
  int retval = 0;
  char teststr[255] = {}; // DEBUG
  char teststr_error[255] = {}; // DEBUG

  // Build Post
  memset(post_fields, 0, sizeof(post_fields));
  snprintf(post_fields, sizeof(post_fields), "username=%s&requestid=%s", username, requestid);
 
  curl_global_init(CURL_GLOBAL_ALL);
 
  curl = curl_easy_init();

  if (curl) {
      curl_easy_setopt(curl, CURLOPT_URL, url);
      curl_easy_setopt(curl, CURLOPT_POST, 1);
      curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_fields);
      //curl_easy_setopt ( curl, CURLOPT_ERRORBUFFER, teststr_error );  // DEBUG
 
      res = curl_easy_perform(curl);

      curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &status_code);

      // DEBUG
      /*
      memset(teststr, 0, sizeof(teststr));
      memset(teststr_error, 0, sizeof(teststr_error));
      snprintf(teststr, sizeof(teststr), "DEBUG: ret=%d, status_code=%Ld\n", ret, status_code);
      fputs(teststr, stderr);
      fputs(teststr_error, stderr);
      */
      // END DEBUG

      if ( /*ret != CURLE_OK || */status_code != 200 ) { // TODO: the ret value is 1 for some reason, thats bad
          retval = 1;
      }
 
      curl_easy_cleanup(curl);
  }

  curl_global_cleanup();

  return retval;
}


int status_pivportal(const char *username, const char *requestid, const char *url)
{
  CURL *curl;
  CURLcode res;
  char post_fields[255] = {};
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
      curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_fields);
 
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
    int retval;
    const char* pUsername;
    char *requestid;
    char request_auth_str[255] = {};

    requestid = randstring(16);

    retval = pam_get_user(pamh, &pUsername, "Username: ");

    if (retval != PAM_SUCCESS) {
        return retval;
    }

    // TODO: url should be loaded from a config file
    // TODO: http for testing, https later
    // Register a unique Auth request
    retval = register_pivportal(pUsername, requestid, "http://192.168.0.103/api/request/register");

    if (retval != 0) {
        return PAM_AUTH_ERR;
    }

    // Wait For User To Auth
    snprintf(request_auth_str, sizeof(request_auth_str), "Request ID: %s", requestid);
    printf("Press Enter After Authorizing This Request\n");
    getchar();

    // Verify User Authed
    retval = status_pivportal(pUsername, requestid, "http://192.168.0.103/api/request/status");

    if (retval != 0) {
        return PAM_AUTH_ERR;
    }

    return PAM_SUCCESS;
}