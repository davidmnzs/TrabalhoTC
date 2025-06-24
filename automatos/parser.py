import xml.etree.ElementTree as ET

class AFD:
    def __init__(self):
        self.estados = set()
        self.alfabeto = set()
        self.transicoes = dict()  # (estado, simbolo) -> estado
        self.estado_inicial = None
        self.estados_finais = set()
    
    # (Mantenha as funções carregar_afd_jff e salvar_afd_jff aqui)

def carregar_afd_jff(arquivo):
    afd = AFD()
    tree = ET.parse(arquivo)
    root = tree.getroot()

    id_para_nome = {}
    
    for state in root.findall('automaton/state'):
        id_ = state.get('id')
        nome = state.get('name')
        id_para_nome[id_] = nome
        afd.estados.add(nome)
        
        if state.find('initial') is not None:
            afd.estado_inicial = nome
        if state.find('final') is not None:
            afd.estados_finais.add(nome)
    
    for trans in root.findall('automaton/transition'):
        origem_id = trans.find('from').text
        destino_id = trans.find('to').text
        simbolo = trans.find('read').text or ''
        
        origem = id_para_nome[origem_id]
        destino = id_para_nome[destino_id]
        
        if simbolo != '':
            afd.alfabeto.add(simbolo)
        
        afd.transicoes[(origem, simbolo)] = destino
    
    return afd

def salvar_afd_jff(afd, arquivo):
    """Salva um AFD no formato JFF exatamente como o JFLAP exporta"""
    import xml.etree.ElementTree as ET
    
    # Cria a estrutura do XML
    root = ET.Element('structure')
    
    # Adiciona o tipo
    tipo = ET.SubElement(root, 'type')
    tipo.text = 'fa'
    
    automaton = ET.SubElement(root, 'automaton')
    
    # Adiciona estados com coordenadas separadas
    estados_ordenados = sorted(afd.estados)
    coordenadas = {
        'x': 100.0,
        'y': 100.0
    }
    
    for i, estado in enumerate(estados_ordenados):
        state = ET.SubElement(automaton, 'state', {
            'id': str(i),
            'name': estado
        })
        
        # Coordenadas como elementos separados
        x_elem = ET.SubElement(state, 'x')
        x_elem.text = str(coordenadas['x'])
        y_elem = ET.SubElement(state, 'y')
        y_elem.text = str(coordenadas['y'])
        
        if estado == afd.estado_inicial:
            ET.SubElement(state, 'initial')
        if estado in afd.estados_finais:
            ET.SubElement(state, 'final')
        
        # Atualiza coordenadas para o próximo estado
        coordenadas['x'] += 100.0
        if i % 3 == 0:  # Quebra linha a cada 3 estados
            coordenadas['x'] = 100.0
            coordenadas['y'] += 100.0
    
    # Mapeia nomes de estados para IDs numéricos
    estado_para_id = {estado: str(i) for i, estado in enumerate(estados_ordenados)}
    
    # Adiciona transições
    for (origem, simbolo), destino in sorted(afd.transicoes.items()):
        transition = ET.SubElement(automaton, 'transition')
        
        from_elem = ET.SubElement(transition, 'from')
        from_elem.text = estado_para_id[origem]
        
        to_elem = ET.SubElement(transition, 'to')
        to_elem.text = estado_para_id[destino]
        
        read_elem = ET.SubElement(transition, 'read')
        read_elem.text = simbolo
    
    # Gera o XML com formatação
    xml_str = ET.tostring(root, encoding='UTF-8')
    
    # Processa para adicionar formatação e comentários
    xml_final = b'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    xml_final += b'<!--Created with AFD Tool-->\n'
    xml_final += xml_str.replace(b'<automaton>', b'<automaton>\n\t\t<!--The list of states.-->')
    xml_final = xml_final.replace(b'</state>', b'</state>\n\t\t')
    xml_final = xml_final.replace(b'<transition>', b'\t\t<!--The list of transitions.-->\n\t\t<transition>')
    xml_final = xml_final.replace(b'</transition>', b'</transition>\n\t\t')
    xml_final = xml_final.replace(b'</automaton>', b'\t</automaton>')
    xml_final = xml_final.replace(b'&#13;', b'')  # Remove &#13; se existir
    
    # Escreve no arquivo
    with open(arquivo, 'wb') as f:
        f.write(xml_final)