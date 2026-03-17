import streamlit as st
import torch
from sentence_transformers import SentenceTransformer

# FIX: cache model, không reload mỗi lần rerun
@st.cache_resource
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    return SentenceTransformer("intfloat/multilingual-e5-base", device=device), device

def embed_text(text: str):
    model, device = load_model()
    return model.encode(text, device=device)

def embed_batch(texts: list):
    """Encode nhiều văn bản 1 lần, hiệu quả hơn gọi từng cái"""
    model, device = load_model()
    return model.encode(texts, device=device, batch_size=32)