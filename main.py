from automatos import carregar_afd_jff, salvar_afd_jff, reverso,intersecao
import os

def mostrar_menu():
    print("\n=== Ferramenta de Operações com AFD ===")
    print("1. Interseção de AFDs")
    print("2. Reverso de AFD")
    print("3. Sair")
    return input("Escolha uma opção: ")

def listar_arquivos_jff(pasta='arquivos'):
    """Lista todos os arquivos .jff na pasta especificada"""
    try:
        arquivos = [f for f in os.listdir(pasta) if f.endswith('.jff')]
        if not arquivos:
            print(f"Nenhum arquivo .jff encontrado na pasta '{pasta}'")
            return None
        return arquivos
    except FileNotFoundError:
        print(f"Pasta '{pasta}' não encontrada")
        return None

def selecionar_arquivo(arquivos):
    """Menu para seleção de um arquivo da lista"""
    print("\nArquivos disponíveis:")
    for i, arquivo in enumerate(arquivos, 1):
        print(f"{i}. {arquivo}")
    
    while True:
        try:
            escolha = int(input("Digite o número do arquivo: ")) - 1
            if 0 <= escolha < len(arquivos):
                return os.path.join('arquivos', arquivos[escolha])
            print("Número inválido. Tente novamente.")
        except ValueError:
            print("Entrada inválida. Digite um número.")

def executar_intersecao():
    print("\n=== Interseção de AFDs ===")
    arquivos = listar_arquivos_jff()
    if not arquivos:
        return
    
    print("\nSelecione o PRIMEIRO AFD:")
    arquivo1 = selecionar_arquivo(arquivos)
    if not arquivo1:
        return
    
    print("\nSelecione o SEGUNDO AFD:")
    arquivo2 = selecionar_arquivo(arquivos)
    if not arquivo2:
        return
    
    try:
        afd1 = carregar_afd_jff(arquivo1)
        afd2 = carregar_afd_jff(arquivo2)
        resultado = intersecao(afd1, afd2)
        
        os.makedirs('saida', exist_ok=True)
        salvar_afd_jff(resultado, 'saida/intersecao.jff')
        print("\n✓ Interseção salva em 'saida/intersecao.jff'")
    except Exception as e:
        print(f"\nErro durante a interseção: {str(e)}")

def executar_reverso():
    print("\n=== Reverso de AFD ===")
    arquivos = listar_arquivos_jff()
    if not arquivos:
        return
    
    arquivo = selecionar_arquivo(arquivos)
    if not arquivo:
        return
    
    try:
        afd = carregar_afd_jff(arquivo)
        resultado = reverso(afd)
        
        os.makedirs('saida', exist_ok=True)
        salvar_afd_jff(resultado, 'saida/reverso.jff')
        print("\n✓ Reverso salvo em 'saida/reverso.jff'")
    except Exception as e:
        print(f"\nErro durante o reverso: {str(e)}")

def main():
    # Garante que as pastas existam
    os.makedirs('arquivos', exist_ok=True)
    os.makedirs('saida', exist_ok=True)
    
    while True:
        opcao = mostrar_menu()
        
        if opcao == '1':
            executar_intersecao()
        elif opcao == '2':
            executar_reverso()
        elif opcao == '3':
            print("\nSaindo do programa...")
            break
        else:
            print("\nOpção inválida! Tente novamente.")

if __name__ == "__main__":
    main()