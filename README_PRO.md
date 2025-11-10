# PDF Editor Pro - Advanced PDF Editor

Una potente applicazione desktop per modificare file PDF con funzionalità avanzate simili ad **Adobe Acrobat DC**, sviluppata in Python e completamente compatibile con Windows.

## 🌟 NOVITÀ PDF EDITOR PRO v2.0

### ✨ Tre Modalità di Utilizzo

1. **🎯 EDITOR AVANZATO** - Interfaccia stile Adobe Acrobat
2. **📝 EDITOR BASE** - Funzioni essenziali semplificate  
3. **📋 EDITOR FORM** - Specializzato per form interattivi

## 🚀 Funzionalità Principali

### 📝 **Editing Avanzato (Nuovo!)**
- **Editing visuale interattivo** - Clicca e modifica direttamente nel PDF
- **Aggiunta testo** - Inserisci testo ovunque con controllo font e dimensione
- **Inserimento immagini** - Trascina e inserisci immagini nel PDF
- **Modifica esistente** - Modifica testo e immagini già presenti

### 🎨 **Sistema Annotazioni Completo (Nuovo!)**
- **Evidenziatori** - Evidenzia testo con colori personalizzabili
- **Note adesive** - Aggiungi note popup cliccabili
- **Disegno a mano libera** - Disegna direttamente sul PDF
- **Forme geometriche** - Rettangoli, cerchi, linee, frecce
- **Controllo colori e spessore** - Personalizza completamente l'aspetto

### 📋 **Editor Form Interattivi (Nuovo!)**
- **Campi di testo** - Singola riga e area di testo multi-riga
- **Checkbox e Radio Button** - Per selezioni multiple e singole
- **Dropdown e Liste** - Menu a discesa e liste di selezione
- **Pulsanti** - Con azioni personalizzabili
- **Campi firma digitale** - Per firme elettroniche
- **Gestione dati** - Importa/esporta dati form in JSON
- **Validazione** - Controlla campi obbligatori e formati

### 🔒 **Sicurezza Avanzata (Nuovo!)**
- **Crittografia PDF** - Password utente e proprietario
- **Controllo permessi** - Stampa, copia, modifica, annotazioni
- **Firma digitale** - Sistema di firma elettronica simulata
- **Watermark sicurezza** - Filigrane per documenti confidenziali
- **Timbri di sicurezza** - CONFIDENTIAL, DRAFT, ecc.
- **Rimozione metadati** - Elimina informazioni sensibili
- **Generazione chiavi** - Crea coppie di chiavi RSA

### 🔧 **Funzionalità Base**
- **Unione PDF** - Combina più file PDF
- **Divisione PDF** - Separa in pagine o intervalli
- **Rotazione** - Ruota pagine di 90°, 180°, 270°
- **Estrazione pagine** - Estrai pagine specifiche
- **Estrazione testo** - Converti PDF in testo
- **Conversione immagini** - Da JPG/PNG/etc. a PDF
- **Anteprima** - Visualizzazione con zoom avanzato

## 🖥️ Interfaccia Professionale

### **Editor Avanzato - Stile Adobe Acrobat**
- **Barra menu completa** - File, Modifica, Visualizza, Strumenti
- **Toolbar icone** - Accesso rapido a tutti gli strumenti
- **Pannello navigazione** - Miniature e controlli pagina
- **Area centrale** - Canvas con zoom e scroll
- **Pannello proprietà** - Controlli strumento attivo
- **Pannello commenti** - Lista annotazioni e commenti
- **Barra stato** - Informazioni documento e progresso

### **Controlli Avanzati**
- **Zoom intelligente** - In/Out, Adatta finestra, Percentuale
- **Navigazione pagine** - Avanti/Indietro, Vai a pagina
- **Selezione strumenti** - Toolbar e radio button
- **Proprietà dinamiche** - Cambiano in base allo strumento
- **Anteprima real-time** - Vedi modifiche immediatamente

## 📦 Requisiti di Sistema

