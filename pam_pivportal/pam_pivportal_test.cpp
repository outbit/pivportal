#include <gtest/gtest.h>
#include "pam_pivportal.h"


// Mockup
int pam_get_user(pam_handle_t *pamh, const char **username, const char *attr) {
    return 0;
}


TEST (write_curl_data, successisok) {
    ASSERT_EQ(write_curl_data(NULL, 5, 5, NULL), 25);
}


TEST (randstring, successisok) {
    char *randstr = NULL;
    randstr = randstring(10);
    ASSERT_EQ(strlen(randstr), 10);
    free(randstr);
}


int main(int argc, char *argv[]) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}