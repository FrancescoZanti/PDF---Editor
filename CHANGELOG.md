# 📝 Changelog

Tutte le modifiche notevoli a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/lang/it/).

## [Non Rilasciato]

### Da Fare
- Compressione PDF intelligente
- Batch processing per file multipli
- OCR per riconoscimento testo
- Tema scuro completo con personalizzazione avanzata
- Drag & drop per file

## [3.0.0] - 2025-11

### 🎉 Versione Principale - Migrazione PySide6

Questa release segna la migrazione completa dell'applicazione da tkinter a PySide6 (Qt), offrendo un'interfaccia moderna compatibile con Windows 11.

### Aggiunto
- ✨ **Interfaccia PySide6 moderna** con design Windows 11
- ✨ **Dialog nativi del sistema** per apertura/salvataggio file
- ✨ **Supporto DPI alto** per schermi 4K, 5K, 8K
- ✨ **Rendering hardware-accelerated** per prestazioni migliorate
- ✨ **Versione Pro completa** con:
  - Editor visuale stile Adobe Acrobat
  - Sistema annotazioni completo (evidenziatori, note, disegni)
  - Editor form interattivi (campi testo, checkbox, dropdown)
  - Sicurezza avanzata (crittografia, password, firme digitali)
- 🌗 **Tema Chiaro/Scuro Automatico**:
  - Rilevamento automatico del tema di sistema Windows 10/11
  - Supporto per modalità chiara, scura e automatica
  - Configurazione persistente delle preferenze tema
  - Documentazione dedicata in TEMA_AUTOMATICO.md
- 📚 **Documentazione completa** migliorata:
  - README.md aggiornato con FAQ e troubleshooting dettagliato
  - CONTRIBUTING.md per linee guida contribuzione
  - CHANGELOG.md per cronologia versioni
  - GUIDA_RAPIDA.md per funzionalità Pro
  - ISTRUZIONI_AVVIO.md dettagliate
  - TEMA_AUTOMATICO.md per guida al tema chiaro/scuro automatico
- 🧪 **Test diagnostici** (`test_simple.py`)
- 🚀 **Launcher multipli** (batch, PowerShell, Python script)

### Modificato
- 🔄 **Migrazione UI completa** da tkinter a PySide6
- 🎨 **Redesign completo interfaccia** con Material Design
- ⚡ **Ottimizzazioni prestazioni** su operazioni PDF
- 📦 **Aggiornamento dipendenze**:
  - Aggiunto PySide6
  - Aggiornato pypdf
  - Aggiunto PyMuPDF per funzionalità Pro
  - Aggiunto cryptography per sicurezza

### Corretto
- 🐛 Risolti problemi con caratteri speciali nei nomi file
- 🐛 Corretta gestione errori durante operazioni PDF
- 🐛 Migliorata gestione memoria per PDF grandi
- 🐛 Risolti problemi di encoding su Windows

### Rimosso
- ❌ Dipendenza da tkinter-tooltip (sostituita da Qt tooltips)
- ❌ Vecchie componenti UI obsolete

## [2.0.0] - Data precedente

### Aggiunto
- Funzionalità avanzate versione Pro (versione tkinter)
- Editor form PDF
- Funzionalità di sicurezza base
- Interfaccia acrobat-like (tkinter)

### Modificato
- Ristrutturazione codice in moduli
- Miglioramenti alle operazioni PDF base

## [1.0.0] - Data iniziale

### Aggiunto
- ✨ Prima release pubblica
- 📄 Funzionalità base:
  - Unione PDF
  - Divisione PDF
  - Rotazione pagine
  - Estrazione pagine
  - Aggiunta watermark
  - Estrazione testo
  - Conversione immagini in PDF
  - Anteprima PDF
- 🖥️ Interfaccia grafica tkinter base
- 📚 Documentazione iniziale

---

## Tipi di Modifiche

- **Aggiunto** - Per nuove funzionalità
- **Modificato** - Per modifiche a funzionalità esistenti
- **Deprecato** - Per funzionalità che saranno rimosse
- **Rimosso** - Per funzionalità rimosse
- **Corretto** - Per correzioni di bug
- **Sicurezza** - In caso di vulnerabilità

## Come Leggere le Versioni

Questo progetto usa [Semantic Versioning](https://semver.org/lang/it/):

- **MAJOR** (X.0.0) - Modifiche incompatibili con versioni precedenti
- **MINOR** (0.X.0) - Nuove funzionalità retrocompatibili
- **PATCH** (0.0.X) - Correzioni bug retrocompatibili

Esempio: `3.0.0`
- `3` = Versione major (migrazione PySide6 - breaking change)
- `0` = Versione minor (nessuna nuova feature dopo la migrazione)
- `0` = Patch (nessuna correzione bug dopo la migrazione)

---

**Nota**: Le date di rilascio seguono il formato YYYY-MM-DD (ISO 8601).
