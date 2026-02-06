import os
import shutil
import time
import subprocess 
from tqdm import tqdm  

def obter_tamanho_pasta(caminho):
    total = 0
    try:
        for dirpath, dirnames, filenames in os.walk(caminho):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.exists(fp):
                    total += os.path.getsize(fp)
    except Exception:
        pass
    return total

def apagar_conteudo(caminho_da_pasta):
    if not os.path.exists(caminho_da_pasta):
        print(f"\n[AVISO] Pasta não encontrada: {caminho_da_pasta}")
        return 0 
    tamanho_inicial = obter_tamanho_pasta(caminho_da_pasta)
    
    itens = os.listdir(caminho_da_pasta)
    if not itens:
        print(f"\n[INFO] A pasta {caminho_da_pasta} já está limpa.")
        return 0

    print(f"\nLimpando: {caminho_da_pasta}")
    for item in tqdm(itens, desc="Progresso", unit="arq"):
        caminho_completo = os.path.join(caminho_da_pasta, item)
        try:
            if os.path.isfile(caminho_completo) or os.path.islink(caminho_completo):
                os.unlink(caminho_completo)
            elif os.path.isdir(caminho_completo):
                shutil.rmtree(caminho_completo)
            time.sleep(0.01) 
        except Exception:
            continue

    tamanho_final = obter_tamanho_pasta(caminho_da_pasta)
    liberado = (tamanho_inicial - tamanho_final) / (1024 * 1024)
    return liberado

def menu_principal():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear') 
        print("="*35)
        print("      LIMPARDOR      ")
        print("="*35)
        print("1. Limpeza Rápida (Pastas Temp)")
        print("2. Abrir Limpeza de Disco do Windows")
        print("3. Sair")
        print("="*35)
        
        escolha = input("\nEscolha uma opção: ")

        if escolha == '1':
            pastas = [os.environ.get('TEMP'), "C:\\Windows\\Temp", "C:\\Windows\\Prefetch"]
            total_liberado = 0
            for p in pastas:
                total_liberado += apagar_conteudo(p)
            print(f"\n[SUCESSO] Você recuperou {total_liberado:.2f} MB!")
            
        elif escolha == '2':
            print("\nAbrindo ferramenta oficial da Microsoft...")
            print("Ao abrir a ferramente clique em OK e depois EXCLUIR ARQUIVOS")
            subprocess.run(["cleanmgr", "/d", "C"])
            
        elif escolha == '3':
            break
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu_principal()