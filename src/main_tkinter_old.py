import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
from pathlib import Path
from pdf_manager import PDFManager
from ui_components import UIComponents

class PDFEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Editor - Modifica PDF")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Inizializza il manager PDF
        self.pdf_manager = PDFManager()
        
        # Inizializza i componenti UI
        self.ui_components = UIComponents(root)
        
        # Crea l'interfaccia
        self.setup_ui()
        
    def setup_ui(self):
        """Configura l'interfaccia utente principale"""
        # Titolo
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="PDF EDITOR", 
                              font=('Arial', 20, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Frame principale
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Frame per i pulsanti delle funzioni
        functions_frame = tk.LabelFrame(main_frame, text="Funzioni PDF", 
                                       font=('Arial', 12, 'bold'),
                                       bg='#f0f0f0', fg='#2c3e50')
        functions_frame.pack(fill='x', pady=10)
        
        # Prima riga di pulsanti
        row1_frame = tk.Frame(functions_frame, bg='#f0f0f0')
        row1_frame.pack(fill='x', padx=10, pady=10)
        
        self.ui_components.create_button(row1_frame, "Unisci PDF", 
                                        self.merge_pdfs, '#3498db')
        self.ui_components.create_button(row1_frame, "Dividi PDF", 
                                        self.split_pdf, '#e74c3c')
        self.ui_components.create_button(row1_frame, "Ruota PDF", 
                                        self.rotate_pdf, '#f39c12')
        self.ui_components.create_button(row1_frame, "Estrai Pagine", 
                                        self.extract_pages, '#9b59b6')
        
        # Seconda riga di pulsanti
        row2_frame = tk.Frame(functions_frame, bg='#f0f0f0')
        row2_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.ui_components.create_button(row2_frame, "Aggiungi Watermark", 
                                        self.add_watermark, '#1abc9c')
        self.ui_components.create_button(row2_frame, "Estrai Testo", 
                                        self.extract_text, '#34495e')
        self.ui_components.create_button(row2_frame, "Converti Immagini", 
                                        self.convert_images, '#e67e22')
        self.ui_components.create_button(row2_frame, "Anteprima PDF", 
                                        self.preview_pdf, '#27ae60')
        
        # Frame per l'output
        self.output_frame = tk.LabelFrame(main_frame, text="Output", 
                                         font=('Arial', 12, 'bold'),
                                         bg='#f0f0f0', fg='#2c3e50')
        self.output_frame.pack(fill='both', expand=True, pady=10)
        
        # Text widget per mostrare i risultati
        self.output_text = tk.Text(self.output_frame, height=8, wrap='word',
                                  font=('Consolas', 10), bg='white')
        scrollbar = tk.Scrollbar(self.output_frame, orient='vertical', 
                                command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Pulsante per pulire l'output
        clear_btn = tk.Button(self.output_frame, text="Pulisci Output", 
                             command=self.clear_output,
                             bg='#95a5a6', fg='white', font=('Arial', 10))
        clear_btn.pack(pady=(0, 10))
        
    def log_message(self, message):
        """Aggiunge un messaggio al text widget di output"""
        self.output_text.insert('end', f"{message}\n")
        self.output_text.see('end')
        self.root.update()
        
    def clear_output(self):
        """Pulisce l'area di output"""
        self.output_text.delete('1.0', 'end')
        
    def merge_pdfs(self):
        """Unisce più file PDF in uno solo"""
        try:
            files = filedialog.askopenfilenames(
                title="Seleziona i PDF da unire",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if len(files) < 2:
                messagebox.showwarning("Attenzione", "Seleziona almeno 2 file PDF")
                return
                
            output_file = filedialog.asksaveasfilename(
                title="Salva PDF unito come",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if not output_file:
                return
                
            self.log_message("Inizio unione PDF...")
            result = self.pdf_manager.merge_pdfs(files, output_file)
            
            if result:
                self.log_message(f"✓ PDF uniti con successo in: {output_file}")
                messagebox.showinfo("Successo", "PDF uniti correttamente!")
            else:
                self.log_message("✗ Errore durante l'unione dei PDF")
                
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            messagebox.showerror("Errore", f"Errore durante l'unione: {str(e)}")
            
    def split_pdf(self):
        """Divide un PDF in pagine singole o intervalli"""
        try:
            file_path = filedialog.askopenfilename(
                title="Seleziona il PDF da dividere",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if not file_path:
                return
                
            # Chiede il tipo di divisione
            split_type = messagebox.askyesno("Tipo di divisione", 
                                           "Sì = Dividi in pagine singole\n"
                                           "No = Dividi per intervallo")
            
            output_dir = filedialog.askdirectory(title="Seleziona cartella di output")
            if not output_dir:
                return
                
            self.log_message("Inizio divisione PDF...")
            
            if split_type:  # Pagine singole
                result = self.pdf_manager.split_pdf_pages(file_path, output_dir)
            else:  # Intervallo
                start_page = simpledialog.askinteger("Pagina iniziale", 
                                                   "Inserisci numero pagina iniziale:", minvalue=1)
                if start_page is None:
                    return
                    
                end_page = simpledialog.askinteger("Pagina finale", 
                                                 "Inserisci numero pagina finale:", minvalue=start_page)
                if end_page is None:
                    return
                    
                result = self.pdf_manager.split_pdf_range(file_path, output_dir, start_page, end_page)
            
            if result:
                self.log_message(f"✓ PDF diviso con successo in: {output_dir}")
                messagebox.showinfo("Successo", "PDF diviso correttamente!")
            else:
                self.log_message("✗ Errore durante la divisione del PDF")
                
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            messagebox.showerror("Errore", f"Errore durante la divisione: {str(e)}")
            
    def rotate_pdf(self):
        """Ruota le pagine di un PDF"""
        try:
            file_path = filedialog.askopenfilename(
                title="Seleziona il PDF da ruotare",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if not file_path:
                return
                
            # Selezione angolo di rotazione
            rotation_window = tk.Toplevel(self.root)
            rotation_window.title("Rotazione PDF")
            rotation_window.geometry("300x200")
            rotation_window.configure(bg='#f0f0f0')
            
            tk.Label(rotation_window, text="Seleziona angolo di rotazione:",
                    font=('Arial', 12), bg='#f0f0f0').pack(pady=20)
            
            rotation_var = tk.IntVar(value=90)
            
            for angle in [90, 180, 270]:
                tk.Radiobutton(rotation_window, text=f"{angle}°", 
                             variable=rotation_var, value=angle,
                             font=('Arial', 10), bg='#f0f0f0').pack()
            
            def apply_rotation():
                output_file = filedialog.asksaveasfilename(
                    title="Salva PDF ruotato come",
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf")]
                )
                
                if not output_file:
                    rotation_window.destroy()
                    return
                    
                self.log_message("Inizio rotazione PDF...")
                result = self.pdf_manager.rotate_pdf(file_path, output_file, rotation_var.get())
                
                if result:
                    self.log_message(f"✓ PDF ruotato con successo: {output_file}")
                    messagebox.showinfo("Successo", "PDF ruotato correttamente!")
                else:
                    self.log_message("✗ Errore durante la rotazione del PDF")
                    
                rotation_window.destroy()
            
            tk.Button(rotation_window, text="Applica Rotazione", 
                     command=apply_rotation, bg='#3498db', fg='white',
                     font=('Arial', 10)).pack(pady=20)
            
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            messagebox.showerror("Errore", f"Errore durante la rotazione: {str(e)}")
            
    def extract_pages(self):
        """Estrae pagine specifiche da un PDF"""
        try:
            file_path = filedialog.askopenfilename(
                title="Seleziona il PDF per l'estrazione",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if not file_path:
                return
                
            pages_str = simpledialog.askstring("Pagine da estrarre", 
                                             "Inserisci i numeri delle pagine (es: 1,3,5-8):")
            
            if not pages_str:
                return
                
            output_file = filedialog.asksaveasfilename(
                title="Salva pagine estratte come",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if not output_file:
                return
                
            self.log_message("Inizio estrazione pagine...")
            result = self.pdf_manager.extract_pages(file_path, output_file, pages_str)
            
            if result:
                self.log_message(f"✓ Pagine estratte con successo: {output_file}")
                messagebox.showinfo("Successo", "Pagine estratte correttamente!")
            else:
                self.log_message("✗ Errore durante l'estrazione delle pagine")
                
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            messagebox.showerror("Errore", f"Errore durante l'estrazione: {str(e)}")
            
    def add_watermark(self):
        """Aggiunge un watermark al PDF"""
        try:
            file_path = filedialog.askopenfilename(
                title="Seleziona il PDF per il watermark",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if not file_path:
                return
                
            watermark_text = simpledialog.askstring("Testo watermark", 
                                                   "Inserisci il testo del watermark:")
            
            if not watermark_text:
                return
                
            output_file = filedialog.asksaveasfilename(
                title="Salva PDF con watermark come",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if not output_file:
                return
                
            self.log_message("Aggiunta watermark in corso...")
            result = self.pdf_manager.add_watermark(file_path, output_file, watermark_text)
            
            if result:
                self.log_message(f"✓ Watermark aggiunto con successo: {output_file}")
                messagebox.showinfo("Successo", "Watermark aggiunto correttamente!")
            else:
                self.log_message("✗ Errore durante l'aggiunta del watermark")
                
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            messagebox.showerror("Errore", f"Errore durante l'aggiunta del watermark: {str(e)}")
            
    def extract_text(self):
        """Estrae il testo da un PDF"""
        try:
            file_path = filedialog.askopenfilename(
                title="Seleziona il PDF per l'estrazione del testo",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if not file_path:
                return
                
            output_file = filedialog.asksaveasfilename(
                title="Salva testo come",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt")]
            )
            
            if not output_file:
                return
                
            self.log_message("Estrazione testo in corso...")
            result = self.pdf_manager.extract_text(file_path, output_file)
            
            if result:
                self.log_message(f"✓ Testo estratto con successo: {output_file}")
                messagebox.showinfo("Successo", "Testo estratto correttamente!")
            else:
                self.log_message("✗ Errore durante l'estrazione del testo")
                
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            messagebox.showerror("Errore", f"Errore durante l'estrazione del testo: {str(e)}")
            
    def convert_images(self):
        """Converte immagini in PDF"""
        try:
            files = filedialog.askopenfilenames(
                title="Seleziona le immagini da convertire",
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff")]
            )
            
            if not files:
                return
                
            output_file = filedialog.asksaveasfilename(
                title="Salva PDF come",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")]
            )
            
            if not output_file:
                return
                
            self.log_message("Conversione immagini in corso...")
            result = self.pdf_manager.convert_images_to_pdf(files, output_file)
            
            if result:
                self.log_message(f"✓ Immagini convertite con successo: {output_file}")
                messagebox.showinfo("Successo", "Immagini convertite correttamente!")
            else:
                self.log_message("✗ Errore durante la conversione delle immagini")
                
        except Exception as e:
            self.log_message(f"✗ Errore: {str(e)}")
            messagebox.showerror("Errore", f"Errore durante la conversione: {str(e)}")
            
    def preview_pdf(self):
        """Mostra un'anteprima del PDF"""
        try:
            file_path = filedialog.askopenfilename(
                title="Seleziona il PDF per l'anteprima",
                filetypes=[("PDF files", "*.pdf")]
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
            messagebox.showerror("Errore", f"Errore durante l'anteprima: {str(e)}")

def main():
    root = tk.Tk()
    app = PDFEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()