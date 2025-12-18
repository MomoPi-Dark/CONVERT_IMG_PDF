:: WRun.bat (Windows GUI launcher for Image to PDF Converter)
:: Licensed under MIT License
:: Copyright (c) 2025 GAMFLAZ

@echo off
SETLOCAL EnableExtensions EnableDelayedExpansion

:: Always run from script directory
cd /d "%~dp0"


:: Enable ANSI colors
for /F %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"

set "RED=%ESC%[0;31m"
set "GREEN=%ESC%[0;32m"
set "YELLOW=%ESC%[1;33m"
set "BLUE=%ESC%[0;34m"
set "NC=%ESC%[0m"

set "INFO=%BLUE%[INFO]%NC%"
set "WARN=%YELLOW%[WARN]%NC%"
set "ERROR=%RED%[ERROR]%NC%"

:: Venv paths
set "VENV_ROOT=.venv"
set "VENV_SCRIPTS=%VENV_ROOT%\Scripts"
set "VENV_PY=%VENV_SCRIPTS%\python.exe"
set "DEPS_MARKER=%VENV_ROOT%\.deps_installed"

echo =======================================
echo %GREEN%  IMAGE TO PDF CONVERTER - GUI MODE%NC%
echo =======================================
echo.

echo %INFO% Initializing environment...

:: Prevent launching if the app is already running (checked via Python lock file)
@REM set "APP_LOCK=%TEMP%\convert_img_pdf.lock"
@REM if exist "%APP_LOCK%" (
@REM     set "RUN_PID="
@REM     set /p RUN_PID=<"%APP_LOCK%"
@REM     set "TASKLINE="
@REM     if defined RUN_PID (
@REM         for /f "usebackq tokens=* delims=" %%L in (`tasklist /FI "PID eq %RUN_PID%" /FO CSV /NH 2^>nul`) do set "TASKLINE=%%~L"
@REM     )
@REM     if defined TASKLINE (
@REM         rem If TASKLINE does not start with INFO:, a process exists with this PID
@REM         set "_HDR=!TASKLINE:~0,5!"
@REM         if /I not "!_HDR!"=="INFO:" (
@REM             echo %WARN% Application is already running (PID %RUN_PID%). Close it first.
@REM             exit /b 0
@REM         )
@REM     )
@REM     rem Stale lock; remove
@REM     del "%APP_LOCK%" >nul 2>nul
@REM )

:: Detect Python 3.8+
set "PY_CMD="

for %%P in (python py python3) do (
    where %%P >nul 2>nul || continue
    %%P -c "import sys; exit(0 if sys.version_info >= (3,8) else 1)" >nul 2>nul || continue
    set "PY_CMD=%%P"
    goto :python_found
)

:python_found
if not defined PY_CMD (
    echo %ERROR% Python 3.8+ not found
    pause
    exit /b 1
)

for /f "delims=" %%V in ('%PY_CMD% --version 2^>^&1') do (
    echo %INFO% Using %%V
)

:: Check tkinter
"%PY_CMD%" -c "import tkinter" 2>nul
if errorlevel 1 (
    echo %ERROR% Tkinter not found. Please install Tkinter for your Python.
    echo Usage 
    pause
    exit /b 1
)

:: Ensure venv + dependencies
if not exist "%VENV_PY%" (
    echo %ERROR% Virtual environment setup failed!
    call :delete_venv || exit /b 1
    call :create_venv || exit /b 1
)

if not exist "%DEPS_MARKER%" (
    echo %WARN% Dependencies not installed
    call :install_deps || exit /b 1
) else (
    rem Optionally ensure updated requirements are present without forcing every run
    for /f "usebackq tokens=* delims=" %%R in ("requirements.txt") do (
        rem Touch marker if requirements file is newer/changed is complex; users can delete marker to force reinstall
        rem Keeping as-is for performance.
    )
)

:: Run application (USE VENV PYTHON!!)
echo %INFO% Starting Image to PDF Converter GUI...
"%VENV_PY%" init.py

set "ERR=%ERRORLEVEL%"
if not "%ERR%"=="0" (
    echo %ERROR% Application exited with code %ERR%
    pause
    exit /b %ERR%
)

exit /b 0

:delete_venv
if not exist "%VENV_ROOT%" (
    exit /b 0
)
echo %INFO% Deleting existing virtual environment...
rmdir /s /q "%VENV_ROOT%"

:: Create virtual environment
:create_venv
echo %INFO% Creating virtual environment...

"%PY_CMD%" -m venv "%VENV_ROOT%"
if errorlevel 1 (
    echo %ERROR% Failed to create virtual environment
    exit /b 1
)

if not exist "%VENV_PY%" (
    echo %ERROR% python.exe not found in venv
    exit /b 1
)

exit /b 0


:: Install dependencies
:install_deps
if not exist "requirements.txt" (
    echo %ERROR% requirements.txt not found
    exit /b 1
)

echo %INFO% Installing pip...
"%VENV_PY%" -m ensurepip --upgrade || exit /b 1
"%VENV_PY%" -m pip install --upgrade pip || exit /b 1

echo %INFO% Installing dependencies from requirements.txt...
"%VENV_PY%" -m pip install -r requirements.txt || exit /b 1

echo. > "%DEPS_MARKER%"
echo %INFO% Dependencies installed successfully

exit /b 0
