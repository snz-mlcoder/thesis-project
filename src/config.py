"""
Central configuration module for all project constants and settings.
Maintains single source of truth for paths, models, and hyperparameters.
"""

from pathlib import Path
from typing import Final

# ============================================================================
# PATHS
# ============================================================================
PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
MODELS_DIR: Final[Path] = PROJECT_ROOT / "models"
RESULTS_DIR: Final[Path] = PROJECT_ROOT / "results"
LOGS_DIR: Final[Path] = PROJECT_ROOT / "logs"

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, RESULTS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# ============================================================================
# DATA SOURCES
# ============================================================================
MOVIELENS_URL: Final[str] = "https://files.grouplens.org/datasets/movielens/ml-1m.zip"
MOVIELENS_FILES: Final[dict] = {
    "movies": DATA_DIR / "movies.dat",
    "ratings": DATA_DIR / "ratings.dat",
    "users": DATA_DIR / "users.dat"
}

# ============================================================================
# EMBEDDINGS
# ============================================================================
SBERT_MODEL: Final[str] = "all-MiniLM-L6-v2"  # Fast, lightweight model
SBERT_EMBEDDING_DIM: Final[int] = 384
SBERT_BATCH_SIZE: Final[int] = 256
SBERT_NORMALIZE: Final[bool] = True  # Required for cosine similarity

# Cached embeddings
EMBEDDINGS_PATH: Final[Path] = DATA_DIR / "embeddings.npy"
MOVIES_CACHE_PATH: Final[Path] = DATA_DIR / "movies.pkl"
AMAZON_PRODUCTS_CACHE_PATH: Final[Path] = DATA_DIR / "amazon_products.pkl"
AMAZON_EMBEDDINGS_PATH: Final[Path] = DATA_DIR / "amazon_embeddings.npy"

# ============================================================================
# CLUSTERING
# ============================================================================
CLUSTERING_SEED: Final[int] = 42
K_MIN: Final[int] = 2
K_MAX: Final[int] = 10
ELBOW_MULTIPLIER: Final[float] = 1.2  # For adaptive k selection

# ============================================================================
# INFORMATION GAIN
# ============================================================================
IG_THRESHOLD: Final[float] = 0.01  # Minimum meaningful information gain

# ============================================================================
# INTERACTION SIMULATION
# ============================================================================
INTERACTION_SEED: Final[int] = 42
INTERACTION_ROUNDS: Final[int] = 10

# ============================================================================
# LLM / OPENAI
# ============================================================================
OPENAI_MODEL: Final[str] = "gpt-3.5-turbo"
OPENAI_MAX_TOKENS: Final[int] = 100
OPENAI_TEMPERATURE: Final[float] = 0.3
OPENAI_RETRY_ATTEMPTS: Final[int] = 3

# ============================================================================
# LOGGING
# ============================================================================
LOG_LEVEL: Final[str] = "INFO"
LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# REPRODUCIBILITY
# ============================================================================
GLOBAL_SEED: Final[int] = 42

def set_seeds() -> None:
    """Set random seeds for reproducibility across all libraries."""
    import random
    import numpy as np
    import torch
    
    random.seed(GLOBAL_SEED)
    np.random.seed(GLOBAL_SEED)
    torch.manual_seed(GLOBAL_SEED)
    torch.cuda.manual_seed_all(GLOBAL_SEED)
