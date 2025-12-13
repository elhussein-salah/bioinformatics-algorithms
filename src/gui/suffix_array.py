"""
Suffix Array Generator GUI.
"""

import tkinter as tk
from tkinter import scrolledtext

from .base import BaseApp
from ..core.indexing import build_suffix_array


class SuffixArrayApp(BaseApp):
    """GUI application for generating suffix arrays."""
    
    def __init__(self, root: tk.Tk):
        super().__init__(root, "Suffix Array Generator", height=600)
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout all widgets."""
        # Text input
        self.text_label = self.create_label(self.root, "Enter text string:")
        self.text_label.pack(pady=10)
        
        self.text_entry = self.create_entry(self.root)
        self.text_entry.pack(pady=10)
        
        # Generate button
        self.generate_button = self.create_button(
            self.root, "Generate Suffix Array", self._generate_suffix_array
        )
        self.generate_button.pack(pady=10)
        
        # Clear button
        self.clear_button = self.create_button(
            self.root, "Clear", self._clear, danger=True
        )
        self.clear_button.pack(pady=10)
        
        # Results display
        self.result_text = scrolledtext.ScrolledText(
            self.root,
            wrap="word",
            width=90,
            height=20,
            font=('Arial', 12),
            bg='#2C3E50',
            fg='white'
        )
        self.result_text.pack(pady=10)
    
    def _generate_suffix_array(self):
        """Generate and display the suffix array."""
        text = self.text_entry.get().strip()
        
        if not text:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Please enter a text string")
            return
        
        suffix_ranks, suffix_table = build_suffix_array(text)
        
        # Format output
        output_lines = [
            f"Input Text: {text}",
            f"Length: {len(text)}",
            "",
            "Suffix Array (sorted suffixes with ranks):",
            "-" * 50,
            f"{'Suffix':<30} {'Position':<10} {'Rank':<10}",
            "-" * 50
        ]
        
        for suffix, pos, rank in suffix_table:
            # Truncate long suffixes for display
            display_suffix = suffix[:25] + "..." if len(suffix) > 25 else suffix
            output_lines.append(f"{display_suffix:<30} {pos:<10} {rank:<10}")
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "\n".join(output_lines))
    
    def _clear(self):
        """Clear all inputs and results."""
        self.text_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)


def run():
    """Run the Suffix Array application."""
    root = tk.Tk()
    app = SuffixArrayApp(root)
    root.mainloop()


if __name__ == "__main__":
    run()
