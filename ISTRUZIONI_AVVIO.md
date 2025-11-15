# 🚀 COME AVVIARE PDF EDITOR

Guida completa per avviare PDF Editor in tutti i modi possibili su Windows.

## 📋 Prerequisiti

Prima di avviare l'applicazione, assicurati di avere:

1. ✅ **Python 3.8 o superiore** installato ([Scarica qui](https://www.python.org/downloads/))
2. ✅ **Tutte le dipendenze** installate: `pip install -r requirements.txt`
3. ✅ **Sei nella directory corretta** del progetto

### Verifica Rapida

```bash
# Controlla versione Python
python --version

# Dovrebbe mostrare Python 3.8.x o superiore
# Se non funziona, prova:
python3 --version
py --version
```

## 🎯 Metodi di Avvio

### 🥇 Metodo 1: Doppio Click su File Batch (Più Semplice)

**Per avviare l'applicazione (consigliato - PRO):**
1. Vai nella cartella del progetto
2. **Doppio click** su `avvia_pdf_editor_pro.bat`
3. Si aprirà un menu di selezione per scegliere la modalità

**Vantaggi:**
- ✅ Più veloce e semplice
- ✅ Non richiede conoscenze tecniche
- ✅ Configura automaticamente l'encoding

**Quando usarlo:**
- Sei un utente non tecnico
- Vuoi avviare rapidamente l'app
- Non hai familiarità con il terminale

---

### 🥈 Metodo 2: PowerShell Script (Raccomandato per Windows 10+)

1. Individua il file `Avvia_PDF_Editor.ps1`
2. **Tasto destro** sul file
3. Seleziona **"Esegui con PowerShell"**
4. Se richiesto, autorizza l'esecuzione dello script

**Vantaggi:**
- ✅ Più robusto del batch
- ✅ Migliore gestione degli errori
- ✅ Output colorato e formattato
- ✅ Verifica automatica dipendenze

**Quando usarlo:**
- Usi Windows 10 o 11
- Vuoi feedback dettagliato sull'avvio
- Preferisci script più moderni

---

### 🥉 Metodo 3: Terminale/Prompt dei Comandi (Universale)

**Avvio da terminale (universale):**
```bash
# Apri il terminale nella cartella del progetto
cd "C:\percorso\del\progetto\PDF---Editor"

# Avvia l'applicazione Pro con menu di selezione
python pdf_editor_pro.py
```

**Vantaggi:**
- ✅ Funziona su qualsiasi sistema
- ✅ Ideale per sviluppatori
- ✅ Consente debug e parametri personalizzati

**Quando usarlo:**
- Sei uno sviluppatore
- Hai bisogno di vedere l'output del terminale
- Vuoi eseguire test o debug

---

### 🔧 Metodo 4: Esecuzione Diretta del Modulo (Sviluppatori)

```bash
# Naviga nella cartella src
cd src

# Esegui il modulo principale
python main.py
```

**Vantaggi:**
- ✅ Accesso diretto al codice
- ✅ Ideale per sviluppo e testing
- ✅ Bypass del launcher

**Quando usarlo:**
- Stai sviluppando/modificando il codice
- Vuoi testare modifiche specifiche
- Stai facendo debugging approfondito

## ⚠️ Risoluzione Problemi

### Problema: "No module named 'main'"
**Soluzione:**
```bash
# Assicurati di essere nella directory principale del progetto
cd "C:\Users\francesco.zanti\OneDrive - SITI B&T GROUP S.p.A\Documenti\Github\PDF - Editor"
python pdf_editor_pro.py
```

### Problema: "ModuleNotFoundError"
**Soluzione:**
```bash
pip install -r requirements.txt
```

**Nota:** Assicurati che PySide6 sia installato:
```bash
pip install PySide6
```

### Problema: Errori di encoding nel terminale
**Soluzione:**
- Usa il file PowerShell: `Avvia_PDF_Editor.ps1`
- Oppure imposta encoding UTF-8:
```bash
chcp 65001
set PYTHONIOENCODING=utf-8
python pdf_editor_pro.py
```

## 📁 Struttura File di Avvio

- `pdf_editor_pro.py` - Script principale (Pro)
- `avvia_pdf_editor_pro.bat` - Launcher batch Windows (Pro)
- `Avvia_PDF_Editor.ps1` - Launcher PowerShell (raccomandato)
- `src/main.py` - Applicazione core (PySide6)

## 🎯 Cosa Aspettarsi

Quando avvii l'applicazione correttamente, vedrai:
1. Una finestra grafica moderna con titolo "PDF Editor - Modifica PDF"
2. **Interfaccia moderna Windows 11** con angoli arrotondati e colori moderni
3. 8 pulsanti colorati con effetti hover per le diverse funzioni:
   - Unisci PDF (blu)
   - Dividi PDF (rosso)  
   - Ruota PDF (arancione)
   - Estrai Pagine (viola)
   - Aggiungi Watermark (verde acqua)
   - Estrai Testo (grigio scuro)
   - Converti Immagini (arancione scuro)
   - Anteprima PDF (verde)
4. Un'area di output in basso per i messaggi
5. **Dialog nativi di Windows 11** per l'apertura e il salvataggio dei file

## 🎨 Interfaccia Moderna PySide6

L'applicazione utilizza **PySide6 (Qt 6)** per l'interfaccia grafica, offrendo:
- ✅ **Design moderno** compatibile con Windows 11 con Material Design
- ✅ **Prestazioni superiori** con rendering hardware-accelerated
- ✅ **Dialog nativi** del sistema operativo per apertura/salvataggio file
- ✅ **Alta risoluzione** supporto completo per schermi 4K, 5K, 8K e Retina
- ✅ **Temi personalizzabili** preparato per supporto dark mode
- ✅ **Animazioni fluide** transizioni e effetti visivi moderni

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
1. Python installato correttamente (versione 3.8 o superiore)
2. Dipendenze installate: `pip install PySide6 pypdf pillow pdf2image reportlab`
3. Sei nella directory corretta del progetto
4. Su Windows, verifica che non ci siano conflitti con altre installazioni Qt