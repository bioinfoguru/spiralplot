@echo off
echo ==========================================
echo      Push SpiralPlot to GitHub
echo ==========================================

REM Check if git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo Git is not installed or not in the PATH.
    pause
    exit /b
)

REM Initialize git if not already initialized
if not exist .git (
    echo Initializing new Git repository...
    git init
) else (
    echo Git repository already initialized.
)

REM Add all files
echo Adding files to staging...
git add .

REM Commit
echo Committing changes...
git commit -m "Initial commit"

REM Rename branch to main
git branch -M main

REM Check if remote 'origin' already exists
git remote get-url origin >nul 2>nul
if %errorlevel% equ 0 (
    echo Remote 'origin' already exists.
) else (
    echo Adding remote origin...
    git remote add origin https://github.com/bioinfoguru/spiralplot.git
)

REM Push
echo Pushing to GitHub...
git push -u origin main

echo ==========================================
echo      Done!
echo ==========================================
pause
