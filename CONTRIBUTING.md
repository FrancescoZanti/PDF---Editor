# 🤝 Guida per Contribuire a PDF Editor

Grazie per l'interesse nel contribuire al progetto PDF Editor! Questa guida ti aiuterà a iniziare.

## 📋 Indice

- [Codice di Condotta](#codice-di-condotta)
- [Come Iniziare](#come-iniziare)
- [Processo di Contribuzione](#processo-di-contribuzione)
- [Linee Guida del Codice](#linee-guida-del-codice)
- [Convenzioni di Commit](#convenzioni-di-commit)
- [Testing](#testing)
- [Documentazione](#documentazione)
- [Revisione del Codice](#revisione-del-codice)

## 📜 Codice di Condotta

### Il Nostro Impegno

Ci impegniamo a rendere la partecipazione a questo progetto un'esperienza libera da molestie per tutti, indipendentemente da età, corporatura, disabilità, etnia, identità di genere, livello di esperienza, nazionalità, aspetto personale, razza, religione o identità e orientamento sessuale.

### Comportamenti Attesi

- Usare un linguaggio accogliente e inclusivo
- Rispettare punti di vista ed esperienze diverse
- Accettare con grazia le critiche costruttive
- Concentrarsi su ciò che è meglio per la comunità
- Mostrare empatia verso gli altri membri della comunità

### Comportamenti Non Accettabili

- Uso di linguaggio o immagini sessualizzate
- Trolling, commenti offensivi/sprezzanti e attacchi personali o politici
- Molestie pubbliche o private
- Pubblicazione di informazioni private altrui senza esplicito permesso
- Altre condotte che potrebbero essere ragionevolmente considerate inappropriate

## 🚀 Come Iniziare

### 1. Setup Ambiente di Sviluppo

```bash
# Fork il repository su GitHub

# Clona il tuo fork
git clone https://github.com/TUO-USERNAME/PDF---Editor.git
cd PDF---Editor

# Aggiungi il repository originale come remote
git remote add upstream https://github.com/FrancescoZanti/PDF---Editor.git

# Crea un ambiente virtuale
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Installa le dipendenze
pip install -r requirements.txt

# Verifica l'installazione
python test_simple.py
```

### 2. Sincronizza con Upstream

Tieni il tuo fork aggiornato:

```bash
# Scarica le modifiche dall'upstream
git fetch upstream

# Aggiorna il tuo branch main
git checkout main
git merge upstream/main
```

## 🔄 Processo di Contribuzione

### 1. Trova o Crea una Issue

- Cerca nelle [issue esistenti](https://github.com/FrancescoZanti/PDF---Editor/issues)
- Se trovi una issue che vuoi risolvere, commentala per far sapere agli altri
- Se non trovi una issue per il tuo contributo, creane una nuova

### 2. Crea un Branch

```bash
# Crea un branch descrittivo
git checkout -b feature/nome-funzionalità
# oppure
git checkout -b bugfix/descrizione-bug
```

**Convenzioni nomi branch:**
- `feature/` - Nuove funzionalità
- `bugfix/` - Correzioni bug
- `docs/` - Modifiche alla documentazione
- `refactor/` - Refactoring del codice
- `test/` - Aggiunta o modifica test

### 3. Sviluppa

- Scrivi codice pulito e ben documentato
- Segui le [linee guida del codice](#linee-guida-del-codice)
- Testa le tue modifiche frequentemente
- Committa spesso con messaggi chiari

### 4. Testa

```bash
# Esegui test diagnostici
python test_simple.py

# Test manuale completo
python pdf_editor_pro.py

# Verifica tutte le funzionalità che hai modificato
```

### 5. Commit e Push

```bash
# Aggiungi i file modificati
git add .

# Committa con un messaggio descrittivo
git commit -m "Add: nuova funzionalità X"

# Push al tuo fork
git push origin feature/nome-funzionalità
```

### 6. Apri una Pull Request

1. Vai sul tuo fork su GitHub
2. Clicca "Compare & pull request"
3. Compila il template della PR con:
   - Descrizione delle modifiche
   - Issue correlata (se presente)
   - Screenshot (se applicabile)
   - Test effettuati
4. Invia la PR

## 📝 Linee Guida del Codice

### Stile Python (PEP 8)

```python
# ✅ BUONO
def merge_pdf_files(input_files, output_file):
    """
    Unisce più file PDF in un singolo documento.
    
    Args:
        input_files (list): Lista dei percorsi dei file PDF da unire
        output_file (str): Percorso del file PDF di output
        
    Returns:
        bool: True se l'operazione ha successo, False altrimenti
    """
    if not input_files:
        return False
    
    try:
        merger = PdfMerger()
        for pdf_file in input_files:
            merger.append(pdf_file)
        merger.write(output_file)
        merger.close()
        return True
    except Exception as e:
        print(f"Errore durante l'unione: {e}")
        return False

# ❌ EVITARE
def MergePDF(files,output):  # Nomi non seguono PEP 8
    if files==[]:return False  # Troppo compatto, difficile da leggere
    try:
        m=PdfMerger()  # Nomi variabili non descrittivi
        for f in files:m.append(f)
        m.write(output);m.close()
        return True
    except:  # Catch troppo generico
        return False
```

### Regole Fondamentali

1. **Indentazione**: 4 spazi (no tab)
2. **Lunghezza linea**: Massimo 88 caratteri (PEP 8 permette 79, ma siamo flessibili)
3. **Naming**:
   - `snake_case` per funzioni e variabili
   - `PascalCase` per classi
   - `UPPER_CASE` per costanti
4. **Imports**:
   ```python
   # Standard library
   import os
   import sys
   
   # Third party
   from PySide6.QtWidgets import QApplication
   import pypdf
   
   # Local
   from src.pdf_manager import PDFManager
   ```
5. **Docstrings**: Usa docstring per tutte le funzioni pubbliche
6. **Type hints**: Raccomandati ma non obbligatori
   ```python
   def split_pdf(input_file: str, output_dir: str, page_ranges: list[int]) -> bool:
       pass
   ```

### Gestione Errori

```python
# ✅ BUONO - Gestione specifica degli errori
try:
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        return pdf_reader
except FileNotFoundError:
    print(f"Errore: File {file_path} non trovato")
    return None
except PermissionError:
    print(f"Errore: Permessi insufficienti per {file_path}")
    return None
except Exception as e:
    print(f"Errore imprevisto: {e}")
    return None

# ❌ EVITARE - Catch troppo generico
try:
    # ... codice ...
except:  # Non cattura eccezioni specifiche
    pass  # Non gestisce l'errore
```

### UI e PySide6

```python
# ✅ BUONO - Struttura chiara e organizzata
class PDFEditorWindow(QMainWindow):
    """Finestra principale dell'applicazione PDF Editor."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Editor")
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Configura l'interfaccia utente."""
        # Widget setup
        self.merge_button = QPushButton("Unisci PDF")
        self.merge_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.merge_button)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def connect_signals(self):
        """Connette i segnali agli slot."""
        self.merge_button.clicked.connect(self.on_merge_clicked)
    
    def on_merge_clicked(self):
        """Gestisce il click sul pulsante Unisci."""
        # Logica del pulsante
        pass
```

## 💬 Convenzioni di Commit

Usa commit messages chiari e descrittivi seguendo questo formato:

```
Tipo: Breve descrizione (max 50 caratteri)

Descrizione dettagliata opzionale (se necessaria).
Spiega COSA è stato cambiato e PERCHÉ.

Riferimenti:
- Closes #123
- Related to #456
```

### Tipi di Commit

- **Add**: Aggiunta di nuove funzionalità
  ```
  Add: supporto per compressione PDF
  ```

- **Fix**: Correzione di bug
  ```
  Fix: errore durante unione di PDF grandi
  ```

- **Update**: Aggiornamento di funzionalità esistenti
  ```
  Update: migliora performance di divisione PDF
  ```

- **Refactor**: Refactoring del codice senza cambiare funzionalità
  ```
  Refactor: semplifica logica di gestione file
  ```

- **Docs**: Modifiche alla documentazione
  ```
  Docs: aggiorna README con esempi di utilizzo
  ```

- **Style**: Modifiche di formattazione (no cambio logica)
  ```
  Style: applica PEP 8 a pdf_manager.py
  ```

- **Test**: Aggiunta o modifica di test
  ```
  Test: aggiungi test per funzione merge_pdf
  ```

### Esempi Completi

```
Add: funzionalità di compressione PDF

Implementa algoritmo di compressione che riduce la dimensione
dei file PDF mantenendo la qualità visiva.

La compressione funziona su:
- Immagini incorporate (riduce qualità JPEG)
- Contenuto duplicato (rimuove ridondanze)
- Metadati non essenziali

Closes #42
```

## 🧪 Testing

### Test Manuale

Ogni contribuzione deve essere testata manualmente:

1. **Avvia l'applicazione**
    ```bash
    python pdf_editor_pro.py
    ```

2. **Testa la funzionalità modificata**
   - Prova casi normali
   - Prova casi limite (file vuoti, molto grandi, etc.)
   - Prova scenari di errore

3. **Verifica altre funzionalità**
   - Assicurati di non aver rotto nulla

4. **Documenta i test**
   - Nella PR, descrivi i test effettuati
   - Allega screenshot se pertinenti

### Test Diagnostico

```bash
# Esegui sempre prima di committare
python test_simple.py
```

### Checklist di Testing

- [ ] L'applicazione si avvia senza errori
- [ ] La funzionalità modificata funziona come previsto
- [ ] Non ci sono nuovi warning o errori
- [ ] L'interfaccia è responsive e non si blocca
- [ ] I file PDF di output sono corretti
- [ ] Gestione errori appropriata
- [ ] Nessuna regressione su altre funzionalità

## 📚 Documentazione

### Documenta il Codice

```python
def extract_pages(input_file: str, output_file: str, pages: list[int]) -> bool:
    """
    Estrae pagine specifiche da un PDF.
    
    Args:
        input_file (str): Percorso del file PDF di input
        output_file (str): Percorso dove salvare il PDF estratto
        pages (list[int]): Lista dei numeri di pagina da estrarre (1-indexed)
        
    Returns:
        bool: True se l'estrazione ha successo, False altrimenti
        
    Raises:
        FileNotFoundError: Se input_file non esiste
        ValueError: Se pages contiene numeri di pagina non validi
        
    Example:
        >>> extract_pages("input.pdf", "output.pdf", [1, 3, 5])
        True
    """
    pass
```

### Aggiorna la Documentazione

Se le tue modifiche cambiano il comportamento dell'applicazione:

1. **README.md** - Aggiorna se necessario
2. **Docstrings** - Mantieni aggiornate
3. **Commenti** - Aggiungi per logica complessa
4. **CONTRIBUTING.md** - Se cambi il processo di contribuzione

## 🔍 Revisione del Codice

### Cosa Aspettarsi

- Un maintainer revisionerà la tua PR
- Potrebbero essere richieste modifiche
- Le revisioni sono un'opportunità di apprendimento

### Come Rispondere ai Feedback

1. **Sii aperto** - Le revisioni migliorano il codice
2. **Fai domande** - Se non capisci un feedback
3. **Implementa i cambiamenti** - Committa le modifiche richieste
4. **Rispondi** - Conferma quando hai fatto i cambiamenti

### Dopo l'Approvazione

1. Un maintainer farà il merge della tua PR
2. Il tuo branch sarà eliminato
3. Le tue modifiche saranno nella prossima release!

## 🎉 Primo Contributo?

Ecco alcune issue perfette per iniziare:
- Issue taggate con `good first issue`
- Issue taggate con `documentation`
- Correzioni di typo nella documentazione
- Miglioramenti all'interfaccia utente

## 💡 Idee per Contribuire

Non sai da dove iniziare? Ecco alcune idee:

### Bug Fixing
- Cerca issue taggate con `bug`
- Testa l'applicazione e segnala bug che trovi

### Nuove Funzionalità
- Implementa funzionalità dalla [roadmap](README.md#-roadmap-e-aggiornamenti-futuri)
- Proponi nuove funzionalità aprendo una issue

### Documentazione
- Migliora README.md
- Aggiungi esempi e tutorial
- Traduci la documentazione in altre lingue

### Testing
- Aggiungi unit test
- Migliora test_simple.py
- Testa su diverse configurazioni

### UI/UX
- Migliora l'aspetto dell'interfaccia
- Ottimizza l'usabilità
- Aggiungi temi (dark mode)

## 📞 Hai Domande?

- Apri una [Discussion](https://github.com/FrancescoZanti/PDF---Editor/discussions)
- Commenta sulla issue relativa
- Contatta i maintainer

## 🙏 Grazie!

Ogni contributo, grande o piccolo, è apprezzato e aiuta a rendere PDF Editor migliore per tutti! 🚀

---

**Buon coding!** 💻✨
