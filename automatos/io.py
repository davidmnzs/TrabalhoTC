def carregar_afd(caminho):
    # Exemplo básico de leitura XML
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()

def salvar_afd(conteudo, caminho):
    # Exemplo básico de escrita
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
