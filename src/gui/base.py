"""
Base GUI components and theme configuration.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional, Callable
import os


# Theme configuration
THEME = {
    'bg_color': '#2C3E50',
    'button_bg': '#16A085',
    'button_fg': 'white',
    'button_active_bg': '#1ABC9C',
    'danger_bg': '#E74C3C',
    'font_family': 'Arial',
    'font_size': 12,
    'title_font_size': 16,
    'window_width': 800,
    'window_height': 600
}


class BaseApp:
    """Base class for all GUI applications with common functionality."""
    
    def __init__(self, root: tk.Tk, title: str, width: int = None, height: int = None):
        """
        Initialize the base application.
        
        Args:
            root: The Tkinter root window
            title: Window title
            width: Window width (optional, uses theme default)
            height: Window height (optional, uses theme default)
        """
        self.root = root
        self.root.title(title)
        
        width = width or THEME['window_width']
        height = height or THEME['window_height']
        self.root.geometry(f"{width}x{height}")
        self.root.configure(bg=THEME['bg_color'])
        
        # Try to set icon, but don't fail if not found
        self._set_icon()
        
        # Initialize file path storage
        self.current_file: Optional[str] = None
    
    def _set_icon(self):
        """Set the application icon if available."""
        try:
            icon_path = self._find_icon()
            if icon_path:
                self.root.iconbitmap(icon_path)
        except tk.TclError:
            pass  # Icon not found or invalid, continue without it
    
    def _find_icon(self) -> Optional[str]:
        """Find the favicon.ico file."""
        # Check common locations
        possible_paths = [
            'favicon.ico',
            os.path.join(os.path.dirname(__file__), '..', '..', 'favicon.ico'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'favicon.ico')
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
    
    def create_button(self, parent: tk.Widget, text: str, command: Callable,
                      danger: bool = False, **kwargs) -> tk.Button:
        """
        Create a styled button.
        
        Args:
            parent: Parent widget
            text: Button text
            command: Button callback function
            danger: If True, use danger (red) styling
            **kwargs: Additional button options
            
        Returns:
            Configured Button widget
        """
        bg = THEME['danger_bg'] if danger else THEME['button_bg']
        
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=THEME['button_fg'],
            font=(THEME['font_family'], THEME['font_size']),
            padx=20,
            pady=5,
            **kwargs
        )
        return button
    
    def create_label(self, parent: tk.Widget, text: str, **kwargs) -> tk.Label:
        """
        Create a styled label.
        
        Args:
            parent: Parent widget
            text: Label text
            **kwargs: Additional label options
            
        Returns:
            Configured Label widget
        """
        label = tk.Label(
            parent,
            text=text,
            bg=THEME['bg_color'],
            fg='white',
            font=(THEME['font_family'], THEME['font_size']),
            **kwargs
        )
        return label
    
    def create_entry(self, parent: tk.Widget, width: int = 50, **kwargs) -> tk.Entry:
        """
        Create a styled entry field.
        
        Args:
            parent: Parent widget
            width: Entry width in characters
            **kwargs: Additional entry options
            
        Returns:
            Configured Entry widget
        """
        entry = tk.Entry(
            parent,
            width=width,
            font=(THEME['font_family'], THEME['font_size']),
            **kwargs
        )
        return entry
    
    def choose_file(self, title: str = "Select File", 
                    filetypes: list = None) -> Optional[str]:
        """
        Open a file dialog to choose a file.
        
        Args:
            title: Dialog title
            filetypes: List of (description, pattern) tuples
            
        Returns:
            Selected file path or None if cancelled
        """
        filetypes = filetypes or [("FASTA files", "*.fasta"), ("All files", "*.*")]
        
        file_path = filedialog.askopenfilename(
            title=title,
            filetypes=filetypes
        )
        
        if file_path:
            self.current_file = file_path
            return file_path
        return None
    
    def show_error(self, title: str, message: str):
        """Show an error message box."""
        messagebox.showerror(title, message)
    
    def show_warning(self, title: str, message: str):
        """Show a warning message box."""
        messagebox.showwarning(title, message)
    
    def show_info(self, title: str, message: str):
        """Show an info message box."""
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
            with open(file_path, 'r') as file:
                lines = [line.strip() for line in file.readlines()]
                
                # Find sequence lines (skip headers starting with >)
                sequence_lines = [line for line in lines if line and not line.startswith('>')]
                
                if sequence_lines:
                    return "".join(sequence_lines)
                else:
                    self.show_error("Error", "No sequence found in file")
                    return None
                    
        except FileNotFoundError:
            self.show_error("Error", f"File not found: {file_path}")
            return None
        except Exception as e:
            self.show_error("Error", f"Error reading file: {e}")
            return None
