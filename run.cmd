@echo off

IF NOT EXIST .venv (
    ECHO "Creating virtual environment .venv for python."
    py -m venv .venv
)

call .venv\Scripts\activate
py -m pip install --upgrade pip -q
pip install -r requirements.txt -q
REM py Source/Run.py
py Source/RunPersonalAssistant.py

