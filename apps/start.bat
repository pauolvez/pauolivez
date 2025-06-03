@echo off
REM Launch backend and frontend for development
REM Assume this script is executed from project root
start cmd /k "cd apps\backend && uvicorn main:app --reload"
start cmd /k "cd apps\frontend && npm run dev"
