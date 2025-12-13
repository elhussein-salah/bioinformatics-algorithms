"""
Pattern Matching GUI Applications.
"""

import tkinter as tk

from .base import BaseApp
from ..core.pattern_matching import naive_match, bad_character_match


class NaiveMatcherApp(BaseApp):
    """GUI application for naive pattern matching."""
    
    def __init__(self, root: tk.Tk):
        super().__init__(root, "Naive Pattern Matching", height=500)
        self.dna_file = None  # Initialize file path
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
        self.pattern_label = self.create_label(self.root, "Enter pattern to search:")
        self.pattern_label.pack(pady=5)
        
        self.pattern_entry = self.create_entry(self.root)
        self.pattern_entry.pack(pady=10)
        
        # Match button
        self.match_button = self.create_button(
            self.root, "Find Pattern", self._match_sequence
        )
        self.match_button.pack(pady=10)
        
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
    
    def _match_sequence(self):
        """Perform pattern matching."""
        pattern = self.pattern_entry.get().strip().upper()
        
        if not pattern:
            self.result_label.config(text="Please enter a pattern")
            return
        
        if not self.dna_file:
            self.result_label.config(text="Please select a DNA file first")
            return
        
        sequence = self.read_fasta_file(self.dna_file)
        
        if sequence:
            position = naive_match(sequence.upper(), pattern)
            
            if position >= 0:
                self.result_label.config(
                    text=f"Pattern '{pattern}' found at position: {position}"
                )
            else:
                self.result_label.config(
                    text=f"Pattern '{pattern}' not found in sequence"
                )


class BadCharacterMatcherApp(BaseApp):
    """GUI application for Boyer-Moore bad character matching."""
    
    def __init__(self, root: tk.Tk):
        super().__init__(root, "Boyer-Moore Bad Character Matching", height=500)
        self.dna_file = None  # Initialize file path
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
        self.pattern_label = self.create_label(self.root, "Enter pattern to search:")
        self.pattern_label.pack(pady=5)
        
        self.pattern_entry = self.create_entry(self.root)
        self.pattern_entry.pack(pady=10)
        
        # Match button
        self.match_button = self.create_button(
            self.root, "Find Pattern (Boyer-Moore)", self._match_sequence
        )
        self.match_button.pack(pady=10)
        
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
    
    def _match_sequence(self):
        """Perform Boyer-Moore pattern matching."""
        pattern = self.pattern_entry.get().strip().upper()
        
        if not pattern:
            self.result_label.config(text="Please enter a pattern")
            return
        
        if not self.dna_file:
            self.result_label.config(text="Please select a DNA file first")
            return
        
        sequence = self.read_fasta_file(self.dna_file)
        
        if sequence:
            position = bad_character_match(sequence.upper(), pattern)
            
            if position >= 0:
                self.result_label.config(
                    text=f"Pattern '{pattern}' found at position: {position}"
                )
            else:
                self.result_label.config(
                    text=f"Pattern '{pattern}' not found in sequence"
                )


def run_naive():
    """Run the Naive Matcher application."""
    root = tk.Tk()
    app = NaiveMatcherApp(root)
    root.mainloop()


def run_bad_character():
    """Run the Bad Character Matcher application."""
    root = tk.Tk()
    app = BadCharacterMatcherApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_naive()
