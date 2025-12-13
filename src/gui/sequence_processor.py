"""
FASTA Sequence Processor GUI.
"""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from .base import BaseApp
from ..core.sequence_operations import gc_content, complement, reverse, reverse_complement


class SequenceProcessorApp(BaseApp):
    """GUI application for processing DNA sequences."""
    
    def __init__(self, root: tk.Tk):
        super().__init__(root, "DNA Sequence Processor", height=700)
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout all widgets."""
        # File chooser
        self.choose_button = self.create_button(
            self.root, "Choose FASTA File", self._choose_file
        )
        self.choose_button.pack(pady=10)
        
        # Manual input
        self.input_label = self.create_label(
            self.root, "Or enter DNA sequence manually:"
        )
        self.input_label.pack(pady=5)
        
        self.input_entry = self.create_entry(self.root, width=60)
        self.input_entry.pack(pady=10)
        
        # Process button
        self.process_button = self.create_button(
            self.root, "Process Sequence", self._process_sequence
        )
        self.process_button.pack(pady=10)
        
        # Clear button
        self.clear_button = self.create_button(
            self.root, "Clear", self._clear, danger=True
        )
        self.clear_button.pack(pady=10)
        
        # Results display
        self.result_text = ScrolledText(
            self.root,
            wrap="word",
            width=90,
            height=20,
            font=('Arial', 12),
            bg='#2C3E50',
            fg='white'
        )
        self.result_text.pack(padx=20, pady=10)
    
    def _choose_file(self):
        """Handle file selection."""
        file_path = self.choose_file("Select FASTA File")
        
        if file_path:
            sequence = self.read_fasta_file(file_path)
            if sequence:
                self._display_results(sequence)
    
    def _process_sequence(self):
        """Process the entered sequence."""
        sequence = self.input_entry.get().strip().upper()
        
        if not sequence:
            self.show_error("Error", "Please enter a valid DNA sequence.")
            return
        
        # Validate sequence
        valid_chars = set("ACGT")
        if not all(c in valid_chars for c in sequence):
            self.show_error("Error", "Invalid DNA sequence. Use only A, C, G, T.")
            return
        
        self._display_results(sequence)
    
    def _display_results(self, sequence: str):
        """Display processing results."""
        try:
            gc = gc_content(sequence)
            comp = complement(sequence)
            rev = reverse(sequence)
            rev_comp = reverse_complement(sequence)
            
            results = (
                f"Original Sequence:\n{sequence}\n\n"
                f"GC Content: {gc:.4f} ({gc*100:.2f}%)\n\n"
                f"Complement:\n{comp}\n\n"
                f"Reverse:\n{rev}\n\n"
                f"Reverse Complement:\n{rev_comp}"
            )
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, results)
            
        except ValueError as e:
            self.show_error("Processing Error", str(e))
    
    def _clear(self):
        """Clear all inputs and results."""
        self.input_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)


def run():
    """Run the Sequence Processor application."""
    root = tk.Tk()
    app = SequenceProcessorApp(root)
    root.mainloop()


if __name__ == "__main__":
    run()
