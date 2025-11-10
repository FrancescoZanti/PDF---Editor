# COME AVVIARE PDF EDITOR

## 🚀 Metodi di Avvio

### Metodo 1: Doppio Click (Windows)
```
Doppio click su: avvia_pdf_editor.bat
```

### Metodo 2: PowerShell (Raccomandato)
```
Tasto destro su: Avvia_PDF_Editor.ps1 → "Esegui con PowerShell"
```

### Metodo 3: Terminale
```bash
python pdf_editor.py
```

### Metodo 4: Da Sviluppatore
```bash
cd src
python main.py
```

## ⚠️ Risoluzione Problemi

### Problema: "No module named 'main'"
**Soluzione:**
```bash
# Assicurati di essere nella directory principale del progetto
cd "C:\Users\francesco.zanti\OneDrive - SITI B&T GROUP S.p.A\Documenti\Github\PDF - Editor"
python pdf_editor.py
```

### Problema: "ModuleNotFoundError"
**Soluzione:**
```bash
pip install -r requirements.txt
```

### Problema: Errori di encoding nel terminale
**Soluzione:**
- Usa il file PowerShell: `Avvia_PDF_Editor.ps1`
- Oppure imposta encoding UTF-8:
```bash
chcp 65001
set PYTHONIOENCODING=utf-8
python pdf_editor.py
```

## 📁 Struttura File di Avvio

- `pdf_editor.py` - Script principale
- `avvia_pdf_editor.bat` - Launcher batch Windows
- `Avvia_PDF_Editor.ps1` - Launcher PowerShell (raccomandato)
- `src/main.py` - Applicazione core

## 🎯 Cosa Aspettarsi

Quando avvii l'applicazione correttamente, vedrai:
1. Una finestra grafica con titolo "PDF Editor - Modifica PDF"
2. 8 pulsanti colorati per le diverse funzioni:
   - Unisci PDF (blu)
   - Dividi PDF (rosso)  
   - Ruota PDF (arancione)
   - Estrai Pagine (viola)
   - Aggiungi Watermark (verde acqua)
   - Estrai Testo (grigio scuro)
   - Converti Immagini (arancione scuro)
   - Anteprima PDF (verde)
3. Un'area di output in basso per i messaggi

## 🔧 Se Nulla Funziona

Esegui il test diagnostico:
```bash
python test_simple.py
```

Dovrebbe mostrare:
```
Import main: OK
Funzione main: OK
Classe PDFEditor: OK
Tutti i test superati!
```

Se il test fallisce, controlla:
1. Python installato correttamente
2. Dipendenze installate: `pip install pypdf pillow pdf2image reportlab`
3. Sei nella directory corretta del progetto