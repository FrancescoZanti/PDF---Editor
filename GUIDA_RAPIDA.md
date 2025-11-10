# 🚀 GUIDA RAPIDA - PDF EDITOR PRO v2.0

> **✨ NOVITÀ**: La versione PRO è stata completamente migrata a **PySide6 (Qt)** con interfaccia moderna Windows 11! Tutte le funzionalità avanzate ora beneficiano della nuova UI professionale.

## 📋 Come Iniziare

### Avvio Rapido
1. **Doppio click** su `avvia_pdf_editor_pro.bat` (Windows)
2. **Oppure** esegui `python pdf_editor_pro.py` da terminale

### Modalità Disponibili

#### 🎯 **EDITOR AVANZATO** (Raccomandato)
- **Simile ad Adobe Acrobat Pro**
- Editing visuale con mouse
- Pannelli laterali professionali
- Annotazioni, evidenziazioni, disegni
- Zoom avanzato e navigazione fluida
- **Ideale per**: Editing professionale di documenti

#### 📝 **EDITOR BASE**
- Funzioni essenziali rapide
- Unisci, dividi, ruota PDF
- Estrai testo e pagine
- Converti immagini in PDF
- **Ideale per**: Operazioni veloci e batch

#### 📋 **EDITOR FORM**
- Crea moduli interattivi
- Campi di testo, checkbox, dropdown
- Validazione dati
- Import/Export dati form
- **Ideale per**: Creazione questionari e moduli

---

## 🛠️ Dipendenze Automatiche

L'applicazione installerà automaticamente:
- `PyMuPDF` - Motore PDF avanzato
- `cryptography` - Sicurezza e crittografia
- `numpy` - Calcoli matematici
- `opencv-python` - Elaborazione immagini
- `matplotlib` - Grafici e visualizzazioni

---

## 💡 Funzionalità Principali

### Editing Visuale (Solo Modalità Avanzata)
- ✅ **Click e trascina** per spostare elementi
- ✅ **Doppio click** su testo per modificarlo
- ✅ **Toolbar** con strumenti di disegno
- ✅ **Pannelli** per outline, annotazioni, proprietà
- ✅ **Zoom** con rotella mouse o pulsanti

### Annotazioni e Markup
- 🖊️ **Evidenziatore** - Evidenzia testo importante
- ✏️ **Note adesive** - Aggiungi commenti
- 🖍️ **Disegno libero** - Disegna con il mouse
- 📝 **Testo libero** - Aggiungi testo ovunque
- 🔲 **Forme geometriche** - Rettangoli, cerchi, frecce

### Sicurezza
- 🔐 **Crittografia** - Password e permessi
- 🖋️ **Firme digitali** - Autentica documenti
- 👁️ **Filigrane** - Proteggi da copie non autorizzate

### Form Interattivi
- 📝 **Campi testo** - Input utente
- ☑️ **Checkbox** - Opzioni multiple
- 🔘 **Radio button** - Scelta singola
- 📋 **Dropdown** - Menu a tendina
- ✅ **Validazione** - Controllo dati

---

## 🎛️ Configurazione

### File Recenti
- Accesso rapido agli ultimi PDF aperti
- Menu `File > File Recenti`
- Configurabile fino a 10 file

### Preferenze
- Menu `Opzioni > Preferenze`
- Modalità predefinita all'avvio
- Percorsi di salvataggio preferiti
- Tema interfaccia (futuro)

### Configurazione Persistente
- Le impostazioni sono salvate automaticamente
- Posizione: `%USERPROFILE%/.pdf_editor_pro/config.json`
- Backup automatico delle configurazioni

---

## 🚨 Risoluzione Problemi

### ❌ "Funzionalità avanzate non disponibili"
**Soluzione**: Installa le dipendenze manualmente
```bash
pip install PyMuPDF cryptography numpy opencv-python matplotlib
```

### ❌ "Python non trovato"
**Soluzione**: Installa Python da [python.org](https://python.org)
- ✅ Seleziona "Add Python to PATH" durante l'installazione

### ❌ "Errore di encoding" (caratteri strani)
**Soluzione**: Usa il launcher batch `avvia_pdf_editor_pro.bat`
- Configura automaticamente l'encoding UTF-8

### ❌ "Modulo non trovato"
**Soluzione**: Verifica di essere nella directory corretta
```bash
cd "PDF - Editor"
python pdf_editor_pro.py
```

---

## 📁 Struttura Progetto

```
PDF - Editor/
├── 🚀 avvia_pdf_editor_pro.bat     # Launcher Windows
├── 🎯 pdf_editor_pro.py            # Launcher principale
├── 📝 main.py                      # Editor base
├── 📋 README_PRO.md                # Documentazione completa
├── src/                            # Moduli avanzati
│   ├── acrobat_like_gui.py         # Interfaccia Acrobat-style
│   ├── advanced_pdf_editor.py      # Motore PDF avanzato
│   ├── pdf_form_editor.py          # Editor form
│   ├── pdf_security.py             # Sicurezza e crittografia
│   └── user_config.py              # Configurazione utente
└── .venv/                          # Ambiente virtuale Python
```

---

## 🎨 Tips e Tricks

### Modalità Avanzata
- **Ctrl+Rotella Mouse**: Zoom in/out
- **Spazio+Drag**: Sposta vista (pan)
- **Doppio Click**: Modifica elemento selezionato
- **Del**: Elimina elemento selezionato
- **Ctrl+Z**: Annulla ultima operazione

### Modalità Form
- **Tab**: Passa al campo successivo
- **Shift+Tab**: Passa al campo precedente
- **Enter**: Conferma modifiche
- **Esc**: Annulla modifiche

### Salvataggio
- **Ctrl+S**: Salvataggio rapido
- **Ctrl+Shift+S**: Salva con nome
- **Backup automatico**: Ogni 5 minuti (configurabile)

---

## 🆘 Supporto

Per problemi o suggerimenti:
1. Verifica la sezione "Risoluzione Problemi" sopra
2. Controlla i file di log in `.pdf_editor_pro/`
3. Riavvia l'applicazione in modalità base se necessario

---

**🎉 Buon lavoro con PDF Editor Pro!**
*La soluzione completa per tutti i tuoi PDF*