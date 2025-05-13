# app.py - Sistema de Cadastro de Usuários para Chatbot PUC Campinas
import streamlit as st
import pymongo
import hashlib
import datetime
import re
from bson.objectid import ObjectId

# Configuração da conexão com MongoDB
def conectar_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["chatbot_puc"]
    return db

# Função para validar email institucional
def validar_email(email):
    padrao = r'^[a-zA-Z0-9._%+-]+@(puc-campinas\.edu\.br|puccampinas\.edu\.br)$'
    return bool(re.match(padrao, email))

# Função para criar hash de senha
def criar_hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Função principal de cadastro
def cadastrar_usuario(nome, email, senha, tipo_usuario, ra=None, curso=None, departamento=None):
    db = conectar_mongodb()
    colecao_usuarios = db["usuarios"]
    
    # Verifica se usuário já existe
    if colecao_usuarios.find_one({"email": email}):
        return False, "Email já cadastrado no sistema"
    
    # Validação de email institucional
    if not validar_email(email):
        return False, "Use um email institucional válido (@puc-campinas.edu.br)"
    
    # Prepara documento de usuário
    novo_usuario = {
        "nome_completo": nome,
        "email": email,
        "senha_hash": criar_hash_senha(senha),
        "tipo_usuario": tipo_usuario,
        "data_cadastro": datetime.datetime.now(),
        "ultimo_acesso": datetime.datetime.now(),
        "status": "ativo"
    }
    
    # Adiciona campos específicos por tipo de usuário
    if tipo_usuario == "estudante" and ra:
        novo_usuario["ra"] = ra
        novo_usuario["curso"] = curso
    elif tipo_usuario == "professor":
        novo_usuario["departamento"] = departamento
        novo_usuario["curso"] = curso
    elif tipo_usuario == "funcionario":
        novo_usuario["departamento"] = departamento
    
    # Insere no banco de dados
    try:
        resultado = colecao_usuarios.insert_one(novo_usuario)
        return True, str(resultado.inserted_id)
    except Exception as e:
        return False, f"Erro no banco de dados: {str(e)}"

# Função de autenticação
def autenticar_usuario(email, senha):
    db = conectar_mongodb()
    colecao_usuarios = db["usuarios"]
    
    usuario = colecao_usuarios.find_one({
        "email": email,
        "senha_hash": criar_hash_senha(senha)
    })
    
    if usuario:
        # Atualiza último acesso
        colecao_usuarios.update_one(
            {"_id": usuario["_id"]},
            {"$set": {"ultimo_acesso": datetime.datetime.now()}}
        )
        return True, usuario
    
    return False, None

# Interface Streamlit
st.set_page_config(
    page_title="ChatBot PUC Campinas - Cadastro",
    page_icon="🎓",
    layout="centered"
)

# Título e descrição
st.title("ChatBot PUC Campinas")
st.subheader("Sistema de Cadastro e Login")

# Abas de Login e Cadastro
tab1, tab2 = st.tabs(["Login", "Novo Cadastro"])

# Aba de Login
with tab1:
    st.header("Acesse sua conta")
    
    email_login = st.text_input("Email:", key="login_email")
    senha_login = st.text_input("Senha:", type="password", key="login_senha")
    
    if st.button("Entrar", type="primary", key="btn_login"):
        if email_login and senha_login:
            sucesso, usuario = autenticar_usuario(email_login, senha_login)
            if sucesso:
                st.success(f"Bem-vindo(a), {usuario['nome_completo']}!")
                st.session_state.usuario_logado = usuario
                st.rerun()
            else:
                st.error("Email ou senha incorretos.")
        else:
            st.warning("Preencha todos os campos.")

# Aba de Cadastro
with tab2:
    st.header("Crie sua conta")
    
    nome = st.text_input("Nome completo:")
    email = st.text_input("Email institucional:")
    
    col1, col2 = st.columns(2)
    with col1:
        senha = st.text_input("Senha:", type="password")
    with col2:
        confirma_senha = st.text_input("Confirme a senha:", type="password")
    
    tipo_usuario = st.selectbox(
        "Perfil de usuário:",
        options=["Estudante", "Professor", "Funcionário", "Visitante"]
    )
    
    # Campos específicos por tipo de usuário
    if tipo_usuario == "Estudante":
        ra = st.text_input("RA (Registro Acadêmico):")
        curso = st.selectbox(
            "Curso:",
            options=[
                "Administração", "Ciência da Computação", "Direito", 
                "Engenharia de Computação", "Sistemas de Informação", 
                "Outro"
            ]
        )
        departamento = None
    elif tipo_usuario == "Professor":
        ra = None
        curso = st.selectbox(
            "Curso principal:",
            options=[
                "Administração", "Ciência da Computação", "Direito", 
                "Engenharia de Computação", "Sistemas de Informação", 
                "Outro"
            ]
        )
        departamento = st.selectbox(
            "Centro:",
            options=["CEATEC", "CCV", "CLC", "CEA", "CCHSA"]
        )
    elif tipo_usuario == "Funcionário":
        ra = None
        curso = None
        departamento = st.text_input("Setor/Departamento:")
    else:  # Visitante
        ra = None
        curso = None
        departamento = None
    
    if st.button("Cadastrar", type="primary"):
        if not nome or not email or not senha:
            st.error("Preencha todos os campos obrigatórios.")
        elif senha != confirma_senha:
            st.error("As senhas não coincidem.")
        else:
            tipo = tipo_usuario.lower()
            if tipo == "funcionário":
                tipo = "funcionario"
                
            sucesso, mensagem = cadastrar_usuario(
                nome, email, senha, tipo,
                ra=ra, curso=curso, departamento=departamento
            )
            
            if sucesso:
                st.success("Cadastro realizado com sucesso! Você já pode fazer login.")
            else:
                st.error(f"Erro no cadastro: {mensagem}")

# Exibição após login
if "usuario_logado" in st.session_state:
    st.sidebar.success(f"Usuário: {st.session_state.usuario_logado['nome_completo']}")
    if st.sidebar.button("Sair"):
        del st.session_state.usuario_logado
        st.rerun()
    
    st.header(f"Bem-vindo ao ChatBot da PUC Campinas")
    st.write("Em breve você poderá interagir com nosso assistente virtual.")