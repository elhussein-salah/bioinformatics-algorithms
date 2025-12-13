# 🧬 Bioinformatics Toolkit

A modular, clean-architecture bioinformatics toolkit for DNA and protein sequence analysis with an interactive GUI.

---

## 📁 Project Structure

```
Bioinformatics/
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── DOCUMENTATION.md           # Detailed documentation
│
├── src/                       # Source code (Clean Architecture)
│   ├── __init__.py
│   │
│   ├── core/                  # Core algorithms (Business Logic)
│   │   ├── __init__.py
│   │   ├── sequence_operations.py   # GC content, complement, translation
│   │   ├── pattern_matching.py      # Naive & Boyer-Moore algorithms
│   │   ├── indexing.py              # K-mer indexing, suffix arrays
│   │   └── sequence_analysis.py     # Overlap, FASTA parsing
│   │
│   └── gui/                   # GUI components (Presentation Layer)
│       ├── __init__.py
│       ├── base.py                  # Base app class & theme
│       ├── dna_translator.py        # DNA to protein translator
│       ├── sequence_processor.py    # FASTA processor
│       ├── pattern_matcher.py       # Pattern matching GUIs
│       ├── indexing.py              # Indexing GUI
│       ├── suffix_array.py          # Suffix array GUI
│       ├── overlap.py               # Overlap detection GUI
│       └── hemolytic.py             # Hemolytic predictor GUI
│
└── data/                      # Sample data files
    ├── dna1.fasta
    ├── dna2.fasta
    ├── seq.fasta
    └── HAPPENN_dataset.fasta
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Abdelrhman-Ellithy/bioinformatics-project.git
cd bioinformatics-project

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Requirements

- Python 3.9+
- tkinter (included with Python)
- numpy
- pandas

---

## 🧪 Available Tools

| Tool | Description |
|------|-------------|
| **Hemolytic Predictor** | Analyze hemolytic activity of peptides from HAPPENN dataset |
| **FASTA Processor** | Calculate GC content, complement, reverse, and reverse complement |
| **DNA Translator** | Translate DNA sequences to protein using standard genetic code |
| **Exact Match Finder** | Find patterns using naive string matching |
| **Bad Character Match** | Find patterns using Boyer-Moore bad character heuristic |
| **K-mer Indexing** | Build sorted k-mer indices for fast pattern queries |
| **Suffix Array** | Generate suffix arrays for genome indexing |
| **Overlap Detector** | Find overlapping regions between sequences |

---

## 📖 Usage Examples

### Using as a Library

```python
from src.core import (
    gc_content,
    complement,
    translate_dna_to_protein,
    naive_match,
    bad_character_match
)

# Calculate GC content
sequence = "ATGCGATCGATCG"
gc = gc_content(sequence)
print(f"GC Content: {gc:.2%}")

# Translate DNA to protein
full_protein, orf_protein = translate_dna_to_protein("ATGAAATAG")
print(f"Protein: {full_protein}")

# Find pattern
position = naive_match("ATGCGATCGATCG", "GATC")
print(f"Pattern found at position: {position}")
```

### Running Individual Tools

```python
# Run specific GUI module
from src.gui.dna_translator import run
run()
```

---

## 🏗️ Architecture

This project follows **Clean Architecture** principles:

### Core Layer (`src/core/`)

- Pure business logic
- No dependencies on GUI or external frameworks
- Fully testable and reusable

### Presentation Layer (`src/gui/`)

- Tkinter-based GUI components
- Depends only on core layer
- Each tool is a separate module

### Benefits

- ✅ Separation of concerns
- ✅ Easy to test core algorithms
- ✅ GUI can be replaced without changing logic
- ✅ Modular and extensible

---

## 🐛 Bug Fixes Applied

1. **Missing `dna_file` initialization** - Fixed AttributeError when matching before file selection
2. **Unused imports** - Removed `subprocess` and other unused imports
3. **Duplicate code** - Consolidated common GUI patterns into `BaseApp` class
4. **Hard-coded icon path** - Added graceful fallback when favicon.ico is missing
5. **FASTA parsing** - Improved to handle multi-line sequences properly
6. **Type safety** - Added type hints throughout the codebase

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 👥 Contributors

- Bioinformatics Project Team

---

## 📚 Full Documentation

See [DOCUMENTATION.md](DOCUMENTATION.md) for detailed API reference, algorithm explanations, and extension guides.

---