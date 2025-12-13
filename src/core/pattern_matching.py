"""
Pattern matching algorithms for DNA sequence analysis.
"""

from typing import Optional
import numpy as np


def naive_match(text: str, pattern: str) -> int:
    """
    Find the first occurrence of a pattern in text using naive matching.
    
    Args:
        text: The text to search in
        pattern: The pattern to search for
        
    Returns:
        Index of first match, or -1 if not found
    """
    if not pattern or not text:
        return -1
        
    for i in range(len(text) - len(pattern) + 1):
        if text[i:i + len(pattern)] == pattern:
            return i
    return -1


def naive_match_all(text: str, pattern: str) -> list[int]:
    """
    Find all occurrences of a pattern in text using naive matching.
    
    Args:
        text: The text to search in
        pattern: The pattern to search for
        
    Returns:
        List of all match indices
    """
    if not pattern or not text:
        return []
        
    matches = []
    for i in range(len(text) - len(pattern) + 1):
        if text[i:i + len(pattern)] == pattern:
            matches.append(i)
    return matches


def build_bad_character_table(pattern: str, alphabet: str = "ACGT") -> dict[str, list[int]]:
    """
    Build the bad character table for Boyer-Moore algorithm.
    
    Args:
        pattern: The pattern to build table for
        alphabet: The alphabet of possible characters
        
    Returns:
        Dictionary mapping each character to list of shift values
    """
    table = {}
    pattern_len = len(pattern)
    
    for char in alphabet:
        table[char] = []
        last_occurrence = -1
        
        for j in range(pattern_len):
            if pattern[j] == char:
                table[char].append(-1)
                last_occurrence = j
            else:
                if last_occurrence == -1:
                    table[char].append(j)
                else:
                    table[char].append(j - last_occurrence - 1)
    
    return table


def bad_character_match(text: str, pattern: str) -> int:
    """
    Find pattern in text using Boyer-Moore bad character heuristic.
    
    Args:
        text: The text to search in
        pattern: The pattern to search for
        
    Returns:
        Index of first match, or -1 if not found
    """
    if not pattern or not text or len(pattern) > len(text):
        return -1
    
    alphabet = "ACGT"
    n = len(text)
    m = len(pattern)
    
    # Build bad character table using numpy for efficiency
    table = np.zeros((4, m), dtype=int)
    char_to_idx = {"A": 0, "C": 1, "G": 2, "T": 3}
    
    for i in range(4):
        char = alphabet[i]
        count = 0
        for j in range(m):
            if char == pattern[j]:
                table[i, j] = -1
                count = 0
            else:
                table[i, j] = count
                count += 1
    
    # Search for pattern
    result = -1
    i = 0
    
    while i <= n - m:
        # Check if pattern matches at current position
        if pattern == text[i:i + m]:
            result = i
            break
        
        # Find mismatch from right to left
        for j in range(i + m - 1, i - 1, -1):
            if text[j] != pattern[j - i]:
                if text[j] in char_to_idx:
                    k = char_to_idx[text[j]]
                    shift = table[k, j - i]
                    i += max(1, int(shift))
                else:
                    i += 1
                break
        else:
            i += 1
    
    return result


def build_good_suffix_table(pattern: str) -> list[int]:
    """
    Build the good suffix table for Boyer-Moore algorithm.
    
    The good suffix rule is used when a mismatch occurs. It tells us how far
    we can shift the pattern based on the matched suffix.
    
    Args:
        pattern: The pattern to build table for
        
    Returns:
        List of shift values for each position
    """
    m = len(pattern)
    if m == 0:
        return []
    
    # Initialize good suffix table with pattern length
    good_suffix = [0] * (m + 1)
    
    # Build border array for reversed pattern
    border = [0] * (m + 1)
    
    # Case 1: Matching suffix also appears at the beginning of the pattern
    i = m
    j = m + 1
    border[i] = j
    
    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if good_suffix[j] == 0:
                good_suffix[j] = j - i
            j = border[j]
        i -= 1
        j -= 1
        border[i] = j
    
    # Case 2: Part of the matching suffix appears at the beginning of the pattern
    j = border[0]
    for i in range(m + 1):
        if good_suffix[i] == 0:
            good_suffix[i] = j
        if i == j:
            j = border[j]
    
    return good_suffix


