# 📧 IA Spam Classifier — Classificador de E-mails com Inteligência Artificial

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange?style=for-the-badge&logo=scikitlearn" />
  <img src="https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge&logo=sqlite" />
  <img src="https://img.shields.io/badge/Gmail%20API-Google-red?style=for-the-badge&logo=gmail" />
  <img src="https://img.shields.io/badge/Vers%C3%A3o-2.2.1-green?style=for-the-badge" />
</p>

<p align="center">
  Sistema web com Inteligência Artificial para análise e classificação de e-mails como
  <strong>Spam</strong> ou <strong>Não Spam</strong>, com suporte a conexão via
  <strong>Google OAuth/Gmail API</strong> e também conexão manual via <strong>IMAP</strong>.
</p>

---

## 📌 Nome do Projeto

**IA Spam Classifier**

---

## 🎯 Objetivo do Projeto

O objetivo deste projeto é desenvolver uma aplicação web capaz de analisar mensagens de e-mail e classificá-las automaticamente como **Spam** ou **Não Spam**, utilizando técnicas de **Machine Learning**, processamento de texto e integração com serviços de e-mail.

O sistema começou como uma aplicação simples onde o usuário digitava uma mensagem e recebia a classificação. Com a evolução do projeto, ele passou a contar com:

- dashboard;
- conexão com e-mail;
- leitura de mensagens;
- classificação automática;
- histórico de e-mails analisados;
- configurações do sistema;
- integração com Gmail API;
- suporte alternativo via IMAP.

Este projeto foi desenvolvido com fins educacionais, como parte dos estudos de **Inteligência Artificial**, **Machine Learning**, **Flask**, **Frontend Web**, **SQLite** e integração com APIs externas.

---

## 🚀 Versão Atual — 2.2.1 Local

A versão atual está preparada para execução **local**, com foco em estabilidade para demonstração acadêmica.

### Principais recursos da versão atual

- Login com Google via OAuth 2.0;
- Integração com Gmail API;
- Conexão alternativa via IMAP;
- Análise automática de e-mails;
- Classificação entre **Spam** e **Não Spam**;
- Dashboard com métricas;
- Histórico dos últimos e-mails analisados;
- Data e hora real de cada e-mail;
- Registro da última verificação feita;
- Opção de mover e-mails classificados como Spam para a pasta Spam;
- Configurações de análise;
- Notificações no frontend;
- Tema claro e escuro;
- Separação entre backend, frontend, IA, banco e serviços.

---

## 🛠️ Tecnologias Utilizadas

### Linguagem Principal

- **Python**

### Inteligência Artificial / Machine Learning

- **Scikit-learn**
- **TF-IDF**
- **Pandas**
- **Joblib**

### Backend

- **Flask**
- **Flask-CORS**
- **SQLite3**
- **python-dotenv**

### Integração com E-mail

- **Gmail API**
- **Google OAuth 2.0**
- **IMAP / imaplib**

### Frontend

- **HTML5**
- **CSS3**
- **JavaScript**

### Banco de Dados e Arquivos

- **SQLite** para armazenamento local;
- **CSV** para base de treino;
- **PKL** para modelo treinado e vetorizador;
- **JSON** para configurações locais e tokens OAuth.

### Ferramentas

- **Visual Studio Code**
- **Git**
- **GitHub**
- **Postman / Thunder Client**
- **Google Cloud Console**

---

## 📁 Estrutura do Projeto

```bash
Projeto_IA_Spam/
│
├── backend/
│   ├── app.py
│   ├── routes.py
│   ├── __init__.py
│   │
│   └── services/
│       ├── banco_services.py
│       ├── config_server.py
│       ├── dashboard_service.py
│       ├── email_services.py
│       ├── gmail_api_service.py
│       ├── ia_service.py
│       └── google_auth_service.py
│
├── database/
│   ├── criar_tabelas.py
│   └── banco.py
│
├── frontend/
│   ├── index.html
│   ├── conectar.html
│   ├── configuracoes.html
│   ├── sobre.html
│   ├── style.css
│   ├── sidebar.js
│   └── script.js
│
├── ia/
│   ├── dados.py
│   ├── modelo.py
│   ├── treino.py
│   ├── teste.py
│   ├── spam.csv
│   ├── __init__.py
│   │
│   └── modelos/
│       ├── modelo.pkl
│       └── vetorizador.pkl
│
├── .env
├── README.md
├── VERSION.md
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Configuração Inicial

### 1. Clone o repositório

```bash
git clone -b release-v2.2.1 https://github.com/K4yo-rnm/Ia-Spam-Classi.git
```

### 2. Acesse a pasta do projeto

```bash
cd Ia-Spam-Classi
```

### 3. Crie o ambiente virtual

```bash
python -m venv venv
```

### 4. Ative o ambiente virtual

No Windows:

```bash
venv\Scripts\activate
```

No Linux/Mac:

```bash
source venv/bin/activate
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

