import fitz
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QMessageBox, QFileDialog, QRadioButton,
                               QGroupBox, QDialog, QTabWidget, QTreeWidget, 
                               QTreeWidgetItem, QTextEdit, QButtonGroup, QInputDialog,
                               QGridLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from theme_manager import theme_manager
from user_config import user_config

class PDFFormEditor:
    def __init__(self, pdf_editor):
        self.pdf_editor = pdf_editor
        
    def create_text_field(self, page_num, rect, field_name, default_text="", multiline=False):
        """Crea un campo di testo"""
        if not self.pdf_editor.current_doc:
            return False
            
        try:
            page = self.pdf_editor.current_doc[page_num]
            
            # Crea widget testo
            widget = fitz.Widget()
            widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
            widget.field_name = field_name
            widget.rect = rect
            widget.field_value = default_text
            widget.text_maxlen = 0  # Lunghezza illimitata
            
            if multiline:
                widget.field_flags = fitz.PDF_TX_FIELD_IS_MULTILINE
            
            # Styling
            widget.border_color = (0, 0, 0)  # Nero
            widget.fill_color = (1, 1, 1)    # Bianco
            widget.text_color = (0, 0, 0)    # Testo nero
            
            page.add_widget(widget)
            return True
            
        except Exception as e:
            print(f"Errore nella creazione del campo testo: {e}")
            return False
    
    def create_checkbox(self, page_num, rect, field_name, checked=False):
        """Crea una checkbox"""
        if not self.pdf_editor.current_doc:
            return False
            
        try:
            page = self.pdf_editor.current_doc[page_num]
            
            widget = fitz.Widget()
            widget.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
            widget.field_name = field_name
            widget.rect = rect
            widget.field_value = checked
            
            # Styling
            widget.border_color = (0, 0, 0)
            widget.fill_color = (1, 1, 1)
            
            page.add_widget(widget)
            return True
            
        except Exception as e:
            print(f"Errore nella creazione della checkbox: {e}")
            return False
    
    def create_radio_button(self, page_num, rect, group_name, value, selected=False):
        """Crea un radio button"""
        if not self.pdf_editor.current_doc:
            return False
            
        try:
            page = self.pdf_editor.current_doc[page_num]
            
            widget = fitz.Widget()
            widget.field_type = fitz.PDF_WIDGET_TYPE_RADIOBUTTON
            widget.field_name = group_name
            widget.rect = rect
            widget.field_value = value if selected else ""
            widget.button_caption = value
            
            # Styling
            widget.border_color = (0, 0, 0)
            widget.fill_color = (1, 1, 1)
            
            page.add_widget(widget)
            return True
            
        except Exception as e:
            print(f"Errore nella creazione del radio button: {e}")
            return False
    
    def create_dropdown(self, page_num, rect, field_name, options, default_selection=0):
        """Crea un menu dropdown"""
        if not self.pdf_editor.current_doc:
            return False
            
        try:
            page = self.pdf_editor.current_doc[page_num]
            
            widget = fitz.Widget()
            widget.field_type = fitz.PDF_WIDGET_TYPE_COMBOBOX
            widget.field_name = field_name
            widget.rect = rect
            
            # Imposta le opzioni
            widget.choice_values = options
            if 0 <= default_selection < len(options):
                widget.field_value = options[default_selection]
            
            # Styling
            widget.border_color = (0, 0, 0)
            widget.fill_color = (1, 1, 1)
            widget.text_color = (0, 0, 0)
            
            page.add_widget(widget)
            return True
            
        except Exception as e:
            print(f"Errore nella creazione del dropdown: {e}")
            return False
    
    def create_listbox(self, page_num, rect, field_name, options, multi_select=False):
        """Crea una listbox"""
        if not self.pdf_editor.current_doc:
            return False
            
        try:
            page = self.pdf_editor.current_doc[page_num]
            
            widget = fitz.Widget()
            widget.field_type = fitz.PDF_WIDGET_TYPE_LISTBOX
            widget.field_name = field_name
            widget.rect = rect
            
            # Imposta le opzioni
            widget.choice_values = options
            
            if multi_select:
                widget.field_flags = fitz.PDF_CH_FIELD_IS_MULTI_SELECT
            
            # Styling
            widget.border_color = (0, 0, 0)
            widget.fill_color = (1, 1, 1)
            widget.text_color = (0, 0, 0)
            
            page.add_widget(widget)
            return True
            
        except Exception as e:
            print(f"Errore nella creazione della listbox: {e}")
            return False
    
    def create_button(self, page_num, rect, field_name, caption="Button", action=None):
        """Crea un pulsante"""
        if not self.pdf_editor.current_doc:
            return False
            
        try:
            page = self.pdf_editor.current_doc[page_num]
            
            widget = fitz.Widget()
            widget.field_type = fitz.PDF_WIDGET_TYPE_BUTTON
            widget.field_name = field_name
            widget.rect = rect
            widget.button_caption = caption
            
            # JavaScript action (opzionale)
            if action:
                widget.script = action
            
            # Styling
            widget.border_color = (0, 0, 0)
            widget.fill_color = (0.9, 0.9, 0.9)
            widget.text_color = (0, 0, 0)
            
            page.add_widget(widget)
            return True
            
        except Exception as e:
            print(f"Errore nella creazione del pulsante: {e}")
            return False
    
    def create_signature_field(self, page_num, rect, field_name):
        """Crea un campo per la firma digitale"""
        if not self.pdf_editor.current_doc:
            return False
            
        try:
            page = self.pdf_editor.current_doc[page_num]
            
            widget = fitz.Widget()
            widget.field_type = fitz.PDF_WIDGET_TYPE_SIGNATURE
            widget.field_name = field_name
            widget.rect = rect
            
            # Styling per campo firma
            widget.border_color = (0, 0, 0)
            widget.fill_color = (1, 1, 0.9)  # Giallo chiaro
            
            page.add_widget(widget)
            return True
            
        except Exception as e:
            print(f"Errore nella creazione del campo firma: {e}")
            return False
    
    def get_form_fields(self, page_num=None):
        """Ottiene tutti i campi form del documento o di una pagina specifica"""
        if not self.pdf_editor.current_doc:
            return []
            
        fields = []
        try:
            if page_num is not None:
                # Campi di una pagina specifica
                page = self.pdf_editor.current_doc[page_num]
                for widget in page.widgets():
                    field_info = {
                        'name': widget.field_name,
                        'type': widget.field_type_string,
                        'rect': list(widget.rect),
                        'value': widget.field_value,
                        'page': page_num
                    }
                    fields.append(field_info)
            else:
                # Tutti i campi del documento
                for page_num in range(len(self.pdf_editor.current_doc)):
                    page = self.pdf_editor.current_doc[page_num]
                    for widget in page.widgets():
                        field_info = {
                            'name': widget.field_name,
                            'type': widget.field_type_string,
                            'rect': list(widget.rect),
                            'value': widget.field_value,
                            'page': page_num
                        }
                        fields.append(field_info)
                        
            return fields
            
        except Exception as e:
            print(f"Errore nel recupero dei campi form: {e}")
            return []
    
    def set_field_value(self, field_name, value):
        """Imposta il valore di un campo form"""
        if not self.pdf_editor.current_doc:
            return False
            
        try:
            for page_num in range(len(self.pdf_editor.current_doc)):
                page = self.pdf_editor.current_doc[page_num]
                for widget in page.widgets():
                    if widget.field_name == field_name:
                        widget.field_value = value
                        widget.update()
                        return True
            return False
            
        except Exception as e:
            print(f"Errore nell'impostazione del valore del campo: {e}")
            return False
    
    def get_field_value(self, field_name):
        """Ottiene il valore di un campo form"""
        if not self.pdf_editor.current_doc:
            return None
            
        try:
            for page_num in range(len(self.pdf_editor.current_doc)):
                page = self.pdf_editor.current_doc[page_num]
                for widget in page.widgets():
                    if widget.field_name == field_name:
                        return widget.field_value
            return None
            
        except Exception as e:
            print(f"Errore nel recupero del valore del campo: {e}")
            return None
    
    def delete_field(self, field_name):
        """Elimina un campo form"""
        if not self.pdf_editor.current_doc:
            return False
            
        try:
            for page_num in range(len(self.pdf_editor.current_doc)):
                page = self.pdf_editor.current_doc[page_num]
                widgets_to_delete = []
                
                for widget in page.widgets():
                    if widget.field_name == field_name:
                        widgets_to_delete.append(widget)
                
                for widget in widgets_to_delete:
                    page.delete_widget(widget)
                    
            return True
            
        except Exception as e:
            print(f"Errore nell'eliminazione del campo: {e}")
            return False
    
    def export_form_data(self, output_file):
        """Esporta i dati del form in formato JSON"""
        if not self.pdf_editor.current_doc:
            return False
            
        try:
            form_data = {}
            fields = self.get_form_fields()
            
            for field in fields:
                form_data[field['name']] = {
                    'value': field['value'],
                    'type': field['type'],
                    'page': field['page'],
                    'rect': field['rect']
                }
            
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(form_data, f, indent=2, ensure_ascii=False)
                
            return True
            
        except Exception as e:
            print(f"Errore nell'esportazione dei dati form: {e}")
            return False
    
    def import_form_data(self, input_file):
        """Importa i dati del form da un file JSON"""
        if not self.pdf_editor.current_doc:
            return False
            
        try:
            import json
            with open(input_file, 'r', encoding='utf-8') as f:
                form_data = json.load(f)
            
            for field_name, field_info in form_data.items():
                self.set_field_value(field_name, field_info['value'])
                
            return True
            
        except Exception as e:
            print(f"Errore nell'importazione dei dati form: {e}")
            return False
    
    def validate_form(self):
        """Valida tutti i campi form obbligatori"""
        if not self.pdf_editor.current_doc:
            return False, []
            
        errors = []
        try:
            fields = self.get_form_fields()
            
            for field in fields:
                # Controlla campi obbligatori (implementazione base)
                if field['name'].endswith('*') or 'required' in field['name'].lower():
                    if not field['value'] or str(field['value']).strip() == '':
                        errors.append(f"Campo obbligatorio '{field['name']}' non compilato")
                
                # Validazione email
                if 'email' in field['name'].lower() and field['value']:
                    import re
                    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                    if not re.match(email_pattern, str(field['value'])):
                        errors.append(f"Email non valida nel campo '{field['name']}'")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            print(f"Errore nella validazione del form: {e}")
            return False, [f"Errore nella validazione: {e}"]

