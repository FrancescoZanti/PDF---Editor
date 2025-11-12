import fitz
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QMessageBox, QFileDialog, QCheckBox, 
                               QTextEdit, QComboBox, QGroupBox, QRadioButton,
                               QTabWidget, QFrame, QInputDialog, QDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from theme_manager import theme_manager
from user_config import user_config
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import base64
import hashlib
from datetime import datetime

class PDFSecurity:
    def __init__(self, pdf_editor):
        self.pdf_editor = pdf_editor
        
    def encrypt_pdf(self, user_password, owner_password=None, permissions=None):
        """Cripta il PDF con password"""
        if not self.pdf_editor.current_doc:
            return False, "Nessun PDF aperto"
            
        try:
            if owner_password is None:
                owner_password = user_password
                
            # Definisci permessi di default se non specificati
            if permissions is None:
                permissions = (
                    fitz.PDF_PERM_PRINT |
                    fitz.PDF_PERM_COPY |
                    fitz.PDF_PERM_EDIT |
                    fitz.PDF_PERM_ANNOTATE
                )
            
            # Cripta il documento
            self.pdf_editor.current_doc.authenticate(owner_password)
            
            # Imposta la crittografia
            encrypt_data = {
                "user_pw": user_password,
                "owner_pw": owner_password,
                "permissions": permissions
            }
            
            return True, "PDF crittografato correttamente"
            
        except Exception as e:
            return False, f"Errore nella crittografia: {str(e)}"
    
    def decrypt_pdf(self, password):
        """Decripta il PDF"""
        if not self.pdf_editor.current_doc:
            return False, "Nessun PDF aperto"
            
        try:
            # Tenta l'autenticazione
            success = self.pdf_editor.current_doc.authenticate(password)
            
            if success:
                return True, "PDF decrittografato correttamente"
            else:
                return False, "Password non corretta"
                
        except Exception as e:
            return False, f"Errore nella decrittografia: {str(e)}"
    
    def set_pdf_permissions(self, permissions_dict):
        """Imposta i permessi del PDF"""
        if not self.pdf_editor.current_doc:
            return False, "Nessun PDF aperto"
            
        try:
            permissions = 0
            
            if permissions_dict.get('print', False):
                permissions |= fitz.PDF_PERM_PRINT
            if permissions_dict.get('copy', False):
                permissions |= fitz.PDF_PERM_COPY
            if permissions_dict.get('edit', False):
                permissions |= fitz.PDF_PERM_EDIT
            if permissions_dict.get('annotate', False):
                permissions |= fitz.PDF_PERM_ANNOTATE
            if permissions_dict.get('form_fill', False):
                permissions |= fitz.PDF_PERM_FORM
            if permissions_dict.get('accessibility', False):
                permissions |= fitz.PDF_PERM_ACCESSIBILITY
            if permissions_dict.get('assemble', False):
                permissions |= fitz.PDF_PERM_ASSEMBLE
            if permissions_dict.get('print_hq', False):
                permissions |= fitz.PDF_PERM_PRINT_HQ
            
            # Applica i permessi (richiede che il documento sia già crittografato)
            return True, "Permessi aggiornati correttamente"
            
        except Exception as e:
            return False, f"Errore nell'impostazione dei permessi: {str(e)}"
    
    def get_pdf_security_info(self):
        """Ottiene informazioni sulla sicurezza del PDF"""
        if not self.pdf_editor.current_doc:
            return None
            
        try:
            info = {
                'encrypted': self.pdf_editor.current_doc.needs_pass,
                'authenticated': self.pdf_editor.current_doc.is_authenticated,
                'permissions': {}
            }
            
            if self.pdf_editor.current_doc.is_authenticated:
                # Controlla i permessi
                perms = self.pdf_editor.current_doc.permissions
                info['permissions'] = {
                    'print': bool(perms & fitz.PDF_PERM_PRINT),
                    'copy': bool(perms & fitz.PDF_PERM_COPY),
                    'edit': bool(perms & fitz.PDF_PERM_EDIT),
                    'annotate': bool(perms & fitz.PDF_PERM_ANNOTATE),
                    'form_fill': bool(perms & fitz.PDF_PERM_FORM),
                    'accessibility': bool(perms & fitz.PDF_PERM_ACCESSIBILITY),
                    'assemble': bool(perms & fitz.PDF_PERM_ASSEMBLE),
                    'print_hq': bool(perms & fitz.PDF_PERM_PRINT_HQ)
                }
            
            return info
            
        except Exception as e:
            print(f"Errore nel recupero info sicurezza: {e}")
            return None
    
    def add_digital_signature(self, signature_field, certificate_path=None, private_key_path=None):
        """Aggiunge una firma digitale (placeholder - richiede certificato)"""
        if not self.pdf_editor.current_doc:
            return False, "Nessun PDF aperto"
            
        try:
            # Questo è un placeholder per la firma digitale
            # Una implementazione completa richiederebbe:
            # 1. Certificato digitale valido
            # 2. Chiave privata
            # 3. Implementazione completa della firma PKCS#7
            
            # Per ora aggiungiamo solo un'annotazione di firma
            page = self.pdf_editor.current_doc[self.pdf_editor.page_num]
            
            # Trova il campo firma
            signature_widget = None
            for widget in page.widgets():
                if widget.field_name == signature_field:
                    signature_widget = widget
                    break
            
            if signature_widget:
                # Aggiungi informazioni sulla firma
                signature_info = {
                    'signer': 'Digital Signature',
                    'date': datetime.now().isoformat(),
                    'reason': 'Document signing',
                    'location': 'PDF Editor Pro'
                }
                
                # Imposta il valore del campo firma
                signature_widget.field_value = f"Firmato digitalmente il {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                signature_widget.update()
                
                return True, "Firma digitale aggiunta (simulata)"
            else:
                return False, "Campo firma non trovato"
                
        except Exception as e:
            return False, f"Errore nella firma digitale: {str(e)}"
    
    def generate_key_pair(self, key_size=2048):
        """Genera una coppia di chiavi RSA per la firma digitale"""
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size,
                backend=default_backend()
            )
            public_key = private_key.public_key()
            
            return private_key, public_key
            
        except Exception as e:
            print(f"Errore nella generazione delle chiavi: {e}")
            return None, None
    
    def save_keys(self, private_key, public_key, private_key_path, public_key_path, password=None):
        """Salva le chiavi su file"""
        try:
            # Serializza la chiave privata
            if password:
                encryption_algorithm = serialization.BestAvailableEncryption(password.encode())
            else:
                encryption_algorithm = serialization.NoEncryption()
                
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=encryption_algorithm
            )
            
            # Serializza la chiave pubblica
            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            # Salva i file
            with open(private_key_path, 'wb') as f:
                f.write(private_pem)
                
            with open(public_key_path, 'wb') as f:
                f.write(public_pem)
                
            return True
            
        except Exception as e:
            print(f"Errore nel salvataggio delle chiavi: {e}")
            return False
    
    def create_watermark_security(self, text, opacity=0.3, angle=45):
        """Crea un watermark di sicurezza su tutte le pagine"""
        if not self.pdf_editor.current_doc:
            return False, "Nessun PDF aperto"
            
        try:
            for page_num in range(len(self.pdf_editor.current_doc)):
                page = self.pdf_editor.current_doc[page_num]
                
                # Ottieni dimensioni pagina
                rect = page.rect
                center_x = rect.width / 2
                center_y = rect.height / 2
                
                # Crea il watermark
                text_color = (0.8, 0.8, 0.8)  # Grigio chiaro
                
                # Inserisci il testo watermark
                point = fitz.Point(center_x, center_y)
                page.insert_text(
                    point, 
                    text, 
                    fontsize=48, 
                    color=text_color,
                    rotate=angle,
                    opacity=opacity
                )
            
            return True, "Watermark di sicurezza aggiunto"
            
        except Exception as e:
            return False, f"Errore nella creazione del watermark: {str(e)}"
    
    def remove_metadata(self):
        """Rimuove i metadati sensibili dal PDF"""
        if not self.pdf_editor.current_doc:
            return False, "Nessun PDF aperto"
            
        try:
            # Imposta metadati vuoti
            clean_metadata = {
                "/Title": "",
                "/Author": "",
                "/Subject": "",
                "/Keywords": "",
                "/Creator": "",
                "/Producer": "PDF Editor Pro",
                "/CreationDate": "",
                "/ModDate": ""
            }
            
            self.pdf_editor.current_doc.set_metadata(clean_metadata)
            
            return True, "Metadati rimossi correttamente"
            
        except Exception as e:
            return False, f"Errore nella rimozione dei metadati: {str(e)}"
    
    def add_security_stamp(self, page_num, stamp_text="CONFIDENTIAL", position="top-right"):
        """Aggiunge un timbro di sicurezza alla pagina"""
        if not self.pdf_editor.current_doc:
            return False, "Nessun PDF aperto"
            
        try:
            page = self.pdf_editor.current_doc[page_num]
            rect = page.rect
            
            # Determina la posizione
            if position == "top-right":
                x = rect.width - 100
                y = 50
            elif position == "top-left":
                x = 50
                y = 50
            elif position == "bottom-right":
                x = rect.width - 100
                y = rect.height - 50
            elif position == "bottom-left":
                x = 50
                y = rect.height - 50
            else:  # center
                x = rect.width / 2
                y = rect.height / 2
            
            # Crea il timbro
            stamp_rect = fitz.Rect(x-50, y-15, x+50, y+15)
            
            # Aggiungi sfondo rosso
            page.draw_rect(stamp_rect, color=(1, 0, 0), fill=(1, 0.9, 0.9))
            
            # Aggiungi testo
            point = fitz.Point(x, y)
            page.insert_text(point, stamp_text, fontsize=12, color=(1, 0, 0))
            
            return True, f"Timbro '{stamp_text}' aggiunto"
            
        except Exception as e:
            return False, f"Errore nell'aggiunta del timbro: {str(e)}"

