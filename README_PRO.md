# PDF Editor Pro - Advanced PDF Editor

Una potente applicazione desktop per modificare file PDF con funzionalità avanzate simili ad **Adobe Acrobat DC**, sviluppata in Python con interfaccia moderna **PySide6 (Qt)** e completamente compatibile con Windows.

## 🌟 NOVITÀ PDF EDITOR PRO v3.0 - Soluzione Unificata

### ✨ Interfaccia Unificata
**PDF Editor Pro** ora si apre direttamente con l'**Editor Avanzato** pronto all'uso, senza necessità di scegliere tra diverse modalità. L'applicazione è stata unificata per offrire un'esperienza più fluida e professionale.

### 🎯 Avvio Rapido
Basta eseguire `python pdf_editor_pro.py` e l'applicazione si apre immediatamente con l'editor completo, pronto per modificare i tuoi PDF.

## 🚀 Funzionalità Principali

### 📝 **Editing Testo Completo**
- **Aggiunta testo** ✅ - Inserisci testo ovunque con controllo font, dimensione e colore
- **Modifica testo** ✅ - Modifica il contenuto delle annotazioni di testo esistenti
- **Rimozione testo** ✅ - Due opzioni:
  - Copertura con rettangolo bianco (reversibile)
  - Redazione permanente (rimozione definitiva)

### 🖼️ **Gestione Immagini Avanzata**
- **Aggiunta immagini** ✅ - Inserisci immagini (PNG, JPG, BMP, GIF) con dimensioni personalizzabili
- **Rimozione immagini** ✅ - Elimina immagini esistenti dal documento
- **Posizionamento preciso** - Scegli esattamente dove posizionare le immagini

### 🎨 **Sistema Annotazioni Completo**
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

### 🌗 **Tema Chiaro/Scuro Automatico**
- **Rilevamento automatico** - Si adatta al tema di sistema Windows 10/11
- **Modalità personalizzabile** - Scegli tra automatico, chiaro o scuro
- **Configurazione persistente** - Le preferenze vengono salvate
- **Ottimizzazione leggibilità** - Colori ottimizzati per entrambi i temi
- Vedi [TEMA_AUTOMATICO.md](TEMA_AUTOMATICO.md) per maggiori dettagli

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

#### **Metodo Raccomandato: Avvio Diretto**
```bash
python pdf_editor_pro.py
```
L'applicazione si apre direttamente con l'**Editor Avanzato** pronto per modificare PDF.

#### **Metodo 2: Launcher Windows**
```bash
# Doppio click su:
avvia_pdf_editor_pro.bat
# oppure
Avvia_PDF_Editor.ps1
```

#### **Metodo 3: Esecuzione da Sorgente**
```bash
cd src
python acrobat_like_gui.py
```

### **Workflow di Utilizzo Tipico**

1. **Avvia l'applicazione** con `python pdf_editor_pro.py`
2. **Apri un PDF** dal menu File → Apri PDF
3. **Seleziona uno strumento** dalla toolbar:
   - 📝 **Testo** - Clicca dove vuoi aggiungere testo
   - 🖼️ **Immagine** - Clicca per inserire un'immagine
   - 🗑️ **Elimina** - Rimuovi testo, annotazioni o immagini
   - 🖍️ **Evidenzia** - Evidenzia parti del documento
   - 📋 **Nota** - Aggiungi note adesive
4. **Salva le modifiche** dal menu File → Salva come

### **Esempi di Utilizzo**

#### **Aggiungere Testo**
1. Seleziona strumento "Testo" (T) dalla toolbar
2. Clicca nel punto dove vuoi inserire il testo
3. Digita il testo nel dialog che appare
4. Il testo viene aggiunto con font e colore selezionati

#### **Modificare Testo Esistente**
1. Menu Modifica → Modifica testo annotazione
2. Seleziona l'annotazione da modificare
3. Inserisci il nuovo testo
4. Le modifiche vengono applicate immediatamente

#### **Rimuovere Testo**
1. Seleziona strumento "Elimina" (🗑️) dalla toolbar
2. Clicca nell'area dove vuoi rimuovere il testo
3. Scegli il metodo:
   - **Copri con bianco** - Nasconde il testo (reversibile)
   - **Redazione permanente** - Rimuove definitivamente
4. Specifica le dimensioni dell'area
5. Il testo viene rimosso

#### **Inserire Immagini**
1. Seleziona strumento "Immagine" (🖼️) dalla toolbar
2. Clicca dove vuoi posizionare l'immagine
3. Seleziona il file immagine (PNG, JPG, BMP, GIF)
4. Specifica larghezza e altezza
5. L'immagine viene inserita nel documento

