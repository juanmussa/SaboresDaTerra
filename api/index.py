"""Ponto de entrada para deploy Serverless na Vercel."""

import sys
import os

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app  # noqa: E402

app = create_app()
