"""
Modern Base GUI Framework with Single-Window Navigation.

This module provides a modern, sleek UI framework for the bioinformatics toolkit
with single-window navigation, smooth transitions, and premium design aesthetics.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from typing import Optional, Callable, Dict, Any
import os


# Modern Theme Configuration
MODERN_THEME = {
    # Primary colors
    'bg_primary': '#0f0f23',       # Deep dark blue
    'bg_secondary': '#1a1a2e',     # Slightly lighter
    'bg_card': '#16213e',          # Card background
    'bg_hover': '#1f4068',         # Hover state
    
    # Accent colors
    'accent_primary': '#00d4ff',   # Cyan
    'accent_secondary': '#7b2cbf', # Purple
    'accent_gradient_start': '#00d4ff',
    'accent_gradient_end': '#7b2cbf',
    
    # Status colors
    'success': '#00ff88',
    'warning': '#ffbe0b',
    'error': '#ff006e',
    'info': '#4cc9f0',
    
    # Text colors
    'text_primary': '#ffffff',
    'text_secondary': '#a0a0b0',
    'text_muted': '#6c6c7c',
    
    # Font configurations
    'font_family': 'Segoe UI',
    'font_mono': 'Consolas',
    'font_size_sm': 10,
    'font_size_md': 12,
    'font_size_lg': 14,
    'font_size_xl': 18,
    'font_size_title': 24,
    
    # Sizing
    'padding_sm': 5,
    'padding_md': 10,
    'padding_lg': 20,
    'border_radius': 8,
}


class ModernApp:
    """
    Modern single-window application framework with page navigation.
    
    Features:
    - Single-window design with frame-based navigation
    - Back button support
    - Smooth visual feedback
    - Premium aesthetics
    """
    
    def __init__(self, root: tk.Tk, title: str = "Bioinformatics Toolkit"):
        self.root = root
        self.root.title(title)
        self.root.geometry("1100x750")
        self.root.configure(bg=MODERN_THEME['bg_primary'])
        self.root.minsize(900, 600)
        
        # Navigation stack
        self.page_stack = []
        self.current_page = None
        self.pages: Dict[str, tk.Frame] = {}
        
        # Configure styles
        self._configure_styles()
        self._set_icon()
        
        # Main container
        self.main_container = tk.Frame(root, bg=MODERN_THEME['bg_primary'])
        self.main_container.pack(fill='both', expand=True)
    
    def _set_icon(self):
        """Set the application icon if available."""
        try:
            icon_paths = [
                'favicon.ico',
                os.path.join(os.path.dirname(__file__), '..', '..', 'favicon.ico'),
            ]
            for path in icon_paths:
                if os.path.exists(path):
                    self.root.iconbitmap(path)
                    break
        except tk.TclError:
            pass
    
    def _configure_styles(self):
        """Configure ttk styles for modern look."""
        style = ttk.Style()
        
        # Configure Treeview
        style.configure(
            "Modern.Treeview",
            background=MODERN_THEME['bg_card'],
            foreground=MODERN_THEME['text_primary'],
            fieldbackground=MODERN_THEME['bg_card'],
            font=(MODERN_THEME['font_family'], MODERN_THEME['font_size_md'])
        )
        style.configure(
            "Modern.Treeview.Heading",
            background=MODERN_THEME['bg_secondary'],
            foreground=MODERN_THEME['accent_primary'],
            font=(MODERN_THEME['font_family'], MODERN_THEME['font_size_md'], 'bold')
        )
        style.map("Modern.Treeview", 
            background=[('selected', MODERN_THEME['accent_primary'])],
            foreground=[('selected', MODERN_THEME['bg_primary'])]
        )
        
        # Configure Scrollbar
        style.configure(
            "Modern.Vertical.TScrollbar",
            background=MODERN_THEME['bg_secondary'],
            troughcolor=MODERN_THEME['bg_primary'],
            arrowcolor=MODERN_THEME['accent_primary']
        )
    
    def navigate_to(self, page_name: str, page_builder: Callable = None):
        """
        Navigate to a page, creating it if necessary.
        
        Args:
            page_name: Unique identifier for the page
            page_builder: Function to build the page content
        """
        # Hide current page
        if self.current_page:
            self.page_stack.append(self.current_page)
            self.pages[self.current_page].pack_forget()
        
        # Create or show page
        if page_name not in self.pages:
            frame = tk.Frame(self.main_container, bg=MODERN_THEME['bg_primary'])
            self.pages[page_name] = frame
            if page_builder:
                page_builder(frame)
        
        self.pages[page_name].pack(fill='both', expand=True)
        self.current_page = page_name
    
    def go_back(self):
        """Navigate back to the previous page."""
        if self.page_stack:
            # Hide current page
            if self.current_page:
                self.pages[self.current_page].pack_forget()
            
            # Show previous page
            previous = self.page_stack.pop()
            self.pages[previous].pack(fill='both', expand=True)
            self.current_page = previous
    
    def create_header(self, parent: tk.Frame, title: str, show_back: bool = True) -> tk.Frame:
        """
        Create a modern header with optional back button.
        
        Args:
            parent: Parent frame
            title: Page title
            show_back: Whether to show back button
            
        Returns:
            Header frame
        """
        header = tk.Frame(parent, bg=MODERN_THEME['bg_secondary'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Back button
        if show_back and self.page_stack:
            back_btn = self.create_button(
                header, "← Back", self.go_back,
                style='ghost', width=10
            )
            back_btn.pack(side='left', padx=15, pady=15)
        
        # Title
        title_label = tk.Label(
            header,
            text=title,
            font=(MODERN_THEME['font_family'], MODERN_THEME['font_size_xl'], 'bold'),
            bg=MODERN_THEME['bg_secondary'],
            fg=MODERN_THEME['accent_primary']
        )
        title_label.pack(side='left', padx=20, pady=15)
        
        return header
    
    def create_button(self, parent: tk.Widget, text: str, command: Callable,
                      style: str = 'primary', width: int = None,
                      icon: str = None) -> tk.Button:
        """
        Create a modern styled button.
        
        Args:
            parent: Parent widget
            text: Button text
            command: Click callback
            style: 'primary', 'secondary', 'ghost', 'danger', 'success'
            width: Button width
            icon: Optional icon prefix
            
        Returns:
            Styled Button widget
        """
        styles = {
            'primary': {
                'bg': MODERN_THEME['accent_primary'],
                'fg': MODERN_THEME['bg_primary'],
                'active_bg': '#00b8e6'
            },
            'secondary': {
                'bg': MODERN_THEME['bg_card'],
                'fg': MODERN_THEME['text_primary'],
                'active_bg': MODERN_THEME['bg_hover']
            },
            'ghost': {
                'bg': MODERN_THEME['bg_secondary'],
                'fg': MODERN_THEME['text_secondary'],
                'active_bg': MODERN_THEME['bg_card']
            },
            'danger': {
                'bg': MODERN_THEME['error'],
                'fg': MODERN_THEME['text_primary'],
                'active_bg': '#cc0058'
            },
            'success': {
                'bg': MODERN_THEME['success'],
                'fg': MODERN_THEME['bg_primary'],
                'active_bg': '#00cc6e'
            }
        }
        
        btn_style = styles.get(style, styles['primary'])
        display_text = f"{icon} {text}" if icon else text
        
        btn = tk.Button(
            parent,
            text=display_text,
            command=command,
            bg=btn_style['bg'],
            fg=btn_style['fg'],
            activebackground=btn_style['active_bg'],
            activeforeground=btn_style['fg'],
            font=(MODERN_THEME['font_family'], MODERN_THEME['font_size_md'], 'bold'),
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10,
            width=width,
            bd=0
        )
        
        # Hover effects
        def on_enter(e):
            btn.configure(bg=btn_style['active_bg'])
        
        def on_leave(e):
            btn.configure(bg=btn_style['bg'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def create_card(self, parent: tk.Widget, title: str = None, 
                    padding: int = None) -> tk.Frame:
        """
        Create a modern card container.
        
        Args:
            parent: Parent widget
            title: Optional card title
            padding: Internal padding
            
        Returns:
            Card frame
        """
        padding = padding or MODERN_THEME['padding_lg']
        
        card = tk.Frame(
            parent,
            bg=MODERN_THEME['bg_card'],
            padx=padding,
            pady=padding
        )
        
        if title:
            title_label = tk.Label(
                card,
                text=title,
                font=(MODERN_THEME['font_family'], MODERN_THEME['font_size_lg'], 'bold'),
                bg=MODERN_THEME['bg_card'],
                fg=MODERN_THEME['accent_primary']
            )
            title_label.pack(anchor='w', pady=(0, 10))
        
        return card
    
    def create_label(self, parent: tk.Widget, text: str, 
                     size: str = 'md', color: str = None,
                     bold: bool = False) -> tk.Label:
        """
        Create a modern label.
        
        Args:
            parent: Parent widget
            text: Label text
            size: 'sm', 'md', 'lg', 'xl', 'title'
            color: Text color (or use theme default)
            bold: Whether to use bold font
            
        Returns:
            Label widget
        """
        sizes = {
            'sm': MODERN_THEME['font_size_sm'],
            'md': MODERN_THEME['font_size_md'],
            'lg': MODERN_THEME['font_size_lg'],
            'xl': MODERN_THEME['font_size_xl'],
            'title': MODERN_THEME['font_size_title']
        }
        
        font_size = sizes.get(size, sizes['md'])
        font_weight = 'bold' if bold else 'normal'
        fg_color = color or MODERN_THEME['text_primary']
        
        # Determine background based on parent
        try:
            bg_color = parent.cget('bg')
        except:
            bg_color = MODERN_THEME['bg_primary']
        
        return tk.Label(
            parent,
            text=text,
            font=(MODERN_THEME['font_family'], font_size, font_weight),
            bg=bg_color,
            fg=fg_color
        )
    
    def create_entry(self, parent: tk.Widget, width: int = 50,
                     placeholder: str = None) -> tk.Entry:
        """
        Create a modern entry field.
        
        Args:
            parent: Parent widget
            width: Entry width
            placeholder: Placeholder text
            
        Returns:
            Entry widget
        """
        entry = tk.Entry(
            parent,
            width=width,
            font=(MODERN_THEME['font_family'], MODERN_THEME['font_size_md']),
            bg=MODERN_THEME['bg_secondary'],
            fg=MODERN_THEME['text_primary'],
            insertbackground=MODERN_THEME['accent_primary'],
            relief='flat',
            highlightthickness=2,
            highlightcolor=MODERN_THEME['accent_primary'],
            highlightbackground=MODERN_THEME['bg_card']
        )
        
        if placeholder:
            entry.insert(0, placeholder)
            entry.configure(fg=MODERN_THEME['text_muted'])
            
            def on_focus_in(e):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.configure(fg=MODERN_THEME['text_primary'])
            
            def on_focus_out(e):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.configure(fg=MODERN_THEME['text_muted'])
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
        
        return entry
    
    def create_text_area(self, parent: tk.Widget, height: int = 10,
                         readonly: bool = False) -> ScrolledText:
        """
        Create a modern scrolled text area.
        
        Args:
            parent: Parent widget
            height: Text area height in lines
            readonly: Whether the text area is read-only
            
        Returns:
            ScrolledText widget
        """
        text = ScrolledText(
            parent,
            height=height,
            font=(MODERN_THEME['font_mono'], MODERN_THEME['font_size_md']),
            bg=MODERN_THEME['bg_secondary'],
            fg=MODERN_THEME['success'],
            insertbackground=MODERN_THEME['accent_primary'],
            relief='flat',
            wrap='word',
            highlightthickness=2,
            highlightcolor=MODERN_THEME['accent_primary'],
            highlightbackground=MODERN_THEME['bg_card']
        )
        
        if readonly:
            text.configure(state='disabled')
        
        return text
    
    def choose_file(self, title: str = "Select File",
                    filetypes: list = None) -> Optional[str]:
        """
        Open a file dialog.
        
        Args:
            title: Dialog title
            filetypes: List of (description, pattern) tuples
            
        Returns:
            Selected file path or None
        """
        filetypes = filetypes or [
            ("FASTA files", "*.fasta *.fa *.fna *.faa"),
            ("All files", "*.*")
        ]
        
        return filedialog.askopenfilename(title=title, filetypes=filetypes)
    
    def save_file(self, title: str = "Save File",
                  filetypes: list = None,
                  default_ext: str = None) -> Optional[str]:
        """
        Open a save file dialog.
        
        Args:
            title: Dialog title
            filetypes: List of (description, pattern) tuples
            default_ext: Default file extension
            
        Returns:
            Selected file path or None
        """
        filetypes = filetypes or [("All files", "*.*")]
        
        return filedialog.asksaveasfilename(
            title=title,
            filetypes=filetypes,
            defaultextension=default_ext
        )
    
    def show_message(self, title: str, message: str, msg_type: str = 'info'):
        """
        Show a message dialog.
        
        Args:
            title: Dialog title
            message: Message text
            msg_type: 'info', 'warning', 'error', 'success'
        """
        if msg_type == 'error':
            messagebox.showerror(title, message)
        elif msg_type == 'warning':
            messagebox.showwarning(title, message)
        else:
            messagebox.showinfo(title, message)
    
    def read_fasta_file(self, file_path: str) -> Optional[str]:
        """
        Read a FASTA file and return the sequence.
        
        Args:
            file_path: Path to FASTA file
            
        Returns:
            Sequence string or None if error
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file.readlines()]
                sequence_lines = [line for line in lines if line and not line.startswith('>')]
                
                if sequence_lines:
                    return "".join(sequence_lines)
                else:
                    self.show_message("Error", "No sequence found in file", 'error')
                    return None
                    
        except FileNotFoundError:
            self.show_message("Error", f"File not found: {file_path}", 'error')
            return None
        except Exception as e:
            self.show_message("Error", f"Error reading file: {e}", 'error')
            return None
