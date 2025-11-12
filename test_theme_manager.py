#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test per il Theme Manager
"""

import sys
import os
from pathlib import Path

# Aggiungi il percorso src
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
if src_dir.exists():
    sys.path.insert(0, str(src_dir))

def test_theme_manager():
    """Test del theme manager"""
    
    try:
        # Test import
        from theme_manager import ThemeManager, theme_manager
        print("✓ Import theme_manager: OK")
        
        # Test istanza
        tm = ThemeManager()
        print("✓ Creazione istanza ThemeManager: OK")
        
        # Test get_theme
        current_theme = tm.get_theme()
        print(f"✓ Tema rilevato: {current_theme}")
        assert current_theme in ["light", "dark"], "Tema non valido"
        
        # Test get_stylesheet
        stylesheet = tm.get_stylesheet()
        print("✓ get_stylesheet: OK")
        assert isinstance(stylesheet, str), "Stylesheet non è una stringa"
        assert len(stylesheet) > 0, "Stylesheet è vuoto"
        
        # Test get_title_frame_style
        title_style = tm.get_title_frame_style()
        print("✓ get_title_frame_style: OK")
        assert isinstance(title_style, str), "Title style non è una stringa"
        
        # Test get_title_label_style
        label_style = tm.get_title_label_style()
        print("✓ get_title_label_style: OK")
        assert isinstance(label_style, str), "Label style non è una stringa"
        
        # Test get_panel_style
        side_panel_style = tm.get_panel_style("side")
        print("✓ get_panel_style (side): OK")
        assert isinstance(side_panel_style, str), "Side panel style non è una stringa"
        
        center_panel_style = tm.get_panel_style("center")
        print("✓ get_panel_style (center): OK")
        assert isinstance(center_panel_style, str), "Center panel style non è una stringa"
        
        # Test light theme
        tm.current_theme = "light"
        light_stylesheet = tm.get_stylesheet()
        print("✓ Light theme stylesheet: OK")
        assert "background-color: #f5f5f5" in light_stylesheet, "Light theme mancante"
        
        # Test dark theme
        tm.current_theme = "dark"
        dark_stylesheet = tm.get_stylesheet()
        print("✓ Dark theme stylesheet: OK")
        assert "background-color: #1e1e1e" in dark_stylesheet, "Dark theme mancante"
        
        # Test istanza globale
        print(f"✓ Istanza globale theme_manager: {theme_manager.get_theme()}")
        
        print("\n✅ Tutti i test del theme manager superati!")
        return True
        
    except Exception as e:
        print(f"✗ Errore durante i test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_user_config():
    """Test delle modifiche alla user_config"""
    
    try:
        from user_config import UserConfig
        print("\n✓ Import user_config: OK")
        
        # Test default config con auto theme
        uc = UserConfig()
        print("✓ Creazione istanza UserConfig: OK")
        
        default_theme = uc.default_config.get("theme")
        print(f"✓ Tema di default: {default_theme}")
        assert default_theme == "auto", f"Tema di default non è 'auto', è '{default_theme}'"
        
        print("\n✅ Tutti i test di user_config superati!")
        return True
        
    except Exception as e:
        print(f"✗ Errore durante i test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_theme_manager() and test_user_config()
    
    if success:
        print("\n" + "="*50)
        print("✅ TUTTI I TEST SUPERATI!")
        print("="*50)
        print("\nIl theme manager è pronto per l'uso.")
        print("Il tema si adatta automaticamente al tema di sistema di Windows.")
        sys.exit(0)
    else:
        print("\n" + "="*50)
        print("✗ ALCUNI TEST FALLITI")
        print("="*50)
        sys.exit(1)
