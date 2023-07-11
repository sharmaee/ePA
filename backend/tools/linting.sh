#!/bin/bash

echo "Linting with flake8"
flake8 portal --ignore=E203 --count --max-complexity=10 --max-line-length=120 --statistics --exclude migrations

echo "Checking formatting with black"
black portal --check --skip-string-normalization --line-length=120 --exclude=migrations
