#!/usr/bin/env python3
"""
Test per le funzionalità di editing testo avanzato
"""

import sys
import os

# Aggiungi src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test 1: Verifica che tutti i moduli si importino correttamente"""
    print("Test 1: Import dei moduli...")
    try:
        from advanced_pdf_editor import AdvancedPDFEditor
        print("  ✓ AdvancedPDFEditor importato")
        
        from acrobat_like_gui import AcrobatLikeGUI
        print("  ✓ AcrobatLikeGUI importato")
        
        return True
    except Exception as e:
        print(f"  ✗ Errore import: {e}")
        return False

def test_advanced_pdf_editor():
    """Test 2: Verifica metodi di AdvancedPDFEditor"""
    print("\nTest 2: Metodi AdvancedPDFEditor...")
    try:
        from advanced_pdf_editor import AdvancedPDFEditor
        editor = AdvancedPDFEditor()
        
        # Verifica che i nuovi metodi esistano
        assert hasattr(editor, 'get_text_annotations'), "Manca get_text_annotations"
        print("  ✓ get_text_annotations presente")
        
        assert hasattr(editor, 'modify_text_properties'), "Manca modify_text_properties"
        print("  ✓ modify_text_properties presente")
        
        assert hasattr(editor, 'get_annotation_at_point'), "Manca get_annotation_at_point"
        print("  ✓ get_annotation_at_point presente")
        
        return True
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        return False

def test_gui_attributes():
    """Test 3: Verifica attributi GUI"""
    print("\nTest 3: Attributi GUI per editing testo...")
    try:
        # Non possiamo testare completamente senza QApplication
        # ma possiamo verificare che la classe si definisca correttamente
        import inspect
        from acrobat_like_gui import AcrobatLikeGUI
        
        # Verifica che i nuovi metodi esistano
        assert hasattr(AcrobatLikeGUI, 'edit_text_annotation_properties'), "Manca edit_text_annotation_properties"
        print("  ✓ edit_text_annotation_properties presente")
        
        # Verifica signature del metodo
        sig = inspect.signature(AcrobatLikeGUI.on_canvas_click)
        print(f"  ✓ on_canvas_click signature: {sig}")
        
        return True
    except Exception as e:
        print(f"  ✗ Errore: {e}")
        return False

def main():
    """Esegue tutti i test"""
    print("=" * 60)
    print("TEST FUNZIONALITÀ EDITING TESTO AVANZATO")
    print("=" * 60)
    
    results = []
    
    # Esegui test
    results.append(("Import moduli", test_imports()))
    results.append(("Metodi AdvancedPDFEditor", test_advanced_pdf_editor()))
    results.append(("Attributi GUI", test_gui_attributes()))
    
    # Riepilogo
    print("\n" + "=" * 60)
    print("RIEPILOGO TEST")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nTotale: {passed} passati, {failed} falliti")
    
    if failed == 0:
        print("\n🎉 Tutti i test sono passati!")
        return 0
    else:
        print(f"\n⚠️  {failed} test falliti")
        return 1

if __name__ == "__main__":
    sys.exit(main())