---

---

## 🔑 Configuração do Google OAuth e Gmail API

Para usar o login direto com Google, é necessário criar um projeto no **Google Cloud Console**.

### Etapas principais

1. Criar um projeto no Google Cloud;
2. Ativar a **Gmail API**;
3. Configurar a tela de consentimento OAuth;
4. Adicionar seu e-mail como usuário de teste;
5. Criar um cliente OAuth do tipo **Aplicativo da Web**;
6. Adicionar o redirect URI local:

```txt
http://127.0.0.1:5000/callback-google
```

7. Baixar o arquivo de credenciais;
8. Renomear para:

```txt
credentials.json
```

9. Colocar dentro da pasta:

```txt
backend/credentials.json
```

### Arquivos sensíveis

Estes arquivos não devem ser enviados para o GitHub:

```txt
backend/credentials.json
backend/token_google.json
credentials.json
token_google.json
*.db
```

---

## 🧠 Como Treinar o Modelo de IA

Caso seja necessário treinar novamente o modelo, execute o arquivo responsável pelo treinamento dentro da pasta `ia`.

Exemplo:

```bash
python ia/treino.py
```

Durante o treinamento, o sistema realiza:

- leitura da base em CSV;
- limpeza e normalização dos textos;
- vetorização com TF-IDF;
- treinamento do modelo;
- salvamento do modelo;
- salvamento do vetorizador.

Os arquivos gerados ficam em:

```bash
ia/modelos/modelo.pkl
ia/modelos/vetorizador.pkl
```

---

## 🚀 Como Rodar o Projeto Localmente

## 1. Instale o Venv

```bash
py -m venv venv
```

### 2. Ative o ambiente virtual

```bash
venv\Scripts\activate
```

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Inicie o backend Flask

A partir da raiz do projeto:

```bash
python backend/app.py
```

Ou, se estiver dentro da pasta `backend`:

```bash
python app.py
```

O backend será iniciado em:

```txt
http://127.0.0.1:5000
```

### 5. Abra o frontend

Abra o arquivo:

```txt
frontend/index.html
```

Ou utilize a extensão **Live Server** do VS Code.

Caso use Live Server, o frontend normalmente será aberto em:

```txt
http://127.0.0.1:5500/frontend/index.html
```

---

## 🌐 Páginas do Sistema

| Página | Função |
|---|---|
| `index.html` | Painel principal com dashboard e tabela de e-mails |
| `conectar.html` | Conexão com Google ou via IMAP |
| `configuracoes.html` | Configurações do sistema |
| `sobre.html` | Informações sobre o projeto |

---

## 📧 Formas de Conexão com E-mail

O sistema possui dois modos de conexão:

### 1. Login com Google

Método recomendado para contas Gmail.

Fluxo:

```txt
Usuário clica em Entrar com Google
↓
Google solicita autorização
↓
Backend recebe o token OAuth
↓
Sistema usa a Gmail API
↓
E-mails são analisados pela IA
```

### 2. Conexão via IMAP

Método alternativo para provedores compatíveis com IMAP.

Exemplo para Gmail:

```txt
Servidor: imap.gmail.com
Porta: 993
Senha: senha de aplicativo
```

---

## 🧪 Principais Rotas da API

### Dashboard

```http
GET /dashboard
```

Retorna totais de e-mails analisados, spam, não spam e última verificação.

### Listar e-mails analisados

```http
GET /emails
```

Retorna os últimos e-mails armazenados no banco.

### Analisar e-mails via IMAP

```http
POST /analisar-emails
```

Utiliza os dados de conexão IMAP enviados pelo frontend.

### Login com Google

```http
GET /login-google
```

Redireciona o usuário para a autenticação OAuth do Google.

