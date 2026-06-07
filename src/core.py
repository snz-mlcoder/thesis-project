"""
Core algorithms for clustering and information gain-based candidate selection.

This module provides the fundamental functions for:
1. Calculating entropy and information gain
2. Adaptive k selection for clustering
3. K-means clustering
4. Candidate retrieval by similarity
5. Simulated user feedback
"""


import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from typing import Tuple, List, Dict, Optional

from src.config import RANDOM_SEED


def entropy(candidates: np.ndarray) -> float:
    """
    Calculate Shannon entropy of a set of candidates.
    
    Entropy measures the uncertainty/disorder of a set.
    Higher entropy = more diverse/uncertain.
    
    Args:
        candidates: Binary labels (0 or 1) for items
        
    Returns:
        Shannon entropy value (0 to 1)
    """
    if len(candidates) == 0:
        return 0.0
    
    # Count positive and negative labels
    unique, counts = np.unique(candidates, return_counts=True)
    probabilities = counts / len(candidates)
    
    # H(X) = -sum(p_i * log2(p_i))
    entropy_value = -np.sum(probabilities * np.log2(probabilities + 1e-10))
    
    return entropy_value


def expected_entropy(partition: List[np.ndarray]) -> float:
    """
    Calculate expected entropy of a partition (weighted average).
    
    Args:
        partition: List of candidate groups (each group is a binary array)
        
    Returns:
        Expected entropy across all groups
    """
    if not partition or len(partition) == 0:
        return 0.0
    
    total_size = sum(len(group) for group in partition)
    
    if total_size == 0:
        return 0.0
    
    # E[H(partition)] = sum(|G_i| / |all| * H(G_i))
    expected_ent = sum(
        (len(group) / total_size) * entropy(group)
        for group in partition
    )
    
    return expected_ent

def information_gain(
    candidates: np.ndarray,
    partition: List[np.ndarray]
) -> float:
    """
    Calculate information gain from a partition.
    
    Information Gain = H(candidates) - E[H(partition)]
    
    Measures how much the partition reduces uncertainty about labels.
    
    Args:
        candidates: Original binary labels for all items
        partition: Partitioned groups after clustering
        
    Returns:
        Information gain value (higher = better partition)
    """
    h_original = entropy(candidates)
    e_h_partition = expected_entropy(partition)
    
    ig = h_original - e_h_partition
    
    return max(0.0, ig)  # IG should never be negative



def adaptive_k(n_candidates: int) -> int:
    """
    Adaptively select number of clusters based on candidate pool size.
    
    Logic:
    - n ≤ 10 → k=2
    - n ≤ 30 → k=3
    - n ≤ 100 → k=4
    - n > 100 → k=5
    
    Args:
        n_candidates: Number of candidates to cluster
        
    Returns:
        Recommended number of clusters
    """
    if n_candidates <= 10:
        return 2
    elif n_candidates <= 30:
        return 3
    elif n_candidates <= 100:
        return 4
    else:
        return 5

