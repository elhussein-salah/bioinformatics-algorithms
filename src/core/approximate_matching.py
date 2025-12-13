"""
Approximate Pattern Matching Algorithms.

This module provides various approximate string matching algorithms
commonly used in bioinformatics for DNA/protein sequence analysis.
"""

from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class ApproximateMatch:
    """Represents an approximate match result."""
    position: int
    distance: int
    matched_text: str


def edit_distance(x: str, y: str) -> int:
    """
    Calculate the edit distance (Levenshtein distance) between two strings
    using dynamic programming.
    
    The edit distance is the minimum number of single-character edits
    (insertions, deletions, substitutions) required to transform x into y.
    
    Args:
        x: First string (source)
        y: Second string (target)
        
    Returns:
        The edit distance between the two strings
        
    Example:
        >>> edit_distance("ACGACGT", "TCGTACGT")
        2
    """
    m, n = len(x), len(y)
    
    # Create DP table
    D = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize first column (deleting from x)
    for i in range(m + 1):
        D[i][0] = i
    
    # Initialize first row (inserting to x)
    for j in range(n + 1):
        D[0][j] = j
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Cost is 0 if characters match, 1 otherwise
            delta = 0 if x[i - 1] == y[j - 1] else 1
            
            D[i][j] = min(
                D[i - 1][j - 1] + delta,  # Substitution (or match)
                D[i - 1][j] + 1,          # Deletion from x
                D[i][j - 1] + 1           # Insertion to x
            )
    
    return D[m][n]


def edit_distance_with_trace(x: str, y: str) -> Tuple[int, List[str]]:
    """
    Calculate edit distance with alignment trace.
    
    Returns both the distance and a list of operations performed.
    
    Args:
        x: First string (source)
        y: Second string (target)
        
    Returns:
        Tuple of (distance, list of operations)
        Operations are: 'M' (match), 'S' (substitution), 
                       'I' (insertion), 'D' (deletion)
    """
    m, n = len(x), len(y)
    
    # Create DP table
    D = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize
    for i in range(m + 1):
        D[i][0] = i
    for j in range(n + 1):
        D[0][j] = j
    
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            delta = 0 if x[i - 1] == y[j - 1] else 1
            D[i][j] = min(
                D[i - 1][j - 1] + delta,
                D[i - 1][j] + 1,
                D[i][j - 1] + 1
            )
    
    # Traceback to find operations
    operations = []
    i, j = m, n
    
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            delta = 0 if x[i - 1] == y[j - 1] else 1
            if D[i][j] == D[i - 1][j - 1] + delta:
                if delta == 0:
                    operations.append('M')  # Match
                else:
                    operations.append('S')  # Substitution
                i -= 1
                j -= 1
                continue
        
        if i > 0 and D[i][j] == D[i - 1][j] + 1:
            operations.append('D')  # Deletion
            i -= 1
        elif j > 0:
            operations.append('I')  # Insertion
            j -= 1
        else:
            break
    
    operations.reverse()
    return D[m][n], operations


def approximate_match(text: str, pattern: str, max_distance: int) -> List[ApproximateMatch]:
    """
    Find all approximate matches of pattern in text within max_distance edits.
    
    Uses a simplified approach: check edit distance at each position
    for substrings of similar length to the pattern.
    
    Args:
        text: The text to search in
        pattern: The pattern to search for
        max_distance: Maximum allowed edit distance
        
    Returns:
        List of ApproximateMatch objects containing position, distance, 
        and matched substring
    """
    if not pattern or not text:
        return []
    
    matches = []
    pattern_len = len(pattern)
    
    # Check windows of varying sizes around pattern length
    for start in range(len(text)):
        for end_offset in range(-max_distance, max_distance + 1):
            end = start + pattern_len + end_offset
            
            if end > len(text) or end <= start:
                continue
            
            substring = text[start:end]
            distance = edit_distance(pattern, substring)
            
            if distance <= max_distance:
                # Check if this is a better match at same position
                existing = [m for m in matches if m.position == start]
                if existing:
                    if distance < existing[0].distance:
                        matches.remove(existing[0])
                        matches.append(ApproximateMatch(
                            position=start,
                            distance=distance,
                            matched_text=substring
                        ))
                else:
                    matches.append(ApproximateMatch(
                        position=start,
                        distance=distance,
                        matched_text=substring
                    ))
    
    # Sort by position and return
    matches.sort(key=lambda m: (m.position, m.distance))
    
    # Remove overlapping matches, keeping best ones
    filtered = []
    for match in matches:
        overlaps = False
        for existing in filtered:
            # Check for overlap
            match_end = match.position + len(match.matched_text)
            exist_end = existing.position + len(existing.matched_text)
            
            if (match.position < exist_end and match_end > existing.position):
                # Keep the one with smaller distance
                if match.distance < existing.distance:
                    filtered.remove(existing)
                    filtered.append(match)
                overlaps = True
                break
        
        if not overlaps:
            filtered.append(match)
    
    return sorted(filtered, key=lambda m: m.position)


def hamming_distance(s1: str, s2: str) -> int:
    """
    Calculate the Hamming distance between two strings of equal length.
    
    The Hamming distance is the number of positions where the 
    corresponding characters differ.
    
    Args:
        s1: First string
        s2: Second string (must be same length as s1)
        
    Returns:
        The Hamming distance
        
    Raises:
        ValueError: If strings have different lengths
    """
    if len(s1) != len(s2):
        raise ValueError(f"Strings must have equal length: {len(s1)} != {len(s2)}")
    
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def approximate_match_hamming(text: str, pattern: str, max_mismatches: int) -> List[int]:
    """
    Find all positions where pattern approximately matches text
    with at most max_mismatches using Hamming distance.
    
    This only considers substitutions, not insertions or deletions.
    
    Args:
        text: The text to search in
        pattern: The pattern to search for
        max_mismatches: Maximum allowed mismatches
        
    Returns:
        List of positions where approximate matches were found
    """
    if not pattern or not text or len(pattern) > len(text):
        return []
    
    matches = []
    pattern_len = len(pattern)
    
    for i in range(len(text) - pattern_len + 1):
        substring = text[i:i + pattern_len]
        if hamming_distance(pattern, substring) <= max_mismatches:
            matches.append(i)
    
    return matches