class FormEditorGUI(QWidget):
    def __init__(self, parent, pdf_editor):
        super().__init__(parent)
        self.parent = parent
        self.pdf_editor = pdf_editor
        self.form_editor = PDFFormEditor(pdf_editor)
        
        self.form_window = None
        
    def open_form_editor(self):
        """Apre la finestra dell'editor form"""
        if self.form_window:
            self.form_window.activateWindow()
            return
            
        self.form_window = QDialog(self.parent)
        self.form_window.setWindowTitle("Editor Form PDF")
        self.form_window.resize(600, 500)
        
        # Applica il tema
        theme_setting = user_config.get("theme", "auto")
        if theme_setting == "auto":
            current_theme = theme_manager.get_theme()
        else:
            current_theme = theme_setting
            theme_manager.current_theme = current_theme
        self.form_window.setStyleSheet(theme_manager.get_stylesheet())
        
        self.setup_form_editor_ui()
        
        # Mostra la finestra
        self.form_window.show()
    
    def setup_form_editor_ui(self):
        """Configura l'interfaccia dell'editor form"""
        layout = QVBoxLayout(self.form_window)
        
        # Titolo
        title_label = QLabel("EDITOR FORM PDF")
        title_label.setFont(QFont('Arial', 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Tab widget per organizzare le funzioni
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # Tab 1: Crea campi
        create_widget = QWidget()
        tab_widget.addTab(create_widget, "Crea Campi")
        self.setup_create_fields_tab(create_widget)
        
        # Tab 2: Gestisci campi esistenti
        manage_widget = QWidget()
        tab_widget.addTab(manage_widget, "Gestisci Campi")
        self.setup_manage_fields_tab(manage_widget)
        
        # Tab 3: Dati form
        data_widget = QWidget()
        tab_widget.addTab(data_widget, "Dati Form")
        self.setup_form_data_tab(data_widget)
    
    def setup_create_fields_tab(self, parent):
        """Configura il tab per creare campi"""
        layout = QVBoxLayout(parent)
        
        # Frame per tipo di campo
        type_group = QGroupBox("Tipo di Campo")
        type_layout = QGridLayout(type_group)
        
        self.field_type_group = QButtonGroup()
        
        field_types = [
            ("Campo Testo", "text"),
            ("Area Testo", "textarea"),
            ("Checkbox", "checkbox"),
            ("Radio Button", "radio"),
            ("Dropdown", "dropdown"),
            ("Lista", "listbox"),
            ("Pulsante", "button"),
            ("Campo Firma", "signature")
        ]
        
        for i, (text, value) in enumerate(field_types):
            row = i // 4
            col = i % 4
            radio = QRadioButton(text)
            radio.setProperty("value", value)
            if value == "text":
                radio.setChecked(True)
            self.field_type_group.addButton(radio)
            type_layout.addWidget(radio, row, col)
        
        layout.addWidget(type_group)
        
        # Frame per proprietà
        props_group = QGroupBox("Proprietà Campo")
        props_layout = QGridLayout(props_group)
        
        props_layout.addWidget(QLabel("Nome Campo:"), 0, 0)
        self.field_name_entry = QLineEdit()
        props_layout.addWidget(self.field_name_entry, 0, 1)
        
        props_layout.addWidget(QLabel("Valore Default:"), 1, 0)
        self.default_value_entry = QLineEdit()
        props_layout.addWidget(self.default_value_entry, 1, 1)
        
        props_layout.addWidget(QLabel("Opzioni (separate da virgola):"), 2, 0)
        self.options_entry = QLineEdit()
        props_layout.addWidget(self.options_entry, 2, 1)
        
        layout.addWidget(props_group)
        
        # Pulsanti azione
        buttons_layout = QHBoxLayout()
        
        create_btn = QPushButton("Crea Campo")
        create_btn.clicked.connect(self.create_field_interactive)
        create_btn.setFont(QFont('Arial', 10, QFont.Bold))
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        buttons_layout.addWidget(create_btn)
        
        preview_btn = QPushButton("Anteprima")
        preview_btn.clicked.connect(self.preview_field)
        preview_btn.setFont(QFont('Arial', 10, QFont.Bold))
        preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        buttons_layout.addWidget(preview_btn)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
    
    def setup_manage_fields_tab(self, parent):
        """Configura il tab per gestire campi esistenti"""
        layout = QVBoxLayout(parent)
        
        # Lista campi esistenti
        list_group = QGroupBox("Campi Esistenti")
        list_layout = QVBoxLayout(list_group)
        
        # Tree widget per mostrare i campi
        self.fields_tree = QTreeWidget()
        self.fields_tree.setHeaderLabels(['Nome', 'Tipo', 'Valore', 'Pagina'])
        self.fields_tree.setMinimumHeight(250)
        list_layout.addWidget(self.fields_tree)
        
        layout.addWidget(list_group)
        
        # Pulsanti gestione
        buttons_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Aggiorna Lista")
        refresh_btn.clicked.connect(self.refresh_fields_list)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { background-color: #F57C00; }
        """)
        buttons_layout.addWidget(refresh_btn)
        
        edit_btn = QPushButton("Modifica Valore")
        edit_btn.clicked.connect(self.edit_field_value)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { background-color: #7B1FA2; }
        """)
        buttons_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Elimina Campo")
        delete_btn.clicked.connect(self.delete_field)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover { background-color: #D32F2F; }
        """)
        buttons_layout.addWidget(delete_btn)
        
        layout.addLayout(buttons_layout)
    
    def setup_form_data_tab(self, parent):
        """Configura il tab per i dati del form"""
        layout = QVBoxLayout(parent)
        
        # Importa/Esporta dati
        io_group = QGroupBox("Importa/Esporta Dati")
        io_layout = QHBoxLayout(io_group)
        
        export_btn = QPushButton("Esporta Dati Form")
        export_btn.clicked.connect(self.export_form_data)
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                min-width: 150px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        io_layout.addWidget(export_btn)
        
        import_btn = QPushButton("Importa Dati Form")
        import_btn.clicked.connect(self.import_form_data)
        import_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                min-width: 150px;
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        io_layout.addWidget(import_btn)
        
        layout.addWidget(io_group)
        
        # Validazione
        validation_group = QGroupBox("Validazione Form")
        validation_layout = QVBoxLayout(validation_group)
        
        validate_btn = QPushButton("Valida Form")
        validate_btn.clicked.connect(self.validate_form)
        validate_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                min-width: 150px;
            }
            QPushButton:hover { background-color: #F57C00; }
        """)
        validation_layout.addWidget(validate_btn)
        
        # Area risultati validazione
        self.validation_text = QTextEdit()
        self.validation_text.setReadOnly(True)
        self.validation_text.setMinimumHeight(150)
        validation_layout.addWidget(self.validation_text)
        
        layout.addWidget(validation_group)
        layout.addStretch()
    
    def create_field_interactive(self):
        """Crea un campo in modo interattivo"""
        if not self.pdf_editor.current_doc:
            QMessageBox.warning(self.form_window, "Attenzione", "Nessun PDF aperto")
            return
        
        field_name = self.field_name_entry.text().strip()
        if not field_name:
            QMessageBox.warning(self.form_window, "Attenzione", "Inserisci un nome per il campo")
            return
        
        # Nascondi temporaneamente la finestra
        self.form_window.hide()
        
        QMessageBox.information(self.form_window, "Selezione Area", 
                           "Clicca e trascina sulla pagina PDF per definire l'area del campo")
        
        # TODO: Implementare selezione interattiva dell'area
        # Per ora usa valori di default
        page_num = self.pdf_editor.page_num
        rect = fitz.Rect(100, 100, 300, 130)  # Area di default
        
        # Get selected field type
        field_type = "text"
        for button in self.field_type_group.buttons():
            if button.isChecked():
                field_type = button.property("value")
                break
        
        default_value = self.default_value_entry.text()
        options = [opt.strip() for opt in self.options_entry.text().split(',') if opt.strip()]
        
        success = False
        
        if field_type == "text":
            success = self.form_editor.create_text_field(page_num, rect, field_name, default_value)
        elif field_type == "textarea":
            success = self.form_editor.create_text_field(page_num, rect, field_name, default_value, multiline=True)
        elif field_type == "checkbox":
            success = self.form_editor.create_checkbox(page_num, rect, field_name)
        elif field_type == "dropdown" and options:
            success = self.form_editor.create_dropdown(page_num, rect, field_name, options)
        elif field_type == "listbox" and options:
            success = self.form_editor.create_listbox(page_num, rect, field_name, options)
        elif field_type == "button":
            caption = default_value or "Button"
            success = self.form_editor.create_button(page_num, rect, field_name, caption)
        elif field_type == "signature":
            success = self.form_editor.create_signature_field(page_num, rect, field_name)
        
        # Ripristina la finestra
        self.form_window.show()
        
        if success:
            QMessageBox.information(self.form_window, "Successo", f"Campo '{field_name}' creato correttamente")
            self.refresh_fields_list()
        else:
            QMessageBox.critical(self.form_window, "Errore", f"Errore nella creazione del campo '{field_name}'")
    
    def refresh_fields_list(self):
        """Aggiorna la lista dei campi"""
        # Pulisci la lista esistente
        self.fields_tree.clear()
        
        # Ottieni e mostra i campi attuali
        fields = self.form_editor.get_form_fields()
        for field in fields:
            item = QTreeWidgetItem([
                field['name'], 
                field['type'], 
                str(field['value'])[:30] + ('...' if len(str(field['value'])) > 30 else ''),
                str(field['page'] + 1)
            ])
            self.fields_tree.addTopLevelItem(item)
    
    def edit_field_value(self):
        """Modifica il valore di un campo selezionato"""
        selected_items = self.fields_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.form_window, "Attenzione", "Seleziona un campo da modificare")
            return
        
        item = selected_items[0]
        field_name = item.text(0)
        current_value = item.text(2)
        
        new_value, ok = QInputDialog.getText(
            self.form_window, 
            "Modifica Valore", 
            f"Nuovo valore per '{field_name}':",
            QLineEdit.Normal,
            current_value
        )
        
        if ok and new_value is not None:
            if self.form_editor.set_field_value(field_name, new_value):
                QMessageBox.information(self.form_window, "Successo", "Valore aggiornato correttamente")
                self.refresh_fields_list()
            else:
                QMessageBox.critical(self.form_window, "Errore", "Errore nell'aggiornamento del valore")
    
    def delete_field(self):
        """Elimina un campo selezionato"""
        selected_items = self.fields_tree.selectedItems()
        if not selected_items:
            QMessageBox.warning(self.form_window, "Attenzione", "Seleziona un campo da eliminare")
            return
        
        item = selected_items[0]
        field_name = item.text(0)
        
        reply = QMessageBox.question(
            self.form_window,
            "Conferma",
            f"Eliminare il campo '{field_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.form_editor.delete_field(field_name):
                QMessageBox.information(self.form_window, "Successo", "Campo eliminato correttamente")
                self.refresh_fields_list()
            else:
                QMessageBox.critical(self.form_window, "Errore", "Errore nell'eliminazione del campo")
    
    def export_form_data(self):
        """Esporta i dati del form"""
        file_path, _ = QFileDialog.getSaveFileName(
            self.form_window,
            "Esporta Dati Form",
            "",
            "JSON files (*.json)"
        )
        
        if file_path:
            if self.form_editor.export_form_data(file_path):
                QMessageBox.information(self.form_window, "Successo", "Dati form esportati correttamente")
            else:
                QMessageBox.critical(self.form_window, "Errore", "Errore nell'esportazione dei dati")
    
    def import_form_data(self):
        """Importa i dati del form"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.form_window,
            "Importa Dati Form",
            "",
            "JSON files (*.json)"
        )
        
        if file_path:
            if self.form_editor.import_form_data(file_path):
                QMessageBox.information(self.form_window, "Successo", "Dati form importati correttamente")
                self.refresh_fields_list()
            else:
                QMessageBox.critical(self.form_window, "Errore", "Errore nell'importazione dei dati")
    
    def validate_form(self):
        """Valida il form"""
        self.validation_text.clear()
        
        is_valid, errors = self.form_editor.validate_form()
        
        if is_valid:
            self.validation_text.append("✓ FORM VALIDO\n\nTutti i campi sono compilati correttamente.")
        else:
            self.validation_text.append("✗ ERRORI NEL FORM\n\n")
            for i, error in enumerate(errors, 1):
                self.validation_text.append(f"{i}. {error}")
    
    def preview_field(self):
        """Anteprima del campo da creare"""
        # Get selected field type
        field_type = "text"
        for button in self.field_type_group.buttons():
            if button.isChecked():
                field_type = button.property("value")
                break
        
        field_name = self.field_name_entry.text().strip()
        default_value = self.default_value_entry.text()
        
        info = f"Tipo: {field_type}\nNome: {field_name}\nValore Default: {default_value}"
        
        QMessageBox.information(self.form_window, "Anteprima Campo", info)
    
    def close_form_editor(self):
        """Chiude l'editor form"""
        if self.form_window:
            self.form_window.close()
            self.form_window = None
        self.form_window = None