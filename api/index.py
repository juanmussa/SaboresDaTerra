"""Ponto de entrada compatível para rotas legadas ou Serverless Functions."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from index import app  # noqa: E402, F401
