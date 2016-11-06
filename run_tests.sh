#!/bin/bash

# Test Python
export PYTHONPATH="${PYTHONPATH}:./pivportal/lib"
coverage run --source=pivportal $(which nosetests) -w pivportal/test/

# Test Pam Module
pushd pam_pivportal/
    make clean && make && make test
popd
