"""Módulo de rotas da aplicação Sabores da Serra.

Este módulo define o blueprint principal e as rotas para todas as
páginas da aplicação.
"""

import os
from flask import (
    Blueprint, render_template, request, flash, redirect,
    url_for, current_app
)

main_bp = Blueprint('main', __name__)


def get_media_photos() -> list:
    """Varre a pasta de mídia e retorna os nomes das fotos válidas.

    Retorna:
        Uma lista com os nomes dos arquivos de imagem encontrados.
    """
    media_folder = current_app.config['MEDIA_FOLDER']
    allowed_exts = current_app.config['ALLOWED_EXTENSIONS']

    if not os.path.exists(media_folder):
        return []

    try:
        files = os.listdir(media_folder)
        photos = [
            f for f in files
            if os.path.isfile(os.path.join(media_folder, f))
            and f.split('.')[-1].lower() in allowed_exts
        ]
        return sorted(photos)
    except OSError:
        return []


@main_bp.route('/api')
@main_bp.route('/api/index')
def api_fallback():
    """Redireciona rotas da API serverless para a página inicial."""
    return redirect(url_for('main.home'))


@main_bp.route('/')
@main_bp.route('/home')
def home():
    """Renderiza a página inicial (Home)."""
    photos = get_media_photos()
    # Destaques da fazenda para a Home
    destaques = [
        {
            'nome': 'Queijo da Serra',
            'categoria': 'Queijos',
            'descricao': 'Maturado por 60 dias nas montanhas.',
            'link': url_for('main.producao') + '#queijo'
        },
        {
            'nome': 'Geleia de Frutas Vermelhas',
            'categoria': 'Doces',
            'descricao': 'Feita com frutas frescas da colheita matinal.',
            'link': url_for('main.producao') + '#geleia'
        },
        {
            'nome': 'Pão de Fermentação Natural',
            'categoria': 'Pães',
            'descricao': 'Cascudo e macio, fermentado por 36 horas.',
            'link': url_for('main.producao') + '#pao'
        }
    ]
    return render_template('home.html', photos=photos, destaques=destaques)


@main_bp.route('/producao')
def producao():
    """Renderiza a página de produtos rústicos de Nossa Produção."""
    produtos = [
        {
            'id': 'queijo',
            'nome': 'Queijo da Serra Artesanal',
            'categoria': 'Queijos',
            'descricao': 'Preparado com leite cru de vacas criadas soltas, '
                         'maturado por 60 dias sobre tábuas de araucária. '
                         'Possui casca rústica amarelada, textura macia e '
                         'um sabor ligeiramente amanteigado e marcante.',
            'detalhes': 'Maturado 60 dias • Leite Cru • Sem aditivos',
            'imagem': 'foto_fazenda_2.jpg'
        },
        {
            'id': 'geleia',
            'nome': 'Geleia de Frutas Vermelhas',
            'categoria': 'Conservas e Doces',
            'descricao': 'Uma combinação rica e equilibrada de amoras, '
                         'morangos e framboesas frescas colhidas na fazenda. '
                         'Cozida lentamente em tachos de cobre com baixo '
                         'teor de açúcar, preservando o frescor e a acidez.',
            'detalhes': '100% Natural • Tacho de Cobre • Pote 250g',
            'imagem': 'foto_fazenda_3.jpg'
        },
        {
            'id': 'pao',
            'nome': 'Pão de Fermentação Natural (Sourdough)',
            'categoria': 'Padaria',
            'descricao': 'Elaborado apenas com farinha de trigo especial, '
                         'água purificada e sal marinho. O fermento natural '
                         '(levain) da nossa família é alimentado há mais de '
                         'dez anos, garantindo casca crocante e miolo alvéolo.',
            'detalhes': 'Fermentação de 36h • Assado na Pedra • Aprox. 700g',
            'imagem': 'foto_fazenda_3.jpg'
        },
        {
            'id': 'doce-leite',
            'nome': 'Doce de Leite da Fazenda',
            'categoria': 'Conservas e Doces',
            'descricao': 'Doce de leite tradicional e cremoso, cozido por '
                         'horas com o leite fresco ordenhado no mesmo dia e '
                         'uma pitada de baunilha natural. Perfeito equilíbrio '
                         'de doçura e textura aveludada.',
            'detalhes': 'Receita de Vó • Cozimento Lento • Pote 350g',
            'imagem': 'foto_fazenda_3.jpg'
        },
        {
            'id': 'mel',
            'nome': 'Mel Silvestre Artesanal',
            'categoria': 'Mel e Derivados',
            'descricao': 'Mel puro de abelhas que polinizam as flores da '
                         'nossa encosta florestal. Possui coloração âmbar, '
                         'aroma floral rico e textura densa. Totalmente '
                         'cru, filtrado apenas a frio.',
            'detalhes': 'Cru e Filtrado a Frio • Florada Silvestre • Pote 300g',
            'imagem': 'foto_fazenda_3.jpg'
        }
    ]
    return render_template('producao.html', produtos=produtos)


