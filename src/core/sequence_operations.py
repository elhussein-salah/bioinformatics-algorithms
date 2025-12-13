"""
Core sequence operations for DNA/RNA/Protein analysis.
"""

from typing import Optional

# Standard genetic code - DNA codon to amino acid mapping
CODON_TABLE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G"
}

# DNA complement mapping
COMPLEMENT_MAP = {"A": "T", "T": "A", "G": "C", "C": "G"}


def gc_content(sequence: str) -> float:
    """
    Calculate the GC content of a DNA sequence.
    
    Args:
        sequence: DNA sequence string (uppercase)
        
    Returns:
        GC content as a ratio (0.0 to 1.0)
        
    Raises:
        ValueError: If sequence is empty
    """
    if not sequence:
        raise ValueError("Sequence cannot be empty")
    
    sequence = sequence.upper()
    gc_count = sequence.count("G") + sequence.count("C")
    return gc_count / len(sequence)


def complement(sequence: str) -> str:
    """
    Generate the complement of a DNA sequence.
    
    Args:
        sequence: DNA sequence string
        
    Returns:
        Complementary DNA sequence
        
    Raises:
        ValueError: If sequence contains invalid characters
    """
    sequence = sequence.upper()
    result = []
    
    for nucleotide in sequence:
        if nucleotide not in COMPLEMENT_MAP:
            raise ValueError(f"Invalid nucleotide: {nucleotide}")
        result.append(COMPLEMENT_MAP[nucleotide])
    
    return "".join(result)


def reverse(sequence: str) -> str:
    """
    Reverse a DNA sequence.
    
    Args:
        sequence: DNA sequence string
        
    Returns:
        Reversed sequence
    """
    return sequence[::-1]


def reverse_complement(sequence: str) -> str:
    """
    Generate the reverse complement of a DNA sequence.
    
    Args:
        sequence: DNA sequence string
        
    Returns:
        Reverse complement of the sequence
    """
    return complement(reverse(sequence))


def translate_dna_to_protein(sequence: str) -> tuple[str, str]:
    """
    Translate a DNA sequence to protein sequence.
    
    Args:
        sequence: DNA sequence string
        
    Returns:
        Tuple of (full_translation, orf_translation)
        - full_translation: Complete translation of all codons
        - orf_translation: Translation between start (M) and stop (*) codons
        
    Raises:
        ValueError: If sequence contains invalid codons
    """
    sequence = sequence.upper()
    full_translation = []
    orf_translation = []
    in_orf = False
    
    # Process sequence in codons (groups of 3)
    for i in range(0, len(sequence) - 2, 3):
        codon = sequence[i:i + 3]
        
        if codon not in CODON_TABLE:
            raise ValueError(f"Invalid codon: {codon}")
        
        amino_acid = CODON_TABLE[codon]
        full_translation.append(amino_acid)
        
        # Track ORF (Open Reading Frame)
        if amino_acid == "M":
            in_orf = True
        elif amino_acid == "*":
            in_orf = False
            
        if in_orf:
            orf_translation.append(amino_acid)
    
    return "".join(full_translation), "".join(orf_translation)
