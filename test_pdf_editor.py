#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test delle funzionalità principali dell'applicazione PDF Editor
"""

import sys
import os
import tempfile
from pathlib import Path

# Aggiungi il percorso src per gli import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Testa che tutti i moduli necessari siano importabili"""
    print("Test importazione moduli...")
    
    try:
        import pypdf
        print("  OK pypdf")
    except ImportError:
        print("  ERRORE pypdf non trovato")
        return False
    
    try:
        import PIL
        print("  OK Pillow")
    except ImportError:
        print("  ERRORE Pillow non trovato")
        return False
    
    try:
        import reportlab
        print("  OK reportlab")
    except ImportError:
        print("  ERRORE reportlab non trovato")
        return False
    
    try:
        import tkinter
        print("  OK tkinter")
    except ImportError:
        print("  ERRORE tkinter non trovato")
        return False
    
    try:
        from pdf_manager import PDFManager
        print("  OK PDFManager")
    except ImportError as e:
        print(f"  ERRORE PDFManager: {e}")
        return False
    
    try:
        from ui_components import UIComponents
        print("  OK UIComponents")
    except ImportError as e:
        print(f"  ERRORE UIComponents: {e}")
        return False
    
    return True

def test_pdf_manager():
    """Testa le funzionalità base del PDFManager"""
    print("\nTest PDFManager...")
    
    try:
        from pdf_manager import PDFManager
        manager = PDFManager()
        print("  OK PDFManager istanziato correttamente")
        
        # Test metodi esistenti
        methods_to_test = [
            'merge_pdfs', 'split_pdf_pages', 'split_pdf_range',
            'rotate_pdf', 'extract_pages', 'add_watermark',
            'extract_text', 'convert_images_to_pdf', 'preview_pdf'
        ]
        
        for method in methods_to_test:
            if hasattr(manager, method):
                print(f"  OK Metodo {method} disponibile")
            else:
                print(f"  ERRORE Metodo {method} non trovato")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ERRORE durante il test PDFManager: {e}")
        return False

def test_ui_components():
    """Testa i componenti UI senza avviare l'interfaccia grafica"""
    print("\nTest UIComponents...")
    
    try:
        import tkinter as tk
        from ui_components import UIComponents
        
        # Crea una root window temporanea (non visualizzata)
        root = tk.Tk()
        root.withdraw()  # Nascondi la finestra
        
        ui = UIComponents(root)
        print("  OK UIComponents istanziato correttamente")
        
        # Test metodi esistenti
        methods_to_test = [
            'create_button', 'create_progress_bar', 'create_info_display',
            'create_file_list', 'create_status_bar'
        ]
        
        for method in methods_to_test:
            if hasattr(ui, method):
                print(f"  OK Metodo {method} disponibile")
            else:
                print(f"  ERRORE Metodo {method} non trovato")
                return False
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"  ERRORE durante il test UIComponents: {e}")
        return False

def test_main_import():
    """Testa che il modulo main sia importabile"""
    print("\nTest modulo main...")
    
    try:
        import main
        print("  OK main.py importato correttamente")
        
        if hasattr(main, 'PDFEditor'):
            print("  OK Classe PDFEditor trovata")
        else:
            print("  ERRORE Classe PDFEditor non trovata")
            return False
        
        if hasattr(main, 'main'):
            print("  OK Funzione main trovata")
        else:
            print("  ERRORE Funzione main non trovata")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ERRORE durante l'import di main: {e}")
        return False

def main():
    """Esegue tutti i test"""
    print("="*50)
    print("  TEST APPLICAZIONE PDF EDITOR")
    print("="*50)
    
    tests = [
        ("Importazione moduli", test_imports),
        ("PDFManager", test_pdf_manager),
        ("UIComponents", test_ui_components),
        ("Modulo main", test_main_import)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"ERRORE durante {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "="*50)
    print("  RISULTATI TEST")
    print("="*50)
    
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name:.<30} {status}")
        if not result:
            all_passed = False
    
    print("="*50)
    
    if all_passed:
        print("  TUTTI I TEST SUPERATI!")
        print("  L'applicazione è pronta per l'uso.")
        print("\n  Per avviare l'applicazione:")
        print("  - Doppio click su 'avvia_pdf_editor_pro.bat'")
        print("  - Oppure esegui: python pdf_editor_pro.py")
    else:
        print("  ALCUNI TEST FALLITI!")
        print("  Controlla gli errori sopra e installa le dipendenze mancanti.")
        print("  Esegui: pip install -r requirements.txt")
    
    print("="*50)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)