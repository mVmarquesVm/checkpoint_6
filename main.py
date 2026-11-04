# Checkpoint 6 - Pensamento Computacional com Python
# Sistema de Triagem de Chamados de TI
#
# O programa lê os chamados do arquivo dados/chamados.json, decide a
# prioridade de cada um com uma árvore de decisão e mostra dois menus:
# 1 Painel de métricas
# 2 Fila de atendimento

import json

ARQUIVO_CHAMADOS = "dados/chamados.json"

# Tipos de problema que costumam parar muita gente de uma vez
TIPOS_CRITICOS = ["Sistema", "Rede"]

NOMES_PRIORIDADE = {
    1: "P1 - Crítica",
    2: "P2 - Alta",
    3: "P3 - Média",
    4: "P4 - Baixa",
}


# leitura dos dados

def carregar_chamados():
    arquivo = open(ARQUIVO_CHAMADOS, "r", encoding="utf-8")
    chamados = json.load(arquivo)
    arquivo.close()
    return chamados


# árvore de decisão
# AVISO, A ÁRVORE DE DECISÃO COMENTADA FOI FEITA EM IA!!!
def arvore_de_decisao(chamado):
    # Faz as perguntas da árvore e devolve o nível de prioridade
    # e o motivo (o caminho que o chamado fez na árvore)
    #
    # impacto == alto?
    # ├─ sim: tipo é Sistema ou Rede?
    # │   ├─ sim -> P1 Crítica
    # │   └─ não: usuários >= 15?
    # │       ├─ sim -> P1 Crítica
    # │       └─ não -> P2 Alta
    # └─ não: impacto == medio?
    #     ├─ sim: usuários >= 10?
    #     │   ├─ sim -> P2 Alta
    #     │   └─ não -> P3 Média
    #     └─ não -> P4 Baixa
    impacto = chamado["impacto"]
    tipo = chamado["tipo"]
    usuarios = chamado["usuarios_afetados"]

    if impacto == "alto":
        if tipo in TIPOS_CRITICOS:
            return 1, "impacto alto e tipo " + tipo
        elif usuarios >= 15:
            return 1, f"impacto alto e {usuarios} usuários afetados"
        else:
            return 2, f"impacto alto, mas só {usuarios} usuários afetados"
    elif impacto == "medio":
        if usuarios >= 10:
            return 2, f"impacto médio e {usuarios} usuários afetados"
        else:
            return 3, f"impacto médio e {usuarios} usuário(s) afetado(s)"
    else:
        return 4, "impacto baixo"


def classificar_chamados(chamados):
    # Passa cada chamado pela árvore e guarda o resultado no próprio chamado
    for chamado in chamados:
        nivel, motivo = arvore_de_decisao(chamado)
        chamado["prioridade"] = nivel
        chamado["motivo"] = motivo


# fila de atendimento

def vem_antes(a, b):
    # Diz se o chamado a deve ser atendido antes do chamado b
    if a["prioridade"] != b["prioridade"]:
        return a["prioridade"] < b["prioridade"]

    if a["usuarios_afetados"] != b["usuarios_afetados"]:
        return a["usuarios_afetados"] > b["usuarios_afetados"]

    if len(a["setores_afetados"]) != len(b["setores_afetados"]):
        return len(a["setores_afetados"]) > len(b["setores_afetados"])

    abertura_a = a["data_abertura"] + " " + a["hora_abertura"]
    abertura_b = b["data_abertura"] + " " + b["hora_abertura"]
    return abertura_a < abertura_b


def montar_fila(chamados):

    fila = []
    for chamado in chamados:
        fila.append(chamado)

    for i in range(len(fila)):
        for j in range(len(fila) - 1 - i):
            if vem_antes(fila[j + 1], fila[j]):
                fila[j], fila[j + 1] = fila[j + 1], fila[j]

    return fila


# métricas

