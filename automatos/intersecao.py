from .parser import AFD

def intersecao(afd1, afd2):
    novo_afd = AFD()

    # O alfabeto deve ser a união dos alfabetos
    novo_afd.alfabeto = afd1.alfabeto.union(afd2.alfabeto)
    
    estados_produto = {} 
    
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
    
    return novo_afd