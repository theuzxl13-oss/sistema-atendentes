import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sqlite3

# Configuração da página profissional
st.set_page_config(page_title="Painel Integrado Futturis", layout="wide", page_icon="🏢")


# =====================================================================
# 🗄️ CONFIGURAÇÃO DO BANCO DE DADOS (SQLite)
# =====================================================================
def conectar_banco():
    conn = sqlite3.connect("sistema.db", check_same_thread=False)
    return conn


def inicializar_banco():
    conn = conectar_banco()
    cursor = conn.cursor()

    # Criar tabela de usuários/atendentes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        usuario TEXT PRIMARY KEY,
        senha TEXT,
        cargo TEXT,
        local TEXT
    )
    """)

    # Criar tabela de produtos (CORRIGIDA PARA SQLITE)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos_sqlite (
        codigo INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        categoria TEXT,
        preco REAL,
        quantidade INTEGER
    )
    """)

    # Criar tabela de vendas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        produto TEXT,
        quantidade INTEGER,
        total REAL,
        atendente TEXT
    )
    """)

    # Criar tabela de trocas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trocas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_devolvido TEXT,
        quantidade INTEGER,
        motivo TEXT,
        atendente TEXT,
        data TEXT
    )
    """)

    # Inserir usuários padrão caso o banco esteja vazio
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios VALUES ('marcelo', '123', 'Desenvolvedor', 'Sede Central')")
        cursor.execute("INSERT INTO usuarios VALUES ('matheus', '123', 'Desenvolvedor', 'Sede Central')")
        cursor.execute("INSERT INTO usuarios VALUES ('vendedor1', '123', 'Vendedor', 'Balcão Frente')")
        cursor.execute("INSERT INTO usuarios VALUES ('dono', '123', 'Dono', 'Administração')")

        # Inserir produtos padrão se estiver vazio
        cursor.execute("SELECT COUNT(*) FROM produtos_sqlite")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO produtos_sqlite (nome, categoria, preco, quantidade) VALUES ('Cimento CP II', 'Materiais Básicos', 32.00, 45)")
            cursor.execute(
                "INSERT INTO produtos_sqlite (nome, categoria, preco, quantidade) VALUES ('Tijolo Baiano', 'Materiais Básicos', 1.20, 1200)")
            cursor.execute(
                "INSERT INTO produtos_sqlite (nome, categoria, preco, quantidade) VALUES ('Areia Grossa (m³)', 'Materiais Básicos', 110.00, 8)")

    conn.commit()
    conn.close()


# Inicializa as tabelas do banco de dados
inicializar_banco()

# =====================================================================
# 🎨 PALETA DE CORES (Tema Escuro)
# =====================================================================
COR_FUNDO_PAGINA = "#121214"
COR_TEXTO_PRINCIPAL = "#FFFFFF"
COR_TEXTO_MUTED = "#A0A0AA"
COR_BORDAS = "#2E2E33"
COR_DESTAQUE_AZUL = "#0066FF"

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {COR_FUNDO_PAGINA} !important;
    }}
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp span, .stApp label {{
        color: {COR_TEXTO_PRINCIPAL} !important;
    }}
    .titulo-card {{
        font-size: 16px;
        font-weight: bold;
        color: {COR_DESTAQUE_AZUL} !important;
        margin-bottom: 15px;
        border-bottom: 1px solid {COR_BORDAS};
        padding-bottom: 8px;
    }}
    .texto-muted {{
        color: {COR_TEXTO_MUTED} !important;
        font-size: 13px;
        margin: 2px 0;
    }}
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE LOGIN ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

