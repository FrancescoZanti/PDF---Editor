from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QFrame, QGroupBox, QTextEdit,
                               QFileDialog, QMessageBox, QInputDialog, QDialog,
                               QRadioButton, QButtonGroup, QPushButton, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
import sys
import os
from pathlib import Path
from pdf_manager import PDFManager
from ui_components import UIComponents

class PDFEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Editor - Modifica PDF")
        self.resize(800, 600)
        
        # Inizializza il manager PDF
        self.pdf_manager = PDFManager()
        
        # Inizializza i componenti UI
        self.ui_components = UIComponents(self)
        
        # Configura l'interfaccia
        self.setup_ui()
        
        # Applica lo stile moderno Windows 11
        self.apply_modern_style()
        
    def apply_modern_style(self):
        """Applica uno stile moderno compatibile con Windows 11"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
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
        """)
        
    def setup_ui(self):
        """Configura l'interfaccia utente principale"""
        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Titolo
        title_frame = QFrame()
        title_frame.setFixedHeight(60)
        title_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel("PDF EDITOR")
        title_label.setFont(QFont('Arial', 20, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        
        main_layout.addWidget(title_frame)
        
        # Contenitore con padding per il contenuto principale
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(10)
        
        # Frame per i pulsanti delle funzioni
        functions_group = QGroupBox("Funzioni PDF")
        functions_group.setFont(QFont('Arial', 12, QFont.Bold))
        functions_layout = QVBoxLayout(functions_group)
        functions_layout.setContentsMargins(10, 20, 10, 10)
        functions_layout.setSpacing(10)
        
        # Prima riga di pulsanti
        row1_frame = QWidget()
        row1_layout = QHBoxLayout(row1_frame)
        row1_layout.setSpacing(5)
        row1_layout.setContentsMargins(0, 0, 0, 0)
        
        self.ui_components.create_button(row1_frame, "Unisci PDF", 
                                        self.merge_pdfs, '#3498db')
        self.ui_components.create_button(row1_frame, "Dividi PDF", 
                                        self.split_pdf, '#e74c3c')
        self.ui_components.create_button(row1_frame, "Ruota PDF", 
                                        self.rotate_pdf, '#f39c12')
        self.ui_components.create_button(row1_frame, "Estrai Pagine", 
                                        self.extract_pages, '#9b59b6')
        
        functions_layout.addWidget(row1_frame)
        
        # Seconda riga di pulsanti
        row2_frame = QWidget()
        row2_layout = QHBoxLayout(row2_frame)
        row2_layout.setSpacing(5)
        row2_layout.setContentsMargins(0, 0, 0, 0)
        
        self.ui_components.create_button(row2_frame, "Aggiungi Watermark", 
                                        self.add_watermark, '#1abc9c')
        self.ui_components.create_button(row2_frame, "Estrai Testo", 
                                        self.extract_text, '#34495e')
        self.ui_components.create_button(row2_frame, "Converti Immagini", 
                                        self.convert_images, '#e67e22')
        self.ui_components.create_button(row2_frame, "Anteprima PDF", 
                                        self.preview_pdf, '#27ae60')
        
        functions_layout.addWidget(row2_frame)
        content_layout.addWidget(functions_group)
        
        # Frame per l'output
        output_group = QGroupBox("Output")
        output_group.setFont(QFont('Arial', 12, QFont.Bold))
        output_layout = QVBoxLayout(output_group)
        output_layout.setContentsMargins(10, 20, 10, 10)
        
        # Text widget per mostrare i risultati
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont('Consolas', 10))
        self.output_text.setMinimumHeight(150)
        output_layout.addWidget(self.output_text)
        
        # Pulsante per pulire l'output
        clear_btn = QPushButton("Pulisci Output")
        clear_btn.clicked.connect(self.clear_output)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-family: Arial;
                font-size: 10pt;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        output_layout.addWidget(clear_btn)
        
        content_layout.addWidget(output_group)
        
        main_layout.addWidget(content_widget)
        
    def log_message(self, message):
        """Aggiunge un messaggio al text widget di output"""
        self.output_text.append(message)
        # Scrolla alla fine
        scrollbar = self.output_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        QApplication.processEvents()
        
    def clear_output(self):
        """Pulisce l'area di output"""
        self.output_text.clear()
        
    def merge_pdfs(self):
        """Unisce più file PDF in uno solo"""
        try:
            files, _ = QFileDialog.getOpenFileNames(
                self,
                "Seleziona i PDF da unire",
                "",
                "PDF files (*.pdf)"
            )
            
            if len(files) < 2:
                QMessageBox.warning(self, "Attenzione", "Seleziona almeno 2 file PDF")
                return
                
            output_file, _ = QFileDialog.getSaveFileName(
                self,
                "Salva PDF unito come",
                "",
                "PDF files (*.pdf)"
            )
            
            if not output_file:
                return
                
            self.log_message("Inizio unione PDF...")
            result = self.pdf_manager.merge_pdfs(files, output_file)
            
            if result:
                self.log_message(f"✓ PDF uniti con successo in: {output_file}")
                QMessageBox.information(self, "Successo", "PDF uniti correttamente!")
            else:
                self.log_message("✗ Errore durante l'unione dei PDF")
                
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            QMessageBox.critical(self, "Errore", f"Errore durante l'unione: {str(e)}")
            
    def split_pdf(self):
        """Divide un PDF in pagine singole o intervalli"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Seleziona il PDF da dividere",
                "",
                "PDF files (*.pdf)"
            )
            
            if not file_path:
                return
                
            # Chiede il tipo di divisione
            reply = QMessageBox.question(
                self,
                "Tipo di divisione",
                "Vuoi dividere in pagine singole?\n\nSì = Pagine singole\nNo = Intervallo",
                QMessageBox.Yes | QMessageBox.No
            )
            
            output_dir = QFileDialog.getExistingDirectory(
                self,
                "Seleziona cartella di output"
            )
            
            if not output_dir:
                return
                
            self.log_message("Inizio divisione PDF...")
            
            if reply == QMessageBox.Yes:  # Pagine singole
                result = self.pdf_manager.split_pdf_pages(file_path, output_dir)
            else:  # Intervallo
                start_page, ok1 = QInputDialog.getInt(
                    self,
                    "Pagina iniziale",
                    "Inserisci numero pagina iniziale:",
                    1, 1, 10000
                )
                if not ok1:
                    return
                    
                end_page, ok2 = QInputDialog.getInt(
                    self,
                    "Pagina finale",
                    "Inserisci numero pagina finale:",
                    start_page, start_page, 10000
                )
                if not ok2:
                    return
                    
                result = self.pdf_manager.split_pdf_range(file_path, output_dir, start_page, end_page)
            
            if result:
                self.log_message(f"✓ PDF diviso con successo in: {output_dir}")
                QMessageBox.information(self, "Successo", "PDF diviso correttamente!")
            else:
                self.log_message("✗ Errore durante la divisione del PDF")
                
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            QMessageBox.critical(self, "Errore", f"Errore durante la divisione: {str(e)}")
            
    def rotate_pdf(self):
        """Ruota le pagine di un PDF"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Seleziona il PDF da ruotare",
                "",
                "PDF files (*.pdf)"
            )
            
            if not file_path:
                return
                
            # Finestra di dialogo per la selezione dell'angolo
            dialog = QDialog(self)
            dialog.setWindowTitle("Rotazione PDF")
            dialog.setFixedSize(300, 200)
            
            layout = QVBoxLayout(dialog)
            
            label = QLabel("Seleziona angolo di rotazione:")
            label.setFont(QFont('Arial', 12))
            layout.addWidget(label)
            
            button_group = QButtonGroup(dialog)
            rotation_value = [90]  # Default value
            
            for angle in [90, 180, 270]:
                radio = QRadioButton(f"{angle}°")
                radio.setFont(QFont('Arial', 10))
                if angle == 90:
                    radio.setChecked(True)
                radio.toggled.connect(lambda checked, a=angle: rotation_value.__setitem__(0, a) if checked else None)
                button_group.addButton(radio)
                layout.addWidget(radio)
            
            apply_btn = QPushButton("Applica Rotazione")
            apply_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 15px;
                    font-family: Arial;
                    font-size: 10pt;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            apply_btn.clicked.connect(dialog.accept)
            layout.addWidget(apply_btn)
            
            if dialog.exec() == QDialog.Accepted:
                output_file, _ = QFileDialog.getSaveFileName(
                    self,
                    "Salva PDF ruotato come",
                    "",
                    "PDF files (*.pdf)"
                )
                
                if not output_file:
                    return
                    
                self.log_message("Inizio rotazione PDF...")
                result = self.pdf_manager.rotate_pdf(file_path, output_file, rotation_value[0])
                
                if result:
                    self.log_message(f"✓ PDF ruotato con successo: {output_file}")
                    QMessageBox.information(self, "Successo", "PDF ruotato correttamente!")
                else:
                    self.log_message("✗ Errore durante la rotazione del PDF")
            
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            QMessageBox.critical(self, "Errore", f"Errore durante la rotazione: {str(e)}")
            
    def extract_pages(self):
        """Estrae pagine specifiche da un PDF"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Seleziona il PDF per l'estrazione",
                "",
                "PDF files (*.pdf)"
            )
            
            if not file_path:
                return
                
            pages_str, ok = QInputDialog.getText(
                self,
                "Pagine da estrarre",
                "Inserisci i numeri delle pagine (es: 1,3,5-8):"
            )
            
            if not ok or not pages_str:
                return
                
            output_file, _ = QFileDialog.getSaveFileName(
                self,
                "Salva pagine estratte come",
                "",
                "PDF files (*.pdf)"
            )
            
            if not output_file:
                return
                
            self.log_message("Inizio estrazione pagine...")
            result = self.pdf_manager.extract_pages(file_path, output_file, pages_str)
            
            if result:
                self.log_message(f"✓ Pagine estratte con successo: {output_file}")
                QMessageBox.information(self, "Successo", "Pagine estratte correttamente!")
            else:
                self.log_message("✗ Errore durante l'estrazione delle pagine")
                
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            QMessageBox.critical(self, "Errore", f"Errore durante l'estrazione: {str(e)}")
            
    def add_watermark(self):
        """Aggiunge un watermark al PDF"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Seleziona il PDF per il watermark",
                "",
                "PDF files (*.pdf)"
            )
            
            if not file_path:
                return
                
            watermark_text, ok = QInputDialog.getText(
                self,
                "Testo watermark",
                "Inserisci il testo del watermark:"
            )
            
            if not ok or not watermark_text:
                return
                
            output_file, _ = QFileDialog.getSaveFileName(
                self,
                "Salva PDF con watermark come",
                "",
                "PDF files (*.pdf)"
            )
            
            if not output_file:
                return
                
            self.log_message("Aggiunta watermark in corso...")
            result = self.pdf_manager.add_watermark(file_path, output_file, watermark_text)
            
            if result:
                self.log_message(f"✓ Watermark aggiunto con successo: {output_file}")
                QMessageBox.information(self, "Successo", "Watermark aggiunto correttamente!")
            else:
                self.log_message("✗ Errore durante l'aggiunta del watermark")
                
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            QMessageBox.critical(self, "Errore", f"Errore durante l'aggiunta del watermark: {str(e)}")
            
    def extract_text(self):
        """Estrae il testo da un PDF"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Seleziona il PDF per l'estrazione del testo",
                "",
                "PDF files (*.pdf)"
            )
            
            if not file_path:
                return
                
            output_file, _ = QFileDialog.getSaveFileName(
                self,
                "Salva testo come",
                "",
                "Text files (*.txt)"
            )
            
            if not output_file:
                return
                
            self.log_message("Estrazione testo in corso...")
            result = self.pdf_manager.extract_text(file_path, output_file)
            
            if result:
                self.log_message(f"✓ Testo estratto con successo: {output_file}")
                QMessageBox.information(self, "Successo", "Testo estratto correttamente!")
            else:
                self.log_message("✗ Errore durante l'estrazione del testo")
                
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            QMessageBox.critical(self, "Errore", f"Errore durante l'estrazione del testo: {str(e)}")
            
    def convert_images(self):
        """Converte immagini in PDF"""
        try:
            files, _ = QFileDialog.getOpenFileNames(
                self,
                "Seleziona le immagini da convertire",
                "",
                "Image files (*.jpg *.jpeg *.png *.bmp *.gif *.tiff)"
            )
            
            if not files:
                return
                
            output_file, _ = QFileDialog.getSaveFileName(
                self,
                "Salva PDF come",
                "",
                "PDF files (*.pdf)"
            )
            
            if not output_file:
                return
                
            self.log_message("Conversione immagini in corso...")
            result = self.pdf_manager.convert_images_to_pdf(files, output_file)
            
            if result:
                self.log_message(f"✓ Immagini convertite con successo: {output_file}")
                QMessageBox.information(self, "Successo", "Immagini convertite correttamente!")
            else:
                self.log_message("✗ Errore durante la conversione delle immagini")
                
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            QMessageBox.critical(self, "Errore", f"Errore durante la conversione: {str(e)}")
            
    def preview_pdf(self):
        """Mostra un'anteprima del PDF"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Seleziona il PDF per l'anteprima",
                "",
                "PDF files (*.pdf)"
            )
            
            if not file_path:
                return
                
            self.log_message("Apertura anteprima PDF...")
            result = self.pdf_manager.preview_pdf(file_path)
            
            if result:
                self.log_message(f"✓ Anteprima aperta per: {os.path.basename(file_path)}")
            else:
                self.log_message("✗ Errore durante l'apertura dell'anteprima")
                
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            QMessageBox.critical(self, "Errore", f"Errore durante l'anteprima: {str(e)}")

def main():
    app = QApplication(sys.argv)
    
    # Imposta lo stile Fusion per un look moderno
    app.setStyle('Fusion')
    
    window = PDFEditor()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
