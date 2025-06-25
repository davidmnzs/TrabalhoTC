from .parser import AFD

def intersecao(afd1, afd2):
    novo_afd = AFD()

    novo_afd.alfabeto = afd1.alfabeto.union(afd2.alfabeto)
    
    estados_produto = {}  # (estado1, estado2) -> nome_composto
    
    for estado1 in afd1.estados:
        for estado2 in afd2.estados:
            nome_composto = f"({estado1},{estado2})"
            estados_produto[(estado1, estado2)] = nome_composto
            novo_afd.estados.add(nome_composto)
            
            # Verificar se é estado final (ambos devem ser finais)
            if estado1 in afd1.estados_finais and estado2 in afd2.estados_finais:
                novo_afd.estados_finais.add(nome_composto)
    
    estado_inicial_par = (afd1.estado_inicial, afd2.estado_inicial)
    novo_afd.estado_inicial = estados_produto[estado_inicial_par]
    
    # Segundo passo: gerar todas as transições possíveis
    for estado1 in afd1.estados:
        for estado2 in afd2.estados:
            estado_origem = estados_produto[(estado1, estado2)]
            
            for simbolo in novo_afd.alfabeto:
                # Verificar se ambos os AFDs têm transição para este símbolo
                transicao1 = afd1.transicoes.get((estado1, simbolo))
                transicao2 = afd2.transicoes.get((estado2, simbolo))
                
                if transicao1 is not None and transicao2 is not None:
                    estado_destino = estados_produto[(transicao1, transicao2)]
                    novo_afd.transicoes[(estado_origem, simbolo)] = estado_destino
    
    # Terceiro passo: filtrar apenas estados alcançáveis usando simulação simples
    estados_alcancaveis = set()
    estados_alcancaveis.add(novo_afd.estado_inicial)
    
    # Continua adicionando estados até não encontrar mais nenhum novo
    encontrou_novos = True
    while encontrou_novos:
        encontrou_novos = False
        estados_atuais = estados_alcancaveis.copy()
        
        for estado in estados_atuais:
            for simbolo in novo_afd.alfabeto:
                if (estado, simbolo) in novo_afd.transicoes:
                    proximo_estado = novo_afd.transicoes[(estado, simbolo)]
                    if proximo_estado not in estados_alcancaveis:
                        estados_alcancaveis.add(proximo_estado)
                        encontrou_novos = True
    
    # Quarto passo: remover estados não alcançáveis
    afd_final = AFD()
    afd_final.alfabeto = novo_afd.alfabeto.copy()
    afd_final.estado_inicial = novo_afd.estado_inicial
    
    # Apenas estados alcançáveis
    afd_final.estados = estados_alcancaveis
    
    # Apenas estados finais que são alcançáveis
    afd_final.estados_finais = novo_afd.estados_finais.intersection(estados_alcancaveis)
    
    # Apenas transições entre estados alcançáveis
    for (origem, simbolo), destino in novo_afd.transicoes.items():
        if origem in estados_alcancaveis and destino in estados_alcancaveis:
            afd_final.transicoes[(origem, simbolo)] = destino
    
    return afd_final