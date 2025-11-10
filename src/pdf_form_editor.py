import fitz
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

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

class FormEditorGUI:
    def __init__(self, parent, pdf_editor):
        self.parent = parent
        self.pdf_editor = pdf_editor
        self.form_editor = PDFFormEditor(pdf_editor)
        
        self.form_window = None
        
    def open_form_editor(self):
        """Apre la finestra dell'editor form"""
        if self.form_window:
            self.form_window.lift()
            return
            
        self.form_window = tk.Toplevel(self.parent)
        self.form_window.title("Editor Form PDF")
        self.form_window.geometry("600x500")
        self.form_window.configure(bg='#f0f0f0')
        
        self.setup_form_editor_ui()
        
        # Gestisci chiusura finestra
        self.form_window.protocol("WM_DELETE_WINDOW", self.close_form_editor)
    
    def setup_form_editor_ui(self):
        """Configura l'interfaccia dell'editor form"""
        # Titolo
        title_label = tk.Label(self.form_window, text="EDITOR FORM PDF", 
                              font=('Arial', 14, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Notebook per organizzare le funzioni
        notebook = ttk.Notebook(self.form_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Tab 1: Crea campi
        create_frame = ttk.Frame(notebook)
        notebook.add(create_frame, text="Crea Campi")
        self.setup_create_fields_tab(create_frame)
        
        # Tab 2: Gestisci campi esistenti
        manage_frame = ttk.Frame(notebook)
        notebook.add(manage_frame, text="Gestisci Campi")
        self.setup_manage_fields_tab(manage_frame)
        
        # Tab 3: Dati form
        data_frame = ttk.Frame(notebook)
        notebook.add(data_frame, text="Dati Form")
        self.setup_form_data_tab(data_frame)
    
    def setup_create_fields_tab(self, parent):
        """Configura il tab per creare campi"""
        # Frame per tipo di campo
        type_frame = tk.LabelFrame(parent, text="Tipo di Campo")
        type_frame.pack(fill='x', padx=10, pady=5)
        
        self.field_type = tk.StringVar(value="text")
        
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
            tk.Radiobutton(type_frame, text=text, variable=self.field_type, value=value).grid(
                row=row, column=col, sticky='w', padx=5, pady=2)
        
        # Frame per proprietà
        props_frame = tk.LabelFrame(parent, text="Proprietà Campo")
        props_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(props_frame, text="Nome Campo:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.field_name_entry = tk.Entry(props_frame, width=30)
        self.field_name_entry.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(props_frame, text="Valore Default:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.default_value_entry = tk.Entry(props_frame, width=30)
        self.default_value_entry.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(props_frame, text="Opzioni (separate da virgola):").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.options_entry = tk.Entry(props_frame, width=30)
        self.options_entry.grid(row=2, column=1, padx=5, pady=2)
        
        # Pulsanti azione
        action_frame = tk.Frame(parent)
        action_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(action_frame, text="Crea Campo", command=self.create_field_interactive,
                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        tk.Button(action_frame, text="Anteprima", command=self.preview_field,
                 bg='#2196F3', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    
    def setup_manage_fields_tab(self, parent):
        """Configura il tab per gestire campi esistenti"""
        # Lista campi esistenti
        list_frame = tk.LabelFrame(parent, text="Campi Esistenti")
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview per mostrare i campi
        columns = ('Nome', 'Tipo', 'Valore', 'Pagina')
        self.fields_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.fields_tree.heading(col, text=col)
            self.fields_tree.column(col, width=120)
        
        # Scrollbar per treeview
        tree_scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.fields_tree.yview)
        self.fields_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.fields_tree.pack(side='left', fill='both', expand=True)
        tree_scrollbar.pack(side='right', fill='y')
        
        # Pulsanti gestione
        manage_buttons_frame = tk.Frame(parent)
        manage_buttons_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(manage_buttons_frame, text="Aggiorna Lista", command=self.refresh_fields_list,
                 bg='#FF9800', fg='white').pack(side='left', padx=5)
        
        tk.Button(manage_buttons_frame, text="Modifica Valore", command=self.edit_field_value,
                 bg='#9C27B0', fg='white').pack(side='left', padx=5)
        
        tk.Button(manage_buttons_frame, text="Elimina Campo", command=self.delete_field,
                 bg='#F44336', fg='white').pack(side='left', padx=5)
    
    def setup_form_data_tab(self, parent):
        """Configura il tab per i dati del form"""
        # Importa/Esporta dati
        io_frame = tk.LabelFrame(parent, text="Importa/Esporta Dati")
        io_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(io_frame, text="Esporta Dati Form", command=self.export_form_data,
                 bg='#4CAF50', fg='white', width=20).pack(side='left', padx=10, pady=10)
        
        tk.Button(io_frame, text="Importa Dati Form", command=self.import_form_data,
                 bg='#2196F3', fg='white', width=20).pack(side='left', padx=10, pady=10)
        
        # Validazione
        validation_frame = tk.LabelFrame(parent, text="Validazione Form")
        validation_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(validation_frame, text="Valida Form", command=self.validate_form,
                 bg='#FF9800', fg='white', width=20).pack(pady=10)
        
        # Area risultati validazione
        self.validation_text = tk.Text(validation_frame, height=8, width=60)
        validation_scrollbar = tk.Scrollbar(validation_frame, orient='vertical', 
                                          command=self.validation_text.yview)
        self.validation_text.configure(yscrollcommand=validation_scrollbar.set)
        
        self.validation_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        validation_scrollbar.pack(side='right', fill='y', pady=5)
    
    def create_field_interactive(self):
        """Crea un campo in modo interattivo"""
        if not self.pdf_editor.current_doc:
            messagebox.showwarning("Attenzione", "Nessun PDF aperto")
            return
        
        field_name = self.field_name_entry.get().strip()
        if not field_name:
            messagebox.showwarning("Attenzione", "Inserisci un nome per il campo")
            return
        
        # Chiudi la finestra form temporaneamente per permettere la selezione
        self.form_window.withdraw()
        
        messagebox.showinfo("Selezione Area", 
                           "Clicca e trascina sulla pagina PDF per definire l'area del campo")
        
        # TODO: Implementare selezione interattiva dell'area
        # Per ora usa valori di default
        page_num = self.pdf_editor.page_num
        rect = fitz.Rect(100, 100, 300, 130)  # Area di default
        
        field_type = self.field_type.get()
        default_value = self.default_value_entry.get()
        options = [opt.strip() for opt in self.options_entry.get().split(',') if opt.strip()]
        
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
        
        # Ripristina la finestra form
        self.form_window.deiconify()
        
        if success:
            messagebox.showinfo("Successo", f"Campo '{field_name}' creato correttamente")
            self.refresh_fields_list()
        else:
            messagebox.showerror("Errore", f"Errore nella creazione del campo '{field_name}'")
    
    def refresh_fields_list(self):
        """Aggiorna la lista dei campi"""
        # Pulisci la lista esistente
        for item in self.fields_tree.get_children():
            self.fields_tree.delete(item)
        
        # Ottieni e mostra i campi attuali
        fields = self.form_editor.get_form_fields()
        for field in fields:
            self.fields_tree.insert('', 'end', values=(
                field['name'], 
                field['type'], 
                str(field['value'])[:30] + ('...' if len(str(field['value'])) > 30 else ''),
                field['page'] + 1
            ))
    
    def edit_field_value(self):
        """Modifica il valore di un campo selezionato"""
        selection = self.fields_tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona un campo da modificare")
            return
        
        item = self.fields_tree.item(selection[0])
        field_name = item['values'][0]
        current_value = item['values'][2]
        
        new_value = simpledialog.askstring("Modifica Valore", 
                                          f"Nuovo valore per '{field_name}':", 
                                          initialvalue=current_value)
        
        if new_value is not None:
            if self.form_editor.set_field_value(field_name, new_value):
                messagebox.showinfo("Successo", "Valore aggiornato correttamente")
                self.refresh_fields_list()
            else:
                messagebox.showerror("Errore", "Errore nell'aggiornamento del valore")
    
    def delete_field(self):
        """Elimina un campo selezionato"""
        selection = self.fields_tree.selection()
        if not selection:
            messagebox.showwarning("Attenzione", "Seleziona un campo da eliminare")
            return
        
        item = self.fields_tree.item(selection[0])
        field_name = item['values'][0]
        
        if messagebox.askyesno("Conferma", f"Eliminare il campo '{field_name}'?"):
            if self.form_editor.delete_field(field_name):
                messagebox.showinfo("Successo", "Campo eliminato correttamente")
                self.refresh_fields_list()
            else:
                messagebox.showerror("Errore", "Errore nell'eliminazione del campo")
    
    def export_form_data(self):
        """Esporta i dati del form"""
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            title="Esporta Dati Form",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        
        if file_path:
            if self.form_editor.export_form_data(file_path):
                messagebox.showinfo("Successo", "Dati form esportati correttamente")
            else:
                messagebox.showerror("Errore", "Errore nell'esportazione dei dati")
    
    def import_form_data(self):
        """Importa i dati del form"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Importa Dati Form",
            filetypes=[("JSON files", "*.json")]
        )
        
        if file_path:
            if self.form_editor.import_form_data(file_path):
                messagebox.showinfo("Successo", "Dati form importati correttamente")
                self.refresh_fields_list()
            else:
                messagebox.showerror("Errore", "Errore nell'importazione dei dati")
    
    def validate_form(self):
        """Valida il form"""
        self.validation_text.delete('1.0', 'end')
        
        is_valid, errors = self.form_editor.validate_form()
        
        if is_valid:
            self.validation_text.insert('1.0', "✓ FORM VALIDO\n\nTutti i campi sono compilati correttamente.")
        else:
            self.validation_text.insert('1.0', "✗ ERRORI NEL FORM\n\n")
            for i, error in enumerate(errors, 1):
                self.validation_text.insert('end', f"{i}. {error}\n")
    
    def preview_field(self):
        """Anteprima del campo da creare"""
        field_type = self.field_type.get()
        field_name = self.field_name_entry.get().strip()
        default_value = self.default_value_entry.get()
        
        info = f"Tipo: {field_type}\nNome: {field_name}\nValore Default: {default_value}"
        
        messagebox.showinfo("Anteprima Campo", info)
    
    def close_form_editor(self):
        """Chiude l'editor form"""
        self.form_window.destroy()
        self.form_window = None