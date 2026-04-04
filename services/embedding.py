"""
embedding.py  –  Tối ưu batch encoding
Thay đổi:
  - embed_batch() hỗ trợ show_progress_bar để tắt khi gọi nội bộ.
  - Thêm embed_batch_np() trả về numpy array (tránh convert lại ở nơi khác).
"""

import streamlit as st
import torch
from sentence_transformers import SentenceTransformer
import numpy as np


@st.cache_resource(show_spinner=False)
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model  = SentenceTransformer("intfloat/multilingual-e5-base", device=device)
    return model, device


def embed_text(text: str) -> np.ndarray:
    model, device = load_model()
    return model.encode(text, device=device, convert_to_numpy=True)


def embed_batch(texts: list, batch_size: int = 32, show_progress: bool = False) -> np.ndarray:
    """
    Encode nhiều văn bản 1 lần.
    Args:
        texts:         list of strings
        batch_size:    số mẫu mỗi batch GPU (32 phù hợp 8 GB VRAM)
        show_progress: hiện tqdm progress bar (tắt mặc định để Streamlit không bị spam)
    Returns:
        np.ndarray shape (len(texts), embed_dim)
    """
    if not texts:
        return np.array([])

    model, device = load_model()
    return model.encode(
        texts,
        device=device,
        batch_size=batch_size,
        show_progress_bar=show_progress,
        convert_to_numpy=True,
        normalize_embeddings=True,   # L2-norm → cosine_sim chỉ cần dot product
    )