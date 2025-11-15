import fitz  # PyMuPDF
from PIL import Image
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
    
    def add_text(self, page_num, x, y, text, font_size=12, color=(0, 0, 0), font_name="helv", width=200, height=None):
        """Aggiunge testo modificabile alla pagina usando FreeText annotation"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            
            # Calcola altezza automatica se non specificata
            if height is None:
                height = font_size * 1.5
            
            # Crea un rettangolo per il testo
            rect = fitz.Rect(x, y, x + width, y + height)
            
            # Crea annotazione FreeText (testo modificabile)
            annot = page.add_freetext_annot(
                rect,
                text,
                fontsize=font_size,
                fontname=font_name,
                text_color=color,
                fill_color=(1, 1, 1)  # Sfondo bianco
            )
            annot.update()
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
    
    def redact_text(self, page_num, rect):
        """Rimuove testo in una regione specifica usando redaction"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            # Aggiungi area di redaction
            page.add_redact_annot(rect)
            # Applica redaction
            page.apply_redactions()
            return True
        except Exception as e:
            print(f"Errore nella redaction del testo: {e}")
            return False
    
    def cover_text_with_white(self, page_num, rect):
        """Copre testo con un rettangolo bianco"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            # Disegna un rettangolo bianco sopra il testo
            shape = page.new_shape()
            shape.draw_rect(rect)
            shape.finish(fill=(1, 1, 1), color=None)  # Bianco
            shape.commit()
            return True
        except Exception as e:
            print(f"Errore nella copertura del testo: {e}")
            return False
    
    def get_images_on_page(self, page_num):
        """Ottiene lista delle immagini nella pagina"""
        if not self.current_doc:
            return []
            
        try:
            page = self.current_doc[page_num]
            images = page.get_images()
            image_list = []
            for img_index, img in enumerate(images):
                xref = img[0]
                image_list.append({
                    'index': img_index,
                    'xref': xref,
                    'bbox': page.get_image_bbox(img)
                })
            return image_list
        except Exception as e:
            print(f"Errore nel recupero delle immagini: {e}")
            return []
    
    def delete_image_by_xref(self, page_num, xref):
        """Elimina un'immagine dalla pagina usando il suo xref"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            # Trova e rimuovi tutte le occorrenze dell'immagine
            page.delete_image(xref)
            return True
        except Exception as e:
            print(f"Errore nell'eliminazione dell'immagine: {e}")
            return False
    
    def modify_text_annotation(self, page_num, annot_index, new_text):
        """Modifica il contenuto di un'annotazione di testo"""
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            annots = list(page.annots())
            if 0 <= annot_index < len(annots):
                annot = annots[annot_index]
                annot.set_content(new_text)
                annot.update()
                return True
            return False
        except Exception as e:
            print(f"Errore nella modifica dell'annotazione: {e}")
            return False
    
    def get_text_annotations(self, page_num):
        """
        Ottiene tutte le annotazioni di testo (FreeText) su una pagina
        
        Returns:
            Lista di dict con: {
                'index': int,
                'rect': fitz.Rect,
                'text': str,
                'font_size': float,
                'color': tuple,
                'font_name': str
            }
        """
        if not self.current_doc:
            return []
            
        try:
            page = self.current_doc[page_num]
            text_annots = []
            
            for i, annot in enumerate(page.annots()):
                # FreeText annotations hanno type 2
                if annot.type[0] == 2:  # PDF_ANNOT_FREE_TEXT
                    info = {
                        'index': i,
                        'rect': annot.rect,
                        'text': annot.info.get('content', ''),
                        'font_size': annot.font_size if hasattr(annot, 'font_size') else 12,
                        'color': annot.colors.get('stroke', (0, 0, 0)),
                        'font_name': annot.info.get('fontname', 'helv')
                    }
                    text_annots.append(info)
            
            return text_annots
        except Exception as e:
            print(f"Errore nel recupero delle annotazioni di testo: {e}")
            return []
    
    def modify_text_properties(self, page_num, annot_index, **kwargs):
        """
        Modifica tutte le proprietà di un'annotazione di testo
        
        Args:
            page_num: Numero della pagina
            annot_index: Indice dell'annotazione
            **kwargs: Proprietà da modificare:
                - text: nuovo contenuto testuale
                - font_size: nuova dimensione font
                - color: nuovo colore (r, g, b) in range 0-1
                - font_name: nome del font ('helv', 'times', 'cour', etc.)
                - rect: nuovo rettangolo (x0, y0, x1, y1) per spostare/ridimensionare
                - fill_color: colore di sfondo (r, g, b)
        
        Returns:
            bool: True se successo, False altrimenti
        """
        if not self.current_doc:
            return False
            
        try:
            page = self.current_doc[page_num]
            annots = list(page.annots())
            
            if not (0 <= annot_index < len(annots)):
                return False
            
            annot = annots[annot_index]
            
            # Verifica che sia un'annotazione FreeText
            if annot.type[0] != 2:  # PDF_ANNOT_FREE_TEXT
                print("L'annotazione non è di tipo FreeText")
                return False
            
            # Modifica il testo
            if 'text' in kwargs:
                annot.set_info(content=kwargs['text'])
            
            # Modifica il rettangolo (posizione/dimensione)
            if 'rect' in kwargs:
                new_rect = kwargs['rect']
                if isinstance(new_rect, (list, tuple)) and len(new_rect) == 4:
                    annot.set_rect(fitz.Rect(new_rect))
                elif isinstance(new_rect, fitz.Rect):
                    annot.set_rect(new_rect)
            
            # Modifica font size
            if 'font_size' in kwargs:
                # Per modificare font size dobbiamo ricreare l'annotazione
                # Salviamo le proprietà attuali
                current_rect = annot.rect
                current_text = annot.info.get('content', '')
                current_color = annot.colors.get('stroke', (0, 0, 0))
                current_fill = annot.colors.get('fill', (1, 1, 1))
                current_font = kwargs.get('font_name', annot.info.get('fontname', 'helv'))
                
                # Elimina l'annotazione vecchia
                page.delete_annot(annot)
                
                # Crea nuova annotazione con le proprietà aggiornate
                new_annot = page.add_freetext_annot(
                    current_rect,
                    kwargs.get('text', current_text),
                    fontsize=kwargs['font_size'],
                    fontname=current_font,
                    text_color=kwargs.get('color', current_color),
                    fill_color=kwargs.get('fill_color', current_fill)
                )
                new_annot.update()
            else:
                # Se non cambiamo font size, possiamo solo aggiornare colori
                if 'color' in kwargs:
                    annot.set_colors(stroke=kwargs['color'])
                if 'fill_color' in kwargs:
                    annot.set_colors(fill=kwargs['fill_color'])
                
                annot.update()
            
            return True
        except Exception as e:
            print(f"Errore nella modifica delle proprietà del testo: {e}")
            return False
    
    def get_annotation_at_point(self, page_num, x, y):
        """
        Trova l'annotazione che si trova nel punto specificato
        
        Args:
            page_num: Numero della pagina
            x, y: Coordinate del punto
            
        Returns:
            tuple: (index, annotation) o (None, None) se non trovata
        """
        if not self.current_doc:
            return None, None
            
        try:
            page = self.current_doc[page_num]
            point = fitz.Point(x, y)
            
            for i, annot in enumerate(page.annots()):
                if annot.rect.contains(point):
                    return i, annot
            
            return None, None
        except Exception as e:
            print(f"Errore nella ricerca dell'annotazione: {e}")
            return None, None