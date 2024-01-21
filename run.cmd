@echo off

REM py -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
py Source/Run.py
