# PDF Editor - GitHub Copilot Instructions

This file provides context and guidelines for GitHub Copilot when working on this repository.

## Project Overview

PDF Editor is a desktop application for PDF manipulation built with Python and PySide6 (Qt). It provides a modern, native Windows interface for common PDF operations.

**Primary Purpose**: Provide an easy-to-use, open-source PDF editor for Windows users with both basic and advanced features.

**Target Platform**: Windows 10/11 (optimized for Windows 11 UI)

## Technology Stack

### Core Technologies
- **Python 3.8+** - Main programming language (3.11+ recommended)
- **PySide6 (Qt 6)** - Modern GUI framework with native Windows 11 support
- **pypdf** - PDF manipulation library (merge, split, rotate, extract)
- **Pillow (PIL)** - Image processing and handling
- **reportlab** - PDF creation and watermarking
- **pdf2image** - PDF to image conversion for previews

### Advanced Features (Pro Version)
- **PyMuPDF (fitz)** - Advanced PDF editing engine
- **cryptography** - Document encryption and security
- **pytesseract** - OCR capabilities
- **numpy** - Numerical processing for images
- **opencv-python** - Computer vision features
- **matplotlib** - Charts and visualizations

## Project Structure

```
PDF-Editor/
├── src/                          # Source code
│   ├── main.py                   # Base app entry point (PySide6)
│   ├── pdf_manager.py            # PDF operations logic
│   ├── ui_components.py          # Reusable UI components
│   ├── acrobat_like_gui.py       # Pro version interface
│   ├── advanced_pdf_editor.py    # Advanced editing features
│   ├── pdf_form_editor.py        # Interactive forms editor
│   ├── pdf_security.py           # Security and encryption
│   └── user_config.py            # User configuration management
│
├── assets/                       # UI screenshots and resources
├── pdf_editor.py                 # Base version launcher
├── pdf_editor_pro.py             # Pro version launcher
├── requirements.txt              # Python dependencies
├── test_simple.py                # Basic diagnostic tests
├── test_pdf_editor.py            # Test suite
└── .github/
    ├── copilot-instructions.md   # This file
    └── workflows/                # CI/CD workflows
```

## Development Setup

### Prerequisites
- Python 3.8 or higher (3.11+ recommended)
- pip package manager
- Windows 10/11 (primary platform)

### Installation
```bash
# Clone repository
git clone https://github.com/FrancescoZanti/PDF---Editor.git
cd PDF---Editor

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python test_simple.py
```

### Running the Application
```bash
# Base version
python pdf_editor.py

# Pro version (advanced features)
python pdf_editor_pro.py

# Or use launcher scripts
avvia_pdf_editor.bat        # Base
avvia_pdf_editor_pro.bat    # Pro
```

## Code Style and Conventions

### Python Style (PEP 8)
- **Indentation**: 4 spaces (no tabs)
- **Line length**: Max 88 characters (flexible from 79)
- **Naming conventions**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

### Example Code Pattern
```python
def merge_pdf_files(input_files: list[str], output_file: str) -> bool:
    """
    Merge multiple PDF files into a single document.
    
    Args:
        input_files: List of PDF file paths to merge
        output_file: Path for the output PDF file
        
    Returns:
        True if successful, False otherwise
    """
    if not input_files:
        return False
    
    try:
        merger = PdfMerger()
        for pdf_file in input_files:
            merger.append(pdf_file)
        merger.write(output_file)
        merger.close()
        return True
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return False
    except PermissionError as e:
        print(f"Error: Permission denied - {e}")
        return False
    except Exception as e:
        print(f"Unexpected error during merge: {e}")
        return False
```

### UI Code Pattern (PySide6)
```python
from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget

class PDFEditorWindow(QMainWindow):
    """Main window for PDF Editor application."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Editor")
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Configure the user interface."""
        self.merge_button = QPushButton("Merge PDFs")
        self.merge_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        layout = QVBoxLayout()
        layout.addWidget(self.merge_button)
        
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def connect_signals(self):
        """Connect signals to slots."""
        self.merge_button.clicked.connect(self.on_merge_clicked)
    
    def on_merge_clicked(self):
        """Handle merge button click."""
        # Implementation here
        pass
```

## Testing

