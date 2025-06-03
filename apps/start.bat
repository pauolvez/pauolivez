@echo off
REM Launch backend and frontend for development
eazwwx-codex/generar-estructura-base-backend-con-fastapi
set SCRIPT_DIR=%~dp0
start cmd /k "cd /d %SCRIPT_DIR%backend && uvicorn main:app --reload"
start cmd /k "cd /d %SCRIPT_DIR%frontend && npm run dev"
ueft9t-codex/generar-estructura-base-backend-con-fastapi
set SCRIPT_DIR=%~dp0
start cmd /k "cd /d %SCRIPT_DIR%backend && uvicorn main:app --reload"
start cmd /k "cd /d %SCRIPT_DIR%frontend && npm run dev"
start cmd /k "cd backend && uvicorn main:app --reload"
start cmd /k "cd frontend && npm run dev"
main

