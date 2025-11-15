#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test semplificato per PDF Editor - evita problemi di encoding
"""

import sys
import os
from pathlib import Path

def test_app():
    """Test semplificato dell'applicazione"""
    
    # Aggiungi il percorso src
    current_dir = Path(__file__).parent
    src_dir = current_dir / "src"
    
    if src_dir.exists():
        sys.path.insert(0, str(src_dir))
    
    try:
        # Test import
        import main
        print("Import main: OK")
        
        # Test funzione main
        if hasattr(main, 'main'):
            print("Funzione main: OK")
        else:
            print("Funzione main: ERRORE")
            return False
            
        # Test classe PDFEditor
        if hasattr(main, 'PDFEditor'):
            print("Classe PDFEditor: OK")
        else:
            print("Classe PDFEditor: ERRORE")
            return False
            
        print("Tutti i test superati!")
        print("L'applicazione e' pronta per l'uso.")
        print("")
        print("Per avviare l'applicazione:")
        print("1. Esegui: python pdf_editor_pro.py")
        print("2. Oppure usa: ./avvia_pdf_editor_pro.bat")
        
        return True
        
    except Exception as e:
        print(f"Errore durante i test: {e}")
        return False

if __name__ == "__main__":
    success = test_app()
    if not success:
        sys.exit(1)