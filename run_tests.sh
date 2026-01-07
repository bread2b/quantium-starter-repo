#!/usr/bin/env bash

set -e

if [ -d "venv/bin" ]; then
  source venv/bin/activate
elif [ -d "venv/Scripts" ]; then
  source venv/Scripts/activate
else
  echo "Virtual environment not found"
  exit 1
fi

pytest
