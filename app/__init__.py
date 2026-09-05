"""Pacote principal da aplicação Flask Sabores da Serra.

Este pacote inicializa a aplicação usando o padrão de Application Factory,
configurando middlewares para compatibilidade total com o proxy reverso da Vercel.
"""

import os
from flask import Flask, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from app.config import Config


class VercelPathFixMiddleware:
    """Middleware WSGI para compatibilidade com rotas e rewrites da Vercel.

    Quando a Vercel reescreve requisições para Serverless Functions (ex: /api/index),
    ela envia o caminho original solicitado pelo usuário no cabeçalho HTTP
    X-Forwarded-Uri ou X-Matched-Path. Este middleware restaura o PATH_INFO
    original para que o Flask processe as rotas corretamente.
    """

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # Tenta obter o path original passado pelo proxy reverso da Vercel
        forwarded_uri = (
            environ.get('HTTP_X_FORWARDED_URI')
            or environ.get('HTTP_X_MATCHED_PATH')
        )
        if forwarded_uri:
            clean_path = forwarded_uri.split('?')[0]
            if clean_path:
                environ['PATH_INFO'] = clean_path
        elif environ.get('PATH_INFO') in (
            '/index.py', '/index', '/api/index', '/api/index.py', '/api'
        ):
            # Se for chamado diretamente sem o header, cai na raiz do site
            environ['PATH_INFO'] = '/'

        return self.wsgi_app(environ, start_response)


def create_app(config_class=Config) -> Flask:
    """Cria e configura uma instância do aplicativo Flask.

    Args:
        config_class: A classe de configuração a ser utilizada.

    Returns:
        A instância configurada do Flask.
    """
    app = Flask(
        __name__,
        static_folder=config_class.STATIC_FOLDER,
        static_url_path='/static'
    )
    app.config.from_object(config_class)

    # Aplica middlewares para Proxy e Vercel
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    app.wsgi_app = VercelPathFixMiddleware(app.wsgi_app)

    # Tenta criar a pasta de mídia caso o sistema permita (ignora em sistema read-only como Vercel)
    try:
        os.makedirs(app.config['MEDIA_FOLDER'], exist_ok=True)
    except OSError:
        pass

    # Rota dinâmica para servir fotos da pasta de mídia externa
    @app.route('/media/fotos/<path:filename>')
    def serve_media(filename):
        """Serve arquivos de imagem a partir do diretório de mídia externa."""
        if not os.path.exists(app.config['MEDIA_FOLDER']):
            from flask import abort
            abort(404)
        return send_from_directory(app.config['MEDIA_FOLDER'], filename)

    # Registrar os Blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
