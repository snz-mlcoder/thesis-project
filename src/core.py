import numpy as np
from sklearn.cluster import KMeans


def entropy(candidate_indices):
    n = len(candidate_indices)
    return 0.0 if n <= 1 else np.log2(n)


def expected_entropy(partition):
    total = sum(len(g) for g in partition)

    return 0.0 if total == 0 else sum(
        (len(g)/total) * entropy(g)
        for g in partition
    )


def information_gain(candidate_indices, partition):
    return entropy(candidate_indices) - expected_entropy(partition)


def adaptive_k(n):

    if n <= 10:
        return 2

    if n <= 30:
        return 3

    if n <= 100:
        return 4

    return 5


def simulated_user(partition, target_idx):

    for i, group in enumerate(partition):

        if target_idx in group:
            return i

    return 0


def retrieve_candidates(query_embedding, all_embeddings, top_n):

    scores = all_embeddings @ query_embedding

    top_indices = np.argsort(scores)[::-1][:top_n]

    return top_indices.tolist()


def cluster_candidates(candidate_indices, all_embeddings, k):

    k = min(k, len(candidate_indices))

    if k == 1:
        return [candidate_indices], np.zeros(len(candidate_indices), dtype=int)

    embs = all_embeddings[candidate_indices]

    km = KMeans(
        n_clusters=k,
        random_state=42,
        n_init='auto'
    )

    labels = km.fit_predict(embs)

    partition = [[] for _ in range(k)]

    for idx, lbl in zip(candidate_indices, labels):
        partition[lbl].append(idx)

    return partition, labels

def retrieve(query_embedding, all_embeddings, top_n):

    scores = all_embeddings @ query_embedding

    top_indices = np.argsort(scores)[::-1][:top_n]

    return top_indices.tolist()