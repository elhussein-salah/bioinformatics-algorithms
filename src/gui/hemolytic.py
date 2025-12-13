"""
Hemolytic File Processor GUI.
"""

import tkinter as tk
from tkinter.scrolledtext import ScrolledText

from .base import BaseApp
from ..core.sequence_analysis import parse_hemolytic_file, parse_fasta_sequences


class HemolyticApp(BaseApp):
    """GUI application for processing hemolytic and FASTA files."""
    
    def __init__(self, root: tk.Tk):
        super().__init__(root, "Hemolytic File Processor", height=700)
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout all widgets."""
        # Hemolytic file button
        self.hemolytic_button = self.create_button(
            self.root, "Choose Hemolytic Dataset (HAPPENN)", self._process_hemolytic
        )
        self.hemolytic_button.pack(pady=15)
        
        # FASTA file button
        self.fasta_button = self.create_button(
            self.root, "Choose FASTA Sequence File", self._process_fasta
        )
        self.fasta_button.pack(pady=15)
        
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
            height=25,
            font=('Arial', 12),
            bg='#2C3E50',
            fg='white'
        )
        self.result_text.pack(padx=20, pady=20)
    
    def _process_hemolytic(self):
        """Process a hemolytic dataset file."""
        file_path = self.choose_file(
            "Select Hemolytic File",
            [("FASTA files", "*.fasta"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                df = parse_hemolytic_file(file_path)
                
                # Display summary
                summary = (
                    f"Hemolytic Dataset Analysis\n"
                    f"{'='*50}\n"
                    f"Total sequences: {len(df)}\n"
                    f"Hemolytic (1): {len(df[df['y'] == 1])}\n"
                    f"Non-hemolytic (0): {len(df[df['y'] == 0])}\n"
                    f"\n{'='*50}\n"
                    f"Sample Data (first 20 rows):\n\n"
                    f"{df.head(20).to_string(index=False)}"
                )
                
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, summary)
                
            except Exception as e:
                self.show_error("Error", f"Failed to process file: {e}")
    
    def _process_fasta(self):
        """Process a standard FASTA file."""
        file_path = self.choose_file(
            "Select FASTA File",
            [("FASTA files", "*.fasta"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                df = parse_fasta_sequences(file_path)
                
                # Display results
                output = (
                    f"FASTA File Analysis\n"
                    f"{'='*50}\n"
                    f"Total sequences: {len(df)}\n"
                    f"\n{'='*50}\n"
                    f"Sequences:\n\n"
                    f"{df.to_string(index=False)}"
                )
                
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, output)
                
            except Exception as e:
                self.show_error("Error", f"Failed to process file: {e}")
    
    def _clear(self):
        """Clear results."""
        self.result_text.delete(1.0, tk.END)


def run():
    """Run the Hemolytic Processor application."""
    root = tk.Tk()
    app = HemolyticApp(root)
    root.mainloop()


if __name__ == "__main__":
    run()