### **Hardware Minimo**
- **Sistema**: Windows 10/11 (64-bit raccomandato)
- **RAM**: 4GB (8GB raccomandato per PDF grandi)
- **Spazio disco**: 200MB per l'applicazione
- **Processore**: Intel/AMD dual-core o superiore

### **Software**
- **Python**: 3.8+ (viene installato automaticamente)
- **Dipendenze**: Installazione automatica tramite requirements.txt

## 🔧 Installazione

### **Installazione Rapida**
```bash
git clone [repository-url]
cd PDF-Editor
pip install -r requirements.txt
```

### **Verifica Installazione**
```bash
python test_simple.py
```

## 🎯 Utilizzo

### **Avvio Applicazione**

#### **Metodo 1: Selettore Modalità (Raccomandato)**
```bash
python pdf_editor_pro.py
```
Apre una finestra di selezione per scegliere la modalità desiderata.

#### **Metodo 2: Editor Avanzato Diretto**
```bash
python src/acrobat_like_gui.py
```

#### **Metodo 3: Editor Base**
```bash
python pdf_editor.py
```

#### **Metodo 4: Launcher Windows**
```bash
# Doppio click su:
avvia_pdf_editor.bat
# oppure
Avvia_PDF_Editor.ps1
```

### **Esempi di Utilizzo Avanzato**

#### **Annotazioni Professionali**
1. Apri PDF nell'Editor Avanzato
2. Seleziona strumento "Evidenzia"
3. Scegli colore dal selettore
4. Clicca e trascina sul testo da evidenziare
5. Aggiungi note cliccando su "Nota"
6. Salva PDF con annotazioni

#### **Creazione Form Interattivi**
1. Apri "Editor Form" dalla schermata principale
2. Seleziona tipo campo (testo, checkbox, ecc.)
3. Inserisci nome campo e proprietà
4. Clicca "Crea Campo" e seleziona area nel PDF
5. Ripeti per tutti i campi necessari
6. Esporta/importa dati form in JSON

#### **Sicurezza Documento**
1. Nell'Editor Avanzato, vai al menu "Strumenti"
2. Seleziona "Sicurezza PDF"
3. Tab "Crittografia": imposta password
4. Tab "Permessi": configura accessi
5. Tab "Firma Digitale": aggiungi firma
6. Tab "Avanzate": watermark e timbri

## 📂 Struttura Progetto

```
PDF-Editor/
├── 🎯 pdf_editor_pro.py         # ← NUOVO: Launcher con selezione modalità
├── 📝 pdf_editor.py             # Editor base originale  
├── 📂 src/
│   ├── 🆕 acrobat_like_gui.py   # Interfaccia stile Acrobat
│   ├── 🆕 advanced_pdf_editor.py # Engine editing avanzato
│   ├── 🆕 pdf_form_editor.py    # Editor form interattivi
│   ├── 🆕 pdf_security.py       # Sicurezza e crittografia
│   ├── main.py                  # Applicazione base
│   ├── pdf_manager.py           # Operazioni PDF base
│   └── ui_components.py         # Componenti UI
├── 📄 requirements.txt          # Dipendenze aggiornate
├── 🧪 test_simple.py           # Test diagnostico
├── 📖 README.md                # Questa documentazione
└── 📋 ISTRUZIONI_AVVIO.md      # Guida avvio dettagliata
```

## 🔬 Tecnologie Utilizzate

### **Core**
- **Python 3.8+** - Linguaggio principale
- **tkinter** - Framework GUI nativo Windows
- **PyMuPDF (fitz)** - Engine PDF avanzato per editing
- **Pillow (PIL)** - Elaborazione immagini avanzata

### **Sicurezza**
- **cryptography** - Crittografia e firma digitale
- **hashlib** - Funzioni hash sicure

### **Elaborazione**
- **reportlab** - Generazione PDF da zero
- **numpy** - Elaborazione numerica per immagini
- **opencv-python** - Computer vision per OCR futuro

