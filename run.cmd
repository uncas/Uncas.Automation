@echo off

IF NOT EXIST .venv (
    ECHO "Creating virtual environment .venv for python."
    py -m venv .venv
)

call .venv\Scripts\activate
pip install -r requirements.txt
py Source/Run.py
