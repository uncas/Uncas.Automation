#!/bin/bash

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment .venv for python."
  python3 -m venv .venv
fi

source .venv/bin/activate
python -m pip install --upgrade pip -q
pip install -r requirements.txt -q
