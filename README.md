# CadastroPI
Tela de cadastro do projeto integrador de banco de dados
Claro! Aqui está um exemplo de `README.md` para o seu projeto **Sistema de Cadastro de Usuários para Chatbot da PUC Campinas**, desenvolvido com Streamlit e MongoDB:

---

````markdown
# 🎓 Sistema de Cadastro de Usuários - ChatBot PUC Campinas

Este projeto é uma interface web desenvolvida em **Streamlit** para cadastro e login de usuários que utilizarão o **ChatBot da PUC Campinas**. Ele permite autenticação de diferentes perfis (Estudante, Professor, Funcionário e Visitante) com validação de e-mail institucional e persistência de dados via **MongoDB**.

---

## 🚀 Funcionalidades

- Cadastro de novos usuários com perfil específico:
  - Estudante (RA e Curso)
  - Professor (Curso e Departamento)
  - Funcionário (Departamento)
  - Visitante (dados básicos)
- Login com validação de senha (hash SHA-256)
- Validação de e-mails institucionais da PUC Campinas
- Armazenamento de dados em banco MongoDB
- Atualização do último acesso do usuário autenticado
- Interface amigável e responsiva com Streamlit

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [PyMongo](https://pymongo.readthedocs.io/)
- [MongoDB](https://www.mongodb.com/)
- [Hashlib](https://docs.python.org/3/library/hashlib.html)
- Expressões Regulares (`re`)

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/chatbot-puc-cadastro.git
cd chatbot-puc-cadastro
````

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

**Exemplo de `requirements.txt`:**

```
streamlit
pymongo
```

---

## ⚙️ Configuração do MongoDB

Certifique-se de que o MongoDB esteja rodando localmente na porta padrão (27017) ou na versão cloud.

Você pode iniciar o MongoDB via Docker (exemplo):

```bash
docker run -d -p 27017:27017 --name chatbot-mongo mongo
```

---

## ▶️ Executando o app

No diretório do projeto, execute:

```bash
streamlit run app.py
```

Acesse o app no navegador pelo link exibido no terminal (geralmente `http://localhost:8501`).


