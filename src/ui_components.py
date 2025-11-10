import tkinter as tk
from tkinter import ttk

class UIComponents:
    def __init__(self, root):
        self.root = root
        
    def create_button(self, parent, text, command, color):
        """Crea un pulsante stilizzato"""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2',
            activebackground=self._darken_color(color),
            activeforeground='white'
        )
        button.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        
        # Effetto hover
        button.bind("<Enter>", lambda e: self._on_enter(button, color))
        button.bind("<Leave>", lambda e: self._on_leave(button, color))
        
        return button
    
    def _darken_color(self, color):
        """Scurisce un colore per l'effetto hover"""
        color_map = {
            '#3498db': '#2980b9',
            '#e74c3c': '#c0392b',
            '#f39c12': '#e67e22',
            '#9b59b6': '#8e44ad',
            '#1abc9c': '#16a085',
            '#34495e': '#2c3e50',
            '#e67e22': '#d35400',
            '#27ae60': '#229954',
            '#95a5a6': '#7f8c8d'
        }
        return color_map.get(color, color)
    
    def _on_enter(self, button, original_color):
        """Effetto hover - entrata"""
        button.configure(bg=self._darken_color(original_color))
    
    def _on_leave(self, button, original_color):
        """Effetto hover - uscita"""
        button.configure(bg=original_color)
    
    def create_progress_bar(self, parent):
        """Crea una barra di progresso"""
        progress_frame = tk.Frame(parent, bg='#f0f0f0')
        progress_frame.pack(fill='x', padx=10, pady=5)
        
        progress_label = tk.Label(progress_frame, text="Progresso:", 
                                 font=('Arial', 10), bg='#f0f0f0')
        progress_label.pack(anchor='w')
        
        progress_bar = ttk.Progressbar(progress_frame, mode='determinate', 
                                      length=300, height=20)
        progress_bar.pack(fill='x', pady=(5, 0))
        
        return progress_bar, progress_label
    
    def create_info_display(self, parent, title):
        """Crea un'area di visualizzazione informazioni"""
        info_frame = tk.LabelFrame(parent, text=title, 
                                  font=('Arial', 10, 'bold'),
                                  bg='#f0f0f0', fg='#2c3e50')
        info_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        info_text = tk.Text(info_frame, height=6, wrap='word',
                           font=('Consolas', 9), bg='#fafafa',
                           state='disabled')
        
        scrollbar = tk.Scrollbar(info_frame, orient='vertical', 
                               command=info_text.yview)
        info_text.configure(yscrollcommand=scrollbar.set)
        
        info_text.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        scrollbar.pack(side='right', fill='y', pady=5)
        
        return info_text
    
    def update_info_display(self, info_widget, text):
        """Aggiorna il contenuto di un widget di informazioni"""
        info_widget.configure(state='normal')
        info_widget.delete('1.0', 'end')
        info_widget.insert('1.0', text)
        info_widget.configure(state='disabled')
    
    def create_file_list(self, parent, title):
        """Crea una lista di file con scrollbar"""
        list_frame = tk.LabelFrame(parent, text=title,
                                  font=('Arial', 10, 'bold'),
                                  bg='#f0f0f0', fg='#2c3e50')
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Frame per la listbox e scrollbar
        listbox_frame = tk.Frame(list_frame, bg='#f0f0f0')
        listbox_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        listbox = tk.Listbox(listbox_frame, font=('Arial', 9),
                            selectmode='extended', height=6)
        scrollbar = tk.Scrollbar(listbox_frame, orient='vertical',
                               command=listbox.yview)
        listbox.configure(yscrollcommand=scrollbar.set)
        
        listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Frame per i pulsanti
        button_frame = tk.Frame(list_frame, bg='#f0f0f0')
        button_frame.pack(fill='x', padx=5, pady=(0, 5))
        
        return listbox, button_frame
    
    def create_status_bar(self, parent):
        """Crea una barra di stato"""
        status_frame = tk.Frame(parent, bg='#34495e', height=25)
        status_frame.pack(side='bottom', fill='x')
        status_frame.pack_propagate(False)
        
        status_label = tk.Label(status_frame, text="Pronto", 
                               font=('Arial', 9), fg='white', bg='#34495e',
                               anchor='w')
        status_label.pack(side='left', padx=10, fill='x', expand=True)
        
        return status_label
    
    def show_tooltip(self, widget, text):
        """Aggiunge un tooltip a un widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, 
                           font=('Arial', 9), bg='#ffffe0',
                           relief='solid', borderwidth=1, padx=5, pady=2)
            label.pack()
            
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)