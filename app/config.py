"""Módulo de configuração da aplicação Sabores da Serra.

Este módulo define as configurações do Flask, incluindo chaves de segurança
e o caminho para os arquivos de mídia.
"""

import os


class Config:
    """Classe de configuração contendo parâmetros de execução do Flask."""

    SECRET_KEY = os.environ.get(
        'SECRET_KEY', 'chave-secreta-sabores-da-serra-12345'
    )
    # Define a raiz do projeto e a pasta de mídia externa
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
    MEDIA_FOLDER = os.path.join(BASE_DIR, 'media', 'fotos')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
