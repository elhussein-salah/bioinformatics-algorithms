"""
Indexing algorithms for efficient sequence searching.
"""

import bisect
from typing import Optional


def build_sorted_index(text: str, kmer_length: int) -> list[tuple[str, int]]:
    """
    Build a sorted k-mer index for a text sequence.
    
    Args:
        text: The text to index
        kmer_length: Length of k-mers to index
        
    Returns:
        Sorted list of (kmer, position) tuples
    """
    if not text or kmer_length <= 0 or kmer_length > len(text):
        return []
    
    index = []
    for i in range(len(text) - kmer_length + 1):
        kmer = text[i:i + kmer_length]
        index.append((kmer, i))
    
    index.sort(key=lambda x: x[0])
    return index


def query_index(text: str, pattern: str, index: list[tuple[str, int]]) -> list[int]:
    """
    Query a sorted index to find pattern occurrences.
    
    Args:
        text: The original text
        pattern: The pattern to search for
        index: The sorted k-mer index
        
    Returns:
        List of positions where pattern occurs
    """
    if not index or not pattern or not text:
        return []
    
    kmer_length = len(index[0][0])
    prefix = pattern[:kmer_length]
    
    # Extract keys for binary search
    keys = [entry[0] for entry in index]
    
    # Find range of matching k-mers
    start = bisect.bisect_left(keys, prefix)
    end = bisect.bisect_right(keys, prefix)
    
    # Verify full pattern match at each candidate position
    offsets = []
    for i in range(start, end):
        pos = index[i][1]
        if pos + len(pattern) <= len(text) and text[pos:pos + len(pattern)] == pattern:
            offsets.append(pos)
    
    return offsets


def build_suffix_array(text: str) -> tuple[dict[str, int], list[list]]:
    """
    Build a suffix array for a text string.
    
    Args:
        text: The text to build suffix array for
        
    Returns:
        Tuple of (suffix_to_rank, suffix_table)
        - suffix_to_rank: Dictionary mapping each suffix to its rank
        - suffix_table: List of [suffix, original_position, sorted_rank]
    """
    if not text:
        return {}, []
    
    # Generate all suffixes with their positions
    suffixes = [(text[i:], i) for i in range(len(text))]
    
    # Sort suffixes alphabetically
    sorted_suffixes = sorted(suffixes, key=lambda x: x[0])
    
    # Create suffix to rank mapping
    suffix_to_rank = {suffix: rank for rank, (suffix, _) in enumerate(sorted_suffixes)}
    
    # Build result table
    suffix_table = []
    for i in range(len(text)):
        suffix = text[i:]
        suffix_table.append([suffix, i, suffix_to_rank[suffix]])
    
    return suffix_to_rank, suffix_table


def build_suffix_array_simple(text: str) -> list[int]:
    """
    Build a simple suffix array that returns only the position indices.
    
    Args:
        text: The text to build suffix array for
        
    Returns:
        List of starting positions of sorted suffixes
    """
    if not text:
        return []
    
    # Generate all suffixes with their positions
    suffixes = [(text[i:], i) for i in range(len(text))]
    
    # Sort suffixes alphabetically
    sorted_suffixes = sorted(suffixes, key=lambda x: x[0])
    
    # Return only the positions
    return [pos for _, pos in sorted_suffixes]


def build_inverse_suffix_array(text: str) -> list[int]:
    """
    Build the inverse suffix array for a text string.
    
    The inverse suffix array maps each position i in the original text
    to its rank in the sorted order of suffixes. If suffix_array[j] = i,
    then inverse_suffix_array[i] = j.
    
    Args:
        text: The text to build inverse suffix array for
        
    Returns:
        List where inverse_sa[i] gives the rank of suffix starting at position i
        
    Example:
        >>> text = "banana"
        >>> sa = build_suffix_array_simple(text)  # [5, 3, 1, 0, 4, 2]
        >>> isa = build_inverse_suffix_array(text)  # [3, 2, 5, 1, 4, 0]
        >>> # Verification: for all i, isa[sa[i]] == i
    """
    if not text:
        return []
    
    # First build the suffix array
    suffix_array = build_suffix_array_simple(text)
    
    # Build inverse suffix array
    n = len(text)
    inverse_sa = [0] * n
    
    for rank, position in enumerate(suffix_array):
        inverse_sa[position] = rank
    
    return inverse_sa


def build_suffix_array_with_inverse(text: str) -> tuple[list[int], list[int]]:
    """
    Build both suffix array and inverse suffix array simultaneously.
    
    Args:
        text: The text to build arrays for
        
    Returns:
        Tuple of (suffix_array, inverse_suffix_array)
        - suffix_array: List of starting positions of sorted suffixes
        - inverse_suffix_array: List mapping positions to ranks
    """
    if not text:
        return [], []
    
    # Generate all suffixes with their positions
    suffixes = [(text[i:], i) for i in range(len(text))]
    
    # Sort suffixes alphabetically
    sorted_suffixes = sorted(suffixes, key=lambda x: x[0])
    
    # Build suffix array
    suffix_array = [pos for _, pos in sorted_suffixes]
    
    # Build inverse suffix array
    n = len(text)
    inverse_sa = [0] * n
    
    for rank, position in enumerate(suffix_array):
        inverse_sa[position] = rank
    
    return suffix_array, inverse_sa
