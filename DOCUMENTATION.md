# 📚 Bioinformatics Toolkit - Detailed Documentation

This document provides comprehensive documentation for understanding and using the Bioinformatics Toolkit.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Algorithms](#core-algorithms)
3. [GUI Components](#gui-components)
4. [API Reference](#api-reference)
5. [File Formats](#file-formats)
6. [Extending the Toolkit](#extending-the-toolkit)

---

## Architecture Overview

### Clean Architecture Layers

```
┌─────────────────────────────────────────────────┐
│                 PRESENTATION                     │
│              (src/gui/*.py)                      │
│    Tkinter GUIs for user interaction            │
└─────────────────────┬───────────────────────────┘
                      │ depends on
                      ▼
┌─────────────────────────────────────────────────┐
│                   CORE                           │
│              (src/core/*.py)                     │
│    Pure business logic & algorithms             │
└─────────────────────────────────────────────────┘
```

### Design Principles

1. **Single Responsibility**: Each module handles one specific task
2. **Open/Closed**: Easy to extend without modifying existing code
3. **Dependency Inversion**: GUI depends on core, not vice versa
4. **DRY (Don't Repeat Yourself)**: Common patterns abstracted to base classes

---

## Core Algorithms

### 1. Sequence Operations (`sequence_operations.py`)

#### GC Content Calculation

```python
def gc_content(sequence: str) -> float
```

Calculates the ratio of Guanine (G) and Cytosine (C) bases in a DNA sequence.

**Formula**: GC% = (G + C) / Total Length

**Example**:

```python
>>> gc_content("ATGCGC")
0.6666666666666666
```

#### DNA Complement

```python
def complement(sequence: str) -> str
```

Returns the complementary DNA strand following base-pairing rules:

- A ↔ T
- G ↔ C

**Example**:

```python
>>> complement("ATGC")
"TACG"
```

#### Reverse Complement

```python
def reverse_complement(sequence: str) -> str
```

Returns the reverse complement (5' to 3' complement of the opposite strand).

**Example**:

```python
>>> reverse_complement("ATGC")
"GCAT"
```

#### DNA Translation

```python
def translate_dna_to_protein(sequence: str) -> tuple[str, str]
```

Translates DNA to protein using the standard genetic code.

**Returns**:

- `full_translation`: All codons translated
- `orf_translation`: Only the Open Reading Frame (between M start and * stop)

**Codon Table**: Standard genetic code with:

- Start codon: ATG (Methionine/M)
- Stop codons: TAA, TAG, TGA (*)

---

### 2. Pattern Matching (`pattern_matching.py`)

#### Naive Pattern Matching

```python
def naive_match(text: str, pattern: str) -> int
```

Simple brute-force string matching algorithm.

**Time Complexity**: O(n × m) where n = text length, m = pattern length

**Algorithm**:

1. Slide pattern over text one position at a time
2. Compare all characters at each position
3. Return first match position or -1

#### Boyer-Moore Bad Character Heuristic

```python
def bad_character_match(text: str, pattern: str) -> int
```

Efficient string matching using the bad character rule.

**Time Complexity**:

- Best case: O(n/m)
- Worst case: O(n × m)

**Algorithm**:

1. Build a preprocessing table for pattern
2. Scan pattern right-to-left
3. On mismatch, use table to determine optimal shift
4. Skip alignments that cannot match

**Why it's faster**: Instead of shifting by 1, we can shift by multiple positions based on the mismatched character.

---

### 3. Indexing (`indexing.py`)

#### K-mer Index

```python
def build_sorted_index(text: str, kmer_length: int) -> list[tuple[str, int]]
def query_index(text: str, pattern: str, index: list) -> list[int]
```

**K-mer**: A substring of length k

**How it works**:

1. Extract all k-mers and their positions
2. Sort alphabetically for binary search
3. Query uses binary search to find candidate positions
4. Verify full pattern match at candidates

**Time Complexity**:

- Build: O(n log n)
- Query: O(log n + hits)

#### Suffix Array

```python
def build_suffix_array(text: str) -> tuple[dict, list]
```

Builds a suffix array for efficient string matching.

**What is a Suffix Array?**
An array of starting positions of all suffixes, sorted alphabetically.

**Example**:

```
Text: "banana"
Suffixes:     Sorted:       Suffix Array:
0: banana     5: a          [5, 3, 1, 0, 4, 2]
1: anana      3: ana        
2: nana       1: anana      
3: ana        0: banana     
4: na         4: na         
5: a          2: nana       
```

---

### 4. Sequence Analysis (`sequence_analysis.py`)

#### Overlap Detection

```python
def compute_overlap(seq_a: str, seq_b: str, min_length: int = 3) -> tuple[int, str]
```

Finds the longest suffix of `seq_a` that is a prefix of `seq_b`.

**Use Case**: Assembly of DNA reads in genome sequencing

**Example**:

```python
>>> compute_overlap("ACGGTAGGT", "GGTAGGTCC")
(6, "GGTAGT")
```

#### FASTA Parsing

```python
def parse_fasta_sequences(file_path: str) -> pd.DataFrame
def read_fasta_sequence(file_path: str) -> tuple[str, str]
```

Parses FASTA format files into structured data.

---

## GUI Components

### Base Application (`base.py`)

All GUI tools inherit from `BaseApp` which provides:

| Method | Purpose |
|--------|---------|
| `create_button()` | Create styled buttons |
| `create_label()` | Create styled labels |
| `create_entry()` | Create styled text entries |
| `choose_file()` | Open file dialog |
| `read_fasta_file()` | Read and parse FASTA files |
| `show_error()` | Display error messages |

### Theme Configuration

```python
THEME = {
    'bg_color': '#2C3E50',      # Dark blue background
    'button_bg': '#16A085',      # Teal buttons
    'button_fg': 'white',        # White text
    'danger_bg': '#E74C3C',      # Red for clear/delete
    'font_family': 'Arial',
    'font_size': 12,
}
```

---

## API Reference

### Core Module Imports

```python
from src.core import (
    # Sequence Operations
    gc_content,
    complement,
    reverse,
    reverse_complement,
    translate_dna_to_protein,
    
    # Pattern Matching
    naive_match,
    bad_character_match,
    
    # Indexing
    build_sorted_index,
    query_index,
    build_suffix_array,
    
    # Sequence Analysis
    compute_overlap,
    parse_hemolytic_file,
    parse_fasta_sequences
)
```

### GUI Module Imports

```python
from src.gui import (
    BaseApp,
    THEME,
    DNATranslatorApp,
    SequenceProcessorApp,
    NaiveMatcherApp,
    BadCharacterMatcherApp,
    IndexingApp,
    SuffixArrayApp,
    OverlapApp,
    HemolyticApp
)
```

---

## File Formats

### FASTA Format

```
>header_line|optional|metadata
ATGCGATCGATCGATCG
ATCGATCGATCGATCGA
```

- Lines starting with `>` are headers
- Sequence can span multiple lines
- No spaces in sequence data

### HAPPENN Hemolytic Dataset

```
>ID|lcl|data|hemolytic
PEPTIDESEQUENCE
>ID|lcl|data|non-hemolytic
PEPTIDESEQUENCE
```

---

## Extending the Toolkit

### Adding a New Algorithm

1. **Create function in `src/core/`**:

```python
# src/core/my_algorithm.py
def my_algorithm(sequence: str) -> str:
    """
    Description of the algorithm.
    
    Args:
        sequence: Input DNA sequence
        
    Returns:
        Processed result
    """
    # Implementation
    return result
```

2. **Export in `src/core/__init__.py`**:

```python
from .my_algorithm import my_algorithm
__all__ = [..., 'my_algorithm']
```

### Adding a New GUI Tool

1. **Create GUI class in `src/gui/`**:

```python
# src/gui/my_tool.py
from .base import BaseApp

class MyToolApp(BaseApp):
    def __init__(self, root):
        super().__init__(root, "My Tool Title")
        self._create_widgets()
    
    def _create_widgets(self):
        # Add your widgets
        pass

def run():
    root = tk.Tk()
    app = MyToolApp(root)
    root.mainloop()
```

2. **Register in `main.py`**:

```python
tools = [
    # ... existing tools
    ("🔧 My Tool", "my_tool", "Description"),
]
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run from project root directory |
| Icon not showing | `favicon.ico` is optional, app works without it |
| File not reading | Ensure FASTA format is correct |
| Pattern not found | Check sequence is uppercase |

### Debug Mode

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Performance Tips

1. **Large files**: Use indexed search instead of naive matching
2. **Multiple queries**: Build index once, query many times
3. **Memory**: Suffix arrays use O(n) memory

---

## References

1. Boyer, R. S., & Moore, J. S. (1977). "A fast string searching algorithm"
2. Manber, U., & Myers, G. (1993). "Suffix arrays: a new method for on-line string searches"
3. Karp, R. M., & Rabin, M. O. (1987). "Efficient randomized pattern-matching algorithms"
