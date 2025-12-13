"""
Overlap Detection GUI.
"""

import tkinter as tk

from .base import BaseApp
from ..core.sequence_analysis import compute_overlap


class OverlapApp(BaseApp):
    """GUI application for detecting sequence overlaps."""
    
    def __init__(self, root: tk.Tk):
        super().__init__(root, "Sequence Overlap Detector", height=500)
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout all widgets."""
        # Sequence 1 input
        self.seq1_label = self.create_label(self.root, "Sequence 1:")
        self.seq1_label.pack(pady=10)
        
        self.seq1_entry = self.create_entry(self.root)
        self.seq1_entry.pack(pady=5)
        
        # Sequence 2 input
        self.seq2_label = self.create_label(self.root, "Sequence 2:")
        self.seq2_label.pack(pady=10)
        
        self.seq2_entry = self.create_entry(self.root)
        self.seq2_entry.pack(pady=5)
        
        # Check button
        self.check_button = self.create_button(
            self.root, "Check Overlap", self._check_overlap
        )
        self.check_button.pack(pady=20)
        
        # Clear button
        self.clear_button = self.create_button(
            self.root, "Clear", self._clear, danger=True
        )
        self.clear_button.pack(pady=10)
        
        # Result label
        self.result_label = self.create_label(self.root, "")
        self.result_label.pack(pady=20)
    
    def _check_overlap(self):
        """Check for overlap between two sequences."""
        seq1 = self.seq1_entry.get().strip().upper()
        seq2 = self.seq2_entry.get().strip().upper()
        
        if not seq1 or not seq2:
            self.result_label.config(text="Please enter both sequences")
            return
        
        overlap_len, overlap_seq = compute_overlap(seq1, seq2)
        
        if overlap_len > 0:
            self.result_label.config(
                text=f"Overlap found!\nLength: {overlap_len}\nSequence: {overlap_seq}"
            )
        else:
            self.result_label.config(text="No significant overlap found")
    
    def _clear(self):
        """Clear all inputs and results."""
        self.seq1_entry.delete(0, tk.END)
        self.seq2_entry.delete(0, tk.END)
        self.result_label.config(text="")


def run():
    """Run the Overlap application."""
    root = tk.Tk()
    app = OverlapApp(root)
    root.mainloop()


if __name__ == "__main__":
    run()