def cluster_candidates(
    indices: np.ndarray,
    embeddings: np.ndarray,
    k: Optional[int] = None,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Cluster candidates using K-means on embeddings.
    
    Args:
        indices: Index IDs of candidates
        embeddings: Embedding vectors (n_candidates, embedding_dim)
        k: Number of clusters. If None, use adaptive_k()
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple of (cluster_labels, cluster_centers)
        - cluster_labels: Cluster assignment for each candidate
        - cluster_centers: Center of each cluster
    """
    if k is None:
        k = adaptive_k(len(indices))
    
    # Handle edge case: fewer candidates than clusters
    k = min(k, len(indices))
    
    kmeans = KMeans(
        n_clusters=k,
        random_state=random_state,
        n_init="auto"
    )
    
    labels = kmeans.fit_predict(embeddings)
    
    return labels, kmeans.cluster_centers_
def retrieve_candidates(
    query_embedding: np.ndarray,
    embeddings: np.ndarray,
    indices: Optional[np.ndarray] = None,
    top_n: int = 100,
    threshold: float = 0.0
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Retrieve top-N candidates by cosine similarity to query.
    
    Args:
        query_embedding: Query embedding vector (1, embedding_dim)
        embeddings: All item embeddings (n_items, embedding_dim)
        indices: Optional item IDs. If None, use range(n_items)
        top_n: Number of top candidates to retrieve
        threshold: Minimum similarity threshold (default: no threshold)
        
    Returns:
        Tuple of (candidate_indices, similarities)
    """
    if indices is None:
        indices = np.arange(len(embeddings))
    
    # Compute cosine similarities
    query_embedding = query_embedding.reshape(1, -1)
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    
    # Filter by threshold
    valid_mask = similarities >= threshold
    valid_indices = indices[valid_mask]
    valid_similarities = similarities[valid_mask]
    
    # Get top-N
    if len(valid_indices) > top_n:
        top_indices = np.argsort(valid_similarities)[-top_n:][::-1]
        return valid_indices[top_indices], valid_similarities[top_indices]
    else:
        sorted_indices = np.argsort(valid_similarities)[::-1]
        return valid_indices[sorted_indices], valid_similarities[sorted_indices]


def simulated_user(
    partition: Dict[int, List[int]],
    target_idx: int
) -> int:
    """
    Simulate user feedback: which cluster contains the target item?
    
    Args:
        partition: Dict mapping cluster_id → list of item indices
        target_idx: Index of the target item
        
    Returns:
        Cluster ID containing the target
    """
    for cluster_id, items in partition.items():
        if target_idx in items:
            return cluster_id
    
    raise ValueError(f"Target index {target_idx} not found in partition")


def partition_by_clusters(
    indices: np.ndarray,
    labels: np.ndarray
) -> Dict[int, List[int]]:
    """
    Convert cluster labels into a partition dictionary.
    
    Args:
        indices: Item indices
        labels: Cluster label for each item
        
    Returns:
        Dict mapping cluster_id → list of item indices
    """
    partition = {}
    for idx, label in zip(indices, labels):
        if label not in partition:
            partition[label] = []
        partition[label].append(idx)
    
    return partition


def calculate_ig_per_cluster(
    partition: Dict[int, List[int]],
    candidates: np.ndarray,
    labels: np.ndarray
) -> Dict[int, float]:
    """
    Calculate information gain for each cluster.
    
    Args:
        partition: Dict mapping cluster_id → list of item indices
        candidates: Binary labels for all items
        labels: Cluster labels for retrieved candidates
        
    Returns:
        Dict mapping cluster_id → information gain value
    """
    ig_per_cluster = {}
    
    for cluster_id, items in partition.items():
        # Get labels for items in this cluster
        cluster_labels = candidates[items]
        
        # Calculate entropy for this cluster
        ig_per_cluster[cluster_id] = entropy(cluster_labels)
    
    return ig_per_cluster


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS FOR EVALUATION
# ─────────────────────────────────────────────────────────────────────────────

def silhouette_score_custom(
    embeddings: np.ndarray,
    labels: np.ndarray
) -> float:
    """
    Simplified silhouette score calculation.
    (Uses sklearn internally for accuracy)
    
    Args:
        embeddings: Item embeddings
        labels: Cluster labels
        
    Returns:
        Silhouette score (-1 to 1)
    """
    from sklearn.metrics import silhouette_score
    
    if len(np.unique(labels)) == 1:
        return 0.0  # No clustering
    
    return silhouette_score(embeddings, labels)


def davies_bouldin_index(
    embeddings: np.ndarray,
    labels: np.ndarray
) -> float:
    """
    Davies-Bouldin Index (lower is better).
    
    Args:
        embeddings: Item embeddings
        labels: Cluster labels
        
    Returns:
        Davies-Bouldin Index score
    """
    from sklearn.metrics import davies_bouldin_score
    
    if len(np.unique(labels)) == 1:
        return 0.0
    
    return davies_bouldin_score(embeddings, labels)


if __name__ == "__main__":
    # Quick test
    print("Testing core functions...")
    
    # Test entropy
    test_labels = np.array([1, 1, 0, 0, 0])
    print(f"Entropy: {entropy(test_labels):.4f}")
    
    # Test adaptive_k
    for n in [5, 15, 50, 150]:
        print(f"n={n} → k={adaptive_k(n)}")
    
    print("✅ Core functions work!")