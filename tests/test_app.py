"""Suíte de testes automatizados para a aplicação Sabores da Serra.

Valida carregamento de configurações, gerenciamento de chaves secretas,
comportamento das rotas, formulário de contato e arquivos estáticos.
"""

import os
import sys
import pytest

# Garante que a raiz do projeto esteja no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.config import Config


@pytest.fixture
def app():
    """Cria uma instância da aplicação para testes."""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test-key-for-automated-tests",
    })
    yield app


@pytest.fixture
def client(app):
    """Retorna um cliente de teste do Flask."""
    return app.test_client()


def test_index_app_instance():
    """Verifica se o ponto de entrada index.py expõe uma instância válida do Flask."""
    from index import app as vercel_app
    assert vercel_app is not None
    assert vercel_app.name == "app"


def test_config_secret_key():
    """Verifica se a SECRET_KEY é carregada e válida."""
    config = Config()
    assert config.SECRET_KEY is not None
    assert len(config.SECRET_KEY) > 0


def test_config_production_security(monkeypatch):
    """Testa se as diretivas de cookies e segurança mudam em produção."""
    monkeypatch.setenv("VERCEL", "1")
    monkeypatch.setenv("SECRET_KEY", "minha-chave-producao-super-segura-123")
    
    # Recarrega módulo de configuração
    import importlib
    import app.config
    importlib.reload(app.config)

    prod_config = app.config.Config()
    assert prod_config.IS_PRODUCTION is True
    assert prod_config.SESSION_COOKIE_SECURE is True
    assert prod_config.SESSION_COOKIE_HTTPONLY is True
    assert prod_config.SESSION_COOKIE_SAMESITE == "Lax"
    assert prod_config.SECRET_KEY == "minha-chave-producao-super-segura-123"

    # Restaura módulo
    monkeypatch.delenv("VERCEL", raising=False)
    importlib.reload(app.config)


def test_route_home(client):
    """Testa a rota principal (Home)."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Sabores da Serra" in response.get_data(as_text=True)

    response_home = client.get("/home")
    assert response_home.status_code == 200


def test_route_producao(client):
    """Testa a rota de Nossa Produção."""
    response = client.get("/producao")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Nossa Produção" in html
    assert "Queijo da Serra Artesanal" in html
    assert "Geleia de Frutas Vermelhas" in html


def test_route_tabela(client):
    """Testa a página de Tabela de Produtos."""
    response = client.get("/tabela")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Produtos e Sabores" in html
    assert "Queijo da Serra Artesanal" in html


def test_route_historia(client):
    """Testa a página de Nossa História."""
    response = client.get("/historia")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Nossa História" in html
    assert "1998" in html


def test_route_contato_get(client):
    """Testa o carregamento da página de contato."""
    response = client.get("/contato")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Contate-nos" in html
    assert "Informações de Contato" in html


def test_route_contato_post_valid(client):
    """Testa o envio com sucesso do formulário de contato."""
    payload = {
        "nome": "Maria Silva",
        "email": "maria@example.com",
        "telefone": "(24) 99999-8888",
        "assunto": "Encomenda de Queijos",
        "mensagem": "Gostaria de encomendar duas peças de Queijo da Serra."
    }
    response = client.post("/contato", data=payload, follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Obrigado, Maria Silva!" in html


def test_route_contato_post_invalid(client):
    """Testa o envio com dados faltantes no formulário de contato."""
    payload = {
        "nome": "",
        "email": "invalido",
        "mensagem": ""
    }
    response = client.post("/contato", data=payload, follow_redirects=True)
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Por favor, preencha todos os campos obrigatórios." in html


def test_static_assets(client):
    """Testa o carregamento dos arquivos estáticos essenciais."""
    css_res = client.get("/static/css/style.css")
    assert css_res.status_code == 200
    assert "text/css" in css_res.headers.get("Content-Type", "")

    js_res = client.get("/static/js/main.js")
    assert js_res.status_code == 200

    img_res = client.get("/static/img/placeholder.svg")
    assert img_res.status_code == 200


def test_vercel_forwarded_uri(client):
    """Testa se o middleware restaura rotas reescritas pela Vercel."""
    # Simula rewrite da Vercel para /api/index com header X-Forwarded-Uri
    res_producao = client.get('/api/index', headers={'X-Forwarded-Uri': '/producao'})
    assert res_producao.status_code == 200
    assert "Nossa Produção" in res_producao.get_data(as_text=True)

    res_tabela = client.get('/api/index', headers={'X-Forwarded-Uri': '/tabela'})
    assert res_tabela.status_code == 200
    assert "Produtos e Sabores" in res_tabela.get_data(as_text=True)

    # Simula chamada direta em /index.py ou /api/index sem header
    res_fallback_index = client.get('/index.py')
    assert res_fallback_index.status_code == 200
    assert "Sabores da Serra" in res_fallback_index.get_data(as_text=True)

    res_fallback_api = client.get('/api/index')
    assert res_fallback_api.status_code == 200
    assert "Sabores da Serra" in res_fallback_api.get_data(as_text=True)
