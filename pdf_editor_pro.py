#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Editor Pro - Advanced PDF Editor with Acrobat-like features
Versione professionale con funzionalità avanzate simili ad Adobe Acrobat DC
"""

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QMessageBox, QFileDialog, QDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys
import os
from pathlib import Path

# Aggiungi il percorso src se necessario
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
if src_dir.exists():
    sys.path.insert(0, str(src_dir))

# Import dei moduli avanzati
try:
    from acrobat_like_gui import AcrobatLikeGUI
    from advanced_pdf_editor import AdvancedPDFEditor
    from pdf_form_editor import FormEditorGUI
    from pdf_security import SecurityGUI
    from user_config import user_config
    
    ADVANCED_FEATURES = True
except ImportError as e:
    print(f"Alcune funzionalità avanzate non sono disponibili: {e}")
    # Fallback alla versione base
    try:
        from main import main as basic_main
        from user_config import user_config
    except ImportError:
        user_config = None
    ADVANCED_FEATURES = False

class FeatureSelectionDialog(QDialog):
    """Finestra di selezione delle modalità"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Editor Pro - Selezione Modalità")
        self.resize(600, 600)
        self.setStyleSheet("background-color: #f0f0f0;")
        
        # Centra la finestra
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura l'interfaccia utente"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 20)
        layout.setSpacing(15)
        
        # Titolo
        title_label = QLabel("PDF EDITOR PRO")
        title_label.setFont(QFont('Arial', 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50;")
        layout.addWidget(title_label)
        
        # Sottotitolo
        subtitle_label = QLabel("Scegli la modalità di utilizzo")
        subtitle_label.setFont(QFont('Arial', 12))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #666;")
        layout.addWidget(subtitle_label)
        
        layout.addSpacing(20)
        
        # Pulsante Editor Avanzato
        if ADVANCED_FEATURES:
            advanced_btn = QPushButton("🎯 EDITOR AVANZATO\n(Simile ad Adobe Acrobat)")
            advanced_btn.setFont(QFont('Arial', 12, QFont.Bold))
            advanced_btn.setMinimumHeight(80)
            advanced_btn.clicked.connect(self.open_advanced_editor)
            advanced_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 15px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            layout.addWidget(advanced_btn)
            
            advanced_desc = QLabel("• Editing visuale interattivo\n• Annotazioni e disegni\n• Pannelli laterali\n• Zoom avanzato")
            advanced_desc.setFont(QFont('Arial', 9))
            advanced_desc.setStyleSheet("color: #666; margin-left: 20px;")
            layout.addWidget(advanced_desc)
            
            layout.addSpacing(15)
        
        # Pulsante Editor Base
        basic_btn = QPushButton("📝 EDITOR BASE\n(Funzioni essenziali)")
        basic_btn.setFont(QFont('Arial', 12, QFont.Bold))
        basic_btn.setMinimumHeight(80)
        basic_btn.clicked.connect(self.open_basic_editor)
        basic_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        layout.addWidget(basic_btn)
        
        basic_desc = QLabel("• Unisci, dividi, ruota PDF\n• Estrai testo e pagine\n• Converti immagini\n• Watermark semplici")
        basic_desc.setFont(QFont('Arial', 9))
        basic_desc.setStyleSheet("color: #666; margin-left: 20px;")
        layout.addWidget(basic_desc)
        
        layout.addSpacing(15)
        
        # Pulsante Editor Form
        if ADVANCED_FEATURES:
            form_btn = QPushButton("📋 EDITOR FORM\n(Campi interattivi)")
            form_btn.setFont(QFont('Arial', 12, QFont.Bold))
            form_btn.setMinimumHeight(80)
            form_btn.clicked.connect(self.open_form_editor)
            form_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    border-radius: 10px;
                    padding: 15px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            layout.addWidget(form_btn)
            
            form_desc = QLabel("• Crea campi di testo, checkbox\n• Radio button, dropdown\n• Gestione dati form\n• Validazione campi")
            form_desc.setFont(QFont('Arial', 9))
            form_desc.setStyleSheet("color: #666; margin-left: 20px;")
            layout.addWidget(form_desc)
        
        layout.addStretch()
        
        # Info versione
        version_text = "PDF Editor Pro v3.0 (PySide6)"
        if ADVANCED_FEATURES:
            version_text += " - Tutte le funzionalità disponibili"
        else:
            version_text += " - Modalità base"
        
        version_label = QLabel(version_text)
        version_label.setFont(QFont('Arial', 8))
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: #888;")
        layout.addWidget(version_label)
        
    def open_advanced_editor(self):
        """Apre l'editor avanzato"""
        if user_config:
            user_config.set("default_mode", "advanced")
        
        self.accept()
        
        if ADVANCED_FEATURES:
            window = AcrobatLikeGUI()
            window.show()
            # Keep window reference alive
            self.advanced_window = window
        else:
            QMessageBox.critical(self, "Errore", "Funzionalità avanzate non disponibili")
    
    def open_basic_editor(self):
        """Apre l'editor base"""
        if user_config:
            user_config.set("default_mode", "basic")
        
        self.accept()
        
        try:
            from main import PDFEditor
            window = PDFEditor()
            window.show()
            # Keep window reference alive
            self.basic_window = window
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile avviare l'editor base: {e}")
    
    def open_form_editor(self):
        """Apre l'editor di form"""
        if user_config:
            user_config.set("default_mode", "form")
        
        if not ADVANCED_FEATURES:
            QMessageBox.critical(self, "Errore", "Funzionalità avanzate non disponibili")
            return
        
        # Crea editor PDF di base
        pdf_editor = AdvancedPDFEditor()
        
        # Apri PDF
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Apri PDF per editing form",
            "",
            "PDF files (*.pdf)"
        )
        
        if file_path:
            # Aggiungi ai file recenti
            if user_config:
                user_config.add_recent_file(file_path)
            
            if pdf_editor.open_pdf(file_path):
                self.accept()
                form_gui = FormEditorGUI(None, pdf_editor)
                form_gui.open_form_editor()
                # Keep reference alive
                self.form_gui = form_gui
            else:
                QMessageBox.critical(self, "Errore", "Impossibile aprire il PDF")

def main():
    """Funzione principale - Apre direttamente l'editor avanzato"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # Apri direttamente l'editor avanzato senza dialog di selezione
        if ADVANCED_FEATURES:
            window = AcrobatLikeGUI()
            window.show()
            
            # Mostra messaggio di benvenuto
            QMessageBox.information(
                window,
                "PDF Editor Pro",
                "Benvenuto in PDF Editor Pro!\n\n"
                "Funzionalità disponibili:\n"
                "• Aggiungi testo\n"
                "• Modifica testo annotazioni\n"
                "• Rimuovi testo\n"
                "• Aggiungi immagini\n"
                "• Rimuovi immagini\n"
                "• Annotazioni e disegni\n\n"
                "Usa la toolbar per selezionare gli strumenti.\n"
                "Inizia aprendo un PDF dal menu File."
            )
            
            return app.exec()
        else:
            QMessageBox.critical(
                None, 
                "Errore", 
                "Funzionalità avanzate non disponibili.\n"
                "Assicurati di aver installato tutte le dipendenze:\n"
                "pip install -r requirements.txt"
            )
            return 1
        
    except Exception as e:
        print(f"Errore nell'avvio dell'applicazione: {e}")
        QMessageBox.critical(None, "Errore Critico", 
                           f"Impossibile avviare l'applicazione:\n{e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