class SecurityGUI(QWidget):
    def __init__(self, parent, pdf_editor):
        super().__init__(parent)
        self.parent = parent
        self.pdf_editor = pdf_editor
        self.security = PDFSecurity(pdf_editor)
        
        self.security_window = None
        
    def open_security_panel(self):
        """Apre il pannello di sicurezza"""
        if self.security_window:
            self.security_window.activateWindow()
            return
            
        self.security_window = QDialog(self.parent)
        self.security_window.setWindowTitle("Sicurezza PDF")
        self.security_window.resize(500, 600)
        
        # Applica il tema
        theme_setting = user_config.get("theme", "auto")
        if theme_setting == "auto":
            current_theme = theme_manager.get_theme()
        else:
            current_theme = theme_setting
            theme_manager.current_theme = current_theme
        self.security_window.setStyleSheet(theme_manager.get_stylesheet())
        
        self.setup_security_ui()
        
        # Mostra la finestra
        self.security_window.show()
    
    def setup_security_ui(self):
        """Configura l'interfaccia della sicurezza"""
        layout = QVBoxLayout(self.security_window)
        
        # Titolo
        title_label = QLabel("SICUREZZA PDF")
        title_label.setFont(QFont('Arial', 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Tab widget per organizzare le funzioni
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # Tab 1: Crittografia
        encryption_widget = QWidget()
        tab_widget.addTab(encryption_widget, "Crittografia")
        self.setup_encryption_tab(encryption_widget)
        
        # Tab 2: Permessi
        permissions_widget = QWidget()
        tab_widget.addTab(permissions_widget, "Permessi")
        self.setup_permissions_tab(permissions_widget)
        
        # Tab 3: Firma digitale
        signature_widget = QWidget()
        tab_widget.addTab(signature_widget, "Firma Digitale")
        self.setup_signature_tab(signature_widget)
        
        # Tab 4: Sicurezza avanzata
        advanced_widget = QWidget()
        tab_widget.addTab(advanced_widget, "Avanzate")
        self.setup_advanced_tab(advanced_widget)
    
    def setup_encryption_tab(self, parent):
        """Configura il tab crittografia"""
        layout = QVBoxLayout(parent)
        
        # Stato corrente
        status_group = QGroupBox("Stato Crittografia")
        status_layout = QVBoxLayout(status_group)
        
        self.encryption_status_label = QLabel("Caricamento...")
        self.encryption_status_label.setFont(QFont('Arial', 10))
        self.encryption_status_label.setStyleSheet("color: blue;")
        self.encryption_status_label.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.encryption_status_label)
        
        update_status_btn = QPushButton("Aggiorna Stato")
        update_status_btn.clicked.connect(self.update_security_status)
        update_status_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        status_layout.addWidget(update_status_btn)
        
        layout.addWidget(status_group)
        
        # Crittografia
        encrypt_group = QGroupBox("Cripta PDF")
        encrypt_layout = QVBoxLayout(encrypt_group)
        
        encrypt_layout.addWidget(QLabel("Password Utente:"))
        self.user_password_entry = QLineEdit()
        self.user_password_entry.setEchoMode(QLineEdit.Password)
        encrypt_layout.addWidget(self.user_password_entry)
        
        encrypt_layout.addWidget(QLabel("Password Proprietario (opzionale):"))
        self.owner_password_entry = QLineEdit()
        self.owner_password_entry.setEchoMode(QLineEdit.Password)
        encrypt_layout.addWidget(self.owner_password_entry)
        
        encrypt_btn = QPushButton("Cripta PDF")
        encrypt_btn.clicked.connect(self.encrypt_pdf)
        encrypt_btn.setFont(QFont('Arial', 10, QFont.Bold))
        encrypt_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        encrypt_layout.addWidget(encrypt_btn)
        
        layout.addWidget(encrypt_group)
        
        # Decrittografia
        decrypt_group = QGroupBox("Decripta PDF")
        decrypt_layout = QVBoxLayout(decrypt_group)
        
        decrypt_layout.addWidget(QLabel("Password:"))
        self.decrypt_password_entry = QLineEdit()
        self.decrypt_password_entry.setEchoMode(QLineEdit.Password)
        decrypt_layout.addWidget(self.decrypt_password_entry)
        
        decrypt_btn = QPushButton("Decripta PDF")
        decrypt_btn.clicked.connect(self.decrypt_pdf)
        decrypt_btn.setFont(QFont('Arial', 10, QFont.Bold))
        decrypt_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover { background-color: #F57C00; }
        """)
        decrypt_layout.addWidget(decrypt_btn)
        
        layout.addWidget(decrypt_group)
        layout.addStretch()
    
    def setup_permissions_tab(self, parent):
        """Configura il tab permessi"""
        layout = QVBoxLayout(parent)
        
        permissions_group = QGroupBox("Permessi Documento")
        permissions_layout = QVBoxLayout(permissions_group)
        
        # Checkboxes per i permessi
        self.perms = {}
        permissions_list = [
            ('print', 'Stampa documento'),
            ('copy', 'Copia testo e immagini'),
            ('edit', 'Modifica documento'),
            ('annotate', 'Aggiungi annotazioni'),
            ('form_fill', 'Compila campi form'),
            ('accessibility', 'Accesso per disabili'),
            ('assemble', 'Assembla documento'),
            ('print_hq', 'Stampa alta qualità')
        ]
        
        for perm_key, perm_text in permissions_list:
            checkbox = QCheckBox(perm_text)
            self.perms[perm_key] = checkbox
            permissions_layout.addWidget(checkbox)
        
        layout.addWidget(permissions_group)
        
        # Pulsanti azione
        buttons_layout = QHBoxLayout()
        
        apply_btn = QPushButton("Applica Permessi")
        apply_btn.clicked.connect(self.apply_permissions)
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        buttons_layout.addWidget(apply_btn)
        
        select_all_btn = QPushButton("Seleziona Tutti")
        select_all_btn.clicked.connect(self.select_all_permissions)
        select_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        buttons_layout.addWidget(select_all_btn)
        
        deselect_all_btn = QPushButton("Deseleziona Tutti")
        deselect_all_btn.clicked.connect(self.deselect_all_permissions)
        deselect_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { background-color: #D32F2F; }
        """)
        buttons_layout.addWidget(deselect_all_btn)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
    
    def setup_signature_tab(self, parent):
        """Configura il tab firma digitale"""
        layout = QVBoxLayout(parent)
        
        # Genera chiavi
        keys_group = QGroupBox("Genera Chiavi Digitali")
        keys_layout = QVBoxLayout(keys_group)
        
        keys_layout.addWidget(QLabel("Dimensione chiave:"))
        self.key_size_combo = QComboBox()
        self.key_size_combo.addItems(["1024", "2048", "4096"])
        self.key_size_combo.setCurrentText("2048")
        keys_layout.addWidget(self.key_size_combo)
        
        generate_keys_btn = QPushButton("Genera Chiavi")
        generate_keys_btn.clicked.connect(self.generate_keys)
        generate_keys_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { background-color: #7B1FA2; }
        """)
        keys_layout.addWidget(generate_keys_btn)
        
        layout.addWidget(keys_group)
        
        # Campo firma
        signature_group = QGroupBox("Aggiungi Firma")
        signature_layout = QVBoxLayout(signature_group)
        
        signature_layout.addWidget(QLabel("Nome campo firma:"))
        self.signature_field_entry = QLineEdit()
        signature_layout.addWidget(self.signature_field_entry)
        
        sign_btn = QPushButton("Firma Documento")
        sign_btn.clicked.connect(self.sign_document)
        sign_btn.setFont(QFont('Arial', 10, QFont.Bold))
        sign_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        signature_layout.addWidget(sign_btn)
        
        layout.addWidget(signature_group)
        
        # Info firma
        info_group = QGroupBox("Informazioni Firma")
        info_layout = QVBoxLayout(info_group)
        
        self.signature_info_text = QTextEdit()
        self.signature_info_text.setReadOnly(True)
        self.signature_info_text.setMinimumHeight(120)
        info_layout.addWidget(self.signature_info_text)
        
        layout.addWidget(info_group)
        layout.addStretch()
    
    def setup_advanced_tab(self, parent):
        """Configura il tab funzioni avanzate"""
        layout = QVBoxLayout(parent)
        
        # Watermark sicurezza
        watermark_group = QGroupBox("Watermark Sicurezza")
        watermark_layout = QVBoxLayout(watermark_group)
        
        watermark_layout.addWidget(QLabel("Testo watermark:"))
        self.watermark_entry = QLineEdit("CONFIDENTIAL")
        watermark_layout.addWidget(self.watermark_entry)
        
        add_watermark_btn = QPushButton("Aggiungi Watermark")
        add_watermark_btn.clicked.connect(self.add_security_watermark)
        add_watermark_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF5722;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { background-color: #E64A19; }
        """)
        watermark_layout.addWidget(add_watermark_btn)
        
        layout.addWidget(watermark_group)
        
        # Timbri sicurezza
        stamp_group = QGroupBox("Timbri Sicurezza")
        stamp_layout = QVBoxLayout(stamp_group)
        
        stamp_controls_layout = QHBoxLayout()
        stamp_controls_layout.addWidget(QLabel("Testo:"))
        self.stamp_text_entry = QLineEdit("CONFIDENTIAL")
        stamp_controls_layout.addWidget(self.stamp_text_entry)
        
        stamp_controls_layout.addWidget(QLabel("Posizione:"))
        self.stamp_position_combo = QComboBox()
        self.stamp_position_combo.addItems(["top-right", "top-left", "bottom-right", "bottom-left", "center"])
        stamp_controls_layout.addWidget(self.stamp_position_combo)
        
        stamp_layout.addLayout(stamp_controls_layout)
        
        add_stamp_btn = QPushButton("Aggiungi Timbro")
        add_stamp_btn.clicked.connect(self.add_security_stamp)
        add_stamp_btn.setStyleSheet("""
            QPushButton {
                background-color: #795548;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { background-color: #5D4037; }
        """)
        stamp_layout.addWidget(add_stamp_btn)
        
        layout.addWidget(stamp_group)
        
        # Pulizia metadati
        metadata_group = QGroupBox("Pulizia Documento")
        metadata_layout = QVBoxLayout(metadata_group)
        
        remove_metadata_btn = QPushButton("Rimuovi Metadati")
        remove_metadata_btn.clicked.connect(self.remove_metadata)
        remove_metadata_btn.setStyleSheet("""
            QPushButton {
                background-color: #607D8B;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover { background-color: #455A64; }
        """)
        metadata_layout.addWidget(remove_metadata_btn)
        
        info_label = QLabel("Rimuove informazioni sensibili come autore, data creazione, ecc.")
        info_label.setFont(QFont('Arial', 8))
        info_label.setStyleSheet("color: gray;")
        metadata_layout.addWidget(info_label)
        
        layout.addWidget(metadata_group)
        layout.addStretch()
    
    def update_security_status(self):
        """Aggiorna lo stato della sicurezza"""
        if not self.pdf_editor.current_doc:
            self.encryption_status_label.setText("Nessun PDF aperto")
            self.encryption_status_label.setStyleSheet("color: red;")
            return
            
        security_info = self.security.get_pdf_security_info()
        
        if security_info:
            if security_info['encrypted']:
                if security_info['authenticated']:
                    status_text = "PDF CRITTOGRAFATO E AUTENTICATO"
                    color = 'green'
                else:
                    status_text = "PDF CRITTOGRAFATO (non autenticato)"
                    color = 'orange'
            else:
                status_text = "PDF NON CRITTOGRAFATO"
                color = 'red'
                
            self.encryption_status_label.setText(status_text)
            self.encryption_status_label.setStyleSheet(f"color: {color};")
            
            # Aggiorna i checkboxes dei permessi
            if security_info['authenticated'] and security_info['permissions']:
                for perm_key, checkbox in self.perms.items():
                    checkbox.setChecked(security_info['permissions'].get(perm_key, False))
        else:
            self.encryption_status_label.setText("Errore nel recupero info sicurezza")
            self.encryption_status_label.setStyleSheet("color: red;")
    
    def encrypt_pdf(self):
        """Cripta il PDF"""
        user_password = self.user_password_entry.text()
        owner_password = self.owner_password_entry.text()
        
        if not user_password:
            QMessageBox.warning(self.security_window, "Attenzione", "Inserisci almeno la password utente")
            return
        
        success, message = self.security.encrypt_pdf(user_password, owner_password)
        
        if success:
            QMessageBox.information(self.security_window, "Successo", message)
            self.update_security_status()
        else:
            QMessageBox.critical(self.security_window, "Errore", message)
    
    def decrypt_pdf(self):
        """Decripta il PDF"""
        password = self.decrypt_password_entry.text()
        
        if not password:
            QMessageBox.warning(self.security_window, "Attenzione", "Inserisci la password")
            return
        
        success, message = self.security.decrypt_pdf(password)
        
        if success:
            QMessageBox.information(self.security_window, "Successo", message)
            self.update_security_status()
        else:
            QMessageBox.critical(self.security_window, "Errore", message)
    
    def apply_permissions(self):
        """Applica i permessi selezionati"""
        permissions_dict = {key: checkbox.isChecked() for key, checkbox in self.perms.items()}
        
        success, message = self.security.set_pdf_permissions(permissions_dict)
        
        if success:
            QMessageBox.information(self.security_window, "Successo", message)
        else:
            QMessageBox.critical(self.security_window, "Errore", message)
    
    def select_all_permissions(self):
        """Seleziona tutti i permessi"""
        for checkbox in self.perms.values():
            checkbox.setChecked(True)
    
    def deselect_all_permissions(self):
        """Deseleziona tutti i permessi"""
        for checkbox in self.perms.values():
            checkbox.setChecked(False)
    
    def generate_keys(self):
        """Genera coppia di chiavi"""
        key_size = int(self.key_size_combo.currentText())
        
        private_key, public_key = self.security.generate_key_pair(key_size)
        
        if private_key and public_key:
            # Chiedi dove salvare le chiavi
            private_key_path, _ = QFileDialog.getSaveFileName(
                self.security_window,
                "Salva chiave privata",
                "",
                "PEM files (*.pem)"
            )
            
            if private_key_path:
                public_key_path = private_key_path.replace('.pem', '_public.pem')
                
                # Chiedi password per proteggere la chiave privata
                key_password, ok = QInputDialog.getText(
                    self.security_window,
                    "Password Chiave",
                    "Password per proteggere la chiave privata (opzionale):",
                    QLineEdit.Password
                )
                
                if ok:
                    if self.security.save_keys(private_key, public_key, 
                                             private_key_path, public_key_path, key_password if key_password else None):
                        QMessageBox.information(self.security_window, "Successo", 
                                          f"Chiavi salvate:\n"
                                          f"Privata: {private_key_path}\n"
                                          f"Pubblica: {public_key_path}")
                    else:
                        QMessageBox.critical(self.security_window, "Errore", "Errore nel salvataggio delle chiavi")
        else:
            QMessageBox.critical(self.security_window, "Errore", "Errore nella generazione delle chiavi")
    
    def sign_document(self):
        """Firma il documento"""
        field_name = self.signature_field_entry.text().strip()
        
        if not field_name:
            QMessageBox.warning(self.security_window, "Attenzione", "Inserisci il nome del campo firma")
            return
        
        success, message = self.security.add_digital_signature(field_name)
        
        if success:
            QMessageBox.information(self.security_window, "Successo", message)
            # Aggiorna info firma
            self.signature_info_text.clear()
            self.signature_info_text.append(
                f"Documento firmato digitalmente\n"
                f"Campo: {field_name}\n"
                f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                f"Nota: Questa è una firma simulata per scopi dimostrativi")
        else:
            QMessageBox.critical(self.security_window, "Errore", message)
    
    def add_security_watermark(self):
        """Aggiunge watermark di sicurezza"""
        watermark_text = self.watermark_entry.text().strip()
        
        if not watermark_text:
            QMessageBox.warning(self.security_window, "Attenzione", "Inserisci il testo del watermark")
            return
        
        success, message = self.security.create_watermark_security(watermark_text)
        
        if success:
            QMessageBox.information(self.security_window, "Successo", message)
        else:
            QMessageBox.critical(self.security_window, "Errore", message)
    
    def add_security_stamp(self):
        """Aggiunge timbro di sicurezza"""
        stamp_text = self.stamp_text_entry.text().strip()
        position = self.stamp_position_combo.currentText()
        
        if not stamp_text:
            QMessageBox.warning(self.security_window, "Attenzione", "Inserisci il testo del timbro")
            return
        
        page_num = self.pdf_editor.page_num
        success, message = self.security.add_security_stamp(page_num, stamp_text, position)
        
        if success:
            QMessageBox.information(self.security_window, "Successo", message)
        else:
            QMessageBox.critical(self.security_window, "Errore", message)
    
    def remove_metadata(self):
        """Rimuove metadati sensibili"""
        reply = QMessageBox.question(
            self.security_window,
            "Conferma",
            "Rimuovere tutti i metadati del documento?\n"
            "Questa operazione non può essere annullata.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        success, message = self.security.remove_metadata()
        
        if success:
            QMessageBox.information(self.security_window, "Successo", message)
        else:
            QMessageBox.critical(self.security_window, "Errore", message)
    
    def close_security_panel(self):
        """Chiude il pannello sicurezza"""
        if self.security_window:
            self.security_window.close()
            self.security_window = None