# Lista de selos abreviados
selos_disponiveis = {
    "PAS": "Pássaro",
    "JAV": "Javali",
    "CAO": "Cão",
    "DRA": "Dragão",
    "BOI": "Boi",
    "TIG": "Tigre",
    "COB": "Cobra",
    "RAT": "Rato",
    "CAV": "Cavalo",
    "MAC": "Macaco",
    "COE": "Coelho",
    "CAR": "Carneiro"
}

# Base de jutsus
jutsus = {
    "Goukakyuu no Jutsu": ["COB", "BOI", "MAC", "TIG"],
    "Suiton Suiryuudan": ["BOI", "MAC", "RAT", "TIG", "CAO"],
    "Doton Doryuuheki": ["TIG", "COE", "BOI", "CAO"],
    "Kage Mane no Jutsu": ["RAT", "COB", "TIG"],
    "Chidori": ["BOI", "COE", "MAC"]
}

# Monta a tabela dinâmica
def construir_afnd(base_jutsus):
    tabela_transicoes = {}
    estados_finais = {}

    for nome_jutsu, sequencia_selos in base_jutsus.items():
        for indice, selo in enumerate(sequencia_selos):
            estado_atual = (nome_jutsu, indice)
            proximo_estado = (nome_jutsu, indice + 1)

            if (estado_atual, selo) not in tabela_transicoes:
                tabela_transicoes[(estado_atual, selo)] = set()

            tabela_transicoes[(estado_atual, selo)].add(proximo_estado)

        estados_finais[(nome_jutsu, len(sequencia_selos))] = nome_jutsu

    return tabela_transicoes, estados_finais

# Identifica o jutsu
def identificar_jutsu(selos_informados, base_jutsus):
    tabela_transicoes, estados_finais = construir_afnd(base_jutsus)

    estados_atuais = set((nome_jutsu, 0) for nome_jutsu in base_jutsus)

    for selo in selos_informados:
        proximos_estados = set()

        for estado in estados_atuais:
            if (estado, selo) in tabela_transicoes:
                proximos_estados.update(tabela_transicoes[(estado, selo)])

        estados_atuais = proximos_estados

        if not estados_atuais:
            raise ValueError("Erro: sequência de selos não corresponde a nenhum jutsu.")

    jutsus_reconhecidos = []

    for estado in estados_atuais:
        if estado in estados_finais:
            jutsus_reconhecidos.append(estados_finais[estado])

    if not jutsus_reconhecidos:
        raise ValueError("Erro: sequência incompleta ou inválida para um jutsu.")

    return jutsus_reconhecidos

# Mostra os selos
print("Selos disponíveis:")
for sigla, nome in selos_disponiveis.items():
    print(f"{sigla} - {nome}")

try:
    # Lê a entrada
    entrada = input("\nDigite os selos separados por espaço: ").upper().strip()
    sequencia_digitada = entrada.split()

    # Valida os selos
    for selo in sequencia_digitada:
        if selo not in selos_disponiveis:
            raise ValueError(f"Erro: selo inválido informado -> {selo}")

    # Executa o AFND
    resultado = identificar_jutsu(sequencia_digitada, jutsus)

    # Mostra o resultado
    print("\nJutsu identificado:")
    for jutsu in resultado:
        print(jutsu)

except ValueError as erro:
    print(f"\n{erro}")
