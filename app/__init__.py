"""Pacote principal da aplicação Flask Sabores da Serra.

Este pacote inicializa a aplicação usando o padrão de Application Factory.
"""

import os
from flask import Flask, send_from_directory
from app.config import Config


def create_app(config_class=Config) -> Flask:
    """Cria e configura uma instância do aplicativo Flask.

    Args:
        config_class: A classe de configuração a ser utilizada.

    Returns:
        A instância configurada do Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Garante que a pasta de mídia exista
    os.makedirs(app.config['MEDIA_FOLDER'], exist_ok=True)

    # Rota dinâmica para servir fotos da pasta de mídia externa
    @app.route('/media/fotos/<path:filename>')
    def serve_media(filename):
        """Serve arquivos de imagem a partir do diretório de mídia externa."""
        return send_from_directory(app.config['MEDIA_FOLDER'], filename)

    # Registrar os Blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
