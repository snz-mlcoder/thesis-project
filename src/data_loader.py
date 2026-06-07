"""
Data loading and preprocessing module for MovieLens dataset and embeddings.
Handles downloading, caching, and preparing data for the pipeline.
"""

import io
import zipfile
from pathlib import Path
from typing import Tuple, Optional
import logging

import numpy as np
import pandas as pd
import requests
from sentence_transformers import SentenceTransformer

from src.config import (
    MOVIELENS_URL, MOVIELENS_FILES, DATA_DIR,
    SBERT_MODEL, SBERT_BATCH_SIZE, SBERT_NORMALIZE, SBERT_EMBEDDING_DIM,
    EMBEDDINGS_PATH, MOVIES_CACHE_PATH, GLOBAL_SEED
)
from src.logging_setup import setup_logging

logger = setup_logging(__name__)


class DataLoader:
    """
    Responsible for downloading, loading, and caching MovieLens data.
    """
    
    def __init__(self, data_dir: Path = DATA_DIR):
        """
        Initialize DataLoader.
        
        Args:
            data_dir: Directory to store data files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True, parents=True)
    
    def download_movielens(self, url: str = MOVIELENS_URL, force: bool = False) -> None:
        """
        Download MovieLens 1M dataset from GroupLens.
        
        Args:
            url: URL to download from
            force: If True, re-download even if files exist
            
        Raises:
            requests.RequestException: If download fails
            ValueError: If dataset is incomplete
        """
        # Check if already downloaded
        movies_file = MOVIELENS_FILES["movies"]
        if movies_file.exists() and not force:
            logger.info(f"MovieLens data already exists at {movies_file}")
            return
        
        logger.info(f"Downloading MovieLens 1M from {url}...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Download failed: {e}")
            raise
        
        logger.info("Extracting files...")
        try:
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                for name in z.namelist():
                    if name.endswith('.dat'):
                        filename = Path(name).name
                        target_path = self.data_dir / filename
                        
                        with z.open(name) as src:
                            target_path.write_bytes(src.read())
                        logger.debug(f"Extracted: {filename}")
        except zipfile.BadZipFile as e:
            logger.error(f"Failed to extract zip: {e}")
            raise
        
        # Validate extraction
        for file_name, file_path in MOVIELENS_FILES.items():
            if not file_path.exists():
                raise ValueError(f"Expected file not found: {file_name}")
        
        logger.info("MovieLens 1M download and extraction completed successfully")
    
    def load_movies(self) -> pd.DataFrame:
        """
        Load and preprocess MovieLens movies data.
        
        Returns:
            DataFrame with columns: movie_id, title, genres, year, title_clean, 
                                   genres_clean, text
        """
        movies_path = MOVIELENS_FILES["movies"]
        logger.info(f"Loading movies from {movies_path}...")
        
        movies = pd.read_csv(
            movies_path,
            sep="::",
            engine="python",
            names=["movie_id", "title", "genres"],
            encoding="latin-1"
        )
        
        logger.debug(f"Loaded {len(movies)} movies")
        
        # Extract year from title
        movies["year"] = movies["title"].str.extract(r"\((\d{4})\)").astype(float)
        
        # Clean title (remove year)
        movies["title_clean"] = (
            movies["title"]
            .str.replace(r"\s*\(\d{4}\)", "", regex=True)
            .str.strip()
        )
        
        # Clean genres (replace pipes with spaces)
        movies["genres_clean"] = movies["genres"].str.replace("|", " ", regex=False)
        
        # Create text for embedding (title + genres)
        movies["text"] = movies["title_clean"] + " | " + movies["genres_clean"]
        
        logger.info(f"Preprocessed {len(movies)} movies")
        return movies


class EmbeddingGenerator:
    """
    Handles embedding generation using Sentence-BERT model with caching.
    """
    
    def __init__(self, model_name: str = SBERT_MODEL):
        """
        Initialize EmbeddingGenerator.
        
        Args:
            model_name: Name of the Sentence-BERT model to use
        """
        self.model_name = model_name
        self.model: Optional[SentenceTransformer] = None
        logger.debug(f"EmbeddingGenerator initialized with model: {model_name}")
    
    def _load_model(self) -> SentenceTransformer:
        """
        Lazy-load the Sentence-BERT model.
        
        Returns:
            Loaded SentenceTransformer model
        """
        if self.model is None:
            logger.info(f"Loading Sentence-BERT model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.debug(f"Model loaded successfully")
        return self.model
    
    def generate_embeddings(
        self,
        texts: list,
        cache_path: Path = EMBEDDINGS_PATH,
        force: bool = False
    ) -> np.ndarray:
        """
        Generate or load cached embeddings for texts.
        
        Args:
            texts: List of text strings to embed
            cache_path: Path to cache embeddings
            force: If True, regenerate embeddings even if cache exists
            
        Returns:
            numpy array of shape (n_texts, embedding_dim)
        """
        if cache_path.exists() and not force:
            logger.info(f"Loading cached embeddings from {cache_path}")
            embeddings = np.load(cache_path)
            if embeddings.shape[0] != len(texts):
                logger.warning(
                    f"Cache has {embeddings.shape[0]} embeddings but got {len(texts)} texts. "
                    f"Regenerating..."
                )
            else:
                logger.debug(f"Loaded embeddings shape: {embeddings.shape}")
                return embeddings
        
        logger.info(f"Generating embeddings for {len(texts)} texts...")
        model = self._load_model()
        
        embeddings = model.encode(
            texts,
            batch_size=SBERT_BATCH_SIZE,
            show_progress_bar=True,
            normalize_embeddings=SBERT_NORMALIZE
        )
        
        logger.debug(f"Generated embeddings shape: {embeddings.shape}")
        
        # Save to cache
        cache_path.parent.mkdir(exist_ok=True, parents=True)
        np.save(cache_path, embeddings)
        logger.info(f"Cached embeddings to {cache_path}")
        
        return embeddings


class MovieLensDataset:
    """
    Complete MovieLens dataset with movies and embeddings.
    High-level interface combining DataLoader and EmbeddingGenerator.
    """
    
    def __init__(
        self,
        data_dir: Path = DATA_DIR,
        embeddings_cache_path: Path = EMBEDDINGS_PATH,
        movies_cache_path: Path = MOVIES_CACHE_PATH
    ):
        """
        Initialize MovieLensDataset.
        
        Args:
            data_dir: Directory for data files
            embeddings_cache_path: Path to cache embeddings
            movies_cache_path: Path to cache movies dataframe
        """
        self.data_dir = Path(data_dir)
        self.embeddings_cache_path = embeddings_cache_path
        self.movies_cache_path = movies_cache_path
        
        self.data_loader = DataLoader(data_dir)
        self.embedding_generator = EmbeddingGenerator()
        
        self.movies: Optional[pd.DataFrame] = None
        self.embeddings: Optional[np.ndarray] = None
    
    def prepare(self, force: bool = False) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        Download, load, and generate embeddings for MovieLens dataset.
        Uses caching to avoid redundant work.
        
        Args:
            force: If True, regenerate everything from scratch
            
        Returns:
            Tuple of (movies DataFrame, embeddings array)
        """
        logger.info("Starting MovieLens dataset preparation...")
        
        # Download data
        self.data_loader.download_movielens(force=force)
        
        # Load movies from cache or raw data
        if self.movies_cache_path.exists() and not force:
            logger.info(f"Loading cached movies from {self.movies_cache_path}")
            self.movies = pd.read_pickle(self.movies_cache_path)
        else:
            self.movies = self.data_loader.load_movies()
            self.movies_cache_path.parent.mkdir(exist_ok=True, parents=True)
            self.movies.to_pickle(self.movies_cache_path)
            logger.info(f"Cached movies to {self.movies_cache_path}")
        
        # Generate embeddings
        self.embeddings = self.embedding_generator.generate_embeddings(
            self.movies["text"].tolist(),
            cache_path=self.embeddings_cache_path,
            force=force
        )
        
        # Validate
        if self.embeddings.shape[0] != len(self.movies):
            raise ValueError(
                f"Embeddings ({self.embeddings.shape[0]}) and movies ({len(self.movies)}) "
                f"have different lengths"
            )
        
        if self.embeddings.shape[1] != SBERT_EMBEDDING_DIM:
            raise ValueError(
                f"Expected embedding dimension {SBERT_EMBEDDING_DIM}, "
                f"got {self.embeddings.shape[1]}"
            )
        
        logger.info(
            f"MovieLens dataset ready: {len(self.movies)} movies, "
            f"embeddings shape {self.embeddings.shape}"
        )
        
        return self.movies, self.embeddings
    
    def get_movies(self) -> pd.DataFrame:
        """Get movies DataFrame (must call prepare() first)."""
        if self.movies is None:
            raise RuntimeError("Call prepare() before accessing movies")
        return self.movies
    
    def get_embeddings(self) -> np.ndarray:
        """Get embeddings array (must call prepare() first)."""
        if self.embeddings is None:
            raise RuntimeError("Call prepare() before accessing embeddings")
        return self.embeddings
