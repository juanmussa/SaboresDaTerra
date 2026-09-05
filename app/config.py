"""Módulo de configuração da aplicação Sabores da Serra.

Este módulo define as configurações do Flask, incluindo chaves de segurança
e o caminho para os arquivos de mídia e estáticos em ambientes de desenvolvimento
e produção (Vercel).
"""

import os
import secrets
import warnings

# Tenta carregar variáveis do arquivo .env caso python-dotenv esteja instalado
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    """Classe de configuração contendo parâmetros de execução do Flask."""

    # Identifica se a aplicação está rodando em ambiente de produção (ex: Vercel)
    IS_PRODUCTION = (
        os.environ.get('VERCEL') == '1'
        or os.environ.get('FLASK_ENV') == 'production'
        or os.environ.get('ENV') == 'production'
    )

    # Obtenção da SECRET_KEY das variáveis de ambiente
    _raw_secret_key = os.environ.get('SECRET_KEY')

    if _raw_secret_key and _raw_secret_key != 'chave-secreta-sabores-da-serra-12345':
        SECRET_KEY = _raw_secret_key
    else:
        if IS_PRODUCTION:
            # Em produção na Vercel, caso não tenha sido configurada no painel,
            # geramos uma chave criptográfica forte temporária e alertamos
            SECRET_KEY = secrets.token_hex(32)
            warnings.warn(
                "AVISO DE SEGURANÇA: SECRET_KEY não configurada no ambiente de produção da Vercel! "
                "Uma chave temporária randômica foi gerada para esta instância. "
                "Para manter sessões persistentes, configure a variável SECRET_KEY no painel da Vercel "
                "(Settings > Environment Variables).",
                UserWarning,
                stacklevel=2,
            )
        else:
            # Em desenvolvimento local, usa chave de desenvolvimento caso não haja .env
            SECRET_KEY = _raw_secret_key or 'dev-secret-key-sabores-da-serra-local-only'

    # Configurações de Segurança para Cookies de Sessão
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = IS_PRODUCTION

    # Diretórios base e estáticos
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..')
    )
    PUBLIC_FOLDER = os.path.join(BASE_DIR, 'public')
    STATIC_FOLDER = (
        os.path.join(PUBLIC_FOLDER, 'static')
        if os.path.isdir(os.path.join(PUBLIC_FOLDER, 'static'))
        else os.path.join(BASE_DIR, 'app', 'static')
    )
    MEDIA_FOLDER = os.path.join(BASE_DIR, 'media', 'fotos')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
