from collections import deque

def intersecao(afd1, afd2):
    if afd1.alfabeto != afd2.alfabeto:
        raise ValueError("AFDs possuem alfabetos diferentes")
    
    novo_afd = AFD()
    novo_afd.alfabeto = afd1.alfabeto.copy()
    
    visitados = set()
    fila = deque()
    
    estado_inicial = (afd1.estado_inicial, afd2.estado_inicial)
    fila.append(estado_inicial)
    visitados.add(estado_inicial)
    novo_afd.estado_inicial = str(estado_inicial)
    
    while fila:
        (q1, q2) = fila.popleft()
        
        if q1 in afd1.estados_finais and q2 in afd2.estados_finais:
            novo_afd.estados_finais.add(str((q1, q2)))
        
        for simbolo in afd1.alfabeto:
            if (q1, simbolo) in afd1.transicoes and (q2, simbolo) in afd2.transicoes:
                novo_q1 = afd1.transicoes[(q1, simbolo)]
                novo_q2 = afd2.transicoes[(q2, simbolo)]
                novo_estado = (novo_q1, novo_q2)
                
                novo_afd.transicoes[(str((q1, q2)), simbolo)] = str(novo_estado)
                
                if novo_estado not in visitados:
                    visitados.add(novo_estado)
                    fila.append(novo_estado)
    
    novo_afd.estados = {str(estado) for estado in visitados}
    return novo_afd