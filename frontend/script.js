
const botao = document.getElementById("btnAnalisar");
const campoMensagem = document.getElementById("mensagem");
const divResultado = document.getElementById("resultado");
const btnLoginGoogle = document.getElementById("btn-login-google");

let intervaloAutomatico = null;
let analiseEmAndamento = false
let configuracoesAtuais = {};


async function carregarDashboard() {
  const totalEmails = document.getElementById("total-emails");
  const spamDetectados = document.getElementById("spam-detectados");
  const naoSpam = document.getElementById("nao-spam");
  const ultimaVerificacao = document.getElementById("ultima-verificacao");

  // Se não estiver na página do painel, não tenta carregar dashboard
  if (!totalEmails || !spamDetectados || !naoSpam || !ultimaVerificacao) {
    return;
  }

  if (!temContaConectada()) {
    limparDashboardDesconectado();
    return;
  }

  try {
    const resposta = await fetch("/dashboard");
    const dados = await resposta.json();

    console.log("Dados recebidos do dashboard:", dados);

    totalEmails.textContent = dados.emails_analisados;
    spamDetectados.textContent = dados.spam_detectados;
    naoSpam.textContent = dados.nao_spam;
    ultimaVerificacao.textContent = dados.ultima_verificacao;

  } catch (erro) {
    console.error("Erro ao carregar dashboard:", erro);
  }
}

async function carregarEmails() {
  try {
    const lista = document.getElementById("lista-emails");

    if (!lista) {
      console.warn("Tabela de e-mails não encontrada nesta página.");
      return;
    }

    if (!temContaConectada()) {
      limparDashboardDesconectado();
      return;
    }

    const resposta = await fetch("/emails");
    const emails = await resposta.json();

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
      const resposta = await fetch("/conectar-email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(dados)
      });

      const resultado = await resposta.json();

      const mensagem = document.getElementById("mensagem-conexao");
      mensagem.textContent = resultado.mensagem;

      if (resultado.status === "sucesso") {
        mensagem.style.color = "green";

        sessionStorage.setItem("emailConectado", dados.email);
        sessionStorage.setItem("senhaEmail", dados.senha);
        sessionStorage.setItem("servidorEmail", dados.servidor);
        sessionStorage.setItem("portaEmail", dados.porta);

      } else {
        mensagem.style.color = "red";
      }

      document.getElementById("mensagem-conexao").textContent = resultado.mensagem;

    } catch (erro) {
      console.error("Erro ao conectar e-mail:", erro);
      document.getElementById("mensagem-conexao").textContent = "Erro ao conectar e-mail.";
    }
  });
}

const btnGmail = document.getElementById("btn-gmail");
const btnOutlook = document.getElementById("btn-outlook");

const botaoNotificacoes = document.getElementById("btn-notificacoes");

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

if (btnLoginGoogle) {
  btnLoginGoogle.addEventListener("click", function () {
    window.location.href = "/login-google";
  });
}

async function carregarConfiguracoes() {
  const botaoSalvar = document.getElementById("salvar-configuracoes");

  if (!botaoSalvar) {
    return;
  }

  try {
    const resposta = await fetch("/configuracoes");
    const resultado = await resposta.json();

    if (resultado.status !== "sucesso") {
      console.error("Erro ao carregar configurações:", resultado);
      return;
    }

    const config = resultado.configuracoes;
    configuracoesAtuais = config;

    document.getElementById("intervalo").value = config.intervalo;
    document.getElementById("nao-lidos").checked = config.analisar_nao_lidos;
    document.getElementById("mover-spam").checked = config.mover_spam;
    document.getElementById("notificacoes").checked = config.notificacoes;
    document.getElementById("notificacao-area").checked = config.notificacao_area;
    document.getElementById("idioma").value = config.idioma;
    document.getElementById("tema").value = config.tema;

  } catch (erro) {
    console.error("Erro ao buscar configurações:", erro);
  }
}

