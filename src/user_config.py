"""
PDF Editor Pro - Configurazione Utente
"""
import json
import os
from pathlib import Path

class UserConfig:
    def __init__(self):
        self.config_dir = Path.home() / ".pdf_editor_pro"
        self.config_file = self.config_dir / "config.json"
        self.default_config = {
            "default_mode": "advanced",  # basic, advanced, form
            "recent_files": [],
            "max_recent_files": 10,
            "window_size": "1200x800",
            "window_position": "center",
            "theme": "light",  # light, dark
            "default_save_location": str(Path.home() / "Desktop"),
            "auto_backup": True,
            "backup_location": str(Path.home() / "Documents" / "PDF_Editor_Backups"),
            "compression_level": 1,  # 0-9
            "remember_window_state": True,
            "language": "it",  # it, en
            "show_tooltips": True,
            "auto_check_updates": True
        }
        self.config = self.load_config()
    
    def load_config(self):
        """Carica la configurazione dal file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Aggiorna con eventuali nuove chiavi
                for key, value in self.default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            else:
                return self.default_config.copy()
        except Exception as e:
            print(f"Errore nel caricamento configurazione: {e}")
            return self.default_config.copy()
    
    def save_config(self):
        """Salva la configurazione nel file"""
        try:
            # Crea la directory se non esiste
            self.config_dir.mkdir(exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Errore nel salvataggio configurazione: {e}")
            return False
    
    def get(self, key, default=None):
        """Ottiene un valore di configurazione"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Imposta un valore di configurazione"""
        self.config[key] = value
        self.save_config()
    
    def add_recent_file(self, file_path):
        """Aggiunge un file alla lista dei recenti"""
        recent = self.config.get("recent_files", [])
        file_path = str(file_path)
        
        # Rimuovi se già presente
        if file_path in recent:
            recent.remove(file_path)
        
        # Aggiungi all'inizio
        recent.insert(0, file_path)
        
        # Mantieni solo il numero massimo
        max_files = self.config.get("max_recent_files", 10)
        recent = recent[:max_files]
        
        self.config["recent_files"] = recent
        self.save_config()
    
    def get_recent_files(self):
        """Ottiene la lista dei file recenti"""
        recent = self.config.get("recent_files", [])
        # Filtra i file che esistono ancora
        existing_files = []
        for file_path in recent:
            if os.path.exists(file_path):
                existing_files.append(file_path)
        
        # Aggiorna la lista se sono stati rimossi file
        if len(existing_files) != len(recent):
            self.config["recent_files"] = existing_files
            self.save_config()
        
        return existing_files
    
    def clear_recent_files(self):
        """Pulisce la lista dei file recenti"""
        self.config["recent_files"] = []
        self.save_config()
    
    def reset_to_defaults(self):
        """Ripristina la configurazione predefinita"""
        self.config = self.default_config.copy()
        self.save_config()
    
    def export_config(self, file_path):
        """Esporta la configurazione in un file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Errore nell'esportazione: {e}")
            return False
    
    def import_config(self, file_path):
        """Importa la configurazione da un file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Valida le chiavi importate
            for key, value in imported_config.items():
                if key in self.default_config:
                    self.config[key] = value
            
            self.save_config()
            return True
        except Exception as e:
            print(f"Errore nell'importazione: {e}")
            return False

# Istanza globale della configurazione
user_config = UserConfig()