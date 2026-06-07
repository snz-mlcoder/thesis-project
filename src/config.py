

"""
Configuration module for thesis-project.

Central place to manage all project constants, hyperparameters, and settings.
"""

import os
from pathlib import Path
from typing import Dict, List

# ─────────────────────────────────────────────────────────────────────────────
# PROJECT PATHS
# ─────────────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RESULTS_DIR = PROJECT_ROOT / "results"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# EMBEDDING CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Sentence Transformers model for generating embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384  # Dimension of embeddings from the model

# ─────────────────────────────────────────────────────────────────────────────
# CLUSTERING CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Adaptive k thresholds for dynamic cluster selection
ADAPTIVE_K_THRESHOLDS: Dict[int, int] = {
    10: 2,      # n <= 10 → k=2
    30: 3,      # n <= 30 → k=3
    100: 4,     # n <= 100 → k=4
    float('inf'): 5  # n > 100 → k=5
}

# KMeans hyperparameters
KMEANS_RANDOM_STATE = 42
KMEANS_N_INIT = "auto"  # Sklearn 1.2+
KMEANS_MAX_ITER = 300

# ─────────────────────────────────────────────────────────────────────────────
# RETRIEVAL CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Top-N candidates to retrieve for labeling
DEFAULT_TOP_N = 100

# Similarity threshold (cosine similarity, range: -1 to 1)
SIMILARITY_THRESHOLD = 0.0

# ─────────────────────────────────────────────────────────────────────────────
# INTERACTIVE LOOP CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Maximum interactions per query
MAX_INTERACTIONS = 10

# Information gain threshold for stopping
IG_THRESHOLD = 0.1

# ─────────────────────────────────────────────────────────────────────────────
# LLM CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# OpenAI API settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.7
OPENAI_MAX_TOKENS = 100
OPENAI_REQUEST_TIMEOUT = 30  # seconds

# LLM retry configuration
LLM_MAX_RETRIES = 3
LLM_RETRY_DELAY = 2  # seconds

# ─────────────────────────────────────────────────────────────────────────────
# DATASET CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Movie dataset settings (MovieLens or similar)
MOVIE_DATASET_NAME = "movielens"
MOVIE_DATA_FILE = DATA_DIR / "movies.csv"
MOVIE_REVIEWS_FILE = DATA_DIR / "reviews.csv"

# Amazon dataset settings
AMAZON_DATASET_NAME = "amazon"
AMAZON_DATA_FILE = DATA_DIR / "amazon_products.csv"
AMAZON_REVIEWS_FILE = DATA_DIR / "amazon_reviews.csv"

# ─────────────────────────────────────────────────────────────────────────────
# METRICS CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Evaluation metrics to compute
METRICS_TO_COMPUTE: List[str] = [
    "accuracy",
    "precision",
    "recall",
    "f1",
    "silhouette_score",
    "davies_bouldin_score",
]

# ─────────────────────────────────────────────────────────────────────────────
# RANDOM STATE & REPRODUCIBILITY
# ─────────────────────────────────────────────────────────────────────────────

# Global random seed for reproducibility
RANDOM_SEED = 42

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = RESULTS_DIR / "thesis_project.log"

# ─────────────────────────────────────────────────────────────────────────────
# EXPERIMENT CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Number of runs for ablation studies
ABLATION_NUM_RUNS = 5

# Baseline methods to compare
BASELINE_METHODS: List[str] = [
    "random",
    "entropy_based",
    "information_gain",
]

# ─────────────────────────────────────────────────────────────────────────────
# VISUALIZATION CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# Plot settings
FIGURE_DPI = 300
FIGURE_SIZE = (12, 8)
PLOT_STYLE = "seaborn-v0_8-darkgrid"

# Color palettes
COLORS = {
    "baseline": "#1f77b4",
    "ig_method": "#ff7f0e",
    "ablation": "#2ca02c",
}

# ─────────────────────────────────────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

def validate_config() -> bool:
    """
    Validate critical configuration settings.
    
    Returns:
        bool: True if config is valid, raises exception otherwise
    """
    # Check OpenAI API key
    if not OPENAI_API_KEY:
        print(
            "⚠️  Warning: OPENAI_API_KEY not set. "
            "LLM functionality will not work. "
            "Set it in .env file."
        )
    
    # Check data directories
    if not DATA_DIR.exists():
        print(f"📁 Creating data directory: {DATA_DIR}")
        DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if not RESULTS_DIR.exists():
        print(f"📁 Creating results directory: {RESULTS_DIR}")
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    return True


# ─────────────────────────────────────────────────────────────────────────────
# QUICK REFERENCE
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 80)
    print("THESIS PROJECT CONFIGURATION")
    print("=" * 80)
    print()
    print(f"📂 Project Root: {PROJECT_ROOT}")
    print(f"📂 Data Directory: {DATA_DIR}")
    print(f"📂 Results Directory: {RESULTS_DIR}")
    print()
    print(f" Embedding Model: {EMBEDDING_MODEL}")
    print(f" Embedding Dimension: {EMBEDDING_DIM}")
    print()
    print(f" LLM Model: {OPENAI_MODEL}")
    print(f" OpenAI API Key Set: {bool(OPENAI_API_KEY)}")
    print()
    print(f" Default Top-N: {DEFAULT_TOP_N}")
    print(f" Max Interactions: {MAX_INTERACTIONS}")
    print()
    print(f" Random Seed: {RANDOM_SEED}")
    print()
    print(" Configuration loaded successfully!")
    print()
    
    # Validate
    validate_config()