def build_border_array(pattern: str) -> list[int]:
    """
    Build the border array (failure function) for a pattern.
    
    A border is a substring that is both a prefix and suffix of the pattern.
    
    Args:
        pattern: The pattern to build border array for
        
    Returns:
        List of border lengths for each prefix of the pattern
    """
    m = len(pattern)
    if m == 0:
        return []
    
    border = [0] * m
    
    # Length of the previous longest border
    length = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            border[i] = length
            i += 1
        else:
            if length != 0:
                length = border[length - 1]
            else:
                border[i] = 0
                i += 1
    
    return border


def good_suffix_match(text: str, pattern: str) -> int:
    """
    Find pattern in text using Boyer-Moore good suffix heuristic only.
    
    Args:
        text: The text to search in
        pattern: The pattern to search for
        
    Returns:
        Index of first match, or -1 if not found
    """
    if not pattern or not text or len(pattern) > len(text):
        return -1
    
    n = len(text)
    m = len(pattern)
    
    # Build good suffix table
    good_suffix = build_good_suffix_table(pattern)
    
    # Search for pattern
    i = 0  # Position in text
    
    while i <= n - m:
        j = m - 1  # Position in pattern (right to left)
        
        # Compare pattern from right to left
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        
        if j < 0:
            # Pattern found
            return i
        else:
            # Shift using good suffix rule
            i += good_suffix[j + 1]
    
    return -1


def boyer_moore_match(text: str, pattern: str) -> int:
    """
    Find pattern in text using full Boyer-Moore algorithm with both
    bad character and good suffix heuristics.
    
    This implementation combines both heuristics and takes the maximum
    shift suggested by either rule for optimal performance.
    
    Args:
        text: The text to search in
        pattern: The pattern to search for
        
    Returns:
        Index of first match, or -1 if not found
    """
    if not pattern or not text or len(pattern) > len(text):
        return -1
    
    n = len(text)
    m = len(pattern)
    alphabet = "ACGT"
    
    # Build bad character table
    bad_char = {}
    for char in alphabet:
        bad_char[char] = -1
    for j in range(m):
        bad_char[pattern[j]] = j
    
    # Build good suffix table
    good_suffix = build_good_suffix_table(pattern)
    
    # Search for pattern
    i = 0  # Position in text
    
    while i <= n - m:
        j = m - 1  # Position in pattern (right to left)
        
        # Compare pattern from right to left
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        
        if j < 0:
            # Pattern found
            return i
        else:
            # Calculate shifts from both heuristics
            char = text[i + j]
            
            # Bad character shift
            bad_char_shift = j - bad_char.get(char, -1)
            
            # Good suffix shift
            good_suffix_shift = good_suffix[j + 1]
            
            # Take the maximum shift
            i += max(bad_char_shift, good_suffix_shift, 1)
    
    return -1


def boyer_moore_match_all(text: str, pattern: str) -> list[int]:
    """
    Find all occurrences of pattern in text using full Boyer-Moore algorithm.
    
    Args:
        text: The text to search in
        pattern: The pattern to search for
        
    Returns:
        List of all match positions
    """
    if not pattern or not text or len(pattern) > len(text):
        return []
    
    n = len(text)
    m = len(pattern)
    alphabet = "ACGT"
    matches = []
    
    # Build bad character table
    bad_char = {}
    for char in alphabet:
        bad_char[char] = -1
    for j in range(m):
        bad_char[pattern[j]] = j
    
    # Build good suffix table
    good_suffix = build_good_suffix_table(pattern)
    
    # Search for pattern
    i = 0
    
    while i <= n - m:
        j = m - 1
        
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        
        if j < 0:
            # Pattern found
            matches.append(i)
            # Shift to find next occurrence
            i += good_suffix[0]
        else:
            char = text[i + j]
            bad_char_shift = j - bad_char.get(char, -1)
            good_suffix_shift = good_suffix[j + 1]
            i += max(bad_char_shift, good_suffix_shift, 1)
    
    return matches