async function salvarConfiguracoes() {
  const mensagem = document.getElementById("mensagem-configuracoes");

  const configuracoes = {
    intervalo: document.getElementById("intervalo")?.value || "5",
    analisar_nao_lidos: document.getElementById("nao-lidos")?.checked || false,
    mover_spam: document.getElementById("mover-spam")?.checked || false,
    notificacoes: document.getElementById("notificacoes")?.checked || false,
    notificacao_area: document.getElementById("notificacao-area")?.checked || false,
    idioma: document.getElementById("idioma")?.value || "pt-BR",
    tema: document.getElementById("tema")?.value || "claro"
  };

  try {
    const resposta = await fetch("/configuracoes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(configuracoes)
    });

    const resultado = await resposta.json();

    mensagem.textContent = resultado.mensagem;

    if (resultado.status === "sucesso") {
      mensagem.style.color = "green";
      configuracoesAtuais = configuracoes;
      aplicarTema(configuracoes.tema)

      if (configuracoes.notificacao_area && "Notification" in window) {
        Notification.requestPermission();
      }

    } else {
      mensagem.style.color = "red";
    }

  } catch (erro) {
    console.error("Erro ao salvar configurações:", erro);

    mensagem.textContent = "Erro ao salvar configurações.";
    mensagem.style.color = "red";
  }
}

async function analisarNovosEmails() {
  const botao = document.getElementById("btn-analisar-emails");
  const mensagem = document.getElementById("mensagem-analise");

  if (analiseEmAndamento) {
    console.log("Análise já está em andamento. Ignorando nova chamada.");
    return;
  }

  analiseEmAndamento = true;

  try {
    if (botao) {
      botao.disabled = true;
      botao.textContent = "Analisando...";
    }

    const googleConectado = sessionStorage.getItem("googleConectado") === "true";

    let url = "";
    let dados = {};

    if (googleConectado) {
      url = "/analisar-emails-google";

      dados = {
        limite: 10
      };

      if (mensagem) {
        mensagem.textContent = "Buscando e analisando e-mails pela conta Google...";
        mensagem.style.color = "#111827";
      }

    } else {
      const email = sessionStorage.getItem("emailConectado");
      const senha = sessionStorage.getItem("senhaEmail");
      const servidor = sessionStorage.getItem("servidorEmail") || "imap.gmail.com";
      const porta = sessionStorage.getItem("portaEmail") || 993;

      if (!email || !senha) {
        if (mensagem) {
          mensagem.textContent = "Nenhuma conta conectada. Conecte com Google ou configure IMAP.";
          mensagem.style.color = "red";
        }

        return;
      }

      url = "/analisar-emails";

      dados = {
        email: email,
        senha: senha,
        servidor: servidor,
        porta: porta,
        limite: 10
      };

      if (mensagem) {
        mensagem.textContent = "Buscando e analisando e-mails via IMAP...";
        mensagem.style.color = "#111827";
      }
    }

    const resposta = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(dados)
    });

    const resultado = await resposta.json();

    if (resultado.status !== "sucesso") {
      if (mensagem) {
        mensagem.textContent = resultado.mensagem || "Erro ao analisar e-mails.";
        mensagem.style.color = "red";
      }

      return;
    }

    if (mensagem) {
      mensagem.textContent =
        `Análise concluída: ${resultado.novos_analisados} novos e-mails analisados, ${resultado.repetidos_ignorados} repetidos ignorados e ${resultado.movidos_para_spam || 0} movidos para Spam.`;

      mensagem.style.color = "green";
    }

    if (typeof mostrarNotificacaoSpam === "function" && resultado.emails_analisados) {
      const emailsSpam = resultado.emails_analisados.filter(function (email) {
        return email.classificacao === "SPAM";
      });

      mostrarNotificacaoSpam(emailsSpam.length);
    }

    await carregarDashboard();
    await carregarEmails();

  } catch (erro) {
    console.error("Erro ao analisar novos e-mails:", erro);

    if (mensagem) {
      mensagem.textContent = "Erro ao analisar novos e-mails.";
      mensagem.style.color = "red";
    }

  } finally {
    analiseEmAndamento = false;

    if (botao) {
      botao.disabled = false;
      botao.textContent = "Analisar novos e-mails";
    }
  }
}

async function iniciarVerificacaoAutomatica() {
  const botaoAnalisar = document.getElementById("btn-analisar-emails");

  if (!botaoAnalisar) {
    return;
  }

  try {
    const resposta = await fetch("/configuracoes");
    const resultado = await resposta.json();

    if (resultado.status !== "sucesso") {
      console.error("Erro ao carregar configurações para verificação automática:", resultado);
      return;
    }

    const configuracoes = resultado.configuracoes;

    const intervaloMinutos = parseInt(configuracoes.intervalo || 5);

    if (intervaloAutomatico) {
      clearInterval(intervaloAutomatico);
    }

    const intervaloMilissegundos = intervaloMinutos * 60 * 1000;

    console.log(`Verificação automática ativada a cada ${intervaloMinutos} minutos.`);

    intervaloAutomatico = setInterval(function () {
      console.log("Executando verificação automática de e-mails...");
      analisarNovosEmails();
    }, intervaloMilissegundos);

  } catch (erro) {
    console.error("Erro ao iniciar verificação automática:", erro);
  }
}

