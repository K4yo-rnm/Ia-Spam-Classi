const botao = document.getElementById("btnAnalisar");
const campoMensagem = document.getElementById("mensagem");
const divResultado = document.getElementById("resultado");

async function carregarDashboard() {
  try {
    const resposta = await fetch("http://127.0.0.1:5000/dashboard");
    const dados = await resposta.json();

    document.getElementById("total-emails").textContent = dados.emails_analisados;
    document.getElementById("spam-detectados").textContent = dados.spam_detectados;
    document.getElementById("nao-spam").textContent = dados.nao_spam;
    document.getElementById("ultima-verificacao").textContent = dados.ultima_verificacao;

  } catch (erro) {
    console.error("Erro ao carregar dashboard:", erro);
  }
}

async function carregarEmails() {
  try {
    const resposta = await fetch("http://127.0.0.1:5000/emails");
    const emails = await resposta.json();

    const lista = document.getElementById("lista-emails");
    lista.innerHTML = "";

    emails.forEach(email => {
    const linha = document.createElement("tr");

    const classificacao = email.classificacao.toUpperCase();

    const classeBadge = classificacao === "SPAM"
        ? "badge-spam"
        : "badge-nao-spam";

    linha.innerHTML = `
        <td>${email.remetente}</td>
        <td>${email.assunto}</td>
        <td><span class="${classeBadge}">${classificacao}</span></td>
        <td>${email.data_hora}</td>
    `;

    lista.appendChild(linha);
    });

  } catch (erro) {
    console.error("Erro ao carregar e-mails:", erro);
  }
}

const formConectar = document.getElementById("form-conectar");

if (formConectar) {
  formConectar.addEventListener("submit", async function(evento) {
    evento.preventDefault();

    const dados = {
      email: document.getElementById("email").value,
      senha: document.getElementById("senha").value,
      servidor: document.getElementById("servidor").value,
      porta: document.getElementById("porta").value
    };

    try {
      const resposta = await fetch("http://127.0.0.1:5000/conectar-email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(dados)
      });

      const resultado = await resposta.json();

      document.getElementById("mensagem-conexao").textContent = resultado.mensagem;

    } catch (erro) {
      console.error("Erro ao conectar e-mail:", erro);
      document.getElementById("mensagem-conexao").textContent = "Erro ao conectar e-mail.";
    }
  });
}

const btnGmail = document.getElementById("btn-gmail");
const btnOutlook = document.getElementById("btn-outlook");

if (btnGmail) {
  btnGmail.addEventListener("click", function () {
    document.getElementById("servidor").value = "imap.gmail.com";
    document.getElementById("porta").value = "993";

    btnGmail.classList.add("provedor-ativo");

    if (btnOutlook) {
      btnOutlook.classList.remove("provedor-ativo");
    }
  });
}

if (btnOutlook) {
  btnOutlook.addEventListener("click", function () {
    document.getElementById("servidor").value = "outlook.office365.com";
    document.getElementById("porta").value = "993";

    btnOutlook.classList.add("provedor-ativo");

    if (btnGmail) {
      btnGmail.classList.remove("provedor-ativo");
    }
  });
}

carregarDashboard();
carregarEmails();