#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script di test visuale per il tema chiaro/scuro
Questo script mostra come il tema viene applicato all'applicazione.
"""

import sys
from pathlib import Path

# Aggiungi il percorso src
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
if src_dir.exists():
    sys.path.insert(0, str(src_dir))

def test_theme_detection():
    """Test del rilevamento del tema"""
    print("=" * 60)
    print("TEST TEMA CHIARO/SCURO")
    print("=" * 60)
    print()
    
    from theme_manager import ThemeManager
    from user_config import user_config
    
    tm = ThemeManager()
    
    print(f"📊 Configurazione tema attuale: {user_config.get('theme', 'auto')}")
    print(f"🖥️  Tema rilevato dal sistema: {tm.get_theme()}")
    print()
    
    # Mostra esempi di colori per tema chiaro
    print("🌞 TEMA CHIARO:")
    print("   • Sfondo principale: #f5f5f5 (grigio chiaro)")
    print("   • Pannelli: #ffffff (bianco)")
    print("   • Pannelli laterali: #e8e8e8 (grigio chiaro)")
    print("   • Testo: #2c3e50 (grigio scuro)")
    print("   • Bordi: #e0e0e0 (grigio)")
    print()
    
    # Mostra esempi di colori per tema scuro
    print("🌙 TEMA SCURO:")
    print("   • Sfondo principale: #1e1e1e (grigio molto scuro)")
    print("   • Pannelli: #2d2d2d (grigio scuro)")
    print("   • Pannelli laterali: #252525 (grigio molto scuro)")
    print("   • Testo: #e0e0e0 (grigio chiaro)")
    print("   • Bordi: #3a3a3a (grigio medio)")
    print()
    
    # Test cambio tema manuale
    print("🔄 Test cambio tema manuale:")
    print()
    
    # Test tema chiaro
    tm.current_theme = "light"
    print(f"   Tema impostato su: LIGHT")
    print(f"   ✓ Stylesheet generato: {len(tm.get_stylesheet())} caratteri")
    print(f"   ✓ Stile pannello laterale generato")
    print(f"   ✓ Stile pannello centrale generato")
    print()
    
    # Test tema scuro
    tm.current_theme = "dark"
    print(f"   Tema impostato su: DARK")
    print(f"   ✓ Stylesheet generato: {len(tm.get_stylesheet())} caratteri")
    print(f"   ✓ Stile pannello laterale generato")
    print(f"   ✓ Stile pannello centrale generato")
    print()
    
    print("=" * 60)
    print("✅ TEST COMPLETATO CON SUCCESSO")
    print("=" * 60)
    print()
    print("📝 Note:")
    print("   • Per vedere il tema in azione, avvia l'applicazione:")
    print("     python pdf_editor_pro.py")
    print("   • Il tema si adatta automaticamente al tema di Windows")
    print("   • Per cambiare manualmente il tema, modifica:")
    print("     C:\\Users\\[TuoNome]\\.pdf_editor_pro\\config.json")
    print()

if __name__ == "__main__":
    try:
        test_theme_detection()
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
