from ia.modelo import prever_texto, carregar_modelo


modelo, vetorizador = carregar_modelo()


def padronizar_classificacao(classificacao):
    classificacao = classificacao.strip().lower()

    if classificacao in ["spam", "spams"]:
        return "SPAM"

    if classificacao in [
        "nao spam",
        "não spam",
        "nao_spam",
        "não_spam",
        "ham",
        "normal"
    ]:
        return "NÃO SPAM"

    return classificacao.upper()


def classificar_email(remetente, assunto, conteudo):
    texto_final = remetente + " " + assunto + " " + conteudo

    classificacao = prever_texto(texto_final, modelo, vetorizador)
    classificacao = padronizar_classificacao(classificacao)

    return classificacao