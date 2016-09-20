#!/bin/bash
export PYTHONPATH="${PYTHONPATH}:./pivportal/lib"
coverage run --source=pivportal $(which nosetests) -w pivportal/test/
