#!/bin/sh

# move to folder
cd /data || exit
if [ ! "$(ls -A /data)" ]; then
  echo "ERROR: Looks like you forgot to pass code to check"
  exit 1
fi

# check _all_ the files

# ansible-lint
ansible-lint --version
find . -type d -iname "ansible" -exec ansible-lint {} \;

# yamllint
yamllint -v
find . -type f \( -iname "*.yml" -o -iname "*.yaml" \) -exec yamllint {} \;

# flake8
echo -n "flake8 $(flake8 --version)"
find . -type f -iname "*.py" -exec flake8 {} \;

# pylint
pylint --version
find . -type f -iname "*.py" -exec pylint {} \;

# shell
shellcheck --version
find . -type f -iname "*.sh" -exec yamllint {} \;
