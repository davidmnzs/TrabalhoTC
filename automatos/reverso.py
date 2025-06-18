from .parser import AFD  # Importação relativa corrigida
from collections import defaultdict

def reverso(afd):
    novo_afd = AFD()  # Agora usando a classe importada corretamente
    novo_afd.alfabeto = afd.alfabeto.copy()
    
    # Restante do código permanece igual...
    transicoes_rev = defaultdict(dict)
    for (origem, simbolo), destino in afd.transicoes.items():
        transicoes_rev[destino][simbolo] = origem
    
    novo_afd.estado_inicial = 'novo_inicial'
    novo_afd.estados_finais = {afd.estado_inicial}
    novo_afd.estados = afd.estados.union({novo_afd.estado_inicial})
    
    for estado, trans in transicoes_rev.items():
        for simbolo, destino in trans.items():
            novo_afd.transicoes[(estado, simbolo)] = destino
    
    for estado_final in afd.estados_finais:
        novo_afd.transicoes[(novo_afd.estado_inicial, 'ε')] = estado_final
    
    return novo_afd