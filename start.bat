@echo off
IF EXIST ".\env" (
    CALL .\env\Scripts\activate.bat
    ECHO app already installed
) ELSE (
    ECHO Installing app, this may take a few minutes...
    CALL python -m venv env
    CALL .\env\Scripts\activate.bat
    CALL pip install -r requirements.txt
    ECHO app successfully installed
)
IF EXIST ".\local_variables.bat" (
    CALL .\local_variables.bat
)

SET FLASK_APP=server.py
SET FLASK_DEBUG=1
SET APP_CONFIG_FILE=settings.py
flask run