# 📧 Classificador de Spam com Inteligência Artificial — Versão 2.0

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange?style=for-the-badge&logo=scikitlearn" />
  <img src="https://img.shields.io/badge/SQLite-Banco%20de%20Dados-blue?style=for-the-badge&logo=sqlite" />
  <img src="https://img.shields.io/badge/Vers%C3%A3o-2.0-green?style=for-the-badge" />
</p>

<p align="center">
  Sistema web com Inteligência Artificial para classificação de mensagens como 
  <strong>Spam</strong> ou <strong>Não Spam</strong>, agora com estrutura de login, páginas adicionais e maior organização do projeto.
</p>

---

## 📌 Nome do Projeto

**IA Spam Classifier**

---

## 🎯 Objetivo do Projeto

O objetivo deste projeto é desenvolver uma aplicação web com Inteligência Artificial capaz de analisar mensagens de texto e classificá-las como **Spam** ou **Não Spam**.

Na **versão 1.0**, o sistema já permitia que o usuário digitasse uma mensagem, enviasse para o backend e recebesse a classificação feita pelo modelo de IA.

Na **versão 2.0**, o projeto evoluiu com uma estrutura mais completa, incluindo página de login, conexão, configurações, página sobre, organização do frontend e integração com backend em Flask.

Este projeto foi desenvolvido com fins educacionais, para aplicar conceitos de:

- Inteligência Artificial;
- Machine Learning;
- Processamento de texto;
- Backend com Flask;
- Frontend com HTML, CSS e JavaScript;
- Banco de dados com SQLite;
- Integração entre interface web e API.

---

## 🚀 Novidades da Versão 2.0

A versão **2.0** traz uma estrutura mais completa em relação à primeira versão do projeto.

### Principais melhorias

- Criação de página de **login**;
- Estrutura inicial para controle de acesso;
- Criação de páginas adicionais no frontend;
- Página principal mais organizada;
- Separação melhor entre backend, frontend e modelo de IA;
- Integração com banco de dados SQLite;
- Backend com Flask funcionando como API;
- Rota de previsão para classificar mensagens;
- Organização para futuras integrações com Gmail;
- Estrutura preparada para evolução do sistema.

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

### Frontend

- **HTML5**
- **CSS3**
- **JavaScript**

### Banco de Dados e Arquivos

- **SQLite** para armazenamento local;
- **CSV** para base de treino;
- **PKL** para salvar o modelo treinado;
- **JSON** para feedbacks e possíveis registros auxiliares.

### Ferramentas

- **Visual Studio Code**
- **Git**
- **GitHub**
- **Postman**
- **Navegador Web**

---

## 📁 Estrutura do Projeto

A estrutura pode variar conforme a organização local, mas o projeto segue uma base parecida com esta:

```bash
IA-Spam-Classifier/
│
├── backend/
│   ├── app.py
│   ├── config.db
│   ├── routes.py
│   ├── __init__.py
│   │   
│   └── services/
│       ├── dashboard_server.py
│       └── email.service.py
│ 
├── ia/
│   ├── modelo.py
│   ├── teste.py
│   ├── treino.py
│   ├── dados.py
│   ├── __init__.py
│   ├── spam.csv
│   │
│   └── modelos/
│       ├── modelo_adestrado.pkl
│       └── vetorizador.pkl
│   
├── database/
│   ├── banco.py
│   └── criar_tabelas.py
│   
│
├── frontend/
│   ├── index.html
│   ├── conectar.html
│   ├── configuracoes.html
│   ├── sobre.html
│   ├──  style.css
│   ├── sidbar.js
│   └── script.js
│
├── README.md
├── VERSION.md
├── requeriments.txt
└── .gitignore
```

> Observação: caso sua estrutura esteja com nomes diferentes, basta ajustar os nomes das pastas e arquivos no README.

---