### **Base (dalla versione originale)**
- **pypdf** - Manipolazione PDF base
- **pdf2image** - Conversione PDF in immagini

## 🆚 Confronto Versioni

| Funzionalità | Editor Base | Editor Avanzato | Editor Form |
|--------------|-------------|-----------------|-------------|
| Unisci/Dividi PDF | ✅ | ✅ | ✅ |
| Rotazione | ✅ | ✅ | ✅ |
| Estrazione | ✅ | ✅ | ✅ |
| **Editing visuale** | ❌ | ✅ | ✅ |
| **Annotazioni** | ❌ | ✅ | ✅ |
| **Form interattivi** | ❌ | ✅ | ✅ |
| **Sicurezza avanzata** | ❌ | ✅ | ✅ |
| **Crittografia** | ❌ | ✅ | ✅ |
| **Firma digitale** | ❌ | ✅ | ✅ |
| Facilità d'uso | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Funzionalità | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🚨 Risoluzione Problemi

### **Problemi Comuni**

#### **"Funzionalità avanzate non disponibili"**
```bash
# Installa dipendenze mancanti
pip install PyMuPDF cryptography numpy opencv-python
```

#### **Errori di importazione**
```bash
# Verifica installazione
python test_simple.py

# Reinstalla tutto
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

#### **PDF non si apre nell'editor avanzato**
- Verifica che il PDF non sia corrotto
- Controlla se il PDF è crittografato
- Prova prima a aprirlo nell'editor base

#### **Prestazioni lente con PDF grandi**
- Usa zoom minore per PDF con molte pagine
- Chiudi altri documenti aperti
- Aumenta RAM se possibile

### **Log e Debug**
L'applicazione salva log dettagliati in:
- Finestra di output (Editor Base)
- Barra di stato (Editor Avanzato)
- Console Python per errori critici

## 🔮 Roadmap Futura

### **Versione 2.1 (In Sviluppo)**
- [ ] OCR integrato con Tesseract
- [ ] Supporto per tablet e firma touch
- [ ] Plugin system per estensioni
- [ ] Compressione PDF intelligente

### **Versione 2.2 (Pianificata)**
- [ ] Collaborazione in tempo reale
- [ ] Sincronizzazione cloud
- [ ] Mobile app companion
- [ ] API REST per integrazione

### **Versione 3.0 (Visione)**
- [ ] AI per riconoscimento contenuti
- [ ] Traduzione automatica
- [ ] Generazione PDF da template
- [ ] Workflow automation

## 📄 Licenza

Questo progetto è rilasciato sotto **Licenza MIT**. Vedi il file `LICENSE` per i dettagli completi.

## 🤝 Contributi

I contributi sono benvenuti! Per contribuire:

1. **Fork** del progetto
2. **Clone** in locale
3. **Branch** per la tua funzionalità
4. **Sviluppa** e testa
5. **Pull Request** con descrizione dettagliata

### **Aree di Contributo**
- 🐛 **Bug fixes** - Correzione errori
- ✨ **Nuove funzionalità** - Espansione capabilities
- 📚 **Documentazione** - Miglioramento guide
- 🧪 **Testing** - Casi di test aggiuntivi
- 🎨 **UI/UX** - Miglioramenti interfaccia

## 📞 Supporto

### **Canali di Supporto**
- **GitHub Issues** - Bug report e richieste funzionalità
- **Discussions** - Domande e discussioni generali
- **Wiki** - Documentazione approfondita

### **Prima di Chiedere Supporto**
1. Leggi questo README completamente
2. Controlla `ISTRUZIONI_AVVIO.md`
3. Esegui `python test_simple.py`
4. Cerca negli Issues esistenti

---

## 🎉 **Grazie per aver scelto PDF Editor Pro!**

**PDF Editor Pro** porta le funzionalità professionali di Adobe Acrobat DC direttamente sul tuo desktop Windows, con un'interfaccia moderna e intuitiva, completamente gratuito e open source.

### **Inizia Subito**
```bash
python pdf_editor_pro.py
```

**Buon editing! 📝✨**