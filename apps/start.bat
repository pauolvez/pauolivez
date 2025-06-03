@echo off
REM Launch backend and frontend for development
set SCRIPT_DIR=%~dp0
start cmd /k "cd /d %SCRIPT_DIR%backend && uvicorn main:app --reload"
start cmd /k "cd /d %SCRIPT_DIR%frontend && npm run dev"