@main_bp.route('/contato', methods=['GET', 'POST'])
def contato():
    """Gere a página de contato e o envio do formulário."""
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        telefone = request.form.get('telefone')
        assunto = request.form.get('assunto')
        mensagem = request.form.get('mensagem')

        # Validação simples
        if not nome or not email or not mensagem:
            flash('Por favor, preencha todos os campos obrigatórios.', 'error')
        else:
            # Em uma aplicação real, aqui dispararíamos o envio de e-mail.
            # Armazenamos uma mensagem de sucesso para simulação.
            flash(
                f'Obrigado, {nome}! Sua mensagem sobre "{assunto}" '
                'foi recebida com sucesso. Entraremos em contato em breve.',
                'success'
            )
            return redirect(url_for('main.contato'))

    return render_template('contato.html')


@main_bp.route('/tabela')
def tabela():
    """Renderiza a página de Tabela de Produtos."""
    produtos_tabela = [
        {
            'nome': 'Queijo da Serra Artesanal',
            'categoria': 'Queijos',
            'descricao': 'Maturado por 60 dias em araucária',
            'peso': 'Peça de aprox. 1kg',
            'preco': 'R$ 78,00',
            'disponivel': True
        },
        {
            'nome': 'Geleia de Frutas Vermelhas',
            'categoria': 'Conservas e Doces',
            'descricao': 'Amora, morango e framboesa',
            'peso': 'Pote de 250g',
            'preco': 'R$ 22,00',
            'disponivel': True
        },
        {
            'nome': 'Pão de Fermentação Natural',
            'categoria': 'Padaria',
            'descricao': 'Assado rústico com levain familiar',
            'peso': 'Unidade de aprox. 700g',
            'preco': 'R$ 18,00',
            'disponivel': True
        },
        {
            'nome': 'Doce de Leite da Fazenda',
            'categoria': 'Conservas e Doces',
            'descricao': 'Cremoso, feito com leite fresco da ordenha',
            'peso': 'Pote de 350g',
            'preco': 'R$ 25,00',
            'disponivel': True
        },
        {
            'nome': 'Mel Silvestre Artesanal',
            'categoria': 'Mel e Derivados',
            'descricao': 'Mel puro de florada nativa',
            'peso': 'Pote de 300g',
            'preco': 'R$ 32,00',
            'disponivel': False
        },
        {
            'nome': 'Queijo Frescal da Serra',
            'categoria': 'Queijos',
            'descricao': 'Queijo fresco, suave e de textura leve',
            'peso': 'Peça de aprox. 500g',
            'preco': 'R$ 35,00',
            'disponivel': True
        },
        {
            'nome': 'Geleia de Figo com Nozes',
            'categoria': 'Conservas e Doces',
            'descricao': 'Figos orgânicos cozidos com pedaços de nozes',
            'peso': 'Pote de 250g',
            'preco': 'R$ 24,00',
            'disponivel': True
        }
    ]
    return render_template('tabela.html', produtos=produtos_tabela)


@main_bp.route('/historia')
def historia():
    """Renderiza a página de Nossa História e valores."""
    photos = get_media_photos()
    linha_tempo = [
        {
            'ano': '1998',
            'titulo': 'O Início de Tudo',
            'descricao': 'A família Silva muda-se para a região serrana, '
                         'iniciando a criação de vacas leiteiras e a feitura '
                         'do primeiro queijo caseiro.'
        },
        {
            'ano': '2005',
            'titulo': 'Primeira Receita de Geleia',
            'descricao': 'Aproveitando o excesso de frutas das plantações '
                         'locais, iniciam o cozimento de geleias orgânicas, '
                         'vendendo para vizinhos.'
        },
        {
            'ano': '2012',
            'titulo': 'Nascimento da Marca',
            'descricao': 'A marca "Sabores da Serra" é oficialmente criada, '
                         'com a expansão da produção e a introdução dos pães '
                         'de fermentação natural.'
        },
        {
            'ano': '2020',
            'titulo': 'Reconhecimento Regional',
            'descricao': 'Nossos queijos e doces são premiados em feiras de '
                         'gastronomia regional pela qualidade artesanal.'
        },
        {
            'ano': 'Hoje',
            'titulo': 'Preservando a Tradição',
            'descricao': 'Seguimos fiéis às receitas originais e ao respeito '
                         'à natureza, entregando o melhor sabor da montanha.'
        }
    ]
    return render_template(
        'historia.html', photos=photos, linha_tempo=linha_tempo
    )
