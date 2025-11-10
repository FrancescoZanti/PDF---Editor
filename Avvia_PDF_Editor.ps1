# Script PowerShell per avviare PDF Editor
# Avvia_PDF_Editor.ps1

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "    PDF EDITOR - Avvio Applicazione" -ForegroundColor Cyan  
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Cambio nella directory dello script
Set-Location $PSScriptRoot

# Verifica se Python è installato
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python trovato: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python non trovato"
    }
} catch {
    Write-Host "ERRORE: Python non trovato nel sistema." -ForegroundColor Red
    Write-Host "Installa Python da https://python.org" -ForegroundColor Yellow
    Read-Host "Premi Enter per uscire"
    exit 1
}

# Verifica se il file principale esiste
if (!(Test-Path "pdf_editor.py")) {
    Write-Host "ERRORE: File pdf_editor.py non trovato." -ForegroundColor Red
    Write-Host "Assicurati di essere nella directory corretta del progetto." -ForegroundColor Yellow
    Read-Host "Premi Enter per uscire"
    exit 1
}

# Controllo dipendenze
Write-Host "Controllo dipendenze..." -ForegroundColor Yellow
try {
    $testImport = python -c "import pypdf, PIL, reportlab, tkinter; print('OK')" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Dipendenze mancanti"
    }
    Write-Host "Dipendenze: OK" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "ATTENZIONE: Alcune dipendenze potrebbero mancare." -ForegroundColor Yellow
    Write-Host "Installazione delle dipendenze in corso..." -ForegroundColor Yellow
    Write-Host ""
    
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "ERRORE: Impossibile installare le dipendenze." -ForegroundColor Red
        Write-Host "Prova manualmente: pip install pypdf pillow pdf2image reportlab" -ForegroundColor Yellow
        Read-Host "Premi Enter per uscire"
        exit 1
    }
}

# Avvio applicazione
Write-Host ""
Write-Host "Avvio PDF Editor..." -ForegroundColor Green
Write-Host ""

try {
    # Imposta encoding UTF-8
    $env:PYTHONIOENCODING = "utf-8"
    python pdf_editor.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "L'applicazione si è chiusa con un errore." -ForegroundColor Red
    }
} catch {
    Write-Host "Errore durante l'avvio: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Grazie per aver usato PDF Editor!" -ForegroundColor Cyan
Read-Host "Premi Enter per uscire"