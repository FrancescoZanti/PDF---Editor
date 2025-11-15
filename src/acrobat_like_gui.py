from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QLabel, QPushButton, QFileDialog, QMessageBox, QFrame,
                               QListWidget, QSpinBox, QRadioButton, QButtonGroup,
                               QGroupBox, QScrollArea, QColorDialog, QInputDialog,
                               QMenuBar, QMenu, QToolBar, QSplitter, QDialog, QTextEdit,
                               QComboBox, QGridLayout)
from PySide6.QtCore import Qt, QPoint, QRect as QtRect, Signal
from PySide6.QtGui import QPixmap, QImage, QPainter, QPen, QColor, QFont, QAction
from PIL import Image
import io
import os
from advanced_pdf_editor import AdvancedPDFEditor
from theme_manager import theme_manager
from user_config import user_config
import fitz

class AcrobatLikeGUI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PDF Editor Pro - Advanced PDF Editor")
        self.resize(1200, 800)
        
        # Applica il tema
        theme_setting = user_config.get("theme", "auto")
        if theme_setting == "auto":
            current_theme = theme_manager.get_theme()
        else:
            current_theme = theme_setting
            theme_manager.current_theme = current_theme
        self.setStyleSheet(theme_manager.get_stylesheet())
        
        # Editor PDF avanzato
        self.pdf_editor = AdvancedPDFEditor()
        
        # Variabili di stato
        self.current_tool = "select"
        self.current_color = QColor(0, 0, 255)  # Blu default
        self.line_width = 2
        self.font_size = 12
        
        # Canvas per il disegno
        self.canvas_label = None
        self.canvas_pixmap = None
        self.drawing = False
        self.draw_start_x = 0
        self.draw_start_y = 0
        self.current_points = []
        
        # Variabili per la selezione e modifica testo
        self.selected_annotation = None  # (page_num, annot_index, annotation_obj)
        self.dragging_annotation = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura l'interfaccia utente stile Acrobat"""
        # Menu bar
        self.create_menu_bar()
        
        # Toolbar principale
        self.create_main_toolbar()
        
        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Splitter per pannelli ridimensionabili
        splitter = QSplitter(Qt.Horizontal)
        
        # Pannello sinistro (navigazione e strumenti)
        self.left_panel = QWidget()
        self.left_panel.setFixedWidth(250)
        self.left_panel.setStyleSheet(theme_manager.get_panel_style("side"))
        splitter.addWidget(self.left_panel)
        
        # Area centrale (visualizzazione PDF)
        self.center_panel = QWidget()
        self.center_panel.setStyleSheet(theme_manager.get_panel_style("center"))
        splitter.addWidget(self.center_panel)
        
        # Pannello destro (proprietà e commenti)
        self.right_panel = QWidget()
        self.right_panel.setFixedWidth(250)
        self.right_panel.setStyleSheet(theme_manager.get_panel_style("side"))
        splitter.addWidget(self.right_panel)
        
        # Imposta dimensioni iniziali del splitter
        splitter.setSizes([250, 700, 250])
        
        main_layout.addWidget(splitter)
        
        # Configura i pannelli
        self.setup_left_panel()
        self.setup_center_panel()
        self.setup_right_panel()
        
        # Status bar
        self.create_status_bar()
        
    def create_menu_bar(self):
        """Crea la barra dei menu"""
        menubar = self.menuBar()
        
        # Menu File
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Apri PDF", self)
        open_action.triggered.connect(self.open_pdf)
        file_menu.addAction(open_action)
        
        save_action = QAction("Salva", self)
        save_action.triggered.connect(self.save_pdf)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Salva come...", self)
        save_as_action.triggered.connect(self.save_pdf_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Esci", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menu Modifica
        edit_menu = menubar.addMenu("Modifica")
        
        undo_action = QAction("Annulla", self)
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Ripeti", self)
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        copy_action = QAction("Copia", self)
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Incolla", self)
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        modify_text_action = QAction("Modifica testo annotazione", self)
        modify_text_action.triggered.connect(self.modify_text_annotation)
        edit_menu.addAction(modify_text_action)
        
        # Menu Visualizza
        view_menu = menubar.addMenu("Visualizza")
        
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        fit_window_action = QAction("Adatta alla finestra", self)
        fit_window_action.triggered.connect(self.fit_to_window)
        view_menu.addAction(fit_window_action)
        
        # Menu Strumenti
        tools_menu = menubar.addMenu("Strumenti")
        
        text_action = QAction("Aggiungi testo", self)
        text_action.triggered.connect(lambda: self.set_tool("text"))
        tools_menu.addAction(text_action)
        
        highlight_action = QAction("Evidenziatore", self)
        highlight_action.triggered.connect(lambda: self.set_tool("highlight"))
        tools_menu.addAction(highlight_action)
        
        note_action = QAction("Note adesive", self)
        note_action.triggered.connect(lambda: self.set_tool("note"))
        tools_menu.addAction(note_action)
        
        freehand_action = QAction("Disegno libero", self)
        freehand_action.triggered.connect(lambda: self.set_tool("freehand"))
        tools_menu.addAction(freehand_action)
        
    def create_main_toolbar(self):
        """Crea la toolbar principale"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        toolbar.setStyleSheet("background-color: #d0d0d0; padding: 5px;")
        self.addToolBar(toolbar)
        
        # Pulsanti principali
        open_action = QAction("📁 Apri", self)
        open_action.triggered.connect(self.open_pdf)
        toolbar.addAction(open_action)
        
        save_action = QAction("💾 Salva", self)
        save_action.triggered.connect(self.save_pdf)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Strumenti
        select_action = QAction("🔍 Seleziona", self)
        select_action.triggered.connect(lambda: self.set_tool("select"))
        toolbar.addAction(select_action)
        
        text_action = QAction("T Testo", self)
        text_action.triggered.connect(lambda: self.set_tool("text"))
        toolbar.addAction(text_action)
        
        highlight_action = QAction("🖍️ Evidenzia", self)
        highlight_action.triggered.connect(lambda: self.set_tool("highlight"))
        toolbar.addAction(highlight_action)
        
        note_action = QAction("📝 Nota", self)
        note_action.triggered.connect(lambda: self.set_tool("note"))
        toolbar.addAction(note_action)
        
        rect_action = QAction("⬜ Rettangolo", self)
        rect_action.triggered.connect(lambda: self.set_tool("rectangle"))
        toolbar.addAction(rect_action)
        
        circle_action = QAction("⭕ Cerchio", self)
        circle_action.triggered.connect(lambda: self.set_tool("circle"))
        toolbar.addAction(circle_action)
        
        toolbar.addSeparator()
        
        # Strumenti per immagini e rimozione
        image_action = QAction("🖼️ Immagine", self)
        image_action.triggered.connect(lambda: self.set_tool("image"))
        toolbar.addAction(image_action)
        
        delete_action = QAction("🗑️ Elimina", self)
        delete_action.triggered.connect(lambda: self.set_tool("delete"))
        toolbar.addAction(delete_action)
        
        toolbar.addSeparator()
        
        # Zoom
        zoom_in_action = QAction("🔍+ Zoom In", self)
        zoom_in_action.triggered.connect(self.zoom_in)
        toolbar.addAction(zoom_in_action)
        
        zoom_out_action = QAction("🔍- Zoom Out", self)
        zoom_out_action.triggered.connect(self.zoom_out)
        toolbar.addAction(zoom_out_action)
        
        toolbar.addSeparator()
        
        # Controlli colore e spessore
        color_label = QLabel("Colore:")
        toolbar.addWidget(color_label)
        
        self.color_button = QPushButton()
        self.color_button.setFixedSize(30, 20)
        self.color_button.setStyleSheet("background-color: blue;")
        self.color_button.clicked.connect(self.choose_color)
        toolbar.addWidget(self.color_button)
        
        width_label = QLabel("  Spessore:")
        toolbar.addWidget(width_label)
        
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 10)
        self.width_spinbox.setValue(2)
        self.width_spinbox.valueChanged.connect(lambda v: setattr(self, 'line_width', v))
        toolbar.addWidget(self.width_spinbox)
        
    def setup_left_panel(self):
        """Configura il pannello sinistro"""
        layout = QVBoxLayout(self.left_panel)
        
        # Titolo
        title_label = QLabel("NAVIGAZIONE")
        title_label.setFont(QFont('Arial', 10, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Controlli pagina
        page_group = QGroupBox("Pagina")
        page_layout = QVBoxLayout(page_group)
        
        nav_layout = QHBoxLayout()
        prev_btn = QPushButton("◀")
        prev_btn.clicked.connect(self.prev_page)
        prev_btn.setFixedWidth(40)
        nav_layout.addWidget(prev_btn)
        
        self.page_label = QLabel("1 / 1")
        self.page_label.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(self.page_label)
        
        next_btn = QPushButton("▶")
        next_btn.clicked.connect(self.next_page)
        next_btn.setFixedWidth(40)
        nav_layout.addWidget(next_btn)
        
        page_layout.addLayout(nav_layout)
        layout.addWidget(page_group)
        
        # Lista miniature
        thumb_group = QGroupBox("Miniature")
        thumb_layout = QVBoxLayout(thumb_group)
        
        self.thumb_listbox = QListWidget()
        thumb_layout.addWidget(self.thumb_listbox)
        
        layout.addWidget(thumb_group, 1)  # Stretch factor 1
        
        # Strumenti rapidi
        tools_group = QGroupBox("Strumenti")
        tools_layout = QVBoxLayout(tools_group)
        
        self.tool_button_group = QButtonGroup()
        
        tool_buttons = [
            ("Seleziona", "select"),
            ("Testo", "text"),
            ("Evidenzia", "highlight"),
            ("Nota", "note"),
            ("Forma", "rectangle"),
            ("Immagine", "image"),
            ("Elimina", "delete")
        ]
        
        for text, tool in tool_buttons:
            radio = QRadioButton(text)
            radio.setProperty("tool", tool)
            if tool == "select":
                radio.setChecked(True)
            radio.toggled.connect(lambda checked, t=tool: self.set_tool(t) if checked else None)
            self.tool_button_group.addButton(radio)
            tools_layout.addWidget(radio)
        
        layout.addWidget(tools_group)
        
    def setup_center_panel(self):
        """Configura il pannello centrale per la visualizzazione PDF"""
        layout = QVBoxLayout(self.center_panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Controlli zoom
        zoom_frame = QWidget()
        zoom_frame.setFixedHeight(40)
        zoom_frame.setStyleSheet(theme_manager.get_panel_style("center"))
        zoom_layout = QHBoxLayout(zoom_frame)
        
        zoom_out_btn = QPushButton("🔍-")
        zoom_out_btn.clicked.connect(self.zoom_out)
        zoom_layout.addWidget(zoom_out_btn)
        
        self.zoom_label = QLabel("100%")
        zoom_layout.addWidget(self.zoom_label)
        
        zoom_in_btn = QPushButton("🔍+")
        zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_layout.addWidget(zoom_in_btn)
        
        fit_btn = QPushButton("Adatta")
        fit_btn.clicked.connect(self.fit_to_window)
        zoom_layout.addWidget(fit_btn)
        
        zoom_layout.addStretch()
        
        layout.addWidget(zoom_frame)
        
        # Area di visualizzazione PDF con scrolling
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(theme_manager.get_panel_style("center"))
        
        self.canvas_label = QLabel()
        self.canvas_label.setAlignment(Qt.AlignCenter)
        self.canvas_label.setStyleSheet(theme_manager.get_panel_style("center"))
        
        # Abilita mouse tracking per interazioni
        self.canvas_label.setMouseTracking(True)
        self.canvas_label.mousePressEvent = self.on_canvas_click
        self.canvas_label.mouseMoveEvent = self.on_canvas_drag
        self.canvas_label.mouseReleaseEvent = self.on_canvas_release
        
        scroll_area.setWidget(self.canvas_label)
        layout.addWidget(scroll_area)
        
    def setup_right_panel(self):
        """Configura il pannello destro"""
        layout = QVBoxLayout(self.right_panel)
        
        # Titolo
        title_label = QLabel("PROPRIETÀ")
        title_label.setFont(QFont('Arial', 10, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Proprietà strumento corrente
        props_group = QGroupBox("Strumento")
        props_layout = QVBoxLayout(props_group)
        
        props_layout.addWidget(QLabel("Dimensione font:"))
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(8, 72)
        self.font_size_spinbox.setValue(12)
        self.font_size_spinbox.valueChanged.connect(lambda v: setattr(self, 'font_size', v))
        props_layout.addWidget(self.font_size_spinbox)
        
        layout.addWidget(props_group)
        
        # Commenti e annotazioni
        comments_group = QGroupBox("Commenti")
        comments_layout = QVBoxLayout(comments_group)
        
        self.comments_listbox = QListWidget()
        comments_layout.addWidget(self.comments_listbox)
        
        layout.addWidget(comments_group, 1)  # Stretch factor 1
        
        # Pulsanti azioni
        actions_layout = QVBoxLayout()
        
        delete_btn = QPushButton("Elimina")
        delete_btn.clicked.connect(self.delete_selected)
        actions_layout.addWidget(delete_btn)
        
        props_btn = QPushButton("Proprietà")
        props_btn.clicked.connect(self.show_properties)
        actions_layout.addWidget(props_btn)
        
        layout.addLayout(actions_layout)
        
    def create_status_bar(self):
        """Crea la barra di stato"""
        status_bar = self.statusBar()
        status_bar.setStyleSheet("background-color: #d0d0d0;")
        
        self.status_label = QLabel("Pronto")
        status_bar.addWidget(self.status_label, 1)
        
        self.doc_info_label = QLabel("")
        status_bar.addPermanentWidget(self.doc_info_label)
        
    def open_pdf(self):
        """Apre un file PDF"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Apri PDF",
            "",
            "PDF files (*.pdf)"
        )
        
        if file_path:
            if self.pdf_editor.open_pdf(file_path):
                self.update_display()
                self.update_thumbnails()
                self.status_label.setText(f"PDF aperto: {os.path.basename(file_path)}")
                
                # Aggiorna info documento
                page_count = self.pdf_editor.get_page_count()
                self.doc_info_label.setText(f"Pagine: {page_count}")
                self.page_label.setText(f"1 / {page_count}")
            else:
                QMessageBox.critical(self, "Errore", "Impossibile aprire il file PDF")
    
    def save_pdf(self):
        """Salva il PDF corrente"""
        if not self.pdf_editor.current_doc:
            QMessageBox.warning(self, "Attenzione", "Nessun PDF aperto")
            return
            
        # Per ora salva come nuovo file
        self.save_pdf_as()
    
    def save_pdf_as(self):
        """Salva il PDF con un nuovo nome"""
        if not self.pdf_editor.current_doc:
            QMessageBox.warning(self, "Attenzione", "Nessun PDF aperto")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Salva PDF",
            "",
            "PDF files (*.pdf)"
        )
        
        if file_path:
            if self.pdf_editor.save_pdf(file_path):
                self.status_label.setText(f"PDF salvato: {os.path.basename(file_path)}")
                QMessageBox.information(self, "Successo", "PDF salvato correttamente!")
            else:
                QMessageBox.critical(self, "Errore", "Errore nel salvataggio del PDF")
    
    def set_tool(self, tool):
        """Imposta lo strumento corrente"""
        self.current_tool = tool
        self.status_label.setText(f"Strumento selezionato: {tool}")
    
    def choose_color(self):
        """Apre il selettore colore"""
        color = QColorDialog.getColor(self.current_color, self, "Scegli colore")
        if color.isValid():
            self.current_color = color
            # Aggiorna il pulsante colore
            self.color_button.setStyleSheet(f"background-color: {color.name()};")

    
    def update_display(self):
        """Aggiorna la visualizzazione della pagina corrente"""
        if not self.pdf_editor.current_doc:
            return
            
        image = self.pdf_editor.get_page_image()
        if image:
            # Converti PIL Image a QPixmap
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            qimage = QImage()
            qimage.loadFromData(img_byte_arr)
            self.canvas_pixmap = QPixmap.fromImage(qimage)
            
            # Mostra l'immagine
            self.canvas_label.setPixmap(self.canvas_pixmap)
            
            # Aggiorna label zoom
            zoom_percent = int(self.pdf_editor.zoom_level * 100)
            self.zoom_label.setText(f"{zoom_percent}%")
    
    def update_thumbnails(self):
        """Aggiorna la lista delle miniature"""
        self.thumb_listbox.clear()
        
        if self.pdf_editor.current_doc:
            page_count = self.pdf_editor.get_page_count()
            for i in range(page_count):
                self.thumb_listbox.addItem(f"Pagina {i+1}")
    
    def prev_page(self):
        """Vai alla pagina precedente"""
        if self.pdf_editor.current_doc and self.pdf_editor.page_num > 0:
            self.pdf_editor.page_num -= 1
            self.update_display()
            page_count = self.pdf_editor.get_page_count()
            self.page_label.setText(f"{self.pdf_editor.page_num + 1} / {page_count}")
    
    def next_page(self):
        """Vai alla pagina successiva"""
        if (self.pdf_editor.current_doc and 
            self.pdf_editor.page_num < self.pdf_editor.get_page_count() - 1):
            self.pdf_editor.page_num += 1
            self.update_display()
            page_count = self.pdf_editor.get_page_count()
            self.page_label.setText(f"{self.pdf_editor.page_num + 1} / {page_count}")
    
    def zoom_in(self):
        """Aumenta lo zoom"""
        self.pdf_editor.zoom_level = min(3.0, self.pdf_editor.zoom_level * 1.2)
        self.update_display()
    
    def zoom_out(self):
        """Diminuisce lo zoom"""
        self.pdf_editor.zoom_level = max(0.2, self.pdf_editor.zoom_level / 1.2)
        self.update_display()
    
    def fit_to_window(self):
        """Adatta il PDF alla finestra"""
        if not self.pdf_editor.current_doc:
            return
            
        # Calcola zoom per adattare alla finestra
        canvas_width = self.canvas_label.width()
        canvas_height = self.canvas_label.height()
        
        if canvas_width > 1 and canvas_height > 1:
            # Ottieni dimensioni pagina originale
            page = self.pdf_editor.current_doc[self.pdf_editor.page_num]
            page_rect = page.rect
            
            zoom_x = canvas_width / page_rect.width
            zoom_y = canvas_height / page_rect.height
            
            self.pdf_editor.zoom_level = min(zoom_x, zoom_y) * 0.9  # 90% per margini
            self.update_display()
    
    def on_canvas_click(self, event):
        """Gestisce click sul canvas"""
        if not self.pdf_editor.current_doc:
            return
            
        # Converti coordinate a coordinate PDF
        pdf_x = event.pos().x() / self.pdf_editor.zoom_level
        pdf_y = event.pos().y() / self.pdf_editor.zoom_level
        
        page_num = self.pdf_editor.page_num
        
        # Se tool è select, controlla se clicchiamo su un'annotazione di testo
        if self.current_tool == "select":
            result = self.pdf_editor.get_annotation_at_point(page_num, pdf_x, pdf_y)
            if result:
                annot_index, annot = result
                # Verifica che sia un'annotazione di testo (FreeText)
                if annot.type[0] == 2:  # FreeText annotation
                    self.selected_annotation = (page_num, annot_index, annot)
                    # Doppio click apre dialog di modifica
                    if event.type() == event.Type.MouseButtonDblClick:
                        self.edit_text_annotation_properties()
                    else:
                        # Click singolo: prepara per drag
                        rect = annot.rect
                        self.drag_offset_x = pdf_x - rect.x0
                        self.drag_offset_y = pdf_y - rect.y0
                        self.status_label.setText(f"Annotazione selezionata. Doppio click per modificare, trascina per spostare.")
                    return
            else:
                # Click su area vuota: deseleziona
                self.selected_annotation = None
                self.status_label.setText("")
        
        if self.current_tool == "text":
            self.add_text_at_position(pdf_x, pdf_y)
        elif self.current_tool == "note":
            self.add_note_at_position(pdf_x, pdf_y)
        elif self.current_tool == "image":
            self.add_image_at_position(pdf_x, pdf_y)
        elif self.current_tool == "delete":
            self.delete_at_position(pdf_x, pdf_y)
        elif self.current_tool in ["rectangle", "circle", "line", "arrow"]:
            self.draw_start_x = pdf_x
            self.draw_start_y = pdf_y
            self.drawing = True
        elif self.current_tool == "freehand":
            self.current_points = [(pdf_x, pdf_y)]
            self.drawing = True
    
    def on_canvas_drag(self, event):
        """Gestisce trascinamento sul canvas"""
        pdf_x = event.pos().x() / self.pdf_editor.zoom_level
        pdf_y = event.pos().y() / self.pdf_editor.zoom_level
        
        # Se stiamo trascinando un'annotazione selezionata
        if self.current_tool == "select" and self.selected_annotation and not self.dragging_annotation:
            self.dragging_annotation = True
            self.status_label.setText("Trascinamento annotazione...")
            return
        
        if not self.drawing:
            return
        
        if self.current_tool == "freehand":
            self.current_points.append((pdf_x, pdf_y))
    
    def on_canvas_release(self, event):
        """Gestisce rilascio del mouse sul canvas"""
        pdf_x = event.pos().x() / self.pdf_editor.zoom_level
        pdf_y = event.pos().y() / self.pdf_editor.zoom_level
        
        # Se stavamo trascinando un'annotazione, aggiorna la sua posizione
        if self.dragging_annotation and self.selected_annotation:
            page_num, annot_index, annot = self.selected_annotation
            
            # Calcola nuova posizione considerando l'offset
            new_x = pdf_x - self.drag_offset_x
            new_y = pdf_y - self.drag_offset_y
            
            # Calcola nuovo rettangolo mantenendo dimensioni originali
            old_rect = annot.rect
            width = old_rect.x1 - old_rect.x0
            height = old_rect.y1 - old_rect.y0
            new_rect = fitz.Rect(new_x, new_y, new_x + width, new_y + height)
            
            # Aggiorna posizione
            if self.pdf_editor.modify_text_properties(page_num, annot_index, rect=new_rect):
                self.update_display()
                self.status_label.setText("Annotazione spostata con successo")
            else:
                self.status_label.setText("Errore nello spostamento dell'annotazione")
            
            self.dragging_annotation = False
            return
        
        if not self.drawing:
            return
            
        page_num = self.pdf_editor.page_num
        
        # Converti QColor a tuple RGB (0-1)
        r, g, b = self.current_color.redF(), self.current_color.greenF(), self.current_color.blueF()
        color_tuple = (r, g, b)
        
        if self.current_tool == "rectangle":
            rect = fitz.Rect(self.draw_start_x, self.draw_start_y, pdf_x, pdf_y)
            self.pdf_editor.add_rectangle(page_num, rect, color_tuple, width=self.line_width)
        elif self.current_tool == "circle":
            rect = fitz.Rect(self.draw_start_x, self.draw_start_y, pdf_x, pdf_y)
            self.pdf_editor.add_circle(page_num, rect, color_tuple, width=self.line_width)
        elif self.current_tool == "line":
            start = fitz.Point(self.draw_start_x, self.draw_start_y)
            end = fitz.Point(pdf_x, pdf_y)
            self.pdf_editor.add_line(page_num, start, end, color_tuple, width=self.line_width)
        elif self.current_tool == "arrow":
            start = fitz.Point(self.draw_start_x, self.draw_start_y)
            end = fitz.Point(pdf_x, pdf_y)
            self.pdf_editor.add_arrow(page_num, start, end, color_tuple, width=self.line_width)
        elif self.current_tool == "freehand" and len(self.current_points) > 1:
            points = [fitz.Point(x, y) for x, y in self.current_points]
            self.pdf_editor.add_freehand_drawing(page_num, points, color_tuple, width=self.line_width)
        
        self.drawing = False
        self.current_points = []
        self.update_display()
    
    def add_text_at_position(self, x, y):
        """Aggiunge testo alla posizione specificata"""
        text, ok = QInputDialog.getText(self, "Aggiungi testo", "Inserisci il testo:")
        if ok and text:
            r, g, b = self.current_color.redF(), self.current_color.greenF(), self.current_color.blueF()
            self.pdf_editor.add_text(self.pdf_editor.page_num, x, y, text, 
                                   font_size=self.font_size, color=(r, g, b))
            self.update_display()
    
    def add_note_at_position(self, x, y):
        """Aggiunge una nota alla posizione specificata"""
        content, ok = QInputDialog.getText(self, "Aggiungi nota", "Inserisci il contenuto della nota:")
        if ok and content:
            self.pdf_editor.add_note(self.pdf_editor.page_num, x, y, content)
            self.update_display()
    
    def add_image_at_position(self, start_x, start_y):
        """Aggiunge un'immagine alla posizione specificata"""
        # Apri dialog per selezionare immagine
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona immagine",
            "",
            "Immagini (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            # Chiedi dimensioni dell'immagine
            width, ok = QInputDialog.getInt(self, "Dimensione immagine", "Larghezza (punti):", 200, 10, 1000)
            if ok:
                height, ok = QInputDialog.getInt(self, "Dimensione immagine", "Altezza (punti):", 200, 10, 1000)
                if ok:
                    import fitz
                    rect = fitz.Rect(start_x, start_y, start_x + width, start_y + height)
                    if self.pdf_editor.add_image(self.pdf_editor.page_num, rect, file_path):
                        self.update_display()
                        self.status_label.setText("Immagine aggiunta con successo")
                    else:
                        QMessageBox.critical(self, "Errore", "Impossibile aggiungere l'immagine")
    
    def delete_at_position(self, x, y):
        """Elimina elemento alla posizione specificata"""
        page_num = self.pdf_editor.page_num
        
        # Menu per scegliere cosa eliminare
        from PySide6.QtWidgets import QMenu
        menu = QMenu(self)
        
        text_action = menu.addAction("Rimuovi testo (copri con bianco)")
        redact_action = menu.addAction("Rimuovi testo (redazione permanente)")
        annot_action = menu.addAction("Elimina annotazione")
        image_action = menu.addAction("Elimina immagine")
        
        action = menu.exec(self.canvas_label.mapToGlobal(QPoint(int(x * self.pdf_editor.zoom_level), 
                                                                  int(y * self.pdf_editor.zoom_level))))
        
        if action == text_action or action == redact_action:
            # Chiedi area di selezione
            width, ok = QInputDialog.getInt(self, "Area di rimozione", "Larghezza (punti):", 100, 10, 1000)
            if ok:
                height, ok = QInputDialog.getInt(self, "Area di rimozione", "Altezza (punti):", 50, 10, 1000)
                if ok:
                    import fitz
                    rect = fitz.Rect(x, y, x + width, y + height)
                    
                    if action == text_action:
                        if self.pdf_editor.cover_text_with_white(page_num, rect):
                            self.update_display()
                            self.status_label.setText("Testo coperto con successo")
                        else:
                            QMessageBox.critical(self, "Errore", "Impossibile coprire il testo")
                    else:  # redact_action
                        if self.pdf_editor.redact_text(page_num, rect):
                            self.update_display()
                            self.status_label.setText("Testo rimosso con successo")
                        else:
                            QMessageBox.critical(self, "Errore", "Impossibile rimuovere il testo")
        
        elif action == annot_action:
            # Ottieni annotazioni sulla pagina
            annotations = self.pdf_editor.get_annotations(page_num)
            if not annotations:
                QMessageBox.information(self, "Info", "Nessuna annotazione trovata su questa pagina")
                return
            
            # Mostra lista di annotazioni
            annot_list = [f"{i}: {a['type']} - {a['content'][:30]}" for i, a in enumerate(annotations)]
            annot_str, ok = QInputDialog.getItem(self, "Elimina annotazione", 
                                                  "Seleziona annotazione:", annot_list, 0, False)
            if ok:
                annot_index = int(annot_str.split(":")[0])
                if self.pdf_editor.delete_annotation(page_num, annot_index):
                    self.update_display()
                    self.status_label.setText("Annotazione eliminata")
                else:
                    QMessageBox.critical(self, "Errore", "Impossibile eliminare l'annotazione")
        
        elif action == image_action:
            # Ottieni immagini sulla pagina
            images = self.pdf_editor.get_images_on_page(page_num)
            if not images:
                QMessageBox.information(self, "Info", "Nessuna immagine trovata su questa pagina")
                return
            
            # Mostra lista di immagini
            image_list = [f"{i}: Immagine xref={img['xref']}" for i, img in enumerate(images)]
            image_str, ok = QInputDialog.getItem(self, "Elimina immagine", 
                                                  "Seleziona immagine:", image_list, 0, False)
            if ok:
                img_index = int(image_str.split(":")[0])
                xref = images[img_index]['xref']
                if self.pdf_editor.delete_image_by_xref(page_num, xref):
                    self.update_display()
                    self.status_label.setText("Immagine eliminata")
                else:
                    QMessageBox.critical(self, "Errore", "Impossibile eliminare l'immagine")
    
    # Metodi placeholder per le funzionalità del menu
    def undo(self):
        self.status_label.setText("Annulla - non ancora implementato")
    
    def redo(self):
        self.status_label.setText("Ripeti - non ancora implementato")
    
    def copy(self):
        self.status_label.setText("Copia - non ancora implementato")
    
    def paste(self):
        self.status_label.setText("Incolla - non ancora implementato")
    
    def delete_selected(self):
        self.status_label.setText("Elimina - non ancora implementato")
    
    def show_properties(self):
        self.status_label.setText("Proprietà - non ancora implementato")
    
    def edit_text_annotation_properties(self):
        """Apre un dialog per modificare tutte le proprietà di un'annotazione di testo"""
        if not self.selected_annotation:
            return
        
        page_num, annot_index, annot = self.selected_annotation
        
        # Ottieni proprietà correnti
        text_annots = self.pdf_editor.get_text_annotations(page_num)
        if not text_annots or annot_index >= len(text_annots):
            QMessageBox.warning(self, "Errore", "Impossibile ottenere proprietà dell'annotazione")
            return
        
        current_props = text_annots[annot_index]
        
        # Crea dialog personalizzato
        dialog = QDialog(self)
        dialog.setWindowTitle("Modifica Proprietà Testo")
        dialog.setMinimumWidth(400)
        layout = QVBoxLayout(dialog)
        
        # Campo testo
        layout.addWidget(QLabel("Testo:"))
        text_edit = QTextEdit()
        text_edit.setPlainText(current_props['text'])
        text_edit.setMaximumHeight(100)
        layout.addWidget(text_edit)
        
        # Font size
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Dimensione font:"))
        font_size_spin = QSpinBox()
        font_size_spin.setRange(6, 72)
        font_size_spin.setValue(int(current_props['font_size']))
        font_layout.addWidget(font_size_spin)
        layout.addLayout(font_layout)
        
        # Font name
        font_name_layout = QHBoxLayout()
        font_name_layout.addWidget(QLabel("Font:"))
        font_combo = QComboBox()
        fonts = ["helv", "times", "cour", "symb"]  # Font standard PDF
        font_combo.addItems(fonts)
        current_font = current_props.get('font_name', 'helv')
        if current_font in fonts:
            font_combo.setCurrentText(current_font)
        font_name_layout.addWidget(font_combo)
        layout.addLayout(font_name_layout)
        
        # Colore
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Colore testo:"))
        color_button = QPushButton("Scegli colore")
        current_color = current_props.get('color', (0, 0, 0))
        selected_color = QColor(int(current_color[0]*255), int(current_color[1]*255), int(current_color[2]*255))
        color_button.setStyleSheet(f"background-color: {selected_color.name()}; color: white;")
        
        def choose_color():
            nonlocal selected_color
            color = QColorDialog.getColor(selected_color, dialog, "Seleziona colore testo")
            if color.isValid():
                selected_color = color
                color_button.setStyleSheet(f"background-color: {color.name()}; color: white;")
        
        color_button.clicked.connect(choose_color)
        color_layout.addWidget(color_button)
        layout.addLayout(color_layout)
        
        # Posizione
        pos_group = QGroupBox("Posizione")
        pos_layout = QGridLayout()
        
        rect = current_props['rect']
        pos_x_spin = QSpinBox()
        pos_x_spin.setRange(0, 5000)
        pos_x_spin.setValue(int(rect.x0))
        pos_y_spin = QSpinBox()
        pos_y_spin.setRange(0, 5000)
        pos_y_spin.setValue(int(rect.y0))
        
        pos_layout.addWidget(QLabel("X:"), 0, 0)
        pos_layout.addWidget(pos_x_spin, 0, 1)
        pos_layout.addWidget(QLabel("Y:"), 1, 0)
        pos_layout.addWidget(pos_y_spin, 1, 1)
        pos_group.setLayout(pos_layout)
        layout.addWidget(pos_group)
        
        # Pulsanti
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Annulla")
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        
        # Mostra dialog
        if dialog.exec() == QDialog.Accepted:
            # Raccogli nuovi valori
            new_text = text_edit.toPlainText()
            new_font_size = font_size_spin.value()
            new_font_name = font_combo.currentText()
            new_color = (selected_color.redF(), selected_color.greenF(), selected_color.blueF())
            
            # Calcola nuovo rettangolo con nuova posizione
            width = rect.x1 - rect.x0
            height = rect.y1 - rect.y0
            new_x = pos_x_spin.value()
            new_y = pos_y_spin.value()
            new_rect = fitz.Rect(new_x, new_y, new_x + width, new_y + height)
            
            # Applica modifiche
            success = self.pdf_editor.modify_text_properties(
                page_num, annot_index,
                text=new_text,
                font_size=new_font_size,
                font_name=new_font_name,
                color=new_color,
                rect=new_rect
            )
            
            if success:
                self.update_display()
                self.status_label.setText("Proprietà testo aggiornate con successo")
                # Aggiorna annotazione selezionata
                result = self.pdf_editor.get_annotation_at_point(page_num, new_x + 5, new_y + 5)
                if result:
                    self.selected_annotation = (page_num, result[0], result[1])
            else:
                QMessageBox.critical(self, "Errore", "Impossibile modificare le proprietà del testo")
    
    def modify_text_annotation(self):
        """Modifica il testo di un'annotazione esistente (metodo legacy)"""
        if not self.pdf_editor.current_doc:
            QMessageBox.warning(self, "Attenzione", "Nessun PDF aperto")
            return
        
        page_num = self.pdf_editor.page_num
        annotations = self.pdf_editor.get_annotations(page_num)
        
        if not annotations:
            QMessageBox.information(self, "Info", "Nessuna annotazione trovata su questa pagina")
            return
        
        # Mostra lista di annotazioni
        annot_list = [f"{i}: {a['type']} - {a['content'][:50]}" for i, a in enumerate(annotations)]
        annot_str, ok = QInputDialog.getItem(self, "Modifica annotazione", 
                                              "Seleziona annotazione:", annot_list, 0, False)
        if ok:
            annot_index = int(annot_str.split(":")[0])
            old_content = annotations[annot_index]['content']
            
            new_text, ok = QInputDialog.getText(self, "Modifica testo", 
                                                 "Nuovo testo:", text=old_content)
            if ok:
                if self.pdf_editor.modify_text_annotation(page_num, annot_index, new_text):
                    self.update_display()
                    self.status_label.setText("Annotazione modificata")
                else:
                    QMessageBox.critical(self, "Errore", "Impossibile modificare l'annotazione")

def main():
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    window = AcrobatLikeGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()