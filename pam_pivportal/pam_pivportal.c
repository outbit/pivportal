#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <security/pam_appl.h>
#include <security/pam_modules.h>

#include <stdio.h>
#include <curl/curl.h>
 

int authenticate_pivportal(char *url, char *username)
{
  CURL *curl;
  CURLcode res;
  char post_fields[255] = {}

  // Build Post
  memset(post_fields, 0, sizeof(post_fields));
  snprintf(post_fields, sizeof(post_fields), "username=%s", username);
 
  curl_global_init(CURL_GLOBAL_ALL);
 
  curl = curl_easy_init();

  if (curl) {
      curl_easy_setopt(curl, CURLOPT_URL, url);
      curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_fields);
 
      res = curl_easy_perform(curl);

      if (res != CURLE_OK) {
          return 1;
      }
 
      curl_easy_cleanup(curl);
  }

  curl_global_cleanup();

  return 0;
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

    retval = pam_get_user(pamh, &pUsername, "Username: ");

    if (retval != PAM_SUCCESS) {
        return retval;
    }

    // TODO: url should be loaded from a config file
    retval = authenticate_pivportal(pUsername, "https://127.0.0.1");

    if (retval != 0) {
        return PAM_AUTH_ERR;
    }

    return PAM_SUCCESS;
}