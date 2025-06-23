from .parser import AFD

def intersecao(afd1, afd2):
    novo_afd = AFD()
    
    # O alfabeto da interseção é a interseção dos alfabetos
    novo_afd.alfabeto = afd1.alfabeto.intersection(afd2.alfabeto)
    
    # Mapear estados para facilitar a criação dos nomes compostos
    estados_visitados = set()
    fila = []
    mapeamento_estados = {}
    
    # Estado inicial é o par (q0_1, q0_2)
    estado_inicial_composto = f"({afd1.estado_inicial},{afd2.estado_inicial})"
    novo_afd.estado_inicial = estado_inicial_composto
    novo_afd.estados.add(estado_inicial_composto)
    
    # Inicializar a busca
    fila.append((afd1.estado_inicial, afd2.estado_inicial))
    mapeamento_estados[(afd1.estado_inicial, afd2.estado_inicial)] = estado_inicial_composto
    
    # BFS para gerar todos os estados alcançáveis
    while fila:
        estado1, estado2 = fila.pop(0)
        par_atual = (estado1, estado2)
        
        if par_atual in estados_visitados:
            continue
            
        estados_visitados.add(par_atual)
        estado_atual_nome = mapeamento_estados[par_atual]
        
        # Verificar se é estado final (ambos devem ser finais)
        if estado1 in afd1.estados_finais and estado2 in afd2.estados_finais:
            novo_afd.estados_finais.add(estado_atual_nome)
        
        # Processar transições para cada símbolo do alfabeto comum
        for simbolo in novo_afd.alfabeto:
            # Verificar se ambos os AFDs têm transição para este símbolo
            transicao1 = afd1.transicoes.get((estado1, simbolo))
            transicao2 = afd2.transicoes.get((estado2, simbolo))
            
            if transicao1 is not None and transicao2 is not None:
                # Criar estado destino composto
                par_destino = (transicao1, transicao2)
                
                if par_destino not in mapeamento_estados:
                    nome_destino = f"({transicao1},{transicao2})"
                    mapeamento_estados[par_destino] = nome_destino
                    novo_afd.estados.add(nome_destino)
                    fila.append(par_destino)
                
                nome_destino = mapeamento_estados[par_destino]
                
                # Adicionar transição
                novo_afd.transicoes[(estado_atual_nome, simbolo)] = nome_destino
    
    return novo_afd