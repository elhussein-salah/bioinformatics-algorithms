"""
FASTA File Operations Module.

This module provides utilities for reading, parsing, and converting
FASTA files to various formats including CSV.
"""

import os
from typing import List, Tuple, Optional, Dict, Iterator
from dataclasses import dataclass, field
import csv


@dataclass
class FastaSequence:
    """Represents a single FASTA sequence entry."""
    header: str
    sequence: str
    description: str = ""
    
    @property
    def id(self) -> str:
        """Extract sequence ID from header (first space-separated token)."""
        return self.header.split()[0] if self.header else ""
    
    @property
    def length(self) -> int:
        """Return sequence length."""
        return len(self.sequence)
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for CSV export."""
        return {
            'ID': self.id,
            'Header': self.header,
            'Description': self.description,
            'Sequence': self.sequence,
            'Length': str(self.length)
        }


@dataclass
class FastaFile:
    """Represents a FASTA file with multiple sequences."""
    filepath: str
    sequences: List[FastaSequence] = field(default_factory=list)
    
    def __len__(self) -> int:
        return len(self.sequences)
    
    def __iter__(self) -> Iterator[FastaSequence]:
        return iter(self.sequences)
    
    def __getitem__(self, index: int) -> FastaSequence:
        return self.sequences[index]


class FastaParseError(Exception):
    """Exception raised when FASTA parsing fails."""
    pass


def read_fasta_file(filepath: str) -> FastaFile:
    """
    Read and parse a FASTA file.
    
    Args:
        filepath: Path to the FASTA file
        
    Returns:
        FastaFile object containing all sequences
        
    Raises:
        FileNotFoundError: If file doesn't exist
        FastaParseError: If file format is invalid
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"FASTA file not found: {filepath}")
    
    sequences = []
    current_header = None
    current_description = ""
    current_sequence_lines = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            if not line:
                continue
            
            if line.startswith('>'):
                # Save previous sequence if exists
                if current_header is not None:
                    sequences.append(FastaSequence(
                        header=current_header,
                        sequence="".join(current_sequence_lines),
                        description=current_description
                    ))
                
                # Parse new header
                header_line = line[1:].strip()  # Remove '>'
                parts = header_line.split(None, 1)  # Split on first whitespace
                current_header = parts[0] if parts else f"seq_{line_num}"
                current_description = parts[1] if len(parts) > 1 else ""
                current_sequence_lines = []
            else:
                if current_header is None:
                    raise FastaParseError(
                        f"Sequence data found before header at line {line_num}"
                    )
                current_sequence_lines.append(line)
    
    # Don't forget the last sequence
    if current_header is not None:
        sequences.append(FastaSequence(
            header=current_header,
            sequence="".join(current_sequence_lines),
            description=current_description
        ))
    
    if not sequences:
        raise FastaParseError("No valid sequences found in FASTA file")
    
    return FastaFile(filepath=filepath, sequences=sequences)


def read_single_sequence(filepath: str) -> Tuple[str, str]:
    """
    Read a single sequence from a FASTA file.
    
    Convenience function for files expected to contain only one sequence.
    
    Args:
        filepath: Path to the FASTA file
        
    Returns:
        Tuple of (header, sequence)
        
    Raises:
        FileNotFoundError: If file doesn't exist
        FastaParseError: If file format is invalid
    """
    fasta = read_fasta_file(filepath)
    if not fasta.sequences:
        raise FastaParseError("No sequences found in file")
    
    first_seq = fasta.sequences[0]
    return first_seq.header, first_seq.sequence


def fasta_to_csv(
    fasta_filepath: str,
    csv_filepath: Optional[str] = None,
    include_description: bool = True,
    include_length: bool = True
) -> str:
    """
    Convert a FASTA file to CSV format.
    
    Args:
        fasta_filepath: Path to the input FASTA file
        csv_filepath: Path for output CSV file (auto-generated if None)
        include_description: Include description column
        include_length: Include sequence length column
        
    Returns:
        Path to the created CSV file
        
    Raises:
        FileNotFoundError: If FASTA file doesn't exist
        FastaParseError: If FASTA format is invalid
    """
    # Parse FASTA file
    fasta = read_fasta_file(fasta_filepath)
    
    # Generate output path if not provided
    if csv_filepath is None:
        base_name = os.path.splitext(fasta_filepath)[0]
        csv_filepath = f"{base_name}.csv"
    
    # Build header row based on options
    fieldnames = ['ID', 'Header']
    if include_description:
        fieldnames.append('Description')
    fieldnames.append('Sequence')
    if include_length:
        fieldnames.append('Length')
    
    # Write CSV file
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for seq in fasta.sequences:
            row = {
                'ID': seq.id,
                'Header': seq.header,
                'Sequence': seq.sequence
            }
            if include_description:
                row['Description'] = seq.description
            if include_length:
                row['Length'] = seq.length
            
            writer.writerow(row)
    
    return csv_filepath


def validate_fasta_sequence(sequence: str, alphabet: str = "ACGT") -> Tuple[bool, List[str]]:
    """
    Validate a FASTA sequence against a given alphabet.
    
    Args:
        sequence: The sequence to validate
        alphabet: Valid characters (default: DNA alphabet)
        
    Returns:
        Tuple of (is_valid, list of invalid characters found)
    """
    alphabet_set = set(alphabet.upper())
    invalid_chars = []
    
    for char in sequence.upper():
        if char not in alphabet_set:
            if char not in invalid_chars:
                invalid_chars.append(char)
    
    return len(invalid_chars) == 0, invalid_chars


def get_fasta_statistics(filepath: str) -> Dict[str, any]:
    """
    Calculate statistics for a FASTA file.
    
    Args:
        filepath: Path to the FASTA file
        
    Returns:
        Dictionary containing various statistics
    """
    fasta = read_fasta_file(filepath)
    
    if not fasta.sequences:
        return {
            'num_sequences': 0,
            'total_length': 0,
            'avg_length': 0,
            'min_length': 0,
            'max_length': 0
        }
    
    lengths = [seq.length for seq in fasta.sequences]
    
    return {
        'num_sequences': len(fasta.sequences),
        'total_length': sum(lengths),
        'avg_length': sum(lengths) / len(lengths),
        'min_length': min(lengths),
        'max_length': max(lengths)
    }
