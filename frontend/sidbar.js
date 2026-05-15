function carregarSidebar(paginaAtual) {
  const sidebar = document.getElementById("sidebar");

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
      <strong>E-mail conectado</strong>
      <p>usuario@email.com</p>
      <button>Desconectar</button>
    </div>
  `;
}