if not st.session_state['autenticado']:
    st.subheader("🔑 Identificação do Atendente")
    nome_login = st.text_input("Digite seu nome de usuário:", placeholder="Ex: matheus").lower().strip()
    senha_login = st.text_input("Digite sua senha:", type="password")

    if st.button("Acessar Painel", type="primary"):
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT senha, cargo, local FROM usuarios WHERE usuario = ?", (nome_login,))
        user_db = cursor.fetchone()
        conn.close()

        if user_db:
            senha_db, cargo_db, local_db = user_db
            if senha_db == senha_login:
                st.session_state['autenticado'] = True
                st.session_state['atendente'] = nome_login
                st.session_state['cargo'] = cargo_db
                st.session_state['local'] = local_db
                st.rerun()
            else:
                st.error("Senha incorreta!")
        else:
            st.error("Usuário não encontrado.")

# --- TELA PRINCIPAL (SISTEMA LIBERADO) ---
else:
    # Cabeçalho
    col_header1, col_header2 = st.columns([8, 2])
    with col_header1:
        st.title("🏢 Painel Integrado de Operações")
    with col_header2:
        st.write("")
        if st.button("🚪 Sair / Logoff", use_container_width=True):
            st.session_state['autenticado'] = False
            if 'foto_perfil' in st.session_state:
                del st.session_state['foto_perfil']
            st.rerun()

    # Layout de Duas Colunas
    col_esquerda, col_direita = st.columns([3, 7])

    # --- COLUNA DA ESQUERDA (IDENTIFICAÇÃO) ---
    with col_esquerda:
        with st.container(border=True):
            st.markdown('<div class="titulo-card">🏠 Identificação</div>', unsafe_allow_html=True)
            col_foto, col_dados = st.columns([1, 2])

            with col_foto:
                if 'foto_perfil' in st.session_state and st.session_state['foto_perfil'] is not None:
                    st.image(st.session_state['foto_perfil'], use_container_width=True)
                else:
                    st.markdown("<h1 style='text-align: center; margin-top: 10px; font-size: 70px;'>👤</h1>",
                                unsafe_allow_html=True)

            with col_dados:
                st.markdown(f"### {st.session_state['atendente'].capitalize()}")
                st.markdown(
                    f'<p style="color: #00FF66; font-weight: bold; margin: 0;">🛡️ {st.session_state["cargo"]}</p>',
                    unsafe_allow_html=True)
                st.markdown(f'<p class="texto-muted">📍 {st.session_state["local"]}</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="texto-muted">💻 IP: 200.106.192.140</p>', unsafe_allow_html=True)

            # Botão oculto discreto para alterar imagem
            st.write("")
            col_vazia, col_link = st.columns([5, 1])
            with col_link:
                with st.popover("🔗", help="Alterar foto"):
                    foto_carregada = st.file_uploader("Upload", type=["png", "jpg", "jpeg"],
                                                      label_visibility="collapsed")
                    if foto_carregada is not None:
                        st.session_state['foto_perfil'] = foto_carregada
                        st.rerun()

    # --- COLUNA DA DIREITA (OPERACIONAL) ---
    with col_direita:
        cargo_atual = st.session_state['cargo']

        with st.container(border=True):
            st.markdown('<div class="titulo-card">📋 Recursos e Operações do Sistema</div>', unsafe_allow_html=True)

            # Definição das abas conforme o cargo
            if cargo_atual == "Vendedor":
                lista_abas = ["💰 Vendas", "🔄 Trocas"]
                sub_abas = st.tabs(lista_abas)
                aba_venda = sub_abas[0]
                aba_troca = sub_abas[1]
                aba_cadastro = None
                aba_estoque = None
                aba_relatorio = None
                aba_usuarios = None
            else:
                lista_abas = [
                    "📝 Cadastrar Produto",
                    "📦 Estoque",
                    "💰 Vendas",
                    "📊 Relatórios",
                    "🔄 Trocas",
                    "👥 Cadastrar Atendentes"
                ]
                sub_abas = st.tabs(lista_abas)
                aba_cadastro = sub_abas[0]
                aba_estoque = sub_abas[1]
                aba_venda = sub_abas[2]
                aba_relatorio = sub_abas[3]
                aba_troca = sub_abas[4]
                aba_usuarios = sub_abas[5]

            # --- ABA: CADASTRAR PRODUTO ---
            if aba_cadastro:
                with aba_cadastro:
                    st.write("### 🆕 Cadastrar Novo Item no Estoque")
                    nome_prod = st.text_input("Nome do Produto", placeholder="Ex: Saco de Cimento CP II")
                    categoria = st.selectbox("Categoria", ["Materiais Básicos", "Ferramentas", "Acabamento"])
                    preco = st.number_input("Preço de Venda (R$)", min_value=0.0, step=0.50, value=10.0)
                    quantidade = st.number_input("Quantidade Inicial", min_value=0, step=1, value=10)

                    if st.button("Salvar Produto no Banco de Dados", type="primary"):
                        if nome_prod:
                            conn = conectar_banco()
                            cursor = conn.cursor()
                            cursor.execute(
                                "INSERT INTO produtos_sqlite (nome, categoria, preco, quantidade) VALUES (?, ?, ?, ?)",
                                (nome_prod, categoria, preco, quantidade)
                            )
                            conn.commit()
                            conn.close()
                            st.success(f"✔️ '{nome_prod}' salvo permanentemente no banco de dados!")
                        else:
                            st.error("Preencha o nome do produto.")

            # --- ABA: ESTOQUE ---
            if aba_estoque:
                with aba_estoque:
                    st.write("### 📦 Estoque Atualizado em Tempo Real")
                    conn = conectar_banco()
                    df_prod = pd.read_sql_query(
                        "SELECT codigo as 'Código', nome as 'Item', categoria as 'Categoria', preco as 'Preço (R$)', quantidade as 'Qtd' FROM produtos_sqlite",
                        conn)
                    conn.close()
                    st.dataframe(df_prod, use_container_width=True, hide_index=True)

            # --- ABA: VENDAS ---
            with aba_venda:
                st.write("### 💰 Registrar Nova Venda")
                conn = conectar_banco()
                # Puxa os produtos direto do banco para o atendente selecionar
                cursor = conn.cursor()
                cursor.execute("SELECT nome, preco, quantidade FROM produtos_sqlite")
                produtos_dados = cursor.fetchall()
                conn.close()

                if produtos_dados:
                    nomes_produtos = [p[0] for p in produtos_dados]
                    dict_precos = {p[0]: (p[1], p[2]) for p in produtos_dados}

                    prod_selecionado = st.selectbox("Selecionar Produto", nomes_produtos)
                    preco_unitario, estoque_atual = dict_precos[prod_selecionado]

                    st.write(f"Preço Unitário: R$ {preco_unitario:.2f} | Estoque Disponível: {estoque_atual} un.")
                    qtd_venda = st.number_input("Quantidade", min_value=1, max_value=max(1, estoque_atual), value=1)
                    total_venda = preco_unitario * qtd_venda
                    st.write(f"### **Valor Total: R$ {total_venda:.2f}**")

                    if st.button("Confirmar Venda", type="primary"):
                        if estoque_atual >= qtd_venda:
                            conn = conectar_banco()
                            cursor = conn.cursor()
                            # 1. Deduz do estoque
                            novo_estoque = estoque_atual - qtd_venda
                            cursor.execute("UPDATE produtos_sqlite SET quantidade = ? WHERE nome = ?",
                                           (novo_estoque, prod_selecionado))
                            # 2. Salva a venda
                            data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            cursor.execute(
                                "INSERT INTO vendas (data, produto, quantidade, total, atendente) VALUES (?, ?, ?, ?, ?)",
                                (data_venda, prod_selecionado, qtd_venda, total_venda, st.session_state['atendente'])
                            )
                            conn.commit()
                            conn.close()
                            st.balloons()
                            st.success("Venda efetuada e estoque atualizado com sucesso!")
                            st.rerun()
                        else:
                            st.error("Quantidade acima do estoque disponível!")
                else:
                    st.warning("Nenhum produto cadastrado no banco de dados.")

            # --- ABA: RELATÓRIOS ---
            if aba_relatorio:
                with aba_relatorio:
                    st.write("### 📊 Histórico Geral de Vendas")
                    d_inicio = st.date_input("Data Início", datetime.today() - timedelta(days=7))
                    d_fim = st.date_input("Data Fim", datetime.today())

                    # Converte datas para string para consulta no SQLite
                    str_inicio = d_inicio.strftime("%Y-%m-%d") + " 00:00:00"
                    str_fim = d_fim.strftime("%Y-%m-%d") + " 23:59:59"

                    conn = conectar_banco()
                    query = "SELECT data as 'Data/Hora', produto as 'Item', quantidade as 'Qtd', total as 'Total (R$)', atendente as 'Operador' FROM vendas WHERE data BETWEEN ? AND ?"
                    df_vendas = pd.read_sql_query(query, conn, params=(str_inicio, str_fim))
                    conn.close()

                    if not df_vendas.empty:
                        st.dataframe(df_vendas, use_container_width=True, hide_index=True)
                        total_faturado = df_vendas['Total (R$)'].sum()
                        st.metric("Faturamento do Período", f"R$ {total_faturado:.2f}")
                    else:
                        st.info("Nenhuma venda registrada neste período.")

            # --- ABA: TROCAS ---
            with aba_troca:
                st.write("### 🔄 Registrar Trocas e Devoluções")
                prod_troca = st.text_input("Produto devolvido pelo cliente")
                qtd_troca = st.number_input("Quantidade para Troca", min_value=1, value=1)
                motivo = st.selectbox("Motivo da devolução", ["Defeito de fábrica", "Sobrou da obra", "Compra errada"])

                if st.button("Registrar Devolução"):
                    if prod_troca:
                        conn = conectar_banco()
                        cursor = conn.cursor()
                        data_troca = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        cursor.execute(
                            "INSERT INTO trocas (produto_devolvido, quantidade, motivo, atendente, data) VALUES (?, ?, ?, ?, ?)",
                            (prod_troca, qtd_troca, motivo, st.session_state['atendente'], data_troca)
                        )
                        conn.commit()
                        conn.close()
                        st.warning(f"Troca gravada no banco: {qtd_troca} un. de '{prod_troca}'")
                    else:
                        st.error("Informe o produto devolvido.")

            # --- ABA: CADASTRAR ATENDENTES ---
            if aba_usuarios:
                with aba_usuarios:
                    st.write("### 👥 Controle e Cadastro de Atendentes")
                    col_user1, col_user2 = st.columns(2)
                    with col_user1:
                        novo_nome = st.text_input("Nome de Usuário (Sem espaços)",
                                                  placeholder="Ex: joao").lower().strip()
                        nova_senha = st.text_input("Senha de Acesso", type="password")
                    with col_user2:
                        novo_cargo = st.selectbox("Cargo", ["Vendedor", "Gerente", "Dono"])
                        novo_local = st.text_input("Local/Filial", value="Depósito Principal")

                    if st.button("Registrar Novo Atendente no Banco", type="primary"):
                        if novo_nome != "" and nova_senha != "":
                            try:
                                conn = conectar_banco()
                                cursor = conn.cursor()
                                cursor.execute("INSERT INTO usuarios VALUES (?, ?, ?, ?)",
                                               (novo_nome, nova_senha, novo_cargo, novo_local))
                                conn.commit()
                                conn.close()
                                st.success(f"✔️ Atendente '{novo_nome.capitalize()}' cadastrado permanentemente!")
                                st.rerun()
                            except sqlite3.IntegrityError:
                                st.error("Este nome de usuário já existe!")
                        else:
                            st.error("Preencha todos os campos.")

                    st.write("---")
                    st.write("#### Atendentes Ativos no Banco:")
                    conn = conectar_banco()
                    df_users = pd.read_sql_query(
                        "SELECT usuario as 'Usuário', cargo as 'Cargo', local as 'Local' FROM usuarios", conn)
                    conn.close()
                    st.dataframe(df_users, use_container_width=True, hide_index=True)