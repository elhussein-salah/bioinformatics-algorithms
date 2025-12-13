"""
Bioinformatics Toolkit - Modern Single-Window Application
A sleek, modern bioinformatics GUI with single-window navigation.
"""

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.gui.modern_base import ModernApp, MODERN_THEME


class BioinformaticsApp(ModernApp):
    """Main application with modern single-window navigation."""
    
    def __init__(self, root: tk.Tk):
        super().__init__(root, "🧬 Bioinformatics Toolkit")
        self._build_home_page()
    
    def _build_home_page(self):
        """Build the home page with tool cards."""
        self.navigate_to('home', self._create_home_content)
    
    def _create_home_content(self, container: tk.Frame):
        """Create the home page content."""
        # Header
        header = tk.Frame(container, bg=MODERN_THEME['bg_secondary'], height=100)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # About button (top right)
        about_btn = self.create_button(
            header, "ℹ️ About", self._show_about_dialog,
            style='ghost', width=10
        )
        about_btn.pack(side='right', padx=20, pady=30)
        
        # Logo and title
        title_frame = tk.Frame(header, bg=MODERN_THEME['bg_secondary'])
        title_frame.pack(expand=True)
        
        title = tk.Label(
            title_frame,
            text="🧬 Bioinformatics Toolkit",
            font=(MODERN_THEME['font_family'], 28, 'bold'),
            bg=MODERN_THEME['bg_secondary'],
            fg=MODERN_THEME['accent_primary']
        )
        title.pack(pady=(20, 5))
        
        subtitle = tk.Label(
            title_frame,
            text="DNA & Protein Sequence Analysis Tools",
            font=(MODERN_THEME['font_family'], 12),
            bg=MODERN_THEME['bg_secondary'],
            fg=MODERN_THEME['text_secondary']
        )
        subtitle.pack()
        
        # Scrollable content area
        canvas = tk.Canvas(container, bg=MODERN_THEME['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=MODERN_THEME['bg_primary'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Tool categories
        categories = [
            {
                'name': '🔬 Sequence Analysis',
                'tools': [
                    {
                        'id': 'fasta_processor',
                        'name': 'FASTA Processor',
                        'desc': 'GC content, complement, reverse operations',
                        'icon': '📄',
                        'color': MODERN_THEME['accent_primary']
                    },
                    {
                        'id': 'dna_translator',
                        'name': 'DNA Translator',
                        'desc': 'Translate DNA to protein sequences',
                        'icon': '🧬',
                        'color': MODERN_THEME['success']
                    },
                    {
                        'id': 'hemolytic',
                        'name': 'Hemolytic Predictor',
                        'desc': 'Analyze hemolytic activity of peptides',
                        'icon': '🔬',
                        'color': MODERN_THEME['warning']
                    }
                ]
            },
            {
                'name': '🔍 Pattern Matching',
                'tools': [
                    {
                        'id': 'exact_match',
                        'name': 'Exact Match Finder',
                        'desc': 'Naive pattern matching algorithm',
                        'icon': '🔍',
                        'color': MODERN_THEME['accent_primary']
                    },
                    {
                        'id': 'bad_character',
                        'name': 'Boyer-Moore Match',
                        'desc': 'Bad character heuristic algorithm',
                        'icon': '⚡',
                        'color': MODERN_THEME['info']
                    },
                    {
                        'id': 'approximate_match',
                        'name': 'Approximate Match',
                        'desc': 'Edit Distance & Hamming algorithms',
                        'icon': '🎯',
                        'color': MODERN_THEME['accent_secondary']
                    }
                ]
            },
            {
                'name': '📊 Indexing & Data Structures',
                'tools': [
                    {
                        'id': 'indexing',
                        'name': 'K-mer Indexing',
                        'desc': 'Build and query k-mer indices',
                        'icon': '📊',
                        'color': MODERN_THEME['success']
                    },
                    {
                        'id': 'suffix_array',
                        'name': 'Suffix Array',
                        'desc': 'Generate suffix arrays for strings',
                        'icon': '📝',
                        'color': MODERN_THEME['warning']
                    },
                    {
                        'id': 'overlap',
                        'name': 'Overlap Detector',
                        'desc': 'Find overlaps between sequences',
                        'icon': '🔗',
                        'color': MODERN_THEME['info']
                    }
                ]
            },
            {
                'name': '📁 File Operations',
                'tools': [
                    {
                        'id': 'fasta_converter',
                        'name': 'FASTA Converter',
                        'desc': 'Convert FASTA to CSV & read sequences',
                        'icon': '📁',
                        'color': MODERN_THEME['accent_primary']
                    }
                ]
            }
        ]
        
        for category in categories:
            self._create_category_section(scrollable_frame, category)
    
    def _create_category_section(self, parent: tk.Frame, category: dict):
        """Create a category section with tool cards."""
        # Category header
        cat_frame = tk.Frame(parent, bg=MODERN_THEME['bg_primary'])
        cat_frame.pack(fill='x', pady=(20, 10), padx=10)
        
        cat_label = tk.Label(
            cat_frame,
            text=category['name'],
            font=(MODERN_THEME['font_family'], 16, 'bold'),
            bg=MODERN_THEME['bg_primary'],
            fg=MODERN_THEME['text_primary']
        )
        cat_label.pack(anchor='w')
        
        # Tools grid
        tools_frame = tk.Frame(parent, bg=MODERN_THEME['bg_primary'])
        tools_frame.pack(fill='x', padx=10)
        
        for i, tool in enumerate(category['tools']):
            card = self._create_tool_card(tools_frame, tool)
            card.grid(row=0, column=i, padx=10, pady=10, sticky='nsew')
            tools_frame.grid_columnconfigure(i, weight=1)
    
    def _create_tool_card(self, parent: tk.Frame, tool: dict) -> tk.Frame:
        """Create a modern tool card."""
        card = tk.Frame(
            parent,
            bg=MODERN_THEME['bg_card'],
            padx=20,
            pady=20,
            cursor='hand2'
        )
        
        # Icon
        icon_label = tk.Label(
            card,
            text=tool['icon'],
            font=(MODERN_THEME['font_family'], 32),
            bg=MODERN_THEME['bg_card'],
            fg=tool['color']
        )
        icon_label.pack(pady=(0, 10))
        
        # Title
        title_label = tk.Label(
            card,
            text=tool['name'],
            font=(MODERN_THEME['font_family'], 14, 'bold'),
            bg=MODERN_THEME['bg_card'],
            fg=MODERN_THEME['text_primary']
        )
        title_label.pack(pady=(0, 5))
        
        # Description
        desc_label = tk.Label(
            card,
            text=tool['desc'],
            font=(MODERN_THEME['font_family'], 10),
            bg=MODERN_THEME['bg_card'],
            fg=MODERN_THEME['text_secondary'],
            wraplength=200
        )
        desc_label.pack(pady=(0, 10))
        
        # Hover effects
        def on_enter(e):
            card.configure(bg=MODERN_THEME['bg_hover'])
            for child in card.winfo_children():
                try:
                    child.configure(bg=MODERN_THEME['bg_hover'])
                except:
                    pass
        
        def on_leave(e):
            card.configure(bg=MODERN_THEME['bg_card'])
            for child in card.winfo_children():
                try:
                    child.configure(bg=MODERN_THEME['bg_card'])
                except:
                    pass
        
        def on_click(e):
            self._launch_tool(tool['id'])
        
        # Bind events to card and all children
        for widget in [card, icon_label, title_label, desc_label]:
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
            widget.bind('<Button-1>', on_click)
        
        return card
    
    def _launch_tool(self, tool_id: str):
        """Launch a specific tool in the same window."""
        tool_builders = {
            'hemolytic': self._build_hemolytic_page,
            'fasta_processor': self._build_fasta_processor_page,
            'dna_translator': self._build_dna_translator_page,
            'exact_match': self._build_exact_match_page,
            'bad_character': self._build_bad_character_page,
            'approximate_match': self._build_approximate_match_page,
            'indexing': self._build_indexing_page,
            'suffix_array': self._build_suffix_array_page,
            'overlap': self._build_overlap_page,
            'fasta_converter': self._build_fasta_converter_page,
        }
        
        builder = tool_builders.get(tool_id)
        if builder:
            self.navigate_to(tool_id, builder)
    
    def _show_about_dialog(self):
        """Show the About dialog with team information."""
        # Create a modern dialog window
        about_window = tk.Toplevel(self.root)
        about_window.title("About - Bio Team Project")
        about_window.geometry("500x600")
        about_window.configure(bg=MODERN_THEME['bg_primary'])
        about_window.resizable(False, False)
        
        # Center the window
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Center on screen
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() - 500) // 2
        y = (about_window.winfo_screenheight() - 600) // 2
        about_window.geometry(f"500x600+{x}+{y}")
        
        # Header
        header = tk.Frame(about_window, bg=MODERN_THEME['bg_secondary'], height=120)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        logo_label = tk.Label(
            header,
            text="🧬",
            font=(MODERN_THEME['font_family'], 48),
            bg=MODERN_THEME['bg_secondary'],
            fg=MODERN_THEME['accent_primary']
        )
        logo_label.pack(pady=(15, 5))
        
        title_label = tk.Label(
            header,
            text="Bioinformatics Toolkit",
            font=(MODERN_THEME['font_family'], 18, 'bold'),
            bg=MODERN_THEME['bg_secondary'],
            fg=MODERN_THEME['text_primary']
        )
        title_label.pack()
        
        # Content
        content = tk.Frame(about_window, bg=MODERN_THEME['bg_primary'])
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Version info
        version_label = tk.Label(
            content,
            text="Version 1.0",
            font=(MODERN_THEME['font_family'], 12),
            bg=MODERN_THEME['bg_primary'],
            fg=MODERN_THEME['accent_primary']
        )
        version_label.pack(pady=(0, 20))
        
        # Team section
        team_frame = tk.Frame(content, bg=MODERN_THEME['bg_card'], padx=20, pady=20)
        team_frame.pack(fill='x', pady=10)
        
        team_title = tk.Label(
            team_frame,
            text="👥 Created by Bio Team",
            font=(MODERN_THEME['font_family'], 14, 'bold'),
            bg=MODERN_THEME['bg_card'],
            fg=MODERN_THEME['accent_primary']
        )
        team_title.pack(pady=(0, 15))
        
        # Team members
        team_members = [
            ("EL-Hussein Salah", "🎯"),
            ("Asmaa Nazih", "🔬"),
            # ("Shams Hisham", "🧬"),
            # ("Abdo Nawwar", "💻"),
            # ("Yousef Hussein", "📊"),
            # ("Ziad Mohammed", "⚡"),
        ]
        
        for name, icon in team_members:
            member_frame = tk.Frame(team_frame, bg=MODERN_THEME['bg_card'])
            member_frame.pack(fill='x', pady=5)
            
            member_label = tk.Label(
                member_frame,
                text=f"{icon}  {name}",
                font=(MODERN_THEME['font_family'], 12),
                bg=MODERN_THEME['bg_card'],
                fg=MODERN_THEME['text_primary']
            )
            member_label.pack(anchor='center')
        
        # Description
        desc_frame = tk.Frame(content, bg=MODERN_THEME['bg_primary'])
        desc_frame.pack(fill='x', pady=20)
        
        desc_text = tk.Label(
            desc_frame,
            text="A comprehensive toolkit for DNA and protein\nsequence analysis, pattern matching, and\nbioinformatics operations.",
            font=(MODERN_THEME['font_family'], 10),
            bg=MODERN_THEME['bg_primary'],
            fg=MODERN_THEME['text_secondary'],
            justify='center'
        )
        desc_text.pack()
        
        # Footer
        footer = tk.Frame(about_window, bg=MODERN_THEME['bg_primary'])
        footer.pack(fill='x', padx=30, pady=20)
        
        year_label = tk.Label(
            footer,
            text="© 2024-2025 Bio Team Project",
            font=(MODERN_THEME['font_family'], 10),
            bg=MODERN_THEME['bg_primary'],
            fg=MODERN_THEME['text_muted']
        )
        year_label.pack()
        
        # Close button
        close_btn = self.create_button(
            footer, "Close", about_window.destroy,
            style='primary', width=15
        )
        close_btn.pack(pady=15)
    
    # ==================== Tool Page Builders ====================
    
    def _build_fasta_processor_page(self, container: tk.Frame):
        """Build the FASTA processor page."""
        from src.core.sequence_operations import gc_content, complement, reverse, reverse_complement
        
        header = self.create_header(container, "📄 FASTA Processor")
        
        content = tk.Frame(container, bg=MODERN_THEME['bg_primary'])
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Input section
        input_card = self.create_card(content, "Input Sequence")
        input_card.pack(fill='x', pady=10)
        
        input_frame = tk.Frame(input_card, bg=MODERN_THEME['bg_card'])
        input_frame.pack(fill='x')
        
        # File chooser button
        file_btn = self.create_button(
            input_frame, "Load FASTA File", 
            lambda: self._load_fasta_to_entry(seq_entry, status_label),
            style='secondary', icon='📂'
        )
        file_btn.pack(side='left', pady=10)
        
        status_label = self.create_label(input_frame, "", size='sm', color=MODERN_THEME['text_muted'])
        status_label.pack(side='left', padx=20)
        
        self.create_label(input_card, "Or enter DNA sequence:", size='sm').pack(anchor='w', pady=(10, 5))
        seq_entry = self.create_entry(input_card, width=80, placeholder="Enter DNA sequence (A, C, G, T)...")
        seq_entry.pack(fill='x', pady=5)
        
        # Process button
        result_text = None
        
        def process():
            nonlocal result_text
            seq = seq_entry.get().strip().upper()
            if seq.startswith("ENTER DNA"):
                seq = ""
            
            if not seq:
                self.show_message("Error", "Please enter a DNA sequence", 'error')
                return
            
            valid_chars = set("ACGT")
            if not all(c in valid_chars for c in seq):
                self.show_message("Error", "Invalid DNA sequence. Use only A, C, G, T.", 'error')
                return
            
            try:
                gc = gc_content(seq)
                comp = complement(seq)
                rev = reverse(seq)
                rev_comp = reverse_complement(seq)
                
                result_text.configure(state='normal')
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, 
                    f"═══ Sequence Analysis Results ═══\n\n"
                    f"Original Sequence ({len(seq)} bp):\n{seq[:100]}{'...' if len(seq) > 100 else ''}\n\n"
                    f"GC Content: {gc:.4f} ({gc*100:.2f}%)\n\n"
                    f"Complement:\n{comp[:100]}{'...' if len(comp) > 100 else ''}\n\n"
                    f"Reverse:\n{rev[:100]}{'...' if len(rev) > 100 else ''}\n\n"
                    f"Reverse Complement:\n{rev_comp[:100]}{'...' if len(rev_comp) > 100 else ''}\n"
                )
                result_text.configure(state='disabled')
            except Exception as e:
                self.show_message("Error", f"Processing error: {e}", 'error')
        
        btn_frame = tk.Frame(content, bg=MODERN_THEME['bg_primary'])
        btn_frame.pack(pady=15)
        
        process_btn = self.create_button(btn_frame, "Process Sequence", process, icon='▶')
        process_btn.pack(side='left', padx=5)
        
        clear_btn = self.create_button(
            btn_frame, "Clear", 
            lambda: (seq_entry.delete(0, tk.END), result_text.configure(state='normal'), 
                    result_text.delete(1.0, tk.END), result_text.configure(state='disabled')),
            style='danger', icon='🗑'
        )
        clear_btn.pack(side='left', padx=5)
        
        # Results section
        result_card = self.create_card(content, "Results")
        result_card.pack(fill='both', expand=True, pady=10)
        
        result_text = self.create_text_area(result_card, height=15, readonly=True)
        result_text.pack(fill='both', expand=True)
    
    def _build_dna_translator_page(self, container: tk.Frame):
        """Build the DNA translator page."""
        from src.core.sequence_operations import translate_dna_to_protein
        
        header = self.create_header(container, "🧬 DNA Translator")
        
        content = tk.Frame(container, bg=MODERN_THEME['bg_primary'])
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Input section
        input_card = self.create_card(content, "DNA Sequence Input")
        input_card.pack(fill='x', pady=10)
        
        input_frame = tk.Frame(input_card, bg=MODERN_THEME['bg_card'])
        input_frame.pack(fill='x')
        
        file_btn = self.create_button(
            input_frame, "Load FASTA File",
            lambda: self._load_fasta_to_entry(dna_entry, status_label),
            style='secondary', icon='📂'
        )
        file_btn.pack(side='left', pady=10)
        
        status_label = self.create_label(input_frame, "", size='sm', color=MODERN_THEME['text_muted'])
        status_label.pack(side='left', padx=20)
        
        self.create_label(input_card, "Or enter DNA sequence:", size='sm').pack(anchor='w', pady=(10, 5))
        dna_entry = self.create_entry(input_card, width=80, placeholder="Enter DNA sequence...")
        dna_entry.pack(fill='x', pady=5)
        
        result_text = None
        
        def translate():
            nonlocal result_text
            seq = dna_entry.get().strip().upper()
            if seq.startswith("ENTER DNA"):
                seq = ""
            
            if not seq:
                self.show_message("Error", "Please enter a DNA sequence", 'error')
                return
            
            try:
                protein = translate_dna_to_protein(seq)
                
                result_text.configure(state='normal')
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END,
                    f"═══ Translation Results ═══\n\n"
                    f"DNA Sequence ({len(seq)} bp):\n{seq[:100]}{'...' if len(seq) > 100 else ''}\n\n"
                    f"Protein Sequence ({len(protein)} aa):\n{protein}\n\n"
                    f"Codons: {len(seq)//3}\n"
                )
                result_text.configure(state='disabled')
            except Exception as e:
                self.show_message("Error", f"Translation error: {e}", 'error')
        
        btn_frame = tk.Frame(content, bg=MODERN_THEME['bg_primary'])
        btn_frame.pack(pady=15)
        
        translate_btn = self.create_button(btn_frame, "Translate to Protein", translate, icon='🔄')
        translate_btn.pack(side='left', padx=5)
        
        # Results section
        result_card = self.create_card(content, "Translation Result")
        result_card.pack(fill='both', expand=True, pady=10)
        
        result_text = self.create_text_area(result_card, height=12, readonly=True)
        result_text.pack(fill='both', expand=True)
    
    def _build_exact_match_page(self, container: tk.Frame):
        """Build the exact match page."""
        from src.core.pattern_matching import naive_match, naive_match_all
        
        header = self.create_header(container, "🔍 Exact Match Finder")
        
        content = tk.Frame(container, bg=MODERN_THEME['bg_primary'])
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Input section
        input_card = self.create_card(content, "Search Input")
        input_card.pack(fill='x', pady=10)
        
        # Text input
        self.create_label(input_card, "Text to search in:", size='sm').pack(anchor='w', pady=5)
        text_entry = self.create_entry(input_card, width=80, placeholder="Enter text or load from FASTA...")
        text_entry.pack(fill='x', pady=5)
        
        file_btn = self.create_button(
            input_card, "Load from FASTA",
            lambda: self._load_fasta_to_entry(text_entry, None),
            style='ghost', icon='📂'
        )
        file_btn.pack(anchor='w', pady=5)
        
        self.create_label(input_card, "Pattern to find:", size='sm').pack(anchor='w', pady=(15, 5))
        pattern_entry = self.create_entry(input_card, width=40, placeholder="Enter pattern...")
        pattern_entry.pack(anchor='w', pady=5)
        
        result_text = None
        
        def search():
            nonlocal result_text
            text = text_entry.get().strip().upper()
            pattern = pattern_entry.get().strip().upper()
            
            if "ENTER" in text or "LOAD" in text:
                text = ""
            if "ENTER" in pattern:
                pattern = ""
            
            if not text or not pattern:
                self.show_message("Error", "Please enter both text and pattern", 'error')
                return
            
            try:
                positions = naive_match_all(text, pattern)
                
                result_text.configure(state='normal')
                result_text.delete(1.0, tk.END)
                
                if positions:
                    result_text.insert(tk.END,
                        f"═══ Search Results ═══\n\n"
                        f"Pattern: {pattern}\n"
                        f"Text length: {len(text)}\n\n"
                        f"✅ Found {len(positions)} match(es) at positions:\n\n"
                    )
                    for i, pos in enumerate(positions[:50], 1):
                        context_start = max(0, pos - 10)
                        context_end = min(len(text), pos + len(pattern) + 10)
                        context = text[context_start:context_end]
                        result_text.insert(tk.END, f"  {i}. Position {pos}: ...{context}...\n")
                    
                    if len(positions) > 50:
                        result_text.insert(tk.END, f"\n  ... and {len(positions) - 50} more\n")
                else:
                    result_text.insert(tk.END, f"❌ Pattern '{pattern}' not found in text.\n")
                
                result_text.configure(state='disabled')
            except Exception as e:
                self.show_message("Error", f"Search error: {e}", 'error')
        
        btn_frame = tk.Frame(content, bg=MODERN_THEME['bg_primary'])
        btn_frame.pack(pady=15)
        
        search_btn = self.create_button(btn_frame, "Find Pattern", search, icon='🔍')
        search_btn.pack(side='left', padx=5)
        
        # Results section
        result_card = self.create_card(content, "Search Results")
        result_card.pack(fill='both', expand=True, pady=10)
        
        result_text = self.create_text_area(result_card, height=12, readonly=True)
        result_text.pack(fill='both', expand=True)
    
    def _build_bad_character_page(self, container: tk.Frame):
        """Build the Boyer-Moore bad character page."""
        from src.core.pattern_matching import bad_character_match
        
        header = self.create_header(container, "⚡ Boyer-Moore Bad Character")
        
        content = tk.Frame(container, bg=MODERN_THEME['bg_primary'])
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Input section
        input_card = self.create_card(content, "Search Input")
        input_card.pack(fill='x', pady=10)
        
        self.create_label(input_card, "DNA Text:", size='sm').pack(anchor='w', pady=5)
        text_entry = self.create_entry(input_card, width=80)
        text_entry.pack(fill='x', pady=5)
        
        file_btn = self.create_button(
            input_card, "Load from FASTA",
            lambda: self._load_fasta_to_entry(text_entry, None),
            style='ghost', icon='📂'
        )
        file_btn.pack(anchor='w', pady=5)
        
        self.create_label(input_card, "Pattern:", size='sm').pack(anchor='w', pady=(15, 5))
        pattern_entry = self.create_entry(input_card, width=40)
        pattern_entry.pack(anchor='w', pady=5)
        
        result_label = self.create_label(content, "", size='lg', bold=True)
        result_label.pack(pady=20)
        
        def search():
            text = text_entry.get().strip().upper()
            pattern = pattern_entry.get().strip().upper()
            
            if not text or not pattern:
                self.show_message("Error", "Please enter both text and pattern", 'error')
                return
            
            try:
                position = bad_character_match(text, pattern)
                
                if position >= 0:
                    result_label.configure(
                        text=f"✅ Pattern found at position: {position}",
                        fg=MODERN_THEME['success']
                    )
                else:
                    result_label.configure(
                        text=f"❌ Pattern not found",
                        fg=MODERN_THEME['error']
                    )
            except Exception as e:
                self.show_message("Error", f"Search error: {e}", 'error')
        
        search_btn = self.create_button(content, "Search (Boyer-Moore)", search, icon='⚡')
        search_btn.pack(pady=10)
    
    def _build_approximate_match_page(self, container: tk.Frame):
        """Build the approximate matching page."""
        from src.core.approximate_matching import (
            edit_distance, edit_distance_with_trace,
            approximate_match, approximate_match_hamming
        )
        
        header = self.create_header(container, "🎯 Approximate Match")
        
        content = tk.Frame(container, bg=MODERN_THEME['bg_primary'])
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Options section
        options_card = self.create_card(content, "Options")
        options_card.pack(fill='x', pady=10)
        
        options_frame = tk.Frame(options_card, bg=MODERN_THEME['bg_card'])
        options_frame.pack(fill='x')
        
        # Algorithm selection
        self.create_label(options_frame, "Algorithm:", size='sm').pack(side='left', padx=(0, 10))
        
        algo_var = tk.StringVar(value="edit")
        
        for text, val in [("Edit Distance", "edit"), ("Hamming", "hamming")]:
            rb = tk.Radiobutton(
                options_frame, text=text, variable=algo_var, value=val,
                bg=MODERN_THEME['bg_card'], fg=MODERN_THEME['text_primary'],
                selectcolor=MODERN_THEME['bg_secondary'],
                activebackground=MODERN_THEME['bg_card'],
                font=(MODERN_THEME['font_family'], 11)
            )
            rb.pack(side='left', padx=10)
        
        # Mode selection
        self.create_label(options_frame, "  Mode:", size='sm').pack(side='left', padx=(20, 10))
        
        mode_var = tk.StringVar(value="compare")
        
        for text, val in [("Compare", "compare"), ("Search", "search")]:
            rb = tk.Radiobutton(
                options_frame, text=text, variable=mode_var, value=val,
                bg=MODERN_THEME['bg_card'], fg=MODERN_THEME['text_primary'],
                selectcolor=MODERN_THEME['bg_secondary'],
                activebackground=MODERN_THEME['bg_card'],
                font=(MODERN_THEME['font_family'], 11)
            )
            rb.pack(side='left', padx=10)
        
        # Max distance
        self.create_label(options_frame, "  Max Distance:", size='sm').pack(side='left', padx=(20, 10))
        max_dist_spin = tk.Spinbox(
            options_frame, from_=1, to=10, width=5,
            font=(MODERN_THEME['font_family'], 11),
            bg=MODERN_THEME['bg_secondary'],
            fg=MODERN_THEME['text_primary']
        )
        max_dist_spin.pack(side='left')
        
        # Input section
        input_card = self.create_card(content, "Sequences")
        input_card.pack(fill='x', pady=10)
        
        self.create_label(input_card, "Sequence 1 / Text:", size='sm').pack(anchor='w', pady=5)
        seq1_entry = self.create_entry(input_card, width=80)
        seq1_entry.pack(fill='x', pady=5)
        
        load_btn = self.create_button(
            input_card, "Load from FASTA",
            lambda: self._load_fasta_to_entry(seq1_entry, None),
            style='ghost', icon='📂'
        )
        load_btn.pack(anchor='w', pady=5)
        
        self.create_label(input_card, "Sequence 2 / Pattern:", size='sm').pack(anchor='w', pady=(10, 5))
        seq2_entry = self.create_entry(input_card, width=80)
        seq2_entry.pack(fill='x', pady=5)
        
        result_text = None
        
        def calculate():
            nonlocal result_text
            seq1 = seq1_entry.get().strip().upper()
            seq2 = seq2_entry.get().strip().upper()
            algo = algo_var.get()
            mode = mode_var.get()
            
            if not seq1 or not seq2:
                self.show_message("Error", "Please enter both sequences", 'error')
                return
            
            try:
                max_dist = int(max_dist_spin.get())
            except:
                max_dist = 2
            
            result_text.configure(state='normal')
            result_text.delete(1.0, tk.END)
            
            try:
                if mode == "compare":
                    if algo == "hamming":
                        if len(seq1) != len(seq2):
                            result_text.insert(tk.END,
                                "⚠️ Hamming distance requires equal length sequences!\n"
                                f"Seq1: {len(seq1)}, Seq2: {len(seq2)}\n\n"
                                "Switching to Edit Distance...\n\n"
                            )
                            algo = "edit"
                        else:
                            distance = sum(c1 != c2 for c1, c2 in zip(seq1, seq2))
                            similarity = (1 - distance/len(seq1)) * 100
                            result_text.insert(tk.END,
                                f"═══ Hamming Distance Analysis ═══\n\n"
                                f"Hamming Distance: {distance}\n"
                                f"Similarity: {similarity:.2f}%\n"
                            )
                            result_text.configure(state='disabled')
                            return
                    
                    distance, ops = edit_distance_with_trace(seq1, seq2)
                    max_len = max(len(seq1), len(seq2))
                    similarity = (1 - distance / max_len) * 100 if max_len > 0 else 100
                    
                    result_text.insert(tk.END,
                        f"═══ Edit Distance Analysis ═══\n\n"
                        f"Edit Distance: {distance}\n"
                        f"Similarity: {similarity:.2f}%\n\n"
                        f"Operations:\n"
                        f"  Matches: {ops.count('M')}\n"
                        f"  Substitutions: {ops.count('S')}\n"
                        f"  Insertions: {ops.count('I')}\n"
                        f"  Deletions: {ops.count('D')}\n"
                    )
                else:
                    # Search mode
                    if algo == "hamming":
                        positions = approximate_match_hamming(seq1, seq2, max_dist)
                        if positions:
                            result_text.insert(tk.END,
                                f"✅ Found {len(positions)} match(es):\n\n"
                            )
                            for i, pos in enumerate(positions[:30], 1):
                                matched = seq1[pos:pos+len(seq2)]
                                result_text.insert(tk.END, f"  {i}. Position {pos}: {matched}\n")
                        else:
                            result_text.insert(tk.END, "❌ No matches found.\n")
                    else:
                        matches = approximate_match(seq1, seq2, max_dist)
                        if matches:
                            result_text.insert(tk.END,
                                f"✅ Found {len(matches)} match(es):\n\n"
                            )
                            for i, m in enumerate(matches[:30], 1):
                                result_text.insert(tk.END,
                                    f"  {i}. Pos {m.position}: {m.matched_text} (dist: {m.distance})\n"
                                )
                        else:
                            result_text.insert(tk.END, "❌ No matches found.\n")
                
                result_text.configure(state='disabled')
            except Exception as e:
                result_text.insert(tk.END, f"Error: {e}\n")
                result_text.configure(state='disabled')
        
        calc_btn = self.create_button(content, "Calculate", calculate, icon='🎯')
        calc_btn.pack(pady=15)
        
        # Results
        result_card = self.create_card(content, "Results")
        result_card.pack(fill='both', expand=True, pady=10)
        
        result_text = self.create_text_area(result_card, height=10, readonly=True)
        result_text.pack(fill='both', expand=True)
    
    def _build_indexing_page(self, container: tk.Frame):
        """Build the indexing page."""
        from src.core.indexing import build_sorted_index, query_index
        
        header = self.create_header(container, "📊 K-mer Indexing")
        
        content = tk.Frame(container, bg=MODERN_THEME['bg_primary'])
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Input section
        input_card = self.create_card(content, "Build Index")
        input_card.pack(fill='x', pady=10)
        
        self.create_label(input_card, "Sequence:", size='sm').pack(anchor='w', pady=5)
        seq_entry = self.create_entry(input_card, width=80)
        seq_entry.pack(fill='x', pady=5)
        
        file_btn = self.create_button(
            input_card, "Load from FASTA",
            lambda: self._load_fasta_to_entry(seq_entry, None),
            style='ghost', icon='📂'
        )
        file_btn.pack(anchor='w', pady=5)
        
        kmer_frame = tk.Frame(input_card, bg=MODERN_THEME['bg_card'])
        kmer_frame.pack(fill='x', pady=10)
        
        self.create_label(kmer_frame, "K-mer size:", size='sm').pack(side='left')
        kmer_spin = tk.Spinbox(
            kmer_frame, from_=2, to=20, width=5,
            font=(MODERN_THEME['font_family'], 11),
            bg=MODERN_THEME['bg_secondary'],
            fg=MODERN_THEME['text_primary']
        )
        kmer_spin.delete(0, tk.END)
        kmer_spin.insert(0, "3")
        kmer_spin.pack(side='left', padx=10)
        
        self.create_label(kmer_frame, "Query pattern:", size='sm').pack(side='left', padx=(20, 10))
        query_entry = self.create_entry(kmer_frame, width=20)
        query_entry.pack(side='left')
        
        result_text = None
        index_data = {'index': None, 'keys': None}
        
        def build_index():
            nonlocal result_text
            seq = seq_entry.get().strip().upper()
            try:
                k = int(kmer_spin.get())
            except:
                k = 3
            
            if not seq:
                self.show_message("Error", "Please enter a sequence", 'error')
                return
            
            try:
                index, keys = build_sorted_index(seq, k)
                index_data['index'] = index
                index_data['keys'] = keys
                
                result_text.configure(state='normal')
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END,
                    f"═══ Index Built Successfully ═══\n\n"
                    f"Sequence length: {len(seq)}\n"
                    f"K-mer size: {k}\n"
                    f"Unique k-mers: {len(set(keys))}\n"
                    f"Total entries: {len(keys)}\n\n"
                    f"Sample k-mers:\n"
                )
                for kmer in list(set(keys))[:20]:
                    result_text.insert(tk.END, f"  {kmer}\n")
                result_text.configure(state='disabled')
                
                self.show_message("Success", "Index built successfully!", 'info')
            except Exception as e:
                self.show_message("Error", f"Build error: {e}", 'error')
        
        def query():
            nonlocal result_text
            if index_data['index'] is None:
                self.show_message("Error", "Please build index first", 'error')
                return
            
            pattern = query_entry.get().strip().upper()
            if not pattern:
                self.show_message("Error", "Please enter a query pattern", 'error')
                return
            
            try:
                positions = query_index(pattern, index_data['index'], index_data['keys'])
                
                result_text.configure(state='normal')
                result_text.delete(1.0, tk.END)
                
                if positions:
                    result_text.insert(tk.END,
                        f"═══ Query Results ═══\n\n"
                        f"Pattern: {pattern}\n"
                        f"Found at positions: {positions}\n"
                    )
                else:
                    result_text.insert(tk.END, f"Pattern '{pattern}' not found in index.\n")
                
                result_text.configure(state='disabled')
            except Exception as e:
                self.show_message("Error", f"Query error: {e}", 'error')
        
        btn_frame = tk.Frame(content, bg=MODERN_THEME['bg_primary'])
        btn_frame.pack(pady=15)
        
        build_btn = self.create_button(btn_frame, "Build Index", build_index, icon='🔨')
        build_btn.pack(side='left', padx=5)
        
        query_btn = self.create_button(btn_frame, "Query Index", query, style='secondary', icon='🔍')
        query_btn.pack(side='left', padx=5)
        
        # Results
        result_card = self.create_card(content, "Results")
        result_card.pack(fill='both', expand=True, pady=10)
        
        result_text = self.create_text_area(result_card, height=12, readonly=True)
        result_text.pack(fill='both', expand=True)
    
    def _build_suffix_array_page(self, container: tk.Frame):
        """Build the suffix array page."""
        from src.core.indexing import build_suffix_array
        
        header = self.create_header(container, "📝 Suffix Array")
        
        content = tk.Frame(container, bg=MODERN_THEME['bg_primary'])
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Input section
        input_card = self.create_card(content, "Input")
        input_card.pack(fill='x', pady=10)
        
        self.create_label(input_card, "Text:", size='sm').pack(anchor='w', pady=5)
        text_entry = self.create_entry(input_card, width=80)
        text_entry.pack(fill='x', pady=5)
        
        result_text = None
        
        def build():
            nonlocal result_text
            text = text_entry.get().strip()
            
            if not text:
                self.show_message("Error", "Please enter text", 'error')
                return
            
            try:
                suffix_array = build_suffix_array(text)
                
                result_text.configure(state='normal')
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END,
                    f"═══ Suffix Array ═══\n\n"
                    f"Text: {text}\n"
                    f"Length: {len(text)}\n\n"
                    f"Suffix Array:\n"
                )
                
                for i, idx in enumerate(suffix_array[:50]):
                    suffix = text[idx:]
                    result_text.insert(tk.END, f"  {i}: [{idx}] {suffix}\n")
                
                if len(suffix_array) > 50:
                    result_text.insert(tk.END, f"\n  ... and {len(suffix_array) - 50} more\n")
                
                result_text.configure(state='disabled')
            except Exception as e:
                self.show_message("Error", f"Build error: {e}", 'error')
        
        build_btn = self.create_button(content, "Build Suffix Array", build, icon='📝')
        build_btn.pack(pady=15)
        
        # Results
        result_card = self.create_card(content, "Suffix Array")
        result_card.pack(fill='both', expand=True, pady=10)
        
        result_text = self.create_text_area(result_card, height=15, readonly=True)
        result_text.pack(fill='both', expand=True)
    
    def _build_overlap_page(self, container: tk.Frame):
        """Build the overlap detector page."""
        from src.core.sequence_analysis import compute_overlap
        
        header = self.create_header(container, "🔗 Overlap Detector")
        
        content = tk.Frame(container, bg=MODERN_THEME['bg_primary'])
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Input section
        input_card = self.create_card(content, "Sequences")
        input_card.pack(fill='x', pady=10)
        
        self.create_label(input_card, "Sequence A:", size='sm').pack(anchor='w', pady=5)
        seq_a_entry = self.create_entry(input_card, width=80)
        seq_a_entry.pack(fill='x', pady=5)
        
        self.create_label(input_card, "Sequence B:", size='sm').pack(anchor='w', pady=(10, 5))
        seq_b_entry = self.create_entry(input_card, width=80)
        seq_b_entry.pack(fill='x', pady=5)
        
        min_frame = tk.Frame(input_card, bg=MODERN_THEME['bg_card'])
        min_frame.pack(fill='x', pady=10)
        
        self.create_label(min_frame, "Minimum overlap length:", size='sm').pack(side='left')
        min_spin = tk.Spinbox(
            min_frame, from_=1, to=100, width=5,
            font=(MODERN_THEME['font_family'], 11),
            bg=MODERN_THEME['bg_secondary'],
            fg=MODERN_THEME['text_primary']
        )
        min_spin.delete(0, tk.END)
        min_spin.insert(0, "3")
        min_spin.pack(side='left', padx=10)
        
        result_label = self.create_label(content, "", size='lg', bold=True)
        result_label.pack(pady=20)
        
        def find_overlap():
            seq_a = seq_a_entry.get().strip().upper()
            seq_b = seq_b_entry.get().strip().upper()
            
            try:
                min_len = int(min_spin.get())
            except:
                min_len = 3
            
            if not seq_a or not seq_b:
                self.show_message("Error", "Please enter both sequences", 'error')
                return
            
            try:
                overlap_len, overlap_seq = compute_overlap(seq_a, seq_b, min_len)
                
                if overlap_len > 0:
                    result_label.configure(
                        text=f"✅ Overlap found: {overlap_seq} (length: {overlap_len})",
                        fg=MODERN_THEME['success']
                    )
                else:
                    result_label.configure(
                        text=f"❌ No overlap found with minimum length {min_len}",
                        fg=MODERN_THEME['error']
                    )
            except Exception as e:
                self.show_message("Error", f"Error: {e}", 'error')
        
        find_btn = self.create_button(content, "Find Overlap", find_overlap, icon='🔗')
        find_btn.pack(pady=10)
    
    def _build_hemolytic_page(self, container: tk.Frame):
        """Build the hemolytic predictor page."""
        from src.core.sequence_analysis import parse_hemolytic_file
        
        header = self.create_header(container, "🔬 Hemolytic Predictor")
        
        content = tk.Frame(container, bg=MODERN_THEME['bg_primary'])
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Input section
        input_card = self.create_card(content, "Load Dataset")
        input_card.pack(fill='x', pady=10)
        
        status_label = self.create_label(input_card, "No file loaded", size='sm', 
                                         color=MODERN_THEME['text_muted'])
        status_label.pack(anchor='w', pady=5)
        
        result_text = None
        
        def load_file():
            nonlocal result_text
            file_path = self.choose_file("Select HAPPENN Dataset")
            
            if file_path:
                try:
                    df = parse_hemolytic_file(file_path)
                    status_label.configure(text=f"Loaded: {os.path.basename(file_path)}")
                    
                    result_text.configure(state='normal')
                    result_text.delete(1.0, tk.END)
                    result_text.insert(tk.END,
                        f"═══ Hemolytic Dataset Analysis ═══\n\n"
                        f"Total sequences: {len(df)}\n"
                        f"Hemolytic: {len(df[df['y'] == 1])}\n"
                        f"Non-hemolytic: {len(df[df['y'] == 0])}\n\n"
                        f"Sample sequences:\n"
                    )
                    
                    for i, row in df.head(10).iterrows():
                        label = "Hemolytic" if row['y'] == 1 else "Non-hemolytic"
                        result_text.insert(tk.END, f"  [{label}] {row['Sequence'][:50]}...\n")
                    
                    result_text.configure(state='disabled')
                except Exception as e:
                    self.show_message("Error", f"Failed to parse file: {e}", 'error')
        
        load_btn = self.create_button(input_card, "Load HAPPENN Dataset", load_file, icon='📂')
        load_btn.pack(anchor='w', pady=10)
        
        # Results
        result_card = self.create_card(content, "Analysis Results")
        result_card.pack(fill='both', expand=True, pady=10)
        
        result_text = self.create_text_area(result_card, height=15, readonly=True)
        result_text.pack(fill='both', expand=True)
    
    def _build_fasta_converter_page(self, container: tk.Frame):
        """Build the FASTA converter page with error handling."""
        from src.core.fasta_operations import (
            read_fasta_file, fasta_to_csv, get_fasta_statistics, FastaParseError
        )
        
        header = self.create_header(container, "📁 FASTA Converter")
        
        content = tk.Frame(container, bg=MODERN_THEME['bg_primary'])
        content.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Two columns
        left_col = tk.Frame(content, bg=MODERN_THEME['bg_primary'])
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        right_col = tk.Frame(content, bg=MODERN_THEME['bg_primary'])
        right_col.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Load section
        load_card = self.create_card(left_col, "Load FASTA File")
        load_card.pack(fill='x', pady=10)
        
        status_label = self.create_label(load_card, "No file loaded", size='sm',
                                         color=MODERN_THEME['text_muted'])
        status_label.pack(anchor='w', pady=5)
        
        loaded_file = {'path': None, 'data': None}
        
        stats_text = None
        seq_tree = None
        detail_text = None
        
        def load_fasta():
            file_path = self.choose_file("Select FASTA File")
            
            if not file_path:
                return
            
            try:
                fasta_data = read_fasta_file(file_path)
                loaded_file['path'] = file_path
                loaded_file['data'] = fasta_data
                
                status_label.configure(
                    text=f"✅ Loaded: {os.path.basename(file_path)}",
                    fg=MODERN_THEME['success']
                )
                
                # Update statistics
                try:
                    stats = get_fasta_statistics(file_path)
                    stats_text.configure(state='normal')
                    stats_text.delete(1.0, tk.END)
                    stats_text.insert(tk.END,
                        f"Sequences: {stats['num_sequences']}\n"
                        f"Total length: {stats['total_length']:,} bp\n"
                        f"Average: {stats['avg_length']:,.1f} bp\n"
                        f"Min: {stats['min_length']:,} bp\n"
                        f"Max: {stats['max_length']:,} bp"
                    )
                    stats_text.configure(state='disabled')
                except Exception as e:
                    stats_text.configure(state='normal')
                    stats_text.delete(1.0, tk.END)
                    stats_text.insert(tk.END, f"Stats error: {e}")
                    stats_text.configure(state='disabled')
                
                # Populate tree
                for item in seq_tree.get_children():
                    seq_tree.delete(item)
                
                for seq in fasta_data.sequences:
                    seq_tree.insert('', 'end', values=(
                        seq.id,
                        seq.length,
                        seq.description[:30] + "..." if len(seq.description) > 30 else seq.description
                    ))
                    
            except FastaParseError as e:
                self.show_message("Parse Error", f"Invalid FASTA format:\n{e}", 'error')
                status_label.configure(text=f"❌ Parse error", fg=MODERN_THEME['error'])
            except FileNotFoundError:
                self.show_message("Error", "File not found", 'error')
                status_label.configure(text=f"❌ File not found", fg=MODERN_THEME['error'])
            except Exception as e:
                self.show_message("Error", f"Failed to load file:\n{e}", 'error')
                status_label.configure(text=f"❌ Load error", fg=MODERN_THEME['error'])
        
        load_btn = self.create_button(load_card, "Load FASTA File", load_fasta, icon='📂')
        load_btn.pack(anchor='w', pady=10)
        
        # Statistics section
        stats_card = self.create_card(left_col, "Statistics")
        stats_card.pack(fill='x', pady=10)
        
        stats_text = self.create_text_area(stats_card, height=5, readonly=True)
        stats_text.pack(fill='x')
        
        # Convert section
        convert_card = self.create_card(left_col, "Convert to CSV")
        convert_card.pack(fill='x', pady=10)
        
        # Options
        include_desc_var = tk.BooleanVar(value=True)
        include_len_var = tk.BooleanVar(value=True)
        
        desc_check = tk.Checkbutton(
            convert_card, text="Include Description",
            variable=include_desc_var,
            bg=MODERN_THEME['bg_card'], fg=MODERN_THEME['text_primary'],
            selectcolor=MODERN_THEME['bg_secondary'],
            font=(MODERN_THEME['font_family'], 10)
        )
        desc_check.pack(anchor='w')
        
        len_check = tk.Checkbutton(
            convert_card, text="Include Length",
            variable=include_len_var,
            bg=MODERN_THEME['bg_card'], fg=MODERN_THEME['text_primary'],
            selectcolor=MODERN_THEME['bg_secondary'],
            font=(MODERN_THEME['font_family'], 10)
        )
        len_check.pack(anchor='w')
        
        convert_status = self.create_label(convert_card, "", size='sm')
        convert_status.pack(anchor='w', pady=5)
        
        def convert():
            if not loaded_file['path']:
                self.show_message("Error", "Please load a FASTA file first", 'warning')
                return
            
            # Ask for save location
            save_path = self.save_file(
                "Save CSV As",
                [("CSV files", "*.csv")],
                ".csv"
            )
            
            if not save_path:
                return
            
            try:
                result = fasta_to_csv(
                    loaded_file['path'],
                    save_path,
                    include_description=include_desc_var.get(),
                    include_length=include_len_var.get()
                )
                
                convert_status.configure(
                    text=f"✅ Saved: {os.path.basename(result)}",
                    fg=MODERN_THEME['success']
                )
                self.show_message("Success", f"CSV saved to:\n{result}", 'info')
                
            except FastaParseError as e:
                convert_status.configure(text="❌ Parse error", fg=MODERN_THEME['error'])
                self.show_message("Error", f"FASTA parse error:\n{e}", 'error')
            except PermissionError:
                convert_status.configure(text="❌ Permission denied", fg=MODERN_THEME['error'])
                self.show_message("Error", "Permission denied. File may be open in another program.", 'error')
            except Exception as e:
                convert_status.configure(text="❌ Conversion failed", fg=MODERN_THEME['error'])
                self.show_message("Error", f"Conversion failed:\n{e}", 'error')
        
        convert_btn = self.create_button(convert_card, "Convert to CSV", convert, 
                                         style='success', icon='💾')
        convert_btn.pack(anchor='w', pady=10)
        
        # Right column - Sequence browser
        browse_card = self.create_card(right_col, "Sequences")
        browse_card.pack(fill='both', expand=True, pady=10)
        
        # Treeview
        columns = ('ID', 'Length', 'Description')
        seq_tree = ttk.Treeview(
            browse_card, columns=columns, show='headings',
            height=8, style='Modern.Treeview'
        )
        
        seq_tree.heading('ID', text='ID')
        seq_tree.heading('Length', text='Length')
        seq_tree.heading('Description', text='Description')
        
        seq_tree.column('ID', width=100)
        seq_tree.column('Length', width=60)
        seq_tree.column('Description', width=150)
        
        seq_tree.pack(fill='both', expand=True, pady=5)
        
        # Sequence detail
        detail_card = self.create_card(right_col, "Sequence Detail")
        detail_card.pack(fill='both', expand=True, pady=10)
        
        detail_text = self.create_text_area(detail_card, height=8, readonly=True)
        detail_text.pack(fill='both', expand=True)
        
        def on_select(event):
            selection = seq_tree.selection()
            if not selection or not loaded_file['data']:
                return
            
            values = seq_tree.item(selection[0], 'values')
            seq_id = values[0]
            
            for seq in loaded_file['data'].sequences:
                if seq.id == seq_id:
                    detail_text.configure(state='normal')
                    detail_text.delete(1.0, tk.END)
                    detail_text.insert(tk.END,
                        f"ID: {seq.id}\n"
                        f"Header: {seq.header}\n"
                        f"Length: {seq.length} bp\n\n"
                        f"Sequence:\n"
                    )
                    # Format sequence
                    for i in range(0, len(seq.sequence), 60):
                        detail_text.insert(tk.END, seq.sequence[i:i+60] + '\n')
                    detail_text.configure(state='disabled')
                    break
        
        seq_tree.bind('<<TreeviewSelect>>', on_select)
    
    # ==================== Helper Methods ====================
    
    def _load_fasta_to_entry(self, entry: tk.Entry, status_label=None):
        """Load FASTA file content to an entry widget."""
        file_path = self.choose_file("Select FASTA File")
        
        if file_path:
            sequence = self.read_fasta_file(file_path)
            if sequence:
                entry.delete(0, tk.END)
                entry.insert(0, sequence.upper())
                if status_label:
                    status_label.configure(
                        text=f"Loaded: {os.path.basename(file_path)}",
                        fg=MODERN_THEME['success']
                    )


def main():
    """Main entry point."""
    root = tk.Tk()
    app = BioinformaticsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
