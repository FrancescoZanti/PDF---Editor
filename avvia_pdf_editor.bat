@echo off
title PDF Editor - Avvio
echo ====================================
echo    PDF EDITOR - Avvio Applicazione
echo ====================================
echo.

cd /d "%~dp0"

REM Controlla se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRORE: Python non trovato nel sistema.
    echo Installa Python da https://python.org
    pause
    exit /b 1
)

REM Controlla se esiste il file principale
if not exist "pdf_editor.py" (
    echo ERRORE: File pdf_editor.py non trovato.
    echo Assicurati di essere nella directory corretta del progetto.
    pause
    exit /b 1
)

echo Controllo dipendenze...
python -c "import pypdf, PIL, reportlab, tkinter" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ATTENZIONE: Alcune dipendenze potrebbero mancare.
    echo Installazione delle dipendenze in corso...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERRORE: Impossibile installare le dipendenze.
        echo Prova manualmente: pip install pypdf pillow pdf2image reportlab
        pause
        exit /b 1
    )
)

echo.
echo Avvio PDF Editor...
echo.
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8
python pdf_editor.py

if errorlevel 1 (
    echo.
    echo L'applicazione si è chiusa con un errore.
    pause
)

echo.
echo Grazie per aver usato PDF Editor!
pause