def contar_por_campo(chamados, campo):

    contagem = {}
    for chamado in chamados:
        valor = chamado[campo]
        if valor in contagem:
            contagem[valor] = contagem[valor] + 1
        else:
            contagem[valor] = 1
    return contagem


def calcular_metricas(chamados):
    total_usuarios = 0
    tempo_total = 0
    for chamado in chamados:
        total_usuarios = total_usuarios + chamado["usuarios_afetados"]
        tempo_total = tempo_total + chamado["tempo_estimado_min"]

    if len(chamados) > 0:
        tempo_medio = tempo_total / len(chamados)
    else:
        tempo_medio = 0

    metricas = {
        "total_chamados": len(chamados),
        "total_usuarios": total_usuarios,
        "por_impacto": contar_por_campo(chamados, "impacto"),
        "por_tipo": contar_por_campo(chamados, "tipo"),
        "tempo_total": tempo_total,
        "tempo_medio": tempo_medio,
    }
    return metricas


# telas

def mostrar_menu():
    print()
    print("=== TRIAGEM DE CHAMADOS DE TI ===")
    print("1 - Painel de métricas")
    print("2 - Fila de atendimento")
    print("0 - Sair")


def mostrar_painel(chamados):
    metricas = calcular_metricas(chamados)

    print()
    print("===== PAINEL DE MÉTRICAS =====")
    print("Total de chamados:", metricas["total_chamados"])
    print("Total de usuários afetados:", metricas["total_usuarios"])
    print("Tempo médio estimado:", round(metricas["tempo_medio"], 1), "min")
    print("Tempo total estimado:", metricas["tempo_total"], "min")

    print()
    print("Chamados por impacto:")
    for impacto in ["alto", "medio", "baixo"]:
        if impacto in metricas["por_impacto"]:
            print("-", impacto + ":", metricas["por_impacto"][impacto])
        else:
            print("-", impacto + ":", 0)

    print()
    print("Chamados por tipo:")
    for tipo in metricas["por_tipo"]:
        print("-", tipo + ":", metricas["por_tipo"][tipo])


def mostrar_fila(chamados):
    fila = montar_fila(chamados)

    if len(fila) == 0:
        print("Nenhum chamado na fila.")
        return

    proximo = fila[0]
    print()
    print("===== PRÓXIMO CHAMADO A SER ATENDIDO =====")
    print("ID:", proximo["id"])
    print("Título:", proximo["titulo"])
    print("Tipo:", proximo["tipo"])
    print("Prioridade:", NOMES_PRIORIDADE[proximo["prioridade"]])
    print("Motivo:", proximo["motivo"])
    print("Usuários afetados:", proximo["usuarios_afetados"])
    print("Setores afetados:", len(proximo["setores_afetados"]))
    print("Aberto em:", proximo["data_abertura"], "às", proximo["hora_abertura"])

    print()
    print("===== DEMAIS CHAMADOS NA ORDEM DE ATENDIMENTO =====")
    posicao = 2
    for chamado in fila[1:]:
        print(f"{posicao}º - ID {chamado['id']} | P{chamado['prioridade']} | "
              f"{chamado['tipo']} | {chamado['titulo']} | "
              f"{chamado['usuarios_afetados']} usuário(s), "
              f"{len(chamado['setores_afetados'])} setor(es)")
        posicao = posicao + 1


# programa principal

def main():
    try:
        chamados = carregar_chamados()
    except FileNotFoundError:
        print("Arquivo não encontrado:", ARQUIVO_CHAMADOS)
        print("Execute o programa dentro da pasta do projeto.")
        return
    except json.JSONDecodeError:
        print("O arquivo chamados.json não está em um formato JSON válido.")
        return

    classificar_chamados(chamados)

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            mostrar_painel(chamados)
        elif opcao == "2":
            mostrar_fila(chamados)
        elif opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Digite 1, 2 ou 0.")


if __name__ == "__main__":
    main()
