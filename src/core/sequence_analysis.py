"""
Sequence analysis utilities for FASTA files and overlap detection.
"""

from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass, field
import pandas as pd


def compute_overlap(seq_a: str, seq_b: str, min_length: int = 3) -> tuple[int, str]:
    """
    Compute the overlap between two sequences.
    
    The overlap is the longest suffix of seq_a that is also a prefix of seq_b.
    
    Args:
        seq_a: First sequence
        seq_b: Second sequence  
        min_length: Minimum overlap length to consider
        
    Returns:
        Tuple of (overlap_length, overlapping_sequence)
    """
    if not seq_a or not seq_b:
        return 0, ""
    
    start = 0
    while True:
        # Find where the beginning of seq_b might match in seq_a
        start = seq_a.find(seq_b[:min_length], start)
        
        if start == -1:
            return 0, ""
        
        # Check if seq_b starts with the suffix of seq_a from this position
        if seq_b.startswith(seq_a[start:]):
            overlap_seq = seq_a[start:]
            return len(overlap_seq), overlap_seq
        
        start += 1


def parse_hemolytic_file(file_path: str) -> pd.DataFrame:
    """
    Parse a HAPPENN hemolytic dataset file.
    
    Args:
        file_path: Path to the hemolytic FASTA file
        
    Returns:
        DataFrame with columns ['Sequence', 'y'] where y=0 for non-hemolytic, y=1 for hemolytic
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is invalid
    """
    sequences = []
    current_label = None
    
    with open(file_path, 'r') as infile:
        for line in infile:
            line = line.strip()
            
            if line.startswith(">"):
                # Parse header line for hemolytic status
                parts = line.split("|lcl|")
                if len(parts) >= 4:
                    label = parts[3].strip()
                    current_label = 0 if 'non-hemolytic' in label else 1
            elif line and current_label is not None:
                # Sequence line
                sequences.append([line, current_label])
    
    return pd.DataFrame(sequences, columns=['Sequence', 'y'])


