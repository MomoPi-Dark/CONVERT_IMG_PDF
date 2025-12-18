@echo off
cd /d %~dp0

echo =======================================
echo   IMAGE TO PDF CONVERTER - GUI MODE
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

:: Run the GUI script
echo Starting Image to PDF Converter (GUI)...
echo.
python init_gui.py

echo.
echo =======================================
echo.
