const botao = document.getElementById("btnAnalisar");
const campoMensagem = document.getElementById("mensagem");
const divResultado = document.getElementById("resultado");

botao.addEventListener("click", async () => {
    const texto = campoMensagem.value.trim();

    if (texto === "") {
        divResultado.textContent = "Digite uma mensagem antes de analisar.";
        divResultado.className = "resultado aviso";
        return;
    }

    try {
        divResultado.textContent = "Analisando...";
        divResultado.className = "resultado";

        const resposta = await fetch("http://127.0.0.1:5000/prever", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                texto: texto
            })
        });

        const dados = await resposta.json();

        if (!resposta.ok) {
            divResultado.textContent = dados.erro || "Erro ao analisar mensagem.";
            divResultado.className = "resultado erro";
            return;
        }

        if (dados.resultado === "spam") {
            divResultado.textContent = "Resultado: SPAM";
            divResultado.className = "resultado spam";
        } else {
            divResultado.textContent = "Resultado: NÃO SPAM";
            divResultado.className = "resultado nao-spam";
        }

    } catch (erro) {
        console.error("Erro:", erro);
        divResultado.textContent = "Erro ao conectar com o backend.";
        divResultado.className = "resultado erro";
    }
});