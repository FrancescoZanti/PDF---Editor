import pypdf
from pypdf import PdfWriter, PdfReader
from PIL import Image
import os
import subprocess
import platform
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import tempfile

class PDFManager:
    def __init__(self):
        pass
    
    def merge_pdfs(self, pdf_files, output_path):
        """Unisce più file PDF in uno solo"""
        try:
            pdf_writer = PdfWriter()
            
            for pdf_file in pdf_files:
                pdf_reader = PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
            
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            return True
        except Exception as e:
            print(f"Errore durante l'unione dei PDF: {e}")
            return False
    
    def split_pdf_pages(self, pdf_file, output_dir):
        """Divide un PDF in pagine singole"""
        try:
            pdf_reader = PdfReader(pdf_file)
            filename = os.path.splitext(os.path.basename(pdf_file))[0]
            
            for i, page in enumerate(pdf_reader.pages):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(page)
                
                output_filename = f"{filename}_page_{i+1}.pdf"
                output_path = os.path.join(output_dir, output_filename)
                
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
            
            return True
        except Exception as e:
            print(f"Errore durante la divisione del PDF: {e}")
            return False
    
    def split_pdf_range(self, pdf_file, output_dir, start_page, end_page):
        """Divide un PDF per un intervallo specifico di pagine"""
        try:
            pdf_reader = PdfReader(pdf_file)
            filename = os.path.splitext(os.path.basename(pdf_file))[0]
            
            if end_page > len(pdf_reader.pages):
                end_page = len(pdf_reader.pages)
            
            pdf_writer = PdfWriter()
            
            for i in range(start_page - 1, end_page):
                pdf_writer.add_page(pdf_reader.pages[i])
            
            output_filename = f"{filename}_pages_{start_page}-{end_page}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            return True
        except Exception as e:
            print(f"Errore durante la divisione del PDF per intervallo: {e}")
            return False
    
    def rotate_pdf(self, pdf_file, output_path, rotation_angle):
        """Ruota tutte le pagine di un PDF"""
        try:
            pdf_reader = PdfReader(pdf_file)
            pdf_writer = PdfWriter()
            
            for page in pdf_reader.pages:
                rotated_page = page.rotate(rotation_angle)
                pdf_writer.add_page(rotated_page)
            
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            return True
        except Exception as e:
            print(f"Errore durante la rotazione del PDF: {e}")
            return False
    
    def extract_pages(self, pdf_file, output_path, pages_string):
        """Estrae pagine specifiche da un PDF"""
        try:
            pdf_reader = PdfReader(pdf_file)
            pdf_writer = PdfWriter()
            
            # Parse della stringa delle pagine (es: "1,3,5-8")
            page_numbers = self._parse_page_range(pages_string, len(pdf_reader.pages))
            
            for page_num in page_numbers:
                if 1 <= page_num <= len(pdf_reader.pages):
                    pdf_writer.add_page(pdf_reader.pages[page_num - 1])
            
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            return True
        except Exception as e:
            print(f"Errore durante l'estrazione delle pagine: {e}")
            return False
    
    def _parse_page_range(self, pages_string, max_pages):
        """Parse della stringa delle pagine per estrarre i numeri"""
        page_numbers = []
        
        for part in pages_string.split(','):
            part = part.strip()
            if '-' in part:
                # Range di pagine (es: 5-8)
                start, end = map(int, part.split('-'))
                page_numbers.extend(range(start, min(end + 1, max_pages + 1)))
            else:
                # Singola pagina
                page_num = int(part)
                if page_num <= max_pages:
                    page_numbers.append(page_num)
        
        return sorted(set(page_numbers))
    
    def add_watermark(self, pdf_file, output_path, watermark_text):
        """Aggiunge un watermark di testo al PDF"""
        try:
            # Crea un PDF temporaneo con il watermark
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_watermark_path = temp_file.name
            
            # Crea il watermark usando reportlab
            c = canvas.Canvas(temp_watermark_path, pagesize=letter)
            width, height = letter
            
            # Imposta il testo del watermark
            c.setFont("Helvetica", 50)
            c.setFillAlpha(0.3)  # Trasparenza
            c.rotate(45)  # Rotazione diagonale
            c.drawCentredText(width/2, height/2, watermark_text)
            c.save()
            
            # Applica il watermark al PDF originale
            pdf_reader = PdfReader(pdf_file)
            watermark_reader = PdfReader(temp_watermark_path)
            pdf_writer = PdfWriter()
            
            watermark_page = watermark_reader.pages[0]
            
            for page in pdf_reader.pages:
                page.merge_page(watermark_page)
                pdf_writer.add_page(page)
            
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            # Rimuovi il file temporaneo
            os.unlink(temp_watermark_path)
            
            return True
        except Exception as e:
            print(f"Errore durante l'aggiunta del watermark: {e}")
            return False
    
    def extract_text(self, pdf_file, output_path):
        """Estrae tutto il testo da un PDF"""
        try:
            pdf_reader = PdfReader(pdf_file)
            text_content = []
            
            for i, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                text_content.append(f"--- PAGINA {i+1} ---\n")
                text_content.append(page_text)
                text_content.append("\n\n")
            
            with open(output_path, 'w', encoding='utf-8') as text_file:
                text_file.writelines(text_content)
            
            return True
        except Exception as e:
            print(f"Errore durante l'estrazione del testo: {e}")
            return False
    
    def convert_images_to_pdf(self, image_files, output_path):
        """Converte una lista di immagini in un singolo PDF"""
        try:
            images = []
            
            for image_file in image_files:
                img = Image.open(image_file)
                # Converte in RGB se necessario
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)
            
            if images:
                # Salva il primo come PDF e aggiungi gli altri
                images[0].save(output_path, save_all=True, append_images=images[1:])
            
            return True
        except Exception as e:
            print(f"Errore durante la conversione delle immagini: {e}")
            return False
    
    def preview_pdf(self, pdf_file):
        """Apre il PDF con l'applicazione predefinita del sistema"""
        try:
            if platform.system() == 'Windows':
                os.startfile(pdf_file)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', pdf_file])
            else:  # Linux
                subprocess.run(['xdg-open', pdf_file])
            
            return True
        except Exception as e:
            print(f"Errore durante l'apertura dell'anteprima: {e}")
            return False
    
    def get_pdf_info(self, pdf_file):
        """Ottiene informazioni sul PDF (numero pagine, metadata, ecc.)"""
        try:
            pdf_reader = PdfReader(pdf_file)
            
            info = {
                'num_pages': len(pdf_reader.pages),
                'title': pdf_reader.metadata.get('/Title', 'N/A') if pdf_reader.metadata else 'N/A',
                'author': pdf_reader.metadata.get('/Author', 'N/A') if pdf_reader.metadata else 'N/A',
                'subject': pdf_reader.metadata.get('/Subject', 'N/A') if pdf_reader.metadata else 'N/A',
                'creator': pdf_reader.metadata.get('/Creator', 'N/A') if pdf_reader.metadata else 'N/A',
                'producer': pdf_reader.metadata.get('/Producer', 'N/A') if pdf_reader.metadata else 'N/A',
                'creation_date': pdf_reader.metadata.get('/CreationDate', 'N/A') if pdf_reader.metadata else 'N/A'
            }
            
            return info
        except Exception as e:
            print(f"Errore durante il recupero delle informazioni PDF: {e}")
            return None