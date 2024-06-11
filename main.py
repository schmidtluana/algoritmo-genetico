import random
import numpy as np
import math


CIDADES = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

CIDADES_X = [0.77687122, 0.55726533, 0.65639441, 0.60439895, 0.10984792, 
            0.30681839, 0.03642046, 0.50750194, 0.79819788, 0.79896875,
            0.14326940, 0.07110193, 0.72613150, 0.22624105, 0.62480412, 
            0.54832279, 0.39699388, 0.07545496, 0.67595097, 0.07429705]

CIDADES_Y = [0.27943920, 0.11661366, 0.39053913, 0.66616904, 0.69857584,
            0.20730006, 0.50247213, 0.07393869, 0.67991802, 0.39749278,
            0.14151256, 0.12773617, 0.37197290, 0.69033435, 0.91890348,
            0.52333815, 0.42525695, 0.37166915, 0.99033329, 0.15694232]

NUMERO_INDIVIDUOS = 20
NUMERO_GERACOES = 100

# Valores utilizado para calcular a função de aptidão
max = sum(d for d in range(1, NUMERO_INDIVIDUOS + 1))
# Para não precisarmos calular as probabilidades todas as vezes, a lista será ordenada ao invés de alterar o cálculo de prob.
probabilidades = [(NUMERO_INDIVIDUOS - d)/max for d in range(0, NUMERO_INDIVIDUOS)] 



def main():

  individuos = inicializarIndividuos()

  for _ in range(NUMERO_GERACOES):

    individuos = gerarNovaGeracao(individuos, calcularDistancias(individuos))

    print(individuos)

  distancias_finais = calcularDistancias(individuos)
  distancias_finais.sort(key= lambda dist : dist[1])

  print(distancias_finais)

  print(f"Melhor caminho: {individuos[0]}, distancia do caminho: {distancias_finais[0][1]}")

def inicializarIndividuos():
  
  individuos = []

  for _ in range(NUMERO_INDIVIDUOS):
    random.shuffle(CIDADES)
    individuos.append(CIDADES.copy())

  return individuos

def calcularDistancias(individuos: list):

  distancias_totais = []

  # Os indivíduos possuem uma lista com a ordem das cidades
  for [index_ind, individuo] in enumerate(individuos):
    distancia = 0
    for index_cid in range(len(individuos[index_ind])):
      if index_cid != 0:
        
        # Ambos os indexes tem seu valor por conta da lista começar em 1 e não 0
        cidade_atual = CIDADES[individuo[index_cid] - 1]
        cidade_anterior = CIDADES[individuo[index_cid - 1] - 1]

        # Para calcular a distancia entre dois pontos num plano:
        # d = √(x1 - x2)²  + (y1 - y2)²
        distancia += math.sqrt(math.pow(CIDADES_X[cidade_atual - 1] - CIDADES_X[cidade_anterior - 1], 2) + math.pow(CIDADES_Y[cidade_atual - 1] - CIDADES_Y[cidade_anterior - 1], 2))

    distancias_totais.append((index_ind, distancia))

  return distancias_totais


def gerarNovaGeracao(individuos: list, distancias: list):

  # Ordena a lista de distancias
  distancias.sort(key= lambda dist : dist[1])

  novos_individuos = []

  for _ in range(NUMERO_INDIVIDUOS):  
    novos_individuos.append(gerarFilho(escolherPais(individuos, distancias)))

  return novos_individuos

def gerarFilho(pais):

  filho = []

  for cidade in pais[0]:
    filho.append(cidade) if np.random.choice([0,1]) == 1 else filho.append(None)

  cidades_faltando = list(filter(lambda c : (not c in filho), CIDADES))

  for [index, cidade] in enumerate(filho):
    if cidade == None:
      filho[index] = encontrarPrimeiraCidadeFaltando(cidades_faltando, pais[1])

  return gerarMutacao(filho)

def escolherPais(individuos: list, distancias: list):

  # O calculo de peso se dará da seguinte forma:
  # Peso dos itens:
  #  0 -> 20
  #  1 -> 19 ...
  # 19 -> 1

  # Será escolhido um valor com base na lista ordenada de distâncias.
  # Utilizamos esse valor para retornar o objeto completo do indivíduo

  index_pai1 = distancias[np.random.choice(len(individuos), p=probabilidades)][0]
  
  # Garante que os dois pais não serão o mesmo
  while True:
    index_pai2 = distancias[np.random.choice(len(individuos), p=probabilidades)][0]
    if index_pai1 != index_pai2:
      break

  return (individuos[index_pai1], individuos[index_pai2])

def gerarMutacao(individuo: list):

  chance_mutacao = random.choice(range(0,10))

  if (chance_mutacao != 0):
    return individuo
  
  cidade1 = random.choice(CIDADES)
  cidade2 = random.choice(CIDADES)

  index_cidade1 = individuo.index(cidade1)
  index_cidade2 = individuo.index(cidade2)

  individuo[index_cidade1] = cidade2
  individuo[index_cidade2] = cidade1

  return individuo


def encontrarPrimeiraCidadeFaltando(cidades_faltando, pai):
  for cidade in pai:
    if cidade in cidades_faltando:
      cidades_faltando.remove(cidade)
      return cidade

if __name__ == '__main__':
  main()