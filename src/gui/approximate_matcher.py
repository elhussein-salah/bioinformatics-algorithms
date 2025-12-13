"""
Approximate Pattern Matching GUI Application.

Provides a user interface for approximate string matching using
Edit Distance (Levenshtein) and Hamming distance algorithms.
"""

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from .base import BaseApp, THEME
from ..core.approximate_matching import (
    edit_distance,
    edit_distance_with_trace,
    approximate_match,
    approximate_match_hamming,
    ApproximateMatch
)


class ApproximateMatcherApp(BaseApp):
    """GUI application for approximate pattern matching."""
    
    def __init__(self, root: tk.Tk):
        super().__init__(root, "Approximate Pattern Matching", width=900, height=700)
        self.dna_file = None
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout all widgets."""
        # Title
        title_label = self.create_label(
            self.root, 
            "🧬 Approximate Pattern Matching (Edit Distance)",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=15)
        
        # Algorithm selection
        algo_frame = tk.Frame(self.root, bg=THEME['bg_color'])
        algo_frame.pack(pady=10, fill='x', padx=20)
        
        self.create_label(algo_frame, "Algorithm:").pack(side='left', padx=5)
        
        self.algorithm_var = tk.StringVar(value="edit_distance")
        
        algo_options = [
            ("Edit Distance (Levenshtein)", "edit_distance"),
            ("Hamming Distance", "hamming")
        ]
        
        for text, value in algo_options:
            rb = tk.Radiobutton(
                algo_frame,
                text=text,
                variable=self.algorithm_var,
                value=value,
                bg=THEME['bg_color'],
                fg='white',
                selectcolor=THEME['button_bg'],
                activebackground=THEME['bg_color'],
                activeforeground='white',
                font=('Arial', 11)
            )
            rb.pack(side='left', padx=15)
        
        # Mode selection (Compare or Search)
        mode_frame = tk.Frame(self.root, bg=THEME['bg_color'])
        mode_frame.pack(pady=10, fill='x', padx=20)
        
        self.create_label(mode_frame, "Mode:").pack(side='left', padx=5)
        
        self.mode_var = tk.StringVar(value="compare")
        
        modes = [
            ("Compare Two Sequences", "compare"),
            ("Search in Sequence", "search")
        ]
        
        for text, value in modes:
            rb = tk.Radiobutton(
                mode_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                command=self._update_mode_ui,
                bg=THEME['bg_color'],
                fg='white',
                selectcolor=THEME['button_bg'],
                activebackground=THEME['bg_color'],
                activeforeground='white',
                font=('Arial', 11)
            )
            rb.pack(side='left', padx=15)
        
        # Input frame
        input_frame = tk.Frame(self.root, bg=THEME['bg_color'])
        input_frame.pack(pady=10, fill='x', padx=20)
        
        # Sequence 1 / Text input
        seq1_frame = tk.Frame(input_frame, bg=THEME['bg_color'])
        seq1_frame.pack(fill='x', pady=5)
        
        self.seq1_label = self.create_label(seq1_frame, "Sequence 1:")
        self.seq1_label.pack(anchor='w')
        
        self.seq1_entry = self.create_entry(seq1_frame, width=80)
        self.seq1_entry.pack(fill='x', pady=2)
        
        # File chooser for sequence 1
        btn_frame1 = tk.Frame(seq1_frame, bg=THEME['bg_color'])
        btn_frame1.pack(fill='x')
        
        self.file1_button = self.create_button(
            btn_frame1, "Load from FASTA", self._load_sequence1
        )
        self.file1_button.pack(side='left', pady=5)
        
        self.file1_label = self.create_label(btn_frame1, "", font=('Arial', 9))
        self.file1_label.pack(side='left', padx=10)
        
        # Sequence 2 / Pattern input
        seq2_frame = tk.Frame(input_frame, bg=THEME['bg_color'])
        seq2_frame.pack(fill='x', pady=5)
        
        self.seq2_label = self.create_label(seq2_frame, "Sequence 2:")
        self.seq2_label.pack(anchor='w')
        
        self.seq2_entry = self.create_entry(seq2_frame, width=80)
        self.seq2_entry.pack(fill='x', pady=2)
        
        # Max distance for search mode
        self.max_dist_frame = tk.Frame(input_frame, bg=THEME['bg_color'])
        self.max_dist_frame.pack(fill='x', pady=5)
        
        self.max_dist_label = self.create_label(
            self.max_dist_frame, "Max Edit Distance:"
        )
        self.max_dist_label.pack(side='left')
        
        self.max_dist_spinbox = tk.Spinbox(
            self.max_dist_frame,
            from_=1,
            to=10,
            width=5,
            font=('Arial', 12)
        )
        self.max_dist_spinbox.pack(side='left', padx=10)
        
        # Initially hide max distance (for compare mode)
        self.max_dist_frame.pack_forget()
        
        # Action buttons
        button_frame = tk.Frame(self.root, bg=THEME['bg_color'])
        button_frame.pack(pady=15)
        
        self.calculate_button = self.create_button(
            button_frame, "Calculate Distance", self._calculate
        )
        self.calculate_button.pack(side='left', padx=10)
        
        self.clear_button = self.create_button(
            button_frame, "Clear", self._clear, danger=True
        )
        self.clear_button.pack(side='left', padx=10)
        
        # Results display
        result_label = self.create_label(self.root, "Results:")
        result_label.pack(anchor='w', padx=20)
        
        self.result_text = ScrolledText(
            self.root,
            wrap="word",
            width=100,
            height=15,
            font=('Consolas', 11),
            bg='#1a252f',
            fg='#2ECC71',
            insertbackground='white'
        )
        self.result_text.pack(padx=20, pady=10, fill='both', expand=True)
    
    def _update_mode_ui(self):
        """Update UI based on selected mode."""
        mode = self.mode_var.get()
        
        if mode == "compare":
            self.seq1_label.config(text="Sequence 1:")
            self.seq2_label.config(text="Sequence 2:")
            self.calculate_button.config(text="Calculate Distance")
            self.max_dist_frame.pack_forget()
        else:  # search mode
            self.seq1_label.config(text="Text (to search in):")
            self.seq2_label.config(text="Pattern (to search for):")
            self.calculate_button.config(text="Find Approximate Matches")
            self.max_dist_frame.pack(fill='x', pady=5)
    
    def _load_sequence1(self):
        """Load sequence from FASTA file."""
        file_path = self.choose_file("Select FASTA File")
        
        if file_path:
            sequence = self.read_fasta_file(file_path)
            if sequence:
                self.seq1_entry.delete(0, tk.END)
                self.seq1_entry.insert(0, sequence.upper())
                filename = file_path.split('/')[-1].split('\\')[-1]
                self.file1_label.config(text=f"Loaded: {filename}")
    
    def _calculate(self):
        """Perform calculation based on mode."""
        seq1 = self.seq1_entry.get().strip().upper()
        seq2 = self.seq2_entry.get().strip().upper()
        
        if not seq1:
            self.show_error("Error", "Please enter the first sequence/text.")
            return
        
        if not seq2:
            self.show_error("Error", "Please enter the second sequence/pattern.")
            return
        
        mode = self.mode_var.get()
        algorithm = self.algorithm_var.get()
        
        if mode == "compare":
            self._compare_sequences(seq1, seq2, algorithm)
        else:
            try:
                max_dist = int(self.max_dist_spinbox.get())
            except ValueError:
                max_dist = 2
            self._search_pattern(seq1, seq2, algorithm, max_dist)
    
    def _compare_sequences(self, seq1: str, seq2: str, algorithm: str):
        """Compare two sequences and show edit distance."""
        self.result_text.delete(1.0, tk.END)
        
        if algorithm == "hamming":
            if len(seq1) != len(seq2):
                self.result_text.insert(tk.END, 
                    "⚠️ Hamming distance requires equal length sequences!\n\n"
                    f"Sequence 1 length: {len(seq1)}\n"
                    f"Sequence 2 length: {len(seq2)}\n\n"
                    "Switching to Edit Distance...\n\n"
                )
                algorithm = "edit_distance"
            else:
                distance = sum(c1 != c2 for c1, c2 in zip(seq1, seq2))
                self.result_text.insert(tk.END, 
                    f"═══ Hamming Distance Analysis ═══\n\n"
                    f"Sequence 1: {seq1[:50]}{'...' if len(seq1) > 50 else ''}\n"
                    f"Sequence 2: {seq2[:50]}{'...' if len(seq2) > 50 else ''}\n\n"
                    f"Length: {len(seq1)} characters\n"
                    f"Hamming Distance: {distance}\n"
                    f"Similarity: {(1 - distance/len(seq1))*100:.2f}%\n\n"
                    f"Mismatches at positions:\n"
                )
                mismatches = [(i, seq1[i], seq2[i]) for i in range(len(seq1)) if seq1[i] != seq2[i]]
                for pos, c1, c2 in mismatches[:20]:  # Show first 20
                    self.result_text.insert(tk.END, f"  Position {pos}: '{c1}' → '{c2}'\n")
                if len(mismatches) > 20:
                    self.result_text.insert(tk.END, f"  ... and {len(mismatches) - 20} more\n")
                return
        
        # Edit Distance calculation
        distance, operations = edit_distance_with_trace(seq1, seq2)
        
        self.result_text.insert(tk.END, 
            f"═══ Edit Distance (Levenshtein) Analysis ═══\n\n"
            f"Sequence 1: {seq1[:50]}{'...' if len(seq1) > 50 else ''}\n"
            f"  Length: {len(seq1)}\n\n"
            f"Sequence 2: {seq2[:50]}{'...' if len(seq2) > 50 else ''}\n"
            f"  Length: {len(seq2)}\n\n"
            f"Edit Distance: {distance}\n"
        )
        
        # Calculate similarity
        max_len = max(len(seq1), len(seq2))
        similarity = (1 - distance / max_len) * 100 if max_len > 0 else 100
        self.result_text.insert(tk.END, f"Similarity: {similarity:.2f}%\n\n")
        
        # Operation summary
        op_counts = {
            'M': operations.count('M'),
            'S': operations.count('S'),
            'I': operations.count('I'),
            'D': operations.count('D')
        }
        
        self.result_text.insert(tk.END, 
            f"Operations Summary:\n"
            f"  Matches:       {op_counts['M']}\n"
            f"  Substitutions: {op_counts['S']}\n"
            f"  Insertions:    {op_counts['I']}\n"
            f"  Deletions:     {op_counts['D']}\n\n"
            f"Operation Trace: {''.join(operations[:100])}{'...' if len(operations) > 100 else ''}\n"
        )
    
    def _search_pattern(self, text: str, pattern: str, algorithm: str, max_dist: int):
        """Search for approximate matches of pattern in text."""
        self.result_text.delete(1.0, tk.END)
        
        self.result_text.insert(tk.END, 
            f"═══ Approximate Pattern Search ═══\n\n"
            f"Text length: {len(text)}\n"
            f"Pattern: {pattern}\n"
            f"Pattern length: {len(pattern)}\n"
            f"Max distance: {max_dist}\n"
            f"Algorithm: {'Hamming' if algorithm == 'hamming' else 'Edit Distance'}\n\n"
            f"Searching...\n\n"
        )
        
        self.root.update()  # Update UI during search
        
        if algorithm == "hamming":
            positions = approximate_match_hamming(text, pattern, max_dist)
            if positions:
                self.result_text.insert(tk.END, 
                    f"✅ Found {len(positions)} approximate match(es):\n\n"
                )
                for i, pos in enumerate(positions[:50], 1):
                    matched = text[pos:pos + len(pattern)]
                    mismatches = sum(c1 != c2 for c1, c2 in zip(pattern, matched))
                    self.result_text.insert(tk.END, 
                        f"  {i}. Position {pos}: {matched} (mismatches: {mismatches})\n"
                    )
                if len(positions) > 50:
                    self.result_text.insert(tk.END, 
                        f"\n  ... and {len(positions) - 50} more matches\n"
                    )
            else:
                self.result_text.insert(tk.END, 
                    "❌ No approximate matches found within the specified distance.\n"
                )
        else:
            matches = approximate_match(text, pattern, max_dist)
            if matches:
                self.result_text.insert(tk.END, 
                    f"✅ Found {len(matches)} approximate match(es):\n\n"
                )
                for i, match in enumerate(matches[:50], 1):
                    self.result_text.insert(tk.END, 
                        f"  {i}. Position {match.position}:\n"
                        f"      Matched: {match.matched_text}\n"
                        f"      Edit Distance: {match.distance}\n\n"
                    )
                if len(matches) > 50:
                    self.result_text.insert(tk.END, 
                        f"  ... and {len(matches) - 50} more matches\n"
                    )
            else:
                self.result_text.insert(tk.END, 
                    "❌ No approximate matches found within the specified distance.\n"
                )
    
    def _clear(self):
        """Clear all inputs and results."""
        self.seq1_entry.delete(0, tk.END)
        self.seq2_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)
        self.file1_label.config(text="")


def run():
    """Run the Approximate Matcher application."""
    root = tk.Tk()
    app = ApproximateMatcherApp(root)
    root.mainloop()


if __name__ == "__main__":
    run()