### Callback do Google

```http
GET /callback-google
```

Recebe o retorno do Google OAuth e salva o token localmente.

### Status do Google

```http
GET /status-google
```

Verifica se existe token Google válido.

### Analisar e-mails via Gmail API

```http
POST /analisar-emails-google
```

Busca e analisa e-mails usando a conta Google autorizada.

### Desconectar Google

```http
POST /desconectar-google
```

Remove o token local do Google.

### Configurações

```http
GET /configuracoes
POST /configuracoes
```

Carrega e salva preferências do sistema.

---

## ✅ Funcionalidades Implementadas

- Classificação de e-mails como **Spam** ou **Não Spam**;
- Modelo de IA treinado com Scikit-learn;
- Vetorização com TF-IDF;
- Backend Flask organizado em rotas e serviços;
- Frontend com HTML, CSS e JavaScript;
- Dashboard com métricas;
- Histórico de e-mails analisados;
- Leitura de e-mails via IMAP;
- Login com Google via OAuth 2.0;
- Integração com Gmail API;
- Modo híbrido: Google API ou IMAP;
- Movimento automático de spam para a pasta Spam;
- Configuração para analisar apenas e-mails não lidos;
- Configuração de intervalo de verificação;
- Notificações;
- Tema claro e escuro;
- Registro da última verificação;
- Uso de `.env` para variáveis sensíveis.

---

## 📊 Comparação de Evolução

| Recurso | Versão 1.0 | Versão 2.0 | Versão 2.2.1 |
|---|---:|---:|---:|
| Digitar mensagem manualmente | ✅ | ✅ | ✅ |
| Classificação Spam/Não Spam | ✅ | ✅ | ✅ |
| Backend Flask | ✅ | ✅ | ✅ |
| Frontend organizado | Simples | ✅ | ✅ |
| Banco SQLite | ❌ | Parcial | ✅ |
| Dashboard | ❌ | Parcial | ✅ |
| Configurações | ❌ | ✅ | ✅ |
| Conexão IMAP | ❌ | Planejada | ✅ |
| Login com Google | ❌ | ❌ | ✅ |
| Gmail API | ❌ | ❌ | ✅ |
| Mover Spam para pasta Spam | ❌ | ❌ | ✅ |
| Tema claro/escuro | ❌ | ❌ | ✅ |
| `.env` para variáveis sensíveis | ❌ | ❌ | ✅ |

---

## 🔮 Próximas Melhorias

Algumas melhorias planejadas para futuras versões:

- Reclassificação manual de e-mails;
- Feedback do usuário para melhorar o modelo;
- Tela de detalhes do e-mail;
- Dashboard com gráficos;
- Sistema de login de usuários;
- Migração de SQLite para PostgreSQL;
- Deploy em ambiente online;
- Melhorias no modelo de IA;
- Uso de métricas de confiança da classificação;
- Melhor separação entre dados de teste e dados reais.

---

## ⚠️ Segurança e Privacidade

Este projeto lida com dados de e-mail, por isso alguns cuidados são importantes:

- Não enviar `.env` para o GitHub;
- Não enviar `credentials.json`;
- Não enviar `token_google.json`;
- Não enviar banco SQLite com e-mails reais;
- Usar apenas contas de teste durante o desenvolvimento;
- Em produção, usar HTTPS e variáveis de ambiente seguras.

---

## 📌 Status do Projeto

<p align="center">
  ✅ Projeto funcional localmente — Versão 2.2.1 ✅
</p>

A versão atual está funcionando localmente com suporte a conexão via Google/Gmail API e IMAP, permitindo análise automática de e-mails e exibição dos resultados no dashboard.

---

Projeto criado com o objetivo de estudar e aplicar conceitos de **Inteligência Artificial**, **Machine Learning**, **Flask**, **Frontend Web**, **Banco de Dados**, **OAuth**, **Gmail API** e integração entre sistemas.

---

## 📄 Licença

Este projeto é de uso educacional e pode ser melhorado, adaptado e expandido conforme a evolução do desenvolvimento.

---

## ⭐ Observação Final

Este projeto representa uma evolução prática no estudo de Inteligência Artificial aplicada ao desenvolvimento web.

A versão atual demonstra uma aplicação mais próxima de um sistema real, com integração a e-mails, classificação automática, dashboard, configurações e autenticação com Google.