def parse_fasta_sequences(file_path: str) -> pd.DataFrame:
    """
    Parse a standard FASTA file into a DataFrame.
    
    Args:
        file_path: Path to the FASTA file
        
    Returns:
        DataFrame with columns ['ID', 'Sequence']
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    ids = []
    sequences = []
    current_id = None
    current_seq = []
    
    with open(file_path, 'r') as infile:
        for line in infile:
            line = line.strip()
            
            if line.startswith(">"):
                # Save previous sequence if exists
                if current_id is not None:
                    ids.append(current_id)
                    sequences.append("".join(current_seq))
                
                # Start new sequence
                current_id = line[1:]  # Remove '>' prefix
                current_seq = []
            elif line:
                current_seq.append(line)
        
        # Don't forget the last sequence
        if current_id is not None:
            ids.append(current_id)
            sequences.append("".join(current_seq))
    
    return pd.DataFrame({'ID': ids, 'Sequence': sequences})


def read_fasta_sequence(file_path: str) -> tuple[str, str]:
    """
    Read a single sequence from a FASTA file.
    
    Args:
        file_path: Path to the FASTA file
        
    Returns:
        Tuple of (header, sequence)
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is empty or invalid
    """
    header = None
    sequence_lines = []
    
    with open(file_path, 'r') as infile:
        for line in infile:
            line = line.strip()
            
            if line.startswith(">"):
                if header is not None:
                    # Only return first sequence
                    break
                header = line[1:]
            elif line:
                sequence_lines.append(line)
    
    if header is None:
        raise ValueError("No valid FASTA header found")
    
    return header, "".join(sequence_lines)


# ============================================
# Overlap Graph Implementation
# ============================================

@dataclass
class OverlapEdge:
    """
    Represents an edge in the overlap graph.
    
    An edge connects two sequences where the suffix of the source
    overlaps with the prefix of the target.
    """
    source_id: str  # ID or index of source sequence
    target_id: str  # ID or index of target sequence
    overlap_length: int  # Length of the overlap
    overlap_sequence: str  # The overlapping substring


@dataclass
class OverlapGraph:
    """
    Represents an overlap graph for sequence assembly.
    
    The overlap graph is a directed graph where:
    - Nodes represent sequences (or their IDs)
    - Edges represent overlaps between sequences (suffix of one = prefix of another)
    - Edge weights are the overlap lengths
    """
    nodes: List[str] = field(default_factory=list)  # Sequence IDs
    edges: List[OverlapEdge] = field(default_factory=list)  # All edges
    adjacency: Dict[str, List[OverlapEdge]] = field(default_factory=dict)  # Adjacency list
    
    def add_edge(self, edge: OverlapEdge):
        """Add an edge to the graph."""
        self.edges.append(edge)
        if edge.source_id not in self.adjacency:
            self.adjacency[edge.source_id] = []
        self.adjacency[edge.source_id].append(edge)
    
    def get_outgoing_edges(self, node_id: str) -> List[OverlapEdge]:
        """Get all outgoing edges from a node."""
        return self.adjacency.get(node_id, [])
    
    def get_best_successor(self, node_id: str) -> Optional[OverlapEdge]:
        """Get the edge with the longest overlap from a node."""
        edges = self.get_outgoing_edges(node_id)
        if not edges:
            return None
        return max(edges, key=lambda e: e.overlap_length)
    
    def to_adjacency_matrix(self) -> Tuple[List[str], List[List[int]]]:
        """
        Convert the graph to an adjacency matrix representation.
        
        Returns:
            Tuple of (node_list, adjacency_matrix) where matrix[i][j] is
            the overlap length from node i to node j (0 if no edge)
        """
        n = len(self.nodes)
        node_to_idx = {node: i for i, node in enumerate(self.nodes)}
        matrix = [[0] * n for _ in range(n)]
        
        for edge in self.edges:
            i = node_to_idx[edge.source_id]
            j = node_to_idx[edge.target_id]
            matrix[i][j] = edge.overlap_length
        
        return self.nodes, matrix


def build_overlap_graph(
    sequences: Dict[str, str],
    min_overlap: int = 3
) -> OverlapGraph:
    """
    Build an overlap graph from a dictionary of sequences.
    
    The graph represents how sequences can potentially be assembled
    based on their suffix-prefix overlaps.
    
    Args:
        sequences: Dictionary mapping sequence IDs to their sequences
        min_overlap: Minimum overlap length to create an edge
        
    Returns:
        OverlapGraph object containing all nodes and edges
        
    Example:
        >>> seqs = {"s1": "ACGTACGT", "s2": "CGTACGTA", "s3": "GTACGTAC"}
        >>> graph = build_overlap_graph(seqs, min_overlap=4)
        >>> len(graph.edges)  # Number of overlapping pairs
    """
    graph = OverlapGraph()
    graph.nodes = list(sequences.keys())
    
    # Compare all pairs of sequences
    for id_a, seq_a in sequences.items():
        for id_b, seq_b in sequences.items():
            # Skip self-overlaps
            if id_a == id_b:
                continue
            
            # Compute overlap (suffix of a with prefix of b)
            overlap_len, overlap_seq = compute_overlap(seq_a, seq_b, min_overlap)
            
            if overlap_len >= min_overlap:
                edge = OverlapEdge(
                    source_id=id_a,
                    target_id=id_b,
                    overlap_length=overlap_len,
                    overlap_sequence=overlap_seq
                )
                graph.add_edge(edge)
    
    return graph


def build_overlap_graph_from_list(
    sequences: List[str],
    min_overlap: int = 3
) -> OverlapGraph:
    """
    Build an overlap graph from a list of sequences.
    
    Sequences are automatically assigned numeric IDs (0, 1, 2, ...).
    
    Args:
        sequences: List of sequences
        min_overlap: Minimum overlap length to create an edge
        
    Returns:
        OverlapGraph object
    """
    seq_dict = {str(i): seq for i, seq in enumerate(sequences)}
    return build_overlap_graph(seq_dict, min_overlap)


def find_greedy_path(graph: OverlapGraph) -> List[str]:
    """
    Find a path through the overlap graph using a greedy algorithm.
    
    Starts from each node and greedily follows the edge with the longest
    overlap that hasn't been visited yet. Returns the longest such path.
    
    Args:
        graph: The overlap graph
        
    Returns:
        List of node IDs representing the path
    """
    if not graph.nodes:
        return []
    
    best_path = []
    
    for start_node in graph.nodes:
        path = [start_node]
        visited = {start_node}
        current = start_node
        
        while True:
            # Get all outgoing edges to unvisited nodes
            edges = graph.get_outgoing_edges(current)
            valid_edges = [e for e in edges if e.target_id not in visited]
            
            if not valid_edges:
                break
            
            # Choose edge with longest overlap
            best_edge = max(valid_edges, key=lambda e: e.overlap_length)
            current = best_edge.target_id
            path.append(current)
            visited.add(current)
        
        if len(path) > len(best_path):
            best_path = path
    
    return best_path


def assemble_from_path(
    sequences: Dict[str, str],
    path: List[str],
    graph: OverlapGraph
) -> str:
    """
    Assemble sequences based on a path through the overlap graph.
    
    Args:
        sequences: Dictionary mapping IDs to sequences
        path: List of sequence IDs representing the assembly order
        graph: The overlap graph (to get overlap information)
        
    Returns:
        The assembled (superstring) sequence
    """
    if not path:
        return ""
    
    if len(path) == 1:
        return sequences[path[0]]
    
    # Start with the first sequence
    result = sequences[path[0]]
    
    # Add remaining sequences, removing overlapping parts
    for i in range(1, len(path)):
        source_id = path[i - 1]
        target_id = path[i]
        
        # Find the edge between these nodes
        edges = graph.get_outgoing_edges(source_id)
        edge = next((e for e in edges if e.target_id == target_id), None)
        
        if edge:
            # Append only the non-overlapping suffix of the target
            result += sequences[target_id][edge.overlap_length:]
        else:
            # No edge found, append full sequence
            result += sequences[target_id]
    
    return result


def get_overlap_graph_statistics(graph: OverlapGraph) -> Dict[str, any]:
    """
    Calculate statistics for an overlap graph.
    
    Args:
        graph: The overlap graph
        
    Returns:
        Dictionary containing various statistics
    """
    if not graph.nodes:
        return {
            'num_nodes': 0,
            'num_edges': 0,
            'avg_overlap': 0,
            'max_overlap': 0,
            'min_overlap': 0,
            'density': 0
        }
    
    num_nodes = len(graph.nodes)
    num_edges = len(graph.edges)
    max_possible_edges = num_nodes * (num_nodes - 1)  # Directed graph
    
    overlaps = [e.overlap_length for e in graph.edges]
    
    return {
        'num_nodes': num_nodes,
        'num_edges': num_edges,
        'avg_overlap': sum(overlaps) / len(overlaps) if overlaps else 0,
        'max_overlap': max(overlaps) if overlaps else 0,
        'min_overlap': min(overlaps) if overlaps else 0,
        'density': num_edges / max_possible_edges if max_possible_edges > 0 else 0
    }
