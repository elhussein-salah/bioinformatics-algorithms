"""
Unit tests for pattern matching algorithms.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.pattern_matching import (
    naive_match,
    naive_match_all,
    bad_character_match
)


class TestNaiveMatch:
    """Tests for naive pattern matching."""
    
    def test_match_found(self):
        assert naive_match("ATGCGATCGATCG", "GATC") == 4
    
    def test_match_at_start(self):
        assert naive_match("ATGCGATC", "ATG") == 0
    
    def test_match_at_end(self):
        assert naive_match("ATGCGATC", "GATC") == 4
    
    def test_no_match(self):
        assert naive_match("ATGCGATC", "XXXX") == -1
    
    def test_empty_pattern(self):
        assert naive_match("ATGC", "") == -1
    
    def test_pattern_longer_than_text(self):
        assert naive_match("AT", "ATGC") == -1


class TestNaiveMatchAll:
    """Tests for finding all matches."""
    
    def test_multiple_matches(self):
        matches = naive_match_all("ATGATGATG", "ATG")
        assert matches == [0, 3, 6]
    
    def test_overlapping_matches(self):
        matches = naive_match_all("AAAA", "AA")
        assert matches == [0, 1, 2]
    
    def test_no_matches(self):
        matches = naive_match_all("ATGC", "XX")
        assert matches == []


class TestBadCharacterMatch:
    """Tests for Boyer-Moore bad character matching."""
    
    def test_match_found(self):
        assert bad_character_match("ATGCGATCGATCG", "GATC") == 4
    
    def test_no_match(self):
        assert bad_character_match("ATGCGATC", "XXXX") == -1
    
    def test_pattern_at_start(self):
        assert bad_character_match("ATGCGATC", "ATGC") == 0
    
    def test_empty_inputs(self):
        assert bad_character_match("", "ATG") == -1
        assert bad_character_match("ATG", "") == -1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
