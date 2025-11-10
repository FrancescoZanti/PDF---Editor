#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Editor - Applicazione Desktop per la modifica di file PDF
Compatibile con Windows 10/11

Funzionalità principali:
- Unione di file PDF multipli
- Divisione di PDF in pagine singole o intervalli
- Rotazione delle pagine PDF
- Estrazione di pagine specifiche
- Aggiunta di watermark/filigrane
- Estrazione del testo dai PDF
- Conversione di immagini in PDF
- Anteprima delle pagine
"""

import sys
import os
from pathlib import Path

# Aggiungi il percorso src al sys.path per gli import
current_dir = Path(__file__).parent
src_dir = current_dir / "src"

if src_dir.exists():
    sys.path.insert(0, str(src_dir))
else:
    # Fallback: aggiungi directory corrente
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"Errore nell'importazione: {e}")
    print("Assicurati che tutte le dipendenze siano installate:")
    print("pip install pypdf pillow pdf2image reportlab")
    sys.exit(1)
except Exception as e:
    print(f"Errore durante l'avvio dell'applicazione: {e}")
    sys.exit(1)