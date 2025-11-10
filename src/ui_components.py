from PySide6.QtWidgets import (QPushButton, QProgressBar, QLabel, QTextEdit, 
                               QListWidget, QFrame, QVBoxLayout, QHBoxLayout,
                               QGroupBox, QToolTip)
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QFont, QCursor

class UIComponents:
    def __init__(self, root):
        self.root = root
        
    def create_button(self, parent, text, command, color):
        """Crea un pulsante stilizzato"""
        button = QPushButton(text)
        button.clicked.connect(command)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        
        # Applica lo stile CSS per il pulsante
        hover_color = self._darken_color(color)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 15px;
                font-family: Arial;
                font-size: 10pt;
                font-weight: bold;
                min-height: 35px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(hover_color)};
            }}
        """)
        
        if hasattr(parent, 'layout') and parent.layout():
            parent.layout().addWidget(button)
        
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
    
    def create_progress_bar(self, parent):
        """Crea una barra di progresso"""
        progress_frame = QFrame()
        progress_layout = QVBoxLayout(progress_frame)
        progress_layout.setContentsMargins(10, 5, 10, 5)
        
        progress_label = QLabel("Progresso:")
        progress_label.setFont(QFont('Arial', 10))
        progress_layout.addWidget(progress_label)
        
        progress_bar = QProgressBar()
        progress_bar.setMinimumHeight(20)
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bbb;
                border-radius: 3px;
                text-align: center;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 2px;
            }
        """)
        progress_layout.addWidget(progress_bar)
        
        if hasattr(parent, 'layout') and parent.layout():
            parent.layout().addWidget(progress_frame)
        
        return progress_bar, progress_label
    
    def create_info_display(self, parent, title):
        """Crea un'area di visualizzazione informazioni"""
        info_group = QGroupBox(title)
        info_group.setFont(QFont('Arial', 10, QFont.Bold))
        info_layout = QVBoxLayout(info_group)
        info_layout.setContentsMargins(5, 5, 5, 5)
        
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setFont(QFont('Consolas', 9))
        info_text.setMinimumHeight(150)
        info_text.setStyleSheet("""
            QTextEdit {
                background-color: #fafafa;
                border: 1px solid #ddd;
                border-radius: 3px;
            }
        """)
        info_layout.addWidget(info_text)
        
        if hasattr(parent, 'layout') and parent.layout():
            parent.layout().addWidget(info_group)
        
        return info_text
    
    def update_info_display(self, info_widget, text):
        """Aggiorna il contenuto di un widget di informazioni"""
        info_widget.setPlainText(text)
    
    def create_file_list(self, parent, title):
        """Crea una lista di file con scrollbar"""
        list_group = QGroupBox(title)
        list_group.setFont(QFont('Arial', 10, QFont.Bold))
        list_layout = QVBoxLayout(list_group)
        list_layout.setContentsMargins(5, 5, 5, 5)
        
        listbox = QListWidget()
        listbox.setFont(QFont('Arial', 9))
        listbox.setSelectionMode(QListWidget.ExtendedSelection)
        listbox.setMinimumHeight(150)
        listbox.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
            }
        """)
        list_layout.addWidget(listbox)
        
        # Frame per i pulsanti
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 5, 0, 0)
        list_layout.addWidget(button_frame)
        
        if hasattr(parent, 'layout') and parent.layout():
            parent.layout().addWidget(list_group)
        
        return listbox, button_frame
    
    def create_status_bar(self, parent):
        """Crea una barra di stato"""
        status_label = QLabel("Pronto")
        status_label.setFont(QFont('Arial', 9))
        status_label.setFixedHeight(25)
        status_label.setStyleSheet("""
            QLabel {
                background-color: #34495e;
                color: white;
                padding-left: 10px;
            }
        """)
        
        return status_label
    
    def show_tooltip(self, widget, text):
        """Aggiunge un tooltip a un widget"""
        widget.setToolTip(text)