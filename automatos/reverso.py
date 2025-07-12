import xml.etree.ElementTree as ET

def reverso(caminho_entrada, caminho_saida):
    tree = ET.parse(caminho_entrada)
    root = tree.getroot()

    automaton = root.find("automaton")

    estados = automaton.findall("state")
    transicoes = automaton.findall("transition")

    estado_inicial_antigo = None
    estados_finais_antigos = []

    for estado in estados:
        if estado.find("initial") is not None:
            estado_inicial_antigo = estado
        if estado.find("final") is not None:
            estados_finais_antigos.append(estado)

    if not estado_inicial_antigo:
        raise ValueError("Nenhum estado inicial encontrado.")


    novo_id = max(int(e.get("id")) for e in estados) + 1

    novo_estado = ET.Element("state", id=str(novo_id), name="NovoI")
    ET.SubElement(novo_estado, "x").text = "10.0"
    ET.SubElement(novo_estado, "y").text = "10.0"
    ET.SubElement(novo_estado, "initial")
    automaton.insert(0, novo_estado) 


    if estado_inicial_antigo.find("initial") is not None:
        estado_inicial_antigo.remove(estado_inicial_antigo.find("initial"))
    if estado_inicial_antigo.find("final") is None:
        ET.SubElement(estado_inicial_antigo, "final")

   
    for estado in estados_finais_antigos:
        if estado != estado_inicial_antigo:
            final_tag = estado.find("final")
            if final_tag is not None:
                estado.remove(final_tag)


    transicao_epsilon = ET.Element("transition")
    ET.SubElement(transicao_epsilon, "from").text = str(novo_id)
    for estado in estados_finais_antigos:
        ET.SubElement(transicao_epsilon, "to").text = estado.get("id")
    ET.SubElement(transicao_epsilon, "read") 
    automaton.append(transicao_epsilon)

    for transicao in transicoes:
        leitura = transicao.find("read")
        leitura_vazia = leitura is None or leitura.text in (None, "", "ε")

        de = transicao.find("from")
        para = transicao.find("to")

        if leitura_vazia and de.text == str(novo_id):
            continue  
        de.text, para.text = para.text, de.text

    tree.write(caminho_saida, encoding="utf-8", xml_declaration=True)
    print(f"Arquivo modificado e transições invertidas salvo em: {caminho_saida}")