@echo off
cd /d %~dp0

echo =======================================
echo   IMAGE TO PDF CONVERTER
echo =======================================
echo.

:: Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo Virtual environment not found. Installing dependencies...
    echo.
    
    :: Check if requirements.txt exists
    if exist "requirements.txt" (
        echo Installing required packages from requirements.txt...
        python -m pip install -r requirements.txt
        if errorlevel 1 (
            echo.
            echo ERROR: Failed to install dependencies!
            echo Please check your internet connection and try again.
            echo.
            pause
            exit /b 1
        )
    ) else (
        echo ERROR: requirements.txt not found!
        pause
        exit /b 1
    )
    
    echo.
    echo Dependencies installed successfully!
    echo.
)

:: Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment still not found!
    pause
    exit /b 1
)

echo.

:: Run the Python script
:: Script akan otomatis use default folders atau tanya user untuk custom path
echo Starting Image to PDF Converter...
echo.
python init.py

echo.
echo =======================================
echo.
pause
