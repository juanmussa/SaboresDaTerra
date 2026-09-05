"""Ponto de entrada nativo da aplicação Sabores da Serra para deploy no Vercel.

A infraestrutura moderna da Vercel detecta automaticamente frameworks Python (Flask)
através da presença de Flask no requirements.txt e da exposição da variável 'app'
em arquivos padrão como 'index.py' na raiz do repositório.
"""

import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1")
    )
