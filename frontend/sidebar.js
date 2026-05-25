

function carregarSidebar(paginaAtual) {
  const sidebar = document.getElementById("sidebar");

  if (!sidebar) {
    console.error("Elemento #sidebar não encontrado");
    return;
  }

  const googleConectado = sessionStorage.getItem("googleConectado") === "true";
  const emailConectado = sessionStorage.getItem("emailConectado");

  let tituloStatus = "Nenhum e-mail conectado";
  let textoStatus = "Conecte uma conta para analisar mensagens.";
  let mostrarBotaoDesconectar = false;

  if (googleConectado) {
    tituloStatus = "Google conectado";
    textoStatus = "Conta Google autorizada";
    mostrarBotaoDesconectar = true;
  } else if (emailConectado) {
    tituloStatus = "E-mail conectado";
    textoStatus = emailConectado;
    mostrarBotaoDesconectar = true;
  }

  sidebar.innerHTML = `
    <div>
      <div class="logo">
        <h2>Classificador de E-mails</h2>
        <p>Spam ou Não Spam</p>
      </div>

      <nav>
        <a href="index.html" class="${paginaAtual === 'painel' ? 'active' : ''}">
          Painel Principal
        </a>

        <a href="conectar.html" class="${paginaAtual === 'conectar' ? 'active' : ''}">
          Conectar E-mail
        </a>

        <a href="configuracoes.html" class="${paginaAtual === 'configuracoes' ? 'active' : ''}">
          Configurações
        </a>

        <a href="sobre.html" class="${paginaAtual === 'sobre' ? 'active' : ''}">
          Sobre o Projeto
        </a>
      </nav>
    </div>

    <div class="status-email">
      <strong>${tituloStatus}</strong>
      <p>${textoStatus}</p>
      ${mostrarBotaoDesconectar ? '<button id="btn-desconectar">Desconectar</button>' : ""}
    </div>
  `;

  const btnDesconectar = document.getElementById("btn-desconectar");

  if (btnDesconectar) {
    btnDesconectar.addEventListener("click", async function () {
      sessionStorage.removeItem("googleConectado");

      sessionStorage.removeItem("emailConectado");
      sessionStorage.removeItem("senhaEmail");
      sessionStorage.removeItem("servidorEmail");
      sessionStorage.removeItem("portaEmail");

      try {
        await fetch("/desconectar-google", {
          method: "POST"
        });
      } catch (erro) {
        console.error("Erro ao desconectar Google:", erro);
      }

      window.location.href = "index.html";
    });
  }
}
