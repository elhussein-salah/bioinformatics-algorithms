"""
FASTA File Converter GUI Application.

Provides a user interface for converting FASTA files to CSV format
and reading/displaying FASTA sequence information.
"""

import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.scrolledtext import ScrolledText
import os

from .base import BaseApp, THEME
from ..core.fasta_operations import (
    read_fasta_file,
    fasta_to_csv,
    get_fasta_statistics,
    FastaParseError,
    FastaSequence
)


class FastaConverterApp(BaseApp):
    """GUI application for FASTA file operations."""
    
    def __init__(self, root: tk.Tk):
        super().__init__(root, "FASTA File Converter", width=950, height=750)
        self.loaded_fasta = None
        self._create_widgets()
    
    def _create_widgets(self):
        """Create and layout all widgets."""
        # Title
        title_label = self.create_label(
            self.root, 
            "📁 FASTA to CSV Converter & Sequence Reader",
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=15)
        
        # Main container with two panels
        main_frame = tk.Frame(self.root, bg=THEME['bg_color'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - File operations
        left_panel = tk.Frame(main_frame, bg=THEME['bg_color'])
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # File selection section
        file_section = tk.LabelFrame(
            left_panel,
            text="📂 File Selection",
            bg=THEME['bg_color'],
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=10,
            pady=10
        )
        file_section.pack(fill='x', pady=5)
        
        self.load_button = self.create_button(
            file_section, "Load FASTA File", self._load_fasta
        )
        self.load_button.pack(pady=5)
        
        self.file_path_label = self.create_label(
            file_section, "No file loaded", 
            font=('Arial', 10)
        )
        self.file_path_label.pack(pady=5)
        
        # Statistics section
        stats_section = tk.LabelFrame(
            left_panel,
            text="📊 File Statistics",
            bg=THEME['bg_color'],
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=10,
            pady=10
        )
        stats_section.pack(fill='x', pady=10)
        
        self.stats_text = tk.Text(
            stats_section,
            height=6,
            width=40,
            font=('Consolas', 10),
            bg='#1a252f',
            fg='#3498DB',
            state='disabled',
            wrap='word'
        )
        self.stats_text.pack(fill='x', pady=5)
        
        # Conversion options section
        convert_section = tk.LabelFrame(
            left_panel,
            text="⚙️ CSV Conversion Options",
            bg=THEME['bg_color'],
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=10,
            pady=10
        )
        convert_section.pack(fill='x', pady=10)
        
        # Checkboxes for options
        self.include_desc_var = tk.BooleanVar(value=True)
        desc_check = tk.Checkbutton(
            convert_section,
            text="Include Description Column",
            variable=self.include_desc_var,
            bg=THEME['bg_color'],
            fg='white',
            selectcolor=THEME['button_bg'],
            activebackground=THEME['bg_color'],
            activeforeground='white',
            font=('Arial', 10)
        )
        desc_check.pack(anchor='w')
        
        self.include_length_var = tk.BooleanVar(value=True)
        length_check = tk.Checkbutton(
            convert_section,
            text="Include Sequence Length Column",
            variable=self.include_length_var,
            bg=THEME['bg_color'],
            fg='white',
            selectcolor=THEME['button_bg'],
            activebackground=THEME['bg_color'],
            activeforeground='white',
            font=('Arial', 10)
        )
        length_check.pack(anchor='w')
        
        # Convert button
        self.convert_button = self.create_button(
            convert_section, "Convert to CSV", self._convert_to_csv
        )
        self.convert_button.pack(pady=10)
        
        self.convert_status = self.create_label(
            convert_section, "", font=('Arial', 10)
        )
        self.convert_status.pack(pady=5)
        
        # Right panel - Sequence viewer
        right_panel = tk.Frame(main_frame, bg=THEME['bg_color'])
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Sequence list section
        list_section = tk.LabelFrame(
            right_panel,
            text="🧬 Sequences",
            bg=THEME['bg_color'],
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=10,
            pady=10
        )
        list_section.pack(fill='both', expand=True)
        
        # Treeview for sequences
        columns = ('ID', 'Length', 'Description')
        self.seq_tree = ttk.Treeview(
            list_section,
            columns=columns,
            show='headings',
            height=8
        )
        
        # Configure columns
        self.seq_tree.heading('ID', text='Sequence ID')
        self.seq_tree.heading('Length', text='Length')
        self.seq_tree.heading('Description', text='Description')
        
        self.seq_tree.column('ID', width=100)
        self.seq_tree.column('Length', width=70)
        self.seq_tree.column('Description', width=200)
        
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(
            list_section, orient='vertical', command=self.seq_tree.yview
        )
        self.seq_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.seq_tree.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')
        
        # Bind selection event
        self.seq_tree.bind('<<TreeviewSelect>>', self._on_sequence_select)
        
        # Sequence detail section
        detail_section = tk.LabelFrame(
            right_panel,
            text="📝 Sequence Detail",
            bg=THEME['bg_color'],
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=10,
            pady=10
        )
        detail_section.pack(fill='both', expand=True, pady=10)
        
        self.detail_text = ScrolledText(
            detail_section,
            wrap='word',
            height=12,
            font=('Consolas', 10),
            bg='#1a252f',
            fg='#2ECC71'
        )
        self.detail_text.pack(fill='both', expand=True)
        
        # Copy button
        copy_frame = tk.Frame(detail_section, bg=THEME['bg_color'])
        copy_frame.pack(fill='x', pady=5)
        
        self.copy_button = self.create_button(
            copy_frame, "Copy Sequence", self._copy_sequence
        )
        self.copy_button.pack(side='left')
        
        self.export_single_button = self.create_button(
            copy_frame, "Export Selected", self._export_selected
        )
        self.export_single_button.pack(side='left', padx=10)
    
    def _load_fasta(self):
        """Load a FASTA file."""
        filetypes = [
            ("FASTA files", "*.fasta *.fa *.fna *.faa"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select FASTA File",
            filetypes=filetypes
        )
        
        if not file_path:
            return
        
        try:
            self.loaded_fasta = read_fasta_file(file_path)
            self.current_file = file_path
            
            # Update file path label
            filename = os.path.basename(file_path)
            self.file_path_label.config(text=f"Loaded: {filename}")
            
            # Update statistics
            self._update_statistics(file_path)
            
            # Populate sequence list
            self._populate_sequence_list()
            
            self.convert_status.config(text="", fg='white')
            
        except FastaParseError as e:
            self.show_error("Parse Error", str(e))
        except Exception as e:
            self.show_error("Error", f"Failed to load file: {e}")
    
    def _update_statistics(self, file_path: str):
        """Update the statistics display."""
        try:
            stats = get_fasta_statistics(file_path)
            
            self.stats_text.config(state='normal')
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, 
                f"Number of Sequences: {stats['num_sequences']}\n"
                f"Total Length: {stats['total_length']:,} bp\n"
                f"Average Length: {stats['avg_length']:,.1f} bp\n"
                f"Min Length: {stats['min_length']:,} bp\n"
                f"Max Length: {stats['max_length']:,} bp"
            )
            self.stats_text.config(state='disabled')
        except Exception as e:
            self.stats_text.config(state='normal')
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(tk.END, f"Error calculating statistics: {e}")
            self.stats_text.config(state='disabled')
    
    def _populate_sequence_list(self):
        """Populate the sequence treeview."""
        # Clear existing items
        for item in self.seq_tree.get_children():
            self.seq_tree.delete(item)
        
        if self.loaded_fasta:
            for seq in self.loaded_fasta.sequences:
                self.seq_tree.insert('', 'end', values=(
                    seq.id,
                    seq.length,
                    seq.description[:50] + "..." if len(seq.description) > 50 else seq.description
                ))
    
    def _on_sequence_select(self, event):
        """Handle sequence selection in treeview."""
        selection = self.seq_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.seq_tree.item(item, 'values')
        seq_id = values[0]
        
        # Find the sequence
        for seq in self.loaded_fasta.sequences:
            if seq.id == seq_id:
                self._display_sequence_detail(seq)
                break
    
    def _display_sequence_detail(self, seq: FastaSequence):
        """Display detailed sequence information."""
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(tk.END, 
            f"Header: {seq.header}\n"
            f"Description: {seq.description}\n"
            f"Length: {seq.length} bp\n"
            f"\nSequence:\n"
        )
        
        # Format sequence with line breaks every 60 characters
        formatted_seq = '\n'.join(
            seq.sequence[i:i+60] for i in range(0, len(seq.sequence), 60)
        )
        self.detail_text.insert(tk.END, formatted_seq)
    
    def _copy_sequence(self):
        """Copy the displayed sequence to clipboard."""
        if not self.loaded_fasta:
            return
        
        selection = self.seq_tree.selection()
        if not selection:
            self.show_warning("Warning", "Please select a sequence first.")
            return
        
        values = self.seq_tree.item(selection[0], 'values')
        seq_id = values[0]
        
        for seq in self.loaded_fasta.sequences:
            if seq.id == seq_id:
                self.root.clipboard_clear()
                self.root.clipboard_append(seq.sequence)
                self.show_info("Success", "Sequence copied to clipboard!")
                break
    
    def _export_selected(self):
        """Export selected sequence to a new FASTA file."""
        if not self.loaded_fasta:
            return
        
        selection = self.seq_tree.selection()
        if not selection:
            self.show_warning("Warning", "Please select a sequence first.")
            return
        
        values = self.seq_tree.item(selection[0], 'values')
        seq_id = values[0]
        
        # Find the sequence
        selected_seq = None
        for seq in self.loaded_fasta.sequences:
            if seq.id == seq_id:
                selected_seq = seq
                break
        
        if not selected_seq:
            return
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            title="Save Sequence As",
            defaultextension=".fasta",
            filetypes=[("FASTA files", "*.fasta"), ("All files", "*.*")],
            initialfile=f"{seq_id}.fasta"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(f">{selected_seq.header}\n")
                    # Write sequence in 60-character lines
                    for i in range(0, len(selected_seq.sequence), 60):
                        f.write(selected_seq.sequence[i:i+60] + '\n')
                self.show_info("Success", f"Sequence exported to {os.path.basename(file_path)}")
            except Exception as e:
                self.show_error("Error", f"Failed to export: {e}")
    
    def _convert_to_csv(self):
        """Convert loaded FASTA to CSV."""
        if not self.loaded_fasta or not self.current_file:
            self.show_warning("Warning", "Please load a FASTA file first.")
            return
        
        # Ask for save location
        default_name = os.path.splitext(os.path.basename(self.current_file))[0] + ".csv"
        
        file_path = filedialog.asksaveasfilename(
            title="Save CSV As",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=default_name
        )
        
        if not file_path:
            return
        
        try:
            result_path = fasta_to_csv(
                self.current_file,
                file_path,
                include_description=self.include_desc_var.get(),
                include_length=self.include_length_var.get()
            )
            
            self.convert_status.config(
                text=f"✅ Saved to: {os.path.basename(result_path)}",
                fg='#2ECC71'
            )
            self.show_info("Success", f"CSV file created:\n{result_path}")
            
        except Exception as e:
            self.convert_status.config(
                text=f"❌ Conversion failed",
                fg='#E74C3C'
            )
            self.show_error("Conversion Error", str(e))


def run():
    """Run the FASTA Converter application."""
    root = tk.Tk()
    app = FastaConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    run()