function mostrarNotificacaoSpam(totalSpam) {
  if (!configuracoesAtuais.notificacoes) {
    console.log("Notificações desativadas nas configurações.");
    return;
  }

  if (!totalSpam || totalSpam <= 0) {
    return;
  }

  const titulo = "Spam detectado";
  const mensagem = `${totalSpam} e-mail(s) suspeito(s) foram encontrados.`;

  console.log(`${titulo}: ${mensagem}`);

  const botaoNotificacoes = document.getElementById("btn-notificacoes");

  if (botaoNotificacoes) {
    botaoNotificacoes.textContent = `Notificações ${totalSpam}`;
  }

  if (!configuracoesAtuais.notificacao_area) {
    return;
  }

  if (!("Notification" in window)) {
    console.warn("Este navegador não suporta notificações na área de trabalho.");
    return;
  }

  if (Notification.permission === "granted") {
    new Notification(titulo, {
      body: mensagem
    });
  } else if (Notification.permission !== "denied") {
    Notification.requestPermission().then(function (permissao) {
      if (permissao === "granted") {
        new Notification(titulo, {
          body: mensagem
        });
      }
    });
  }
}

function aplicarTema(tema) {
  if (tema === "escuro") {
    document.body.classList.add("tema-escuro");
    localStorage.setItem("tema", "escuro");
  } else {
    document.body.classList.remove("tema-escuro");
    localStorage.setItem("tema", "claro");
  }
}

function limparDashboardDesconectado() {
  const totalEmails = document.getElementById("total-emails");
  const spamDetectados = document.getElementById("spam-detectados");
  const naoSpam = document.getElementById("nao-spam");
  const ultimaVerificacao = document.getElementById("ultima-verificacao");
  const listaEmails = document.getElementById("lista-emails");
  const mensagem = document.getElementById("mensagem-analise");
  const botaoNotificacoes = document.getElementById("btn-notificacoes");

  if (totalEmails) totalEmails.textContent = "0";
  if (spamDetectados) spamDetectados.textContent = "0";
  if (naoSpam) naoSpam.textContent = "0";
  if (ultimaVerificacao) ultimaVerificacao.textContent = "Nenhuma verificação feita";

  if (listaEmails) {
    listaEmails.innerHTML = `
      <tr>
        <td colspan="4" class="tabela-vazia">
          Conecte um e-mail para visualizar as mensagens analisadas.
        </td>
      </tr>
    `;
  }

  if (mensagem) {
    mensagem.textContent = "Nenhuma conta conectada. Conecte com Google ou configure IMAP.";
    mensagem.style.color = "red";
  }

  if (botaoNotificacoes) {
    botaoNotificacoes.textContent = "Notificações 0";
  }
}

async function verificarGoogleConectado() {
  try {
    const resposta = await fetch("/status-google");
    const resultado = await resposta.json();

    return resultado.status === "sucesso" && resultado.conectado === true;

  } catch (erro) {
    console.error("Erro ao verificar conexão Google:", erro);
    return false;
  }
}

function temContaConectada() {
  const googleConectado = sessionStorage.getItem("googleConectado") === "true";
  const emailConectado = sessionStorage.getItem("emailConectado");

  return googleConectado || !!emailConectado;
}

document.addEventListener("DOMContentLoaded", function () {
  const parametros = new URLSearchParams(window.location.search);

  if (parametros.get("google") === "conectado") {
    sessionStorage.setItem("googleConectado", "true");
    window.history.replaceState({}, document.title, window.location.pathname);
  }

  const temaSalvo = localStorage.getItem("tema") || "claro";
  aplicarTema(temaSalvo);

  const botaoSalvarConfiguracoes = document.getElementById("salvar-configuracoes");
  const botaoAnalisarEmails = document.getElementById("btn-analisar-emails");

  if (botaoAnalisarEmails) {
    carregarDashboard();
    carregarEmails();
    iniciarVerificacaoAutomatica();

    botaoAnalisarEmails.addEventListener("click", analisarNovosEmails);
  }

  if (botaoSalvarConfiguracoes) {
    carregarConfiguracoes();
    botaoSalvarConfiguracoes.addEventListener("click", salvarConfiguracoes);
  }
});
