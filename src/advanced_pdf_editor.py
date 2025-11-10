import fitz  # PyMuPDF
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser, simpledialog
from PIL import Image, ImageTk
import io
import os
import json
from pathlib import Path
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class AdvancedPDFEditor:
    def __init__(self):
        self.current_doc = None
        self.current_page = None
        self.page_num = 0
        self.zoom_level = 1.0
        self.annotations = []
        self.current_tool = "select"
        
    def open_pdf(self, pdf_path):
        """Apre un PDF per l'editing avanzato"""
        try:
            self.current_doc = fitz.open(pdf_path)
            self.page_num = 0
            return True
        except Exception as e:
            print(f"Errore nell'apertura del PDF: {e}")
            return False
    
    def get_page_count(self):
        """Restituisce il numero di pagine del PDF"""
        if self.current_doc:
            return len(self.current_doc)
        return 0
    
    def get_page_image(self, page_num=None, zoom=None):
        """Restituisce l'immagine della pagina corrente"""
        if not self.current_doc:
            return None
            
        if page_num is None:
            page_num = self.page_num
        if zoom is None:
            zoom = self.zoom_level
            
        try:
            page = self.current_doc[page_num]
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img_data = pix.tobytes("ppm")
            return Image.open(io.BytesIO(img_data))
        except Exception as e:
            print(f"Errore nel caricamento della pagina: {e}")
            return None
    
    def add_text(self, page_num, x, y, text, font_size=12, color=(0, 0, 0)):
        """Aggiunge testo alla pagina"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            point = fitz.Point(x, y)
            page.insert_text(point, text, fontsize=font_size, color=color)
            return True
        except Exception as e:
            print(f"Errore nell'aggiunta del testo: {e}")
            return False
    
    def add_highlight(self, page_num, rect, color=(1, 1, 0)):
        """Aggiunge evidenziazione"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            highlight = page.add_highlight_annot(rect)
            highlight.set_colors(stroke=color)
            highlight.update()
            return True
        except Exception as e:
            print(f"Errore nell'evidenziazione: {e}")
            return False
    
    def add_note(self, page_num, x, y, content, icon="Note"):
        """Aggiunge una nota adesiva"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            point = fitz.Point(x, y)
            note = page.add_text_annot(point, content, icon=icon)
            note.update()
            return True
        except Exception as e:
            print(f"Errore nell'aggiunta della nota: {e}")
            return False
    
    def add_rectangle(self, page_num, rect, color=(0, 0, 1), fill_color=None, width=1):
        """Aggiunge un rettangolo"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            annot = page.add_rect_annot(rect)
            annot.set_colors(stroke=color, fill=fill_color)
            annot.set_border(width=width)
            annot.update()
            return True
        except Exception as e:
            print(f"Errore nell'aggiunta del rettangolo: {e}")
            return False
    
    def add_circle(self, page_num, rect, color=(0, 0, 1), fill_color=None, width=1):
        """Aggiunge un cerchio"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            annot = page.add_circle_annot(rect)
            annot.set_colors(stroke=color, fill=fill_color)
            annot.set_border(width=width)
            annot.update()
            return True
        except Exception as e:
            print(f"Errore nell'aggiunta del cerchio: {e}")
            return False
    
    def add_line(self, page_num, start_point, end_point, color=(0, 0, 1), width=1):
        """Aggiunge una linea"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            line = page.add_line_annot(start_point, end_point)
            line.set_colors(stroke=color)
            line.set_border(width=width)
            line.update()
            return True
        except Exception as e:
            print(f"Errore nell'aggiunta della linea: {e}")
            return False
    
    def add_arrow(self, page_num, start_point, end_point, color=(0, 0, 1), width=1):
        """Aggiunge una freccia"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            line = page.add_line_annot(start_point, end_point)
            line.set_colors(stroke=color)
            line.set_border(width=width)
            # Imposta terminazioni freccia
            line.set_line_ends(fitz.PDF_ANNOT_LE_NONE, fitz.PDF_ANNOT_LE_CLOSED_ARROW)
            line.update()
            return True
        except Exception as e:
            print(f"Errore nell'aggiunta della freccia: {e}")
            return False
    
    def add_freehand_drawing(self, page_num, points, color=(0, 0, 1), width=2):
        """Aggiunge disegno a mano libera"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            ink = page.add_ink_annot([points])
            ink.set_colors(stroke=color)
            ink.set_border(width=width)
            ink.update()
            return True
        except Exception as e:
            print(f"Errore nel disegno a mano libera: {e}")
            return False
    
    def add_image(self, page_num, rect, image_path):
        """Inserisce un'immagine nella pagina"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            page.insert_image(rect, filename=image_path)
            return True
        except Exception as e:
            print(f"Errore nell'inserimento dell'immagine: {e}")
            return False
    
    def delete_annotation(self, page_num, annot_index):
        """Elimina un'annotazione"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            annot = page.annots()[annot_index]
            page.delete_annot(annot)
            return True
        except Exception as e:
            print(f"Errore nell'eliminazione dell'annotazione: {e}")
            return False
    
    def extract_text_from_rect(self, page_num, rect):
        """Estrae testo da una regione specifica"""
        if not self.current_doc:
            return ""
            
        try:
            page = self.current_doc[page_num]
            return page.get_text("text", clip=rect)
        except Exception as e:
            print(f"Errore nell'estrazione del testo: {e}")
            return ""
    
    def search_text(self, text, page_num=None):
        """Cerca testo nel documento"""
        if not self.current_doc:
            return []
            
        results = []
        try:
            if page_num is not None:
                page = self.current_doc[page_num]
                text_instances = page.search_for(text)
                for inst in text_instances:
                    results.append((page_num, inst))
            else:
                for page_num in range(len(self.current_doc)):
                    page = self.current_doc[page_num]
                    text_instances = page.search_for(text)
                    for inst in text_instances:
                        results.append((page_num, inst))
            return results
        except Exception as e:
            print(f"Errore nella ricerca: {e}")
            return []
    
    def add_form_field(self, page_num, field_type, rect, field_name, **kwargs):
        """Aggiunge un campo form"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            
            if field_type == "text":
                widget = fitz.Widget()
                widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
                widget.field_name = field_name
                widget.rect = rect
                widget.field_value = kwargs.get('default_text', '')
                page.add_widget(widget)
                
            elif field_type == "checkbox":
                widget = fitz.Widget()
                widget.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
                widget.field_name = field_name
                widget.rect = rect
                widget.field_value = kwargs.get('checked', False)
                page.add_widget(widget)
                
            elif field_type == "button":
                widget = fitz.Widget()
                widget.field_type = fitz.PDF_WIDGET_TYPE_BUTTON
                widget.field_name = field_name
                widget.rect = rect
                widget.button_caption = kwargs.get('caption', 'Button')
                page.add_widget(widget)
                
            return True
        except Exception as e:
            print(f"Errore nell'aggiunta del campo form: {e}")
            return False
    
    def encrypt_pdf(self, password, permissions=None):
        """Cripta il PDF con password"""
        if not self.current_doc:
            return False
            
        try:
            perm = permissions or fitz.PDF_PERM_PRINT | fitz.PDF_PERM_COPY | fitz.PDF_PERM_EDIT
            self.current_doc.authenticate(password)
            self.current_doc.set_metadata({
                "encryption": True,
                "permissions": perm
            })
            return True
        except Exception as e:
            print(f"Errore nella crittografia: {e}")
            return False
    
    def save_pdf(self, output_path, incremental=False):
        """Salva il PDF modificato"""
        if not self.current_doc:
            return False
            
        try:
            self.current_doc.save(output_path, incremental=incremental)
            return True
        except Exception as e:
            print(f"Errore nel salvataggio: {e}")
            return False
    
    def get_annotations(self, page_num):
        """Ottiene tutte le annotazioni di una pagina"""
        if not self.current_doc:
            return []
            
        try:
            page = self.current_doc[page_num]
            annotations = []
            for annot in page.annots():
                annot_info = {
                    "type": annot.type[1],
                    "rect": list(annot.rect),
                    "content": annot.content,
                    "page": page_num
                }
                annotations.append(annot_info)
            return annotations
        except Exception as e:
            print(f"Errore nel recupero delle annotazioni: {e}")
            return []
    
    def close_pdf(self):
        """Chiude il PDF corrente"""
        if self.current_doc:
            self.current_doc.close()
            self.current_doc = None
            self.page_num = 0
            self.zoom_level = 1.0