"""
DNA to Protein Translator GUI.
"""

import tkinter as tk
from tkinter import messagebox

from .base import BaseApp
from ..core.sequence_operations import translate_dna_to_protein


class DNATranslatorApp(BaseApp):
    """GUI application for translating DNA sequences to protein."""
    
    def __init__(self, root: tk.Tk):
        super().__init__(root, "DNA to Protein Translator", height=500)
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout all widgets."""
        # File chooser button
        self.choose_button = self.create_button(
            self.root, "Choose FASTA File", self._choose_file
        )
        self.choose_button.pack(pady=30)
        
        # Manual input
        self.input_label = self.create_label(
            self.root, "Or enter DNA sequence manually:"
        )
        self.input_label.pack(pady=5)
        
        self.input_entry = self.create_entry(self.root)
        self.input_entry.pack(pady=10)
        
        # Translate button
        self.translate_button = self.create_button(
            self.root, "Translate", self._translate
        )
        self.translate_button.pack(pady=10)
        
        # Clear button
        self.clear_button = self.create_button(
            self.root, "Clear", self._clear, danger=True
        )
        self.clear_button.pack(pady=10)
        
        # Result display
        self.result_var = tk.StringVar()
        self.result_label = tk.Label(
            self.root,
            textvariable=self.result_var,
            justify="left",
            wraplength=750,
            bg='#2C3E50',
            fg='white',
            font=('Arial', 12, 'bold')
        )
        self.result_label.pack(pady=20)
    
    def _choose_file(self):
        """Handle file selection."""
        filetypes = [("FASTA files", "*.fasta *.fna"), ("All files", "*.*")]
        file_path = self.choose_file("Select DNA File", filetypes)
        
        if file_path:
            sequence = self.read_fasta_file(file_path)
            if sequence:
                self._display_translation(sequence)
    
    def _translate(self):
        """Translate the entered sequence."""
        sequence = self.input_entry.get().strip().upper()
        
        if not sequence:
            self.show_warning("Warning", "Please enter a DNA sequence.")
            return
        
        # Validate sequence
        valid_chars = set("ACGT")
        if not all(c in valid_chars for c in sequence):
            self.show_error("Error", "Invalid DNA sequence. Use only A, C, G, T.")
            return
        
        self._display_translation(sequence)
    
    def _display_translation(self, sequence: str):
        """Display the translation results."""
        try:
            full_protein, orf_protein = translate_dna_to_protein(sequence)
            
            result = (
                f"Full Translation:\n{full_protein}\n\n"
                f"ORF (Start to Stop):\n{orf_protein if orf_protein else 'No ORF found'}"
            )
            self.result_var.set(result)
            
        except ValueError as e:
            self.show_error("Translation Error", str(e))
    
    def _clear(self):
        """Clear all inputs and results."""
        self.input_entry.delete(0, tk.END)
        self.result_var.set("")


def run():
    """Run the DNA Translator application."""
    root = tk.Tk()
    app = DNATranslatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    run()
