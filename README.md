# 📧 Classificador de Spam com Inteligência Artificial

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/Scikit--Learn-ML-orange?style=for-the-badge&logo=scikitlearn" />
  <img src="https://img.shields.io/badge/Status-Vers%C3%A3o%201.0-green?style=for-the-badge" />
</p>

<p align="center">
  Sistema web com Inteligência Artificial capaz de classificar mensagens como 
  <strong>Spam</strong> ou <strong>Não Spam</strong>.
</p>

---

## 📌 Nome do Projeto

**IA Spam Classifier**

Este projeto é um sistema de Inteligência Artificial desenvolvido para analisar mensagens de texto e classificá-las como **Spam** ou **Não Spam**, utilizando técnicas de Machine Learning, processamento de texto e integração com uma interface web.

---

## 🎯 Objetivo

O objetivo deste projeto é criar uma aplicação capaz de identificar mensagens com características de spam de forma simples, rápida e funcional.

Na versão **1.0**, o usuário pode digitar uma mensagem em uma interface web, enviar essa mensagem para o backend e receber como resposta a classificação feita pelo modelo de IA.

Além disso, o projeto foi estruturado para futuras melhorias, como integração com Gmail, leitura automática de e-mails e classificação de mensagens em tempo real.

---

## 🛠️ Tecnologias Usadas

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

### Frontend

- **HTML**
- **CSS**
- **JavaScript**

### Arquivos e Armazenamento

- **CSV** para base de treino
- **JSON** para armazenamento de feedback
- **PKL** para salvar o modelo treinado

### Ferramentas de Desenvolvimento

- **Visual Studio Code**
- **Git**
- **GitHub**
- **Postman**
- **Navegador Web**

---

## 📁 Estrutura do Projeto

```bash
IA-Spam-Classifier/
│
├── backend/
│   ├── app.py
│   ├── modelo.py
│   ├── teste.py
│   ├── dados_treino.csv
│   ├── feedback.json
│   │
│   └── modelos/
│       ├── modelo.pkl
│       └── vetorizador.pkl
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── README.md
└── requirements.txt
```

---

## ⚙️ Como Instalar

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

Caso ainda não tenha criado o arquivo `requirements.txt`, instale manualmente:

```bash
pip install flask flask-cors pandas scikit-learn joblib
```

---

## 🧠 Como Treinar o Modelo

Para treinar o modelo de IA, execute o arquivo responsável pelo treinamento:

```bash
python modelo.py
```

Durante esse processo, o sistema irá:

- Ler a base de dados em CSV;
- Normalizar os textos;
- Aplicar a vetorização com **TF-IDF**;
- Treinar o modelo de classificação;
- Salvar o modelo treinado na pasta `modelos`;
- Salvar também o vetorizador utilizado no treinamento.

Após o treinamento, os arquivos gerados serão:

```bash
modelos/modelo.pkl
modelos/vetorizador.pkl
```

Esses arquivos permitem que o backend utilize o modelo já treinado, sem precisar treinar tudo novamente a cada execução.

---

## 🚀 Como Rodar o Backend

Acesse a pasta onde está o arquivo principal do backend e execute:

```bash
python app.py
```

Se tudo estiver correto, o terminal deverá mostrar uma mensagem parecida com:

```bash
Servidor rodando em http://127.0.0.1:5000
```

Se der erro de modulo não encontrado, deixe o topo do `backend/app.py` assim:

``` bash
from pathlib import Path
import sys


from flask import Flask, jsonify, request
from flask_cors import CORS 

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
sys.path.append(str(RAIZ_PROJETO))

from ia.modelo import prever_texto, carregar_modelo

```

Agora ou acesse a pasta do backend ou execute no terminal:
```bash
python backend/app.py
```

O backend será responsável por receber as mensagens enviadas pelo frontend, processar a previsão com o modelo de IA e retornar o resultado para o usuário.

---

## 🌐 Como Abrir o Frontend

Para abrir o frontend, acesse a pasta `frontend` e abra o arquivo:

```bash
index.html
```

Você pode abrir diretamente no navegador ou utilizar a extensão **Live Server** no Visual Studio Code.

Com o frontend aberto, o usuário poderá:

- Digitar uma mensagem;
- Enviar a mensagem para análise;
- Receber o resultado da classificação;
- Ver se a mensagem foi classificada como **Spam** ou **Não Spam**.

---

## 🧪 Como Testar a API

A API pode ser testada usando ferramentas como **Postman**, **Insomnia** ou pelo próprio frontend.

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

Outro exemplo de requisição:

```json
{
  "mensagem": "Oi, podemos marcar a reunião para amanhã?"
}
```

Resposta esperada:

```json
{
  "resultado": "nao_spam"
}
```

---

## ✅ Funcionalidades da Versão 1.0

A versão **1.0** do projeto conta com as seguintes funcionalidades:

- Classificação de mensagens como **Spam** ou **Não Spam**;
- Treinamento do modelo com base de dados em CSV;
- Normalização dos textos antes do treinamento;
- Vetorização das mensagens com **TF-IDF**;
- Salvamento do modelo treinado com **Joblib**;
- Backend desenvolvido com **Flask**;
- Rota `/prever` para realizar classificações;
- Interface web simples, funcional e integrada ao backend;
- Testes de funcionamento da API;
- Estrutura inicial organizada para publicação no GitHub.

---

## 📊 Status do Projeto

<p align="center">
  🚧 Projeto em desenvolvimento 🚧
</p>

A versão **1.0** já possui a estrutura principal funcionando, incluindo modelo treinado, backend com Flask e frontend integrado.

---

## 👨‍💻 Autor

Desenvolvido por **Caio da Silva Braga**.

Projeto criado com o objetivo de estudar e aplicar conceitos de **Inteligência Artificial**, **Machine Learning**, **Flask**, **Frontend Web** e integração entre sistemas.

---

## 📄 Licença

Este projeto é de uso educacional e pode ser melhorado, adaptado e expandido conforme a evolução do desenvolvimento.