### Running Tests
```bash
# Basic diagnostic test
python test_simple.py

# Full test suite
python test_pdf_editor.py

# Manual testing
python pdf_editor.py  # Test all features manually
```

### Testing Checklist
- [ ] Application starts without errors
- [ ] All buttons and UI elements are responsive
- [ ] PDF operations produce correct output files
- [ ] Error handling displays appropriate messages
- [ ] No regressions in existing functionality

## Common Tasks

### Adding a New PDF Operation
1. Add the core logic to `src/pdf_manager.py`
2. Create UI components in `src/ui_components.py` or main window
3. Connect signals and slots in the main window class
4. Add error handling with specific exception types
5. Update documentation if user-facing
6. Test manually with various PDF files

### Modifying the UI
1. Locate the relevant component in `src/main.py` or `src/ui_components.py`
2. Update the widget configuration or styling
3. Test on different screen resolutions (min 1366x768)
4. Ensure Windows 11 theme compatibility
5. Check hover states and interactive feedback

### Fixing Bugs
1. Reproduce the issue consistently
2. Check error messages in the output area
3. Add specific exception handling if missing
4. Test with edge cases (empty files, large files, special characters)
5. Verify fix doesn't break other features

## Important Notes

### File Handling
- Always use context managers (`with` statement) for file operations
- Never modify original files unless explicitly requested
- Create new files for output to preserve originals
- Handle file path encoding properly (UTF-8)

### Error Handling
- Use specific exception types (FileNotFoundError, PermissionError, etc.)
- Display user-friendly error messages in the UI
- Log technical details for debugging
- Never use bare `except:` clauses

### Performance
- Large PDF files (>50MB) may require more processing time
- Consider memory usage for PDFs with many pages
- Show progress indicators for long operations
- Close file handles and clean up resources

### UI/UX
- Follow Windows 11 design guidelines
- Use appropriate colors (primary: #3498db, success: #27ae60, error: #e74c3c)
- Add hover effects for interactive elements
- Ensure responsive layout (min 1366x768, recommended 1920x1080)
- Test with high DPI displays

## Dependencies

### Core Dependencies
- `pypdf`: PDF manipulation (merge, split, rotate)
- `PySide6`: Qt-based GUI framework
- `pillow`: Image processing
- `pdf2image`: PDF to image conversion
- `reportlab`: PDF creation and watermarks

### Pro Version Dependencies
- `PyMuPDF`: Advanced PDF editing
- `cryptography`: Encryption and security
- `pytesseract`: OCR (requires Tesseract binary)
- `numpy`: Numerical operations
- `opencv-python`: Computer vision
- `matplotlib`: Plotting and graphs

## Documentation References

- [README.md](../README.md) - Comprehensive user documentation
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [README_PRO.md](../README_PRO.md) - Pro version documentation
- [GUIDA_RAPIDA.md](../GUIDA_RAPIDA.md) - Quick start guide (Italian)
- [MIGRATION_NOTES.md](../MIGRATION_NOTES.md) - PySide6 migration notes

## Security Considerations

- All file processing is done locally (no external servers)
- No telemetry or data collection
- Handle sensitive user data (passwords, encryption keys) securely
- Never log or store passwords
- Use secure random generation for cryptographic operations
- Validate file paths to prevent directory traversal

## Language and Localization

- Primary language: Italian (UI and documentation)
- Code comments: English preferred for technical content
- User-facing messages: Italian
- Variable/function names: English (following Python conventions)

## Commit Message Format

Follow these conventions:
```
Type: Brief description (max 50 chars)

Detailed explanation of WHAT changed and WHY.

References:
- Closes #123
- Related to #456
```

**Types**: Add, Fix, Update, Refactor, Docs, Style, Test

## Additional Context

### Why PySide6?
- Native Windows 11 look and feel
- Better performance than tkinter
- Rich widget ecosystem
- Active development and support
- Cross-platform capability
- DPI scaling support

### Version History
- v3.0.0: Migration to PySide6, modern UI
- v2.x: tkinter-based interface
- v1.x: Basic PDF operations

### Known Limitations
- Optimized for Windows (not extensively tested on macOS/Linux)
- Large files (>100MB) may require significant RAM
- OCR requires external Tesseract installation
- Some advanced PDF features require PyMuPDF (Pro version)