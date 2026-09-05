"""Script de execução principal da aplicação Sabores da Serra para desenvolvimento local.

Este arquivo importa a instância Flask configurada em index.py e
inicializa o servidor de desenvolvimento local.
"""

from index import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
