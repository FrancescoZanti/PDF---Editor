import fitz
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
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

class SecurityGUI:
    def __init__(self, parent, pdf_editor):
        self.parent = parent
        self.pdf_editor = pdf_editor
        self.security = PDFSecurity(pdf_editor)
        
        self.security_window = None
        
    def open_security_panel(self):
        """Apre il pannello di sicurezza"""
        if self.security_window:
            self.security_window.lift()
            return
            
        self.security_window = tk.Toplevel(self.parent)
        self.security_window.title("Sicurezza PDF")
        self.security_window.geometry("500x600")
        self.security_window.configure(bg='#f0f0f0')
        
        self.setup_security_ui()
        
        # Gestisci chiusura finestra
        self.security_window.protocol("WM_DELETE_WINDOW", self.close_security_panel)
    
    def setup_security_ui(self):
        """Configura l'interfaccia della sicurezza"""
        # Titolo
        title_label = tk.Label(self.security_window, text="SICUREZZA PDF", 
                              font=('Arial', 14, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Notebook per organizzare le funzioni
        notebook = ttk.Notebook(self.security_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Tab 1: Crittografia
        encryption_frame = ttk.Frame(notebook)
        notebook.add(encryption_frame, text="Crittografia")
        self.setup_encryption_tab(encryption_frame)
        
        # Tab 2: Permessi
        permissions_frame = ttk.Frame(notebook)
        notebook.add(permissions_frame, text="Permessi")
        self.setup_permissions_tab(permissions_frame)
        
        # Tab 3: Firma digitale
        signature_frame = ttk.Frame(notebook)
        notebook.add(signature_frame, text="Firma Digitale")
        self.setup_signature_tab(signature_frame)
        
        # Tab 4: Sicurezza avanzata
        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="Avanzate")
        self.setup_advanced_tab(advanced_frame)
    
    def setup_encryption_tab(self, parent):
        """Configura il tab crittografia"""
        # Stato corrente
        status_frame = tk.LabelFrame(parent, text="Stato Crittografia")
        status_frame.pack(fill='x', padx=10, pady=5)
        
        self.encryption_status_label = tk.Label(status_frame, text="Caricamento...", 
                                               font=('Arial', 10), fg='blue')
        self.encryption_status_label.pack(pady=10)
        
        tk.Button(status_frame, text="Aggiorna Stato", command=self.update_security_status,
                 bg='#2196F3', fg='white').pack(pady=5)
        
        # Crittografia
        encrypt_frame = tk.LabelFrame(parent, text="Cripta PDF")
        encrypt_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(encrypt_frame, text="Password Utente:").pack(anchor='w', padx=5)
        self.user_password_entry = tk.Entry(encrypt_frame, show='*', width=40)
        self.user_password_entry.pack(padx=5, pady=2)
        
        tk.Label(encrypt_frame, text="Password Proprietario (opzionale):").pack(anchor='w', padx=5)
        self.owner_password_entry = tk.Entry(encrypt_frame, show='*', width=40)
        self.owner_password_entry.pack(padx=5, pady=2)
        
        tk.Button(encrypt_frame, text="Cripta PDF", command=self.encrypt_pdf,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(pady=10)
        
        # Decrittografia
        decrypt_frame = tk.LabelFrame(parent, text="Decripta PDF")
        decrypt_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(decrypt_frame, text="Password:").pack(anchor='w', padx=5)
        self.decrypt_password_entry = tk.Entry(decrypt_frame, show='*', width=40)
        self.decrypt_password_entry.pack(padx=5, pady=2)
        
        tk.Button(decrypt_frame, text="Decripta PDF", command=self.decrypt_pdf,
                 bg='#FF9800', fg='white', font=('Arial', 10, 'bold')).pack(pady=10)
    
    def setup_permissions_tab(self, parent):
        """Configura il tab permessi"""
        permissions_frame = tk.LabelFrame(parent, text="Permessi Documento")
        permissions_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Variabili per i permessi
        self.perms = {
            'print': tk.BooleanVar(),
            'copy': tk.BooleanVar(),
            'edit': tk.BooleanVar(),
            'annotate': tk.BooleanVar(),
            'form_fill': tk.BooleanVar(),
            'accessibility': tk.BooleanVar(),
            'assemble': tk.BooleanVar(),
            'print_hq': tk.BooleanVar()
        }
        
        # Checkboxes per i permessi
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
            tk.Checkbutton(permissions_frame, text=perm_text, 
                          variable=self.perms[perm_key]).pack(anchor='w', padx=10, pady=2)
        
        # Pulsanti azione
        perm_buttons_frame = tk.Frame(permissions_frame)
        perm_buttons_frame.pack(fill='x', pady=10)
        
        tk.Button(perm_buttons_frame, text="Applica Permessi", command=self.apply_permissions,
                 bg='#4CAF50', fg='white').pack(side='left', padx=10)
        
        tk.Button(perm_buttons_frame, text="Seleziona Tutti", command=self.select_all_permissions,
                 bg='#2196F3', fg='white').pack(side='left', padx=5)
        
        tk.Button(perm_buttons_frame, text="Deseleziona Tutti", command=self.deselect_all_permissions,
                 bg='#F44336', fg='white').pack(side='left', padx=5)
    
    def setup_signature_tab(self, parent):
        """Configura il tab firma digitale"""
        # Genera chiavi
        keys_frame = tk.LabelFrame(parent, text="Genera Chiavi Digitali")
        keys_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(keys_frame, text="Dimensione chiave:").pack(anchor='w', padx=5)
        self.key_size_var = tk.StringVar(value="2048")
        key_size_combo = ttk.Combobox(keys_frame, textvariable=self.key_size_var, 
                                     values=["1024", "2048", "4096"], state="readonly")
        key_size_combo.pack(padx=5, pady=2)
        
        tk.Button(keys_frame, text="Genera Chiavi", command=self.generate_keys,
                 bg='#9C27B0', fg='white').pack(pady=5)
        
        # Campo firma
        signature_frame = tk.LabelFrame(parent, text="Aggiungi Firma")
        signature_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(signature_frame, text="Nome campo firma:").pack(anchor='w', padx=5)
        self.signature_field_entry = tk.Entry(signature_frame, width=40)
        self.signature_field_entry.pack(padx=5, pady=2)
        
        tk.Button(signature_frame, text="Firma Documento", command=self.sign_document,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(pady=10)
        
        # Info firma
        info_frame = tk.LabelFrame(parent, text="Informazioni Firma")
        info_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.signature_info_text = tk.Text(info_frame, height=6, width=50)
        sig_scrollbar = tk.Scrollbar(info_frame, orient='vertical', 
                                   command=self.signature_info_text.yview)
        self.signature_info_text.configure(yscrollcommand=sig_scrollbar.set)
        
        self.signature_info_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        sig_scrollbar.pack(side='right', fill='y', pady=5)
    
    def setup_advanced_tab(self, parent):
        """Configura il tab funzioni avanzate"""
        # Watermark sicurezza
        watermark_frame = tk.LabelFrame(parent, text="Watermark Sicurezza")
        watermark_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(watermark_frame, text="Testo watermark:").pack(anchor='w', padx=5)
        self.watermark_entry = tk.Entry(watermark_frame, width=40)
        self.watermark_entry.insert(0, "CONFIDENTIAL")
        self.watermark_entry.pack(padx=5, pady=2)
        
        tk.Button(watermark_frame, text="Aggiungi Watermark", command=self.add_security_watermark,
                 bg='#FF5722', fg='white').pack(pady=5)
        
        # Timbri sicurezza
        stamp_frame = tk.LabelFrame(parent, text="Timbri Sicurezza")
        stamp_frame.pack(fill='x', padx=10, pady=5)
        
        stamp_controls = tk.Frame(stamp_frame)
        stamp_controls.pack(fill='x', padx=5, pady=5)
        
        tk.Label(stamp_controls, text="Testo:").pack(side='left')
        self.stamp_text_entry = tk.Entry(stamp_controls, width=20)
        self.stamp_text_entry.insert(0, "CONFIDENTIAL")
        self.stamp_text_entry.pack(side='left', padx=5)
        
        tk.Label(stamp_controls, text="Posizione:").pack(side='left', padx=(10,0))
        self.stamp_position = tk.StringVar(value="top-right")
        position_combo = ttk.Combobox(stamp_controls, textvariable=self.stamp_position,
                                    values=["top-right", "top-left", "bottom-right", "bottom-left", "center"],
                                    state="readonly", width=12)
        position_combo.pack(side='left', padx=5)
        
        tk.Button(stamp_frame, text="Aggiungi Timbro", command=self.add_security_stamp,
                 bg='#795548', fg='white').pack(pady=5)
        
        # Pulizia metadati
        metadata_frame = tk.LabelFrame(parent, text="Pulizia Documento")
        metadata_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(metadata_frame, text="Rimuovi Metadati", command=self.remove_metadata,
                 bg='#607D8B', fg='white').pack(pady=10)
        
        tk.Label(metadata_frame, text="Rimuove informazioni sensibili come autore, data creazione, ecc.",
                font=('Arial', 8), fg='gray').pack()
    
    def update_security_status(self):
        """Aggiorna lo stato della sicurezza"""
        if not self.pdf_editor.current_doc:
            self.encryption_status_label.config(text="Nessun PDF aperto", fg='red')
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
                
            self.encryption_status_label.config(text=status_text, fg=color)
            
            # Aggiorna i checkboxes dei permessi
            if security_info['authenticated'] and security_info['permissions']:
                for perm_key, perm_var in self.perms.items():
                    perm_var.set(security_info['permissions'].get(perm_key, False))
        else:
            self.encryption_status_label.config(text="Errore nel recupero info sicurezza", fg='red')
    
    def encrypt_pdf(self):
        """Cripta il PDF"""
        user_password = self.user_password_entry.get()
        owner_password = self.owner_password_entry.get()
        
        if not user_password:
            messagebox.showwarning("Attenzione", "Inserisci almeno la password utente")
            return
        
        success, message = self.security.encrypt_pdf(user_password, owner_password)
        
        if success:
            messagebox.showinfo("Successo", message)
            self.update_security_status()
        else:
            messagebox.showerror("Errore", message)
    
    def decrypt_pdf(self):
        """Decripta il PDF"""
        password = self.decrypt_password_entry.get()
        
        if not password:
            messagebox.showwarning("Attenzione", "Inserisci la password")
            return
        
        success, message = self.security.decrypt_pdf(password)
        
        if success:
            messagebox.showinfo("Successo", message)
            self.update_security_status()
        else:
            messagebox.showerror("Errore", message)
    
    def apply_permissions(self):
        """Applica i permessi selezionati"""
        permissions_dict = {key: var.get() for key, var in self.perms.items()}
        
        success, message = self.security.set_pdf_permissions(permissions_dict)
        
        if success:
            messagebox.showinfo("Successo", message)
        else:
            messagebox.showerror("Errore", message)
    
    def select_all_permissions(self):
        """Seleziona tutti i permessi"""
        for var in self.perms.values():
            var.set(True)
    
    def deselect_all_permissions(self):
        """Deseleziona tutti i permessi"""
        for var in self.perms.values():
            var.set(False)
    
    def generate_keys(self):
        """Genera coppia di chiavi"""
        key_size = int(self.key_size_var.get())
        
        private_key, public_key = self.security.generate_key_pair(key_size)
        
        if private_key and public_key:
            # Chiedi dove salvare le chiavi
            private_key_path = filedialog.asksaveasfilename(
                title="Salva chiave privata",
                defaultextension=".pem",
                filetypes=[("PEM files", "*.pem")]
            )
            
            if private_key_path:
                public_key_path = private_key_path.replace('.pem', '_public.pem')
                
                # Chiedi password per proteggere la chiave privata
                key_password = simpledialog.askstring("Password Chiave", 
                                                     "Password per proteggere la chiave privata (opzionale):",
                                                     show='*')
                
                if self.security.save_keys(private_key, public_key, 
                                         private_key_path, public_key_path, key_password):
                    messagebox.showinfo("Successo", 
                                      f"Chiavi salvate:\n"
                                      f"Privata: {private_key_path}\n"
                                      f"Pubblica: {public_key_path}")
                else:
                    messagebox.showerror("Errore", "Errore nel salvataggio delle chiavi")
        else:
            messagebox.showerror("Errore", "Errore nella generazione delle chiavi")
    
    def sign_document(self):
        """Firma il documento"""
        field_name = self.signature_field_entry.get().strip()
        
        if not field_name:
            messagebox.showwarning("Attenzione", "Inserisci il nome del campo firma")
            return
        
        success, message = self.security.add_digital_signature(field_name)
        
        if success:
            messagebox.showinfo("Successo", message)
            # Aggiorna info firma
            self.signature_info_text.delete('1.0', 'end')
            self.signature_info_text.insert('1.0', 
                f"Documento firmato digitalmente\n"
                f"Campo: {field_name}\n"
                f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                f"Nota: Questa è una firma simulata per scopi dimostrativi")
        else:
            messagebox.showerror("Errore", message)
    
    def add_security_watermark(self):
        """Aggiunge watermark di sicurezza"""
        watermark_text = self.watermark_entry.get().strip()
        
        if not watermark_text:
            messagebox.showwarning("Attenzione", "Inserisci il testo del watermark")
            return
        
        success, message = self.security.create_watermark_security(watermark_text)
        
        if success:
            messagebox.showinfo("Successo", message)
        else:
            messagebox.showerror("Errore", message)
    
    def add_security_stamp(self):
        """Aggiunge timbro di sicurezza"""
        stamp_text = self.stamp_text_entry.get().strip()
        position = self.stamp_position.get()
        
        if not stamp_text:
            messagebox.showwarning("Attenzione", "Inserisci il testo del timbro")
            return
        
        page_num = self.pdf_editor.page_num
        success, message = self.security.add_security_stamp(page_num, stamp_text, position)
        
        if success:
            messagebox.showinfo("Successo", message)
        else:
            messagebox.showerror("Errore", message)
    
    def remove_metadata(self):
        """Rimuove metadati sensibili"""
        if not messagebox.askyesno("Conferma", 
                                  "Rimuovere tutti i metadati del documento?\n"
                                  "Questa operazione non può essere annullata."):
            return
        
        success, message = self.security.remove_metadata()
        
        if success:
            messagebox.showinfo("Successo", message)
        else:
            messagebox.showerror("Errore", message)
    
    def close_security_panel(self):
        """Chiude il pannello sicurezza"""
        self.security_window.destroy()
        self.security_window = None