## ⚙️ Como Instalar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
```

### 2. Acesse a pasta do projeto

```bash
cd nome-do-repositorio
```

### 3. Crie um ambiente virtual

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

Caso o arquivo `requirements.txt` ainda não esteja configurado, instale manualmente:

```bash
pip install flask flask-cors pandas scikit-learn joblib
```

---

## 🧠 Como Treinar o Modelo de IA

Para treinar o modelo, acesse a pasta onde está o arquivo `modelo.py` e execute:

```bash
python modelo.py
```

Durante o treinamento, o sistema realiza as seguintes etapas:

- Leitura da base de dados em CSV;
- Limpeza e normalização dos textos;
- Transformação dos textos em vetores com **TF-IDF**;
- Treinamento do modelo de Machine Learning;
- Salvamento do modelo treinado;
- Salvamento do vetorizador utilizado.

Após o treinamento, os arquivos gerados ficam na pasta de modelos:

```bash
modelos/modelo.pkl
modelos/vetorizador.pkl
```

Esses arquivos são usados pelo backend para realizar previsões sem precisar treinar o modelo toda vez que o sistema for iniciado.

---

## 🚀 Como Rodar o Backend

Acesse a pasta do backend e execute:

```bash
python app.py
```

Se tudo estiver funcionando corretamente, o terminal deverá exibir uma mensagem parecida com:

```bash
Servidor rodando em http://127.0.0.1:5000
```

O backend será responsável por:

- Receber requisições do frontend;
- Processar mensagens enviadas pelo usuário;
- Utilizar o modelo de IA treinado;
- Retornar se a mensagem é **Spam** ou **Não Spam**;
- Controlar rotas relacionadas ao sistema.

---

## 🌐 Como Abrir o Frontend

Para acessar a interface do sistema, abra a pasta `frontend` e execute o arquivo principal:

```bash
index.html
```

Também é possível abrir usando a extensão **Live Server** no Visual Studio Code.

### Páginas disponíveis na versão 2.0

- `index.html` — painel principal da aplicação;
- `conectar.html` — página para futuras conexões externas;
- `configuracoes.html` — página de configurações;
- `sobre.html` — página com informações do projeto.

---

## 🧪 Como Testar a API

A API pode ser testada usando **Postman**, **Insomnia** ou o próprio frontend.

### Rota de previsão

```http
POST /prever
```

### URL local

```http
http://127.0.0.1:5000/prever
```

### Exemplo de requisição

```json
{
  "mensagem": "Parabéns, você ganhou um prêmio exclusivo, clique agora para resgatar"
}
```

### Exemplo de resposta esperada

```json
{
  "resultado": "spam"
}
```

Outro exemplo:

```json
{
  "mensagem": "Oi, podemos marcar a reunião amanhã?"
}
```

Resposta esperada:

```json
{
  "resultado": "nao_spam"
}
```

---

## ✅ Funcionalidades da Versão 2.0

A versão **2.0** possui as seguintes funcionalidades:

- Classificação de mensagens como **Spam** ou **Não Spam**;
- Modelo de IA treinado com base de dados em CSV;
- Normalização dos textos;
- Vetorização com **TF-IDF**;
- Salvamento do modelo com **Joblib**;
- Backend desenvolvido com **Flask**;
- Integração entre backend e frontend;
- Página principal da aplicação;
- Página de configurações;
- Página sobre o projeto;
- Página de conexão para futuras integrações;
- Estrutura com banco de dados SQLite;
- Testes de API com Postman;
- Organização do projeto para publicação no GitHub.

---

## 📊 Comparação entre Versão 1.0 e Versão 2.0

| Recurso | Versão 1.0 | Versão 2.0 |
|---|---|---|
| Classificação Spam/Não Spam | ✅ | ✅ |
| Backend Flask | ✅ | ✅ |
| Frontend integrado | ✅ | ✅ |
| Modelo salvo com Joblib | ✅ | ✅ |
| Teste via Postman | ✅ | ✅ |
| Página de login | ❌ | ✅ |
| Página de configurações | ❌ | ✅ |
| Página sobre | ❌ | ✅ |
| Página de conexão | ❌ | ✅ |
| Banco SQLite | Parcial | ✅ |
| Estrutura preparada para Gmail | ❌ | ✅ |

---

## 🔮 Planejamento das Próximas Versões

### Versão 2.1

- Melhorar o visual das telas;
- Criar tela de login;
- Melhorar a responsividade do frontend;
- Exibir mensagens de erro e sucesso para o usuário;
- Melhorar a organização dos arquivos CSS e JavaScript.

### Versão 2.2

- Implementar cadastro de usuários;
- Salvar usuários no banco de dados;
- Criar autenticação com senha criptografada;
- Criar controle de sessão;
- Impedir acesso ao painel sem login.

### Versão 3.0

- Integrar o sistema com Gmail;
- Permitir conexão com uma conta de e-mail;
- Ler mensagens diretamente da caixa de entrada;
- Classificar e-mails automaticamente;
- Exibir resultados em uma tela própria.

### Versão 4.0

- Criar dashboard com gráficos;
- Exibir quantidade de mensagens analisadas;
- Mostrar quantidade de spams detectados;
- Adicionar histórico por usuário;
- Criar relatórios de análise.

### Versão 5.0

- Melhorar o modelo de IA;
- Aumentar a base de treino;
- Utilizar feedbacks dos usuários para reentreinar o modelo;
- Exibir porcentagem de confiança da previsão;
- Criar uma aplicação mais próxima de um sistema profissional.

---

## 📌 Status do Projeto

<p align="center">
  🚧 Projeto em desenvolvimento — Versão 2.0 🚧
</p>

A versão 2.0 já possui a base principal do sistema funcionando, com backend, frontend, modelo de IA, páginas adicionais e estrutura inicial de login.

---



---

## 📄 Licença

Este projeto é de uso educacional e pode ser melhorado, adaptado e expandido conforme a evolução do desenvolvimento.

---

## ⭐ Observação Final

Este projeto representa uma evolução prática no estudo de Inteligência Artificial aplicada ao desenvolvimento web.

A versão 2.0 marca uma etapa importante, pois transforma o sistema em uma aplicação mais completa, organizada e preparada para futuras integrações profissionais.
