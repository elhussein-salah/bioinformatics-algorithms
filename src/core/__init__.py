"""Core algorithms for bioinformatics analysis."""

from .sequence_operations import (
    gc_content,
    complement,
    reverse,
    reverse_complement,
    translate_dna_to_protein
)

from .pattern_matching import (
    naive_match,
    bad_character_match,
    build_bad_character_table,
    build_good_suffix_table,
    build_border_array,
    good_suffix_match,
    boyer_moore_match,
    boyer_moore_match_all
)

from .indexing import (
    build_sorted_index,
    query_index,
    build_suffix_array,
    build_suffix_array_simple,
    build_inverse_suffix_array,
    build_suffix_array_with_inverse
)

from .sequence_analysis import (
    compute_overlap,
    parse_hemolytic_file,
    parse_fasta_sequences,
    OverlapEdge,
    OverlapGraph,
    build_overlap_graph,
    build_overlap_graph_from_list,
    find_greedy_path,
    assemble_from_path,
    get_overlap_graph_statistics
)

from .approximate_matching import (
    edit_distance,
    edit_distance_with_trace,
    approximate_match,
    approximate_match_hamming,
    hamming_distance,
    ApproximateMatch
)

from .fasta_operations import (
    read_fasta_file,
    read_single_sequence,
    fasta_to_csv,
    get_fasta_statistics,
    validate_fasta_sequence,
    FastaSequence,
    FastaFile,
    FastaParseError
)

__all__ = [
    # Sequence operations
    'gc_content',
    'complement', 
    'reverse',
    'reverse_complement',
    'translate_dna_to_protein',
    # Pattern matching
    'naive_match',
    'bad_character_match',
    'build_bad_character_table',
    'build_good_suffix_table',
    'build_border_array',
    'good_suffix_match',
    'boyer_moore_match',
    'boyer_moore_match_all',
    # Indexing and suffix arrays
    'build_sorted_index',
    'query_index',
    'build_suffix_array',
    'build_suffix_array_simple',
    'build_inverse_suffix_array',
    'build_suffix_array_with_inverse',
    # Overlap detection and graph
    'compute_overlap',
    'parse_hemolytic_file',
    'parse_fasta_sequences',
    'OverlapEdge',
    'OverlapGraph',
    'build_overlap_graph',
    'build_overlap_graph_from_list',
    'find_greedy_path',
    'assemble_from_path',
    'get_overlap_graph_statistics',
    # Approximate matching
    'edit_distance',
    'edit_distance_with_trace',
    'approximate_match',
    'approximate_match_hamming',
    'hamming_distance',
    'ApproximateMatch',
    # FASTA operations
    'read_fasta_file',
    'read_single_sequence',
    'fasta_to_csv',
    'get_fasta_statistics',
    'validate_fasta_sequence',
    'FastaSequence',
    'FastaFile',
    'FastaParseError'
]
