"""
PDF Editor Pro - Theme Manager
Gestisce il rilevamento automatico del tema di sistema e l'applicazione degli stili
"""
import sys
import platform


class ThemeManager:
    """Gestisce il rilevamento e l'applicazione dei temi"""
    
    def __init__(self):
        self.current_theme = "light"
        self._detect_system_theme()
    
    def _detect_system_theme(self):
        """Rileva il tema di sistema del PC"""
        try:
            # Rileva il tema di Windows
            if platform.system() == "Windows":
                self.current_theme = self._get_windows_theme()
            else:
                # Default per altri sistemi
                self.current_theme = "light"
        except Exception as e:
            print(f"Errore nel rilevamento del tema: {e}")
            self.current_theme = "light"
    
    def _get_windows_theme(self):
        """Rileva il tema di Windows leggendo il registro"""
        try:
            import winreg
            
            # Percorso della chiave di registro per il tema
            registry_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            
            # Apri la chiave di registro
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                registry_path,
                0,
                winreg.KEY_READ
            )
            
            # Leggi il valore AppsUseLightTheme
            # 0 = tema scuro, 1 = tema chiaro
            value, _ = winreg.QueryValueEx(registry_key, "AppsUseLightTheme")
            winreg.CloseKey(registry_key)
            
            return "light" if value == 1 else "dark"
            
        except Exception as e:
            print(f"Impossibile leggere il tema di Windows: {e}")
            return "light"
    
    def get_theme(self):
        """Restituisce il tema corrente"""
        return self.current_theme
    
    def get_stylesheet(self):
        """Restituisce il foglio di stile per il tema corrente"""
        if self.current_theme == "dark":
            return self._get_dark_stylesheet()
        else:
            return self._get_light_stylesheet()
    
    def _get_light_stylesheet(self):
        """Restituisce lo stylesheet per il tema chiaro"""
        return """
            QMainWindow {
                background-color: #f5f5f5;
            }
            QWidget {
                background-color: #f5f5f5;
                color: #2c3e50;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
                color: #2c3e50;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #2c3e50;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 5px;
                color: #2c3e50;
            }
            QLabel {
                color: #2c3e50;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
                color: #2c3e50;
            }
            QDialog {
                background-color: #f5f5f5;
            }
            QMessageBox {
                background-color: #f5f5f5;
            }
        """
    
    def _get_dark_stylesheet(self):
        """Restituisce lo stylesheet per il tema scuro"""
        return """
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3a3a3a;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #e0e0e0;
            }
            QTextEdit {
                background-color: #2d2d2d;
                border: 1px solid #3a3a3a;
                border-radius: 5px;
                padding: 5px;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
            }
            QScrollBar:vertical {
                border: none;
                background: #2d2d2d;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #5a5a5a;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #6a6a6a;
            }
            QListWidget {
                border: 1px solid #3a3a3a;
                border-radius: 3px;
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QDialog {
                background-color: #1e1e1e;
            }
            QMessageBox {
                background-color: #2d2d2d;
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: #e0e0e0;
                border: 1px solid #4a4a4a;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """
    
    def get_title_frame_style(self):
        """Restituisce lo stile per il frame del titolo"""
        if self.current_theme == "dark":
            return """
                QFrame {
                    background-color: #1a1a1a;
                }
            """
        else:
            return """
                QFrame {
                    background-color: #2c3e50;
                }
            """
    
    def get_title_label_style(self):
        """Restituisce lo stile per l'etichetta del titolo"""
        return "color: white;"
    
    def get_button_color(self, base_color):
        """Adatta il colore del pulsante al tema"""
        # I colori dei pulsanti rimangono gli stessi per mantenere la distintività
        return base_color


# Istanza globale del theme manager
theme_manager = ThemeManager()
