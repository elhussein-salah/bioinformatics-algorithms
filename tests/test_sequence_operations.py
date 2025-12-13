"""
Unit tests for sequence operations.
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.sequence_operations import (
    gc_content,
    complement,
    reverse,
    reverse_complement,
    translate_dna_to_protein
)


class TestGCContent:
    """Tests for GC content calculation."""
    
    def test_gc_content_basic(self):
        assert gc_content("ATGC") == 0.5
    
    def test_gc_content_all_gc(self):
        assert gc_content("GGCC") == 1.0
    
    def test_gc_content_no_gc(self):
        assert gc_content("AATT") == 0.0
    
    def test_gc_content_empty_raises(self):
        with pytest.raises(ValueError):
            gc_content("")


class TestComplement:
    """Tests for DNA complement."""
    
    def test_complement_basic(self):
        assert complement("ATGC") == "TACG"
    
    def test_complement_single(self):
        assert complement("A") == "T"
        assert complement("T") == "A"
        assert complement("G") == "C"
        assert complement("C") == "G"
    
    def test_complement_invalid_raises(self):
        with pytest.raises(ValueError):
            complement("ATGX")


class TestReverse:
    """Tests for sequence reversal."""
    
    def test_reverse_basic(self):
        assert reverse("ATGC") == "CGTA"
    
    def test_reverse_palindrome(self):
        assert reverse("ATAT") == "TATA"


class TestReverseComplement:
    """Tests for reverse complement."""
    
    def test_reverse_complement_basic(self):
        assert reverse_complement("ATGC") == "GCAT"
    
    def test_reverse_complement_symmetry(self):
        seq = "ATGCGATC"
        assert reverse_complement(reverse_complement(seq)) == seq


class TestTranslation:
    """Tests for DNA to protein translation."""
    
    def test_translation_start_codon(self):
        full, orf = translate_dna_to_protein("ATG")
        assert full == "M"
    
    def test_translation_stop_codon(self):
        full, orf = translate_dna_to_protein("TAA")
        assert full == "*"
    
    def test_translation_with_orf(self):
        full, orf = translate_dna_to_protein("ATGAAATAG")
        assert full == "MK*"
        assert orf == "MK"
    
    def test_translation_no_start(self):
        full, orf = translate_dna_to_protein("AAATAG")
        assert full == "K*"
        assert orf == ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
