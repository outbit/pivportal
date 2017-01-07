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
#define MAX_SERVERS 5


extern char g_server_ips[MAX_SERVERS][MAX_STR];
extern char g_server_ips_len;
extern char g_server_port[MAX_STR];
extern char g_client_ssl_cert[MAX_STR];
extern int g_server_ssl_verify_host;


int read_config();
size_t write_curl_data(void *buffer, size_t size, size_t nmemb, void *userp);
char *randstring(size_t length);
int register_pivportal(const char *username, const char *requestid, const char *url, const char *client_ssl_cert, long verifyHost);
int status_pivportal(const char *username, const char *requestid, const char *url, const char *client_ssl_cert, long verifyHost);
PAM_EXTERN int pam_sm_setcred( pam_handle_t *pamh, int flags, int argc, const char **argv );
PAM_EXTERN int pam_sm_acct_mgmt(pam_handle_t *pamh, int flags, int argc, const char **argv);
PAM_EXTERN int pam_sm_authenticate( pam_handle_t *pamh, int flags,int argc, const char **argv );
