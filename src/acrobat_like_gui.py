import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser, simpledialog
from PIL import Image, ImageTk
import io
import os
from advanced_pdf_editor import AdvancedPDFEditor
import fitz

class AcrobatLikeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Editor Pro - Advanced PDF Editor")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Editor PDF avanzato
        self.pdf_editor = AdvancedPDFEditor()
        
        # Variabili di stato
        self.current_tool = tk.StringVar(value="select")
        self.current_color = (0, 0, 1)  # Blu default
        self.line_width = tk.IntVar(value=2)
        self.font_size = tk.IntVar(value=12)
        
        # Canvas per il disegno
        self.canvas = None
        self.canvas_image = None
        self.drawing = False
        self.draw_start_x = 0
        self.draw_start_y = 0
        self.current_points = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configura l'interfaccia utente stile Acrobat"""
        # Menu bar
        self.create_menu_bar()
        
        # Toolbar principale
        self.create_main_toolbar()
        
        # Frame principale con pannelli
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(fill='both', expand=True)
        
        # Pannello sinistro (navigazione e strumenti)
        self.left_panel = tk.Frame(self.main_frame, width=250, bg='#e8e8e8')
        self.left_panel.pack(side='left', fill='y', padx=5, pady=5)
        self.left_panel.pack_propagate(False)
        
        # Area centrale (visualizzazione PDF)
        self.center_panel = tk.Frame(self.main_frame, bg='white')
        self.center_panel.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Pannello destro (proprietà e commenti)
        self.right_panel = tk.Frame(self.main_frame, width=250, bg='#e8e8e8')
        self.right_panel.pack(side='right', fill='y', padx=5, pady=5)
        self.right_panel.pack_propagate(False)
        
        # Configura i pannelli
        self.setup_left_panel()
        self.setup_center_panel()
        self.setup_right_panel()
        
        # Status bar
        self.create_status_bar()
        
    def create_menu_bar(self):
        """Crea la barra dei menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Apri PDF", command=self.open_pdf)
        file_menu.add_command(label="Salva", command=self.save_pdf)
        file_menu.add_command(label="Salva come...", command=self.save_pdf_as)
        file_menu.add_separator()
        file_menu.add_command(label="Esci", command=self.root.quit)
        
        # Menu Modifica
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Modifica", menu=edit_menu)
        edit_menu.add_command(label="Annulla", command=self.undo)
        edit_menu.add_command(label="Ripeti", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Copia", command=self.copy)
        edit_menu.add_command(label="Incolla", command=self.paste)
        
        # Menu Visualizza
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Visualizza", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self.zoom_in)
        view_menu.add_command(label="Zoom Out", command=self.zoom_out)
        view_menu.add_command(label="Adatta alla finestra", command=self.fit_to_window)
        
        # Menu Strumenti
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Strumenti", menu=tools_menu)
        tools_menu.add_command(label="Aggiungi testo", command=lambda: self.set_tool("text"))
        tools_menu.add_command(label="Evidenziatore", command=lambda: self.set_tool("highlight"))
        tools_menu.add_command(label="Note adesive", command=lambda: self.set_tool("note"))
        tools_menu.add_command(label="Disegno libero", command=lambda: self.set_tool("freehand"))
        
    def create_main_toolbar(self):
        """Crea la toolbar principale"""
        toolbar = tk.Frame(self.root, bg='#d0d0d0', height=50)
        toolbar.pack(fill='x', side='top')
        toolbar.pack_propagate(False)
        
        # Pulsanti toolbar
        buttons = [
            ("Apri", self.open_pdf, "📁"),
            ("Salva", self.save_pdf, "💾"),
            ("|", None, None),  # Separatore
            ("Seleziona", lambda: self.set_tool("select"), "🔍"),
            ("Testo", lambda: self.set_tool("text"), "T"),
            ("Evidenzia", lambda: self.set_tool("highlight"), "🖍️"),
            ("Nota", lambda: self.set_tool("note"), "📝"),
            ("Rettangolo", lambda: self.set_tool("rectangle"), "⬜"),
            ("Cerchio", lambda: self.set_tool("circle"), "⭕"),
            ("Linea", lambda: self.set_tool("line"), "📏"),
            ("Freccia", lambda: self.set_tool("arrow"), "➡️"),
            ("Disegno", lambda: self.set_tool("freehand"), "✏️"),
            ("|", None, None),  # Separatore
            ("Zoom In", self.zoom_in, "🔍+"),
            ("Zoom Out", self.zoom_out, "🔍-"),
        ]
        
        for i, (text, command, icon) in enumerate(buttons):
            if text == "|":
                separator = tk.Frame(toolbar, width=2, bg='#a0a0a0')
                separator.pack(side='left', fill='y', padx=5, pady=5)
            else:
                btn = tk.Button(toolbar, text=f"{icon}\\n{text}", command=command,
                               width=8, height=2, font=('Arial', 8),
                               relief='raised', bd=1)
                btn.pack(side='left', padx=2, pady=5)
        
        # Controlli colore e spessore
        color_frame = tk.Frame(toolbar, bg='#d0d0d0')
        color_frame.pack(side='right', padx=10, pady=5)
        
        tk.Label(color_frame, text="Colore:", bg='#d0d0d0').pack(side='left')
        self.color_button = tk.Button(color_frame, width=3, height=1, 
                                     bg='blue', command=self.choose_color)
        self.color_button.pack(side='left', padx=5)
        
        tk.Label(color_frame, text="Spessore:", bg='#d0d0d0').pack(side='left', padx=(10,0))
        width_spinbox = tk.Spinbox(color_frame, from_=1, to=10, width=5, 
                                  textvariable=self.line_width)
        width_spinbox.pack(side='left', padx=5)
        
    def setup_left_panel(self):
        """Configura il pannello sinistro"""
        # Titolo
        title_label = tk.Label(self.left_panel, text="NAVIGAZIONE", 
                              font=('Arial', 10, 'bold'), bg='#e8e8e8')
        title_label.pack(pady=10)
        
        # Controlli pagina
        page_frame = tk.LabelFrame(self.left_panel, text="Pagina", bg='#e8e8e8')
        page_frame.pack(fill='x', padx=10, pady=5)
        
        nav_frame = tk.Frame(page_frame, bg='#e8e8e8')
        nav_frame.pack(pady=5)
        
        tk.Button(nav_frame, text="◀", command=self.prev_page, width=3).pack(side='left')
        self.page_label = tk.Label(nav_frame, text="1 / 1", bg='#e8e8e8', width=8)
        self.page_label.pack(side='left', padx=5)
        tk.Button(nav_frame, text="▶", command=self.next_page, width=3).pack(side='left')
        
        # Lista miniature (placeholder)
        thumb_frame = tk.LabelFrame(self.left_panel, text="Miniature", bg='#e8e8e8')
        thumb_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.thumb_listbox = tk.Listbox(thumb_frame, height=10)
        thumb_scrollbar = tk.Scrollbar(thumb_frame, orient='vertical', 
                                      command=self.thumb_listbox.yview)
        self.thumb_listbox.configure(yscrollcommand=thumb_scrollbar.set)
        
        self.thumb_listbox.pack(side='left', fill='both', expand=True)
        thumb_scrollbar.pack(side='right', fill='y')
        
        # Strumenti rapidi
        tools_frame = tk.LabelFrame(self.left_panel, text="Strumenti", bg='#e8e8e8')
        tools_frame.pack(fill='x', padx=10, pady=5)
        
        tool_buttons = [
            ("Seleziona", "select"),
            ("Testo", "text"),
            ("Evidenzia", "highlight"),
            ("Nota", "note"),
            ("Forma", "rectangle")
        ]
        
        for text, tool in tool_buttons:
            tk.Radiobutton(tools_frame, text=text, variable=self.current_tool, 
                          value=tool, bg='#e8e8e8', 
                          command=lambda t=tool: self.set_tool(t)).pack(anchor='w')
        
    def setup_center_panel(self):
        """Configura il pannello centrale per la visualizzazione PDF"""
        # Frame per i controlli zoom
        zoom_frame = tk.Frame(self.center_panel, bg='white', height=30)
        zoom_frame.pack(fill='x', pady=(0, 5))
        zoom_frame.pack_propagate(False)
        
        tk.Button(zoom_frame, text="🔍-", command=self.zoom_out).pack(side='left', padx=5)
        self.zoom_label = tk.Label(zoom_frame, text="100%", bg='white')
        self.zoom_label.pack(side='left', padx=10)
        tk.Button(zoom_frame, text="🔍+", command=self.zoom_in).pack(side='left', padx=5)
        
        tk.Button(zoom_frame, text="Adatta", command=self.fit_to_window).pack(side='left', padx=20)
        
        # Canvas con scrollbar per il PDF
        canvas_frame = tk.Frame(self.center_panel, bg='white')
        canvas_frame.pack(fill='both', expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white')
        v_scrollbar = tk.Scrollbar(canvas_frame, orient='vertical', command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(canvas_frame, orient='horizontal', command=self.canvas.xview)
        
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.canvas.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind eventi mouse per interazione
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Motion>", self.on_canvas_motion)
        
    def setup_right_panel(self):
        """Configura il pannello destro"""
        # Titolo
        title_label = tk.Label(self.right_panel, text="PROPRIETÀ", 
                              font=('Arial', 10, 'bold'), bg='#e8e8e8')
        title_label.pack(pady=10)
        
        # Proprietà strumento corrente
        props_frame = tk.LabelFrame(self.right_panel, text="Strumento", bg='#e8e8e8')
        props_frame.pack(fill='x', padx=10, pady=5)
        
        # Font size per testo
        tk.Label(props_frame, text="Dimensione font:", bg='#e8e8e8').pack(anchor='w')
        tk.Spinbox(props_frame, from_=8, to=72, textvariable=self.font_size, width=10).pack(anchor='w', pady=2)
        
        # Commenti e annotazioni
        comments_frame = tk.LabelFrame(self.right_panel, text="Commenti", bg='#e8e8e8')
        comments_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.comments_listbox = tk.Listbox(comments_frame, height=10)
        comments_scrollbar = tk.Scrollbar(comments_frame, orient='vertical', 
                                         command=self.comments_listbox.yview)
        self.comments_listbox.configure(yscrollcommand=comments_scrollbar.set)
        
        self.comments_listbox.pack(side='left', fill='both', expand=True)
        comments_scrollbar.pack(side='right', fill='y')
        
        # Pulsanti azioni
        actions_frame = tk.Frame(self.right_panel, bg='#e8e8e8')
        actions_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(actions_frame, text="Elimina", command=self.delete_selected).pack(fill='x', pady=2)
        tk.Button(actions_frame, text="Proprietà", command=self.show_properties).pack(fill='x', pady=2)
        
    def create_status_bar(self):
        """Crea la barra di stato"""
        self.status_bar = tk.Frame(self.root, bg='#d0d0d0', height=25)
        self.status_bar.pack(side='bottom', fill='x')
        self.status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(self.status_bar, text="Pronto", 
                                    bg='#d0d0d0', anchor='w')
        self.status_label.pack(side='left', padx=10, fill='x', expand=True)
        
        # Info documento
        self.doc_info_label = tk.Label(self.status_bar, text="", 
                                      bg='#d0d0d0', anchor='e')
        self.doc_info_label.pack(side='right', padx=10)
        
    def open_pdf(self):
        """Apre un file PDF"""
        file_path = filedialog.askopenfilename(
            title="Apri PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            if self.pdf_editor.open_pdf(file_path):
                self.update_display()
                self.update_thumbnails()
                self.status_label.config(text=f"PDF aperto: {os.path.basename(file_path)}")
                
                # Aggiorna info documento
                page_count = self.pdf_editor.get_page_count()
                self.doc_info_label.config(text=f"Pagine: {page_count}")
                self.page_label.config(text=f"1 / {page_count}")
            else:
                messagebox.showerror("Errore", "Impossibile aprire il file PDF")
    
    def save_pdf(self):
        """Salva il PDF corrente"""
        if not self.pdf_editor.current_doc:
            messagebox.showwarning("Attenzione", "Nessun PDF aperto")
            return
            
        # Per ora salva come nuovo file
        self.save_pdf_as()
    
    def save_pdf_as(self):
        """Salva il PDF con un nuovo nome"""
        if not self.pdf_editor.current_doc:
            messagebox.showwarning("Attenzione", "Nessun PDF aperto")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Salva PDF",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            if self.pdf_editor.save_pdf(file_path):
                self.status_label.config(text=f"PDF salvato: {os.path.basename(file_path)}")
                messagebox.showinfo("Successo", "PDF salvato correttamente!")
            else:
                messagebox.showerror("Errore", "Errore nel salvataggio del PDF")
    
    def set_tool(self, tool):
        """Imposta lo strumento corrente"""
        self.current_tool.set(tool)
        self.status_label.config(text=f"Strumento selezionato: {tool}")
    
    def choose_color(self):
        """Apre il selettore colore"""
        color = colorchooser.askcolor(title="Scegli colore")
        if color[0]:
            # Converte da RGB 0-255 a RGB 0-1 per PyMuPDF
            self.current_color = tuple(c/255.0 for c in color[0])
            # Aggiorna il pulsante colore
            hex_color = '#{:02x}{:02x}{:02x}'.format(*[int(c) for c in color[0]])
            self.color_button.config(bg=hex_color)
    
    def update_display(self):
        """Aggiorna la visualizzazione della pagina corrente"""
        if not self.pdf_editor.current_doc:
            return
            
        image = self.pdf_editor.get_page_image()
        if image:
            # Converti PIL Image in PhotoImage per tkinter
            self.canvas_image = ImageTk.PhotoImage(image)
            
            # Pulisci il canvas e mostra l'immagine
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor='nw', image=self.canvas_image)
            
            # Aggiorna scroll region
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
            # Aggiorna label zoom
            zoom_percent = int(self.pdf_editor.zoom_level * 100)
            self.zoom_label.config(text=f"{zoom_percent}%")
    
    def update_thumbnails(self):
        """Aggiorna la lista delle miniature"""
        self.thumb_listbox.delete(0, 'end')
        
        if self.pdf_editor.current_doc:
            page_count = self.pdf_editor.get_page_count()
            for i in range(page_count):
                self.thumb_listbox.insert('end', f"Pagina {i+1}")
    
    def prev_page(self):
        """Vai alla pagina precedente"""
        if self.pdf_editor.current_doc and self.pdf_editor.page_num > 0:
            self.pdf_editor.page_num -= 1
            self.update_display()
            page_count = self.pdf_editor.get_page_count()
            self.page_label.config(text=f"{self.pdf_editor.page_num + 1} / {page_count}")
    
    def next_page(self):
        """Vai alla pagina successiva"""
        if (self.pdf_editor.current_doc and 
            self.pdf_editor.page_num < self.pdf_editor.get_page_count() - 1):
            self.pdf_editor.page_num += 1
            self.update_display()
            page_count = self.pdf_editor.get_page_count()
            self.page_label.config(text=f"{self.pdf_editor.page_num + 1} / {page_count}")
    
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
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
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
            
        # Converti coordinate canvas in coordinate PDF
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Scala per lo zoom
        pdf_x = canvas_x / self.pdf_editor.zoom_level
        pdf_y = canvas_y / self.pdf_editor.zoom_level
        
        tool = self.current_tool.get()
        
        if tool == "text":
            self.add_text_at_position(pdf_x, pdf_y)
        elif tool == "note":
            self.add_note_at_position(pdf_x, pdf_y)
        elif tool in ["rectangle", "circle", "line", "arrow"]:
            self.draw_start_x = pdf_x
            self.draw_start_y = pdf_y
            self.drawing = True
        elif tool == "freehand":
            self.current_points = [(pdf_x, pdf_y)]
            self.drawing = True
    
    def on_canvas_drag(self, event):
        """Gestisce trascinamento sul canvas"""
        if not self.drawing:
            return
            
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        pdf_x = canvas_x / self.pdf_editor.zoom_level
        pdf_y = canvas_y / self.pdf_editor.zoom_level
        
        tool = self.current_tool.get()
        
        if tool == "freehand":
            self.current_points.append((pdf_x, pdf_y))
    
    def on_canvas_release(self, event):
        """Gestisce rilascio del mouse sul canvas"""
        if not self.drawing:
            return
            
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        pdf_x = canvas_x / self.pdf_editor.zoom_level
        pdf_y = canvas_y / self.pdf_editor.zoom_level
        
        tool = self.current_tool.get()
        page_num = self.pdf_editor.page_num
        
        if tool == "rectangle":
            rect = fitz.Rect(self.draw_start_x, self.draw_start_y, pdf_x, pdf_y)
            self.pdf_editor.add_rectangle(page_num, rect, self.current_color, 
                                        width=self.line_width.get())
        elif tool == "circle":
            rect = fitz.Rect(self.draw_start_x, self.draw_start_y, pdf_x, pdf_y)
            self.pdf_editor.add_circle(page_num, rect, self.current_color, 
                                     width=self.line_width.get())
        elif tool == "line":
            start = fitz.Point(self.draw_start_x, self.draw_start_y)
            end = fitz.Point(pdf_x, pdf_y)
            self.pdf_editor.add_line(page_num, start, end, self.current_color, 
                                   width=self.line_width.get())
        elif tool == "arrow":
            start = fitz.Point(self.draw_start_x, self.draw_start_y)
            end = fitz.Point(pdf_x, pdf_y)
            self.pdf_editor.add_arrow(page_num, start, end, self.current_color, 
                                    width=self.line_width.get())
        elif tool == "freehand" and len(self.current_points) > 1:
            points = [fitz.Point(x, y) for x, y in self.current_points]
            self.pdf_editor.add_freehand_drawing(page_num, points, self.current_color, 
                                               width=self.line_width.get())
        
        self.drawing = False
        self.current_points = []
        self.update_display()
    
    def on_canvas_motion(self, event):
        """Gestisce movimento del mouse sul canvas"""
        pass  # Per ora non utilizzato
    
    def add_text_at_position(self, x, y):
        """Aggiunge testo alla posizione specificata"""
        text = simpledialog.askstring("Aggiungi testo", "Inserisci il testo:")
        if text:
            self.pdf_editor.add_text(self.pdf_editor.page_num, x, y, text, 
                                   font_size=self.font_size.get(), color=self.current_color)
            self.update_display()
    
    def add_note_at_position(self, x, y):
        """Aggiunge una nota alla posizione specificata"""
        content = simpledialog.askstring("Aggiungi nota", "Inserisci il contenuto della nota:")
        if content:
            self.pdf_editor.add_note(self.pdf_editor.page_num, x, y, content)
            self.update_display()
    
    # Metodi placeholder per le funzionalità del menu
    def undo(self):
        self.status_label.config(text="Annulla - non ancora implementato")
    
    def redo(self):
        self.status_label.config(text="Ripeti - non ancora implementato")
    
    def copy(self):
        self.status_label.config(text="Copia - non ancora implementato")
    
    def paste(self):
        self.status_label.config(text="Incolla - non ancora implementato")
    
    def delete_selected(self):
        self.status_label.config(text="Elimina - non ancora implementato")
    
    def show_properties(self):
        self.status_label.config(text="Proprietà - non ancora implementato")

def main():
    root = tk.Tk()
    app = AcrobatLikeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()