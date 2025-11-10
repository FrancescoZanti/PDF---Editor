@echo off
title PDF Editor Pro - Avvio Versione Avanzata
echo ==========================================
echo      PDF EDITOR PRO v2.0 - AVVIO
echo ==========================================
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
if not exist "pdf_editor_pro.py" (
    echo ERRORE: File pdf_editor_pro.py non trovato.
    echo Assicurati di essere nella directory corretta del progetto.
    pause
    exit /b 1
)

echo Controllo dipendenze avanzate...
python -c "import fitz, cryptography, numpy" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ATTENZIONE: Alcune dipendenze avanzate mancano.
    echo Installazione delle dipendenze in corso...
    echo.
    pip install PyMuPDF cryptography numpy opencv-python matplotlib
    if errorlevel 1 (
        echo.
        echo ERRORE: Impossibile installare le dipendenze avanzate.
        echo Prova manualmente: pip install PyMuPDF cryptography numpy
        echo.
        echo Avvio in modalità base...
        python pdf_editor.py
        pause
        exit /b 1
    )
)

echo.
echo Avvio PDF Editor Pro...
echo Seleziona la modalità dalla finestra che si aprirà
echo.
chcp 65001 >nul 2>&1
set PYTHONIOENCODING=utf-8
python pdf_editor_pro.py

if errorlevel 1 (
    echo.
    echo L'applicazione si è chiusa con un errore.
    echo Tentativo di avvio modalità base...
    python pdf_editor.py
    pause
)

echo.
echo Grazie per aver usato PDF Editor Pro!
pause