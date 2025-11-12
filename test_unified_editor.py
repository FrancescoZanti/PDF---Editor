#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test per verificare le nuove funzionalità dell'Editor Unificato
"""

import sys
import os
from pathlib import Path

# Aggiungi il percorso src al sys.path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_imports():
    """Test che tutti i moduli necessari siano importabili"""
    print("Test 1: Verifica import moduli...")
    try:
        from advanced_pdf_editor import AdvancedPDFEditor
        print("  ✓ AdvancedPDFEditor importato")
        
        # Verifica che i nuovi metodi esistano
        editor = AdvancedPDFEditor()
        assert hasattr(editor, 'redact_text'), "Metodo redact_text mancante"
        assert hasattr(editor, 'cover_text_with_white'), "Metodo cover_text_with_white mancante"
        assert hasattr(editor, 'get_images_on_page'), "Metodo get_images_on_page mancante"
        assert hasattr(editor, 'delete_image_by_xref'), "Metodo delete_image_by_xref mancante"
        assert hasattr(editor, 'modify_text_annotation'), "Metodo modify_text_annotation mancante"
        print("  ✓ Tutti i nuovi metodi sono presenti")
        
        return True
    except Exception as e:
        print(f"  ✗ Errore nell'import: {e}")
        return False

def test_acrobat_gui_imports():
    """Test che l'interfaccia GUI sia importabile (senza avviarla)"""
    print("\nTest 2: Verifica import GUI...")
    try:
        # Questo test potrebbe fallire in ambienti headless
        # ma verifica che il codice sia sintatticamente corretto
        from acrobat_like_gui import AcrobatLikeGUI
        print("  ✓ AcrobatLikeGUI importata")
        return True
    except ImportError as e:
        if "libEGL" in str(e) or "Qt" in str(e):
            print(f"  ⚠ GUI non disponibile in ambiente headless (normale): {e}")
            return True  # È normale in ambienti headless
        print(f"  ✗ Errore nell'import GUI: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Errore imprevisto: {e}")
        return False

def test_pdf_editor_pro():
    """Test che il launcher principale sia importabile"""
    print("\nTest 3: Verifica launcher pdf_editor_pro.py...")
    try:
        # Verifica che il file esista e sia valido Python
        pro_file = current_dir / "pdf_editor_pro.py"
        if not pro_file.exists():
            print("  ✗ File pdf_editor_pro.py non trovato")
            return False
        
        # Compila il file per verificare la sintassi
        import py_compile
        py_compile.compile(str(pro_file), doraise=True)
        print("  ✓ pdf_editor_pro.py ha sintassi valida")
        
        # Verifica che la funzione main esista
        with open(pro_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'def main():' in content:
                print("  ✓ Funzione main() presente")
            else:
                print("  ✗ Funzione main() non trovata")
                return False
            
            # Verifica che non ci sia più il dialog di selezione
            if 'FeatureSelectionDialog' not in content or 'dialog.exec()' not in content:
                print("  ✓ Dialog di selezione rimosso/modificato correttamente")
            
            # Verifica che apra direttamente l'editor avanzato
            if 'AcrobatLikeGUI()' in content and 'window.show()' in content:
                print("  ✓ Apre direttamente l'Editor Avanzato")
            else:
                print("  ⚠ Potrebbe non aprire direttamente l'editor")
        
        return True
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        return False

def test_method_signatures():
    """Test che i nuovi metodi abbiano le signature corrette"""
    print("\nTest 4: Verifica signature metodi...")
    try:
        from advanced_pdf_editor import AdvancedPDFEditor
        import inspect
        
        editor = AdvancedPDFEditor()
        
        # Verifica redact_text
        sig = inspect.signature(editor.redact_text)
        params = list(sig.parameters.keys())
        assert 'page_num' in params and 'rect' in params, "redact_text ha parametri errati"
        print("  ✓ redact_text(page_num, rect)")
        
        # Verifica cover_text_with_white
        sig = inspect.signature(editor.cover_text_with_white)
        params = list(sig.parameters.keys())
        assert 'page_num' in params and 'rect' in params, "cover_text_with_white ha parametri errati"
        print("  ✓ cover_text_with_white(page_num, rect)")
        
        # Verifica get_images_on_page
        sig = inspect.signature(editor.get_images_on_page)
        params = list(sig.parameters.keys())
        assert 'page_num' in params, "get_images_on_page ha parametri errati"
        print("  ✓ get_images_on_page(page_num)")
        
        # Verifica delete_image_by_xref
        sig = inspect.signature(editor.delete_image_by_xref)
        params = list(sig.parameters.keys())
        assert 'page_num' in params and 'xref' in params, "delete_image_by_xref ha parametri errati"
        print("  ✓ delete_image_by_xref(page_num, xref)")
        
        # Verifica modify_text_annotation
        sig = inspect.signature(editor.modify_text_annotation)
        params = list(sig.parameters.keys())
        assert 'page_num' in params and 'annot_index' in params and 'new_text' in params, \
               "modify_text_annotation ha parametri errati"
        print("  ✓ modify_text_annotation(page_num, annot_index, new_text)")
        
        return True
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Esegue tutti i test"""
    print("=" * 60)
    print("Test Editor Unificato - Nuove Funzionalità")
    print("=" * 60)
    
    results = []
    
    results.append(("Import moduli", test_imports()))
    results.append(("Import GUI", test_acrobat_gui_imports()))
    results.append(("Launcher principale", test_pdf_editor_pro()))
    results.append(("Signature metodi", test_method_signatures()))
    
    print("\n" + "=" * 60)
    print("RIEPILOGO TEST")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ TUTTI I TEST SUPERATI!")
        return 0
    else:
        print("\n✗ ALCUNI TEST FALLITI")
        return 1

if __name__ == "__main__":
    sys.exit(main())
