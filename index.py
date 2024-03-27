import numpy as np
import random

# Número de cidades
num_cidades = 10

# Gerar posições aleatórias para as cidades
cidades = {i: (random.uniform(0, 100), random.uniform(0, 100)) for i in range(num_cidades)}

# Função para calcular a distância total de uma rota
def calcular_distancia_total(rota):
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += np.linalg.norm(np.array(cidades[rota[i]]) - np.array(cidades[rota[i+1]]))
    # Retorna ao ponto de partida
    distancia_total += np.linalg.norm(np.array(cidades[rota[-1]]) - np.array(cidades[rota[0]]))
    return distancia_total

# Função de aptidão (quanto menor a distância, maior a aptidão)
def aptidao(rota):
    distancia = calcular_distancia_total(rota)
    return 1 / distancia

# Gerar a população inicial com rotas aleatórias
def gerar_populacao_inicial(tamanho_populacao, num_cidades):
    return [random.sample(list(cidades.keys()), num_cidades) for _ in range(tamanho_populacao)]

# Selecionar pais para reprodução baseado na aptidão
def selecionar_pais(populacao):
    return random.choices(populacao, weights=[aptidao(rota) for rota in populacao], k=2)

# Cruzamento de um ponto
def cruzamento(pai1, pai2):
    ponto = random.randint(0, len(pai1) - 1)
    filho = pai1[:ponto] + [cidade for cidade in pai2 if cidade not in pai1[:ponto]]
    return filho

# Mutação por troca de posição
def mutacao(rota, taxa_mutacao):
    rota_mutada = rota[:]
    for i in range(len(rota)):
        if random.random() < taxa_mutacao:
            j = random.randint(0, len(rota) - 1)
            rota_mutada[i], rota_mutada[j] = rota_mutada[j], rota_mutada[i]
    return rota_mutada

# Criar a nova geração
def criar_geracao(populacao, taxa_mutacao):
    nova_populacao = []
    while len(nova_populacao) < len(populacao):
        pai1, pai2 = selecionar_pais(populacao)
        filho1 = cruzamento(pai1, pai2)
        filho1 = mutacao(filho1, taxa_mutacao)
        nova_populacao.append(filho1)
    return nova_populacao

# Algoritmo genético
def algoritmo_genetico(tamanho_populacao, num_geracoes, taxa_mutacao):
    populacao = gerar_populacao_inicial(tamanho_populacao, num_cidades)
    for _ in range(num_geracoes):
        populacao = criar_geracao(populacao, taxa_mutacao)
    
    melhor_rota = min(populacao, key=calcular_distancia_total)
    return melhor_rota, calcular_distancia_total(melhor_rota)

# Configuração do algoritmo genético
tamanho_populacao = 10
num_geracoes = 100
taxa_mutacao = 0.01

# Executar o algoritmo genético
melhor_rota, distancia_melhor_rota = algoritmo_genetico(tamanho_populacao, num_geracoes, taxa_mutacao)

print(f"Melhor rota encontrada: {melhor_rota}")
print(f"Distância da melhor rota: {distancia_melhor_rota}")
