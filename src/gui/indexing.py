"""
Indexing and Pattern Query GUI.
"""

import tkinter as tk

from .base import BaseApp
from ..core.indexing import build_sorted_index, query_index


class IndexingApp(BaseApp):
    """GUI application for k-mer indexing and pattern queries."""
    
    def __init__(self, root: tk.Tk):
        super().__init__(root, "K-mer Index Pattern Query", height=500)
        self.dna_file = None
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout all widgets."""
        # File chooser
        self.file_button = self.create_button(
            self.root, "Choose DNA File", self._choose_dna_file
        )
        self.file_button.pack(pady=10)
        
        # File status label
        self.file_label = self.create_label(self.root, "No file selected")
        self.file_label.pack(pady=5)
        
        # Pattern input
        self.pattern_label = self.create_label(self.root, "Enter pattern to query:")
        self.pattern_label.pack(pady=5)
        
        self.pattern_entry = self.create_entry(self.root)
        self.pattern_entry.pack(pady=10)
        
        # Query button
        self.query_button = self.create_button(
            self.root, "Query Pattern", self._query_pattern
        )
        self.query_button.pack(pady=10)
        
        # Result label
        self.result_label = self.create_label(self.root, "")
        self.result_label.pack(pady=20)
    
    def _choose_dna_file(self):
        """Handle file selection."""
        file_path = self.choose_file("Select DNA File")
        
        if file_path:
            self.dna_file = file_path
            filename = file_path.split('/')[-1].split('\\')[-1]
            self.file_label.config(text=f"Selected: {filename}")
    
    def _query_pattern(self):
        """Query the index for pattern occurrences."""
        pattern = self.pattern_entry.get().strip().upper()
        
        if not pattern:
            self.result_label.config(text="Please enter a pattern")
            return
        
        if not self.dna_file:
            self.result_label.config(text="Please select a DNA file first")
            return
        
        sequence = self.read_fasta_file(self.dna_file)
        
        if sequence:
            sequence = sequence.upper()
            
            # Build index with pattern length
            index = build_sorted_index(sequence, len(pattern))
            
            # Query for pattern
            offsets = query_index(sequence, pattern, index)
            
            if offsets:
                self.result_label.config(
                    text=f"Pattern '{pattern}' found at positions: {offsets}"
                )
            else:
                self.result_label.config(
                    text=f"Pattern '{pattern}' not found in sequence"
                )


def run():
    """Run the Indexing application."""
    root = tk.Tk()
    app = IndexingApp(root)
    root.mainloop()


if __name__ == "__main__":
    run()