#### **Rimuovere Immagini**
1. Seleziona strumento "Elimina" (🗑️) dalla toolbar
2. Clicca nell'area dell'immagine
3. Scegli "Elimina immagine" dal menu
4. Seleziona l'immagine da rimuovere dalla lista
5. L'immagine viene eliminata dal PDF

## 📂 Struttura Progetto

```
PDF-Editor/
├── 🎯 pdf_editor_pro.py         # ← UNIFICATO: Launcher dell'Editor Avanzato
##
├── 📂 src/
│   ├── 🆕 acrobat_like_gui.py   # Interfaccia unificata stile Acrobat
│   ├── 🆕 advanced_pdf_editor.py # Engine editing avanzato con tutte le funzionalità
│   ├── 🆕 pdf_form_editor.py    # Editor form interattivi
│   ├── 🆕 pdf_security.py       # Sicurezza e crittografia
│   ├── main.py                  # Applicazione base
│   ├── pdf_manager.py           # Operazioni PDF base
│   └── ui_components.py         # Componenti UI
├── 📄 requirements.txt          # Dipendenze aggiornate
├── 🧪 test_simple.py           # Test diagnostico
├── 📖 README.md                # Documentazione generale
└── 📖 README_PRO.md            # Questa documentazione

**NOTA:** pdf_editor_pro.py ora è l'**unico punto di accesso** all'editor avanzato.
Non è più necessario scegliere tra diverse modalità - l'applicazione si apre
direttamente pronta per modificare i PDF.
```

## 🆚 Base vs Pro

Questa documentazione si riferisce alla versione Pro. La repository ora mantiene
e supporta esclusivamente `pdf_editor_pro.py` come launcher principale.
La versione base non è più fornita.
| **Annotazioni/Markup** | ❌ | ✅ |
| **Form Interattivi** | ❌ | ✅ |
| **Crittografia/Password** | ❌ | ✅ |
| **Firma Digitale** | ❌ | ✅ |
| **Ideale per** | Operazioni veloci | Editing professionale |

## 🔬 Tecnologie Utilizzate

### **Core**
- **Python 3.8+** - Linguaggio principale
- **PySide6 (Qt 6)** - Framework GUI moderno per interfaccia professionale Windows 11
- **PyMuPDF (fitz)** - Engine PDF avanzato per editing visuale e manipolazione contenuti
- **Pillow (PIL)** - Elaborazione immagini avanzata

### **Sicurezza**
- **cryptography** - Crittografia e firma digitale
- **hashlib** - Funzioni hash sicure

### **Elaborazione**
- **reportlab** - Generazione PDF da zero
- **numpy** - Elaborazione numerica per immagini
- **opencv-python** - Computer vision per OCR futuro

### **Base (dalla versione originale)**
- **pypdf** - Manipolazione PDF base (merge, split, rotate)
- **pdf2image** - Conversione PDF in immagini per anteprima
- **reportlab** - Generazione PDF e watermark

## 🔄 Nuove Funzionalità v3.0

### **Gestione Testo Avanzata**
- `add_text()` - Aggiunge nuovo testo con font e colore personalizzabili
- `modify_text_annotation()` - Modifica il contenuto delle annotazioni esistenti
- `redact_text()` - Rimozione permanente di testo (redaction)
- `cover_text_with_white()` - Copertura reversibile del testo

### **Gestione Immagini Completa**
- `add_image()` - Inserisce immagini con posizionamento e dimensioni precise
- `get_images_on_page()` - Lista tutte le immagini presenti
- `delete_image_by_xref()` - Rimuove immagini selezionate

### **Interfaccia Unificata**
- Avvio diretto nell'Editor Avanzato
- Toolbar completa con strumenti testo, immagine ed eliminazione
- Menu contestuali per operazioni rapide
- Supporto completo per tutte le operazioni richieste

## 🆚 Confronto con Versione Precedente

| Funzionalità | Versione 2.0 | Versione 3.0 (Attuale) |
|--------------|--------------|------------------------|
| Avvio | Selezione modalità | Diretto nell'editor |
| Aggiunta testo | ✅ | ✅ |
| Modifica testo | ❌ | ✅ |
| Rimozione testo | ❌ | ✅ |
| Aggiunta immagini | Limitato | ✅ Completo |
| Rimozione immagini | ❌ | ✅ |
| Interfaccia | 3 modalità separate | Unificata |
| Usabilità | Medio | Alto |

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