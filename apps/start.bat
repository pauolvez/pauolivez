@echo off
REM Launch backend and frontend for development
start cmd /k "cd backend && uvicorn main:app --reload"
start cmd /k "cd frontend && npm run dev"
