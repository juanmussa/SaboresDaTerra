"""Script de execução principal da aplicação Sabores da Serra.

Este arquivo instancia o Flask através da Application Factory e
inicializa o servidor de desenvolvimento local.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
