import random
import matplotlib.pyplot as plt
import configparser
import logging
import pickle
import numpy as np



# Configurações de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Função para gerar uma população inicial
def generate_population(size, num_meses, receita_total, custos_totais):
    population = []

    with open('population_z', 'rb') as f:
        population = pickle.load(f)
    if len(population) > 0:
        return population


    max_perc_fixa = 0.30
    max_perc_variavel = 0.70

    for _ in range(size):
        individual = []
        for _ in range(num_meses):
            perc_fixa = random.uniform(0.25, max_perc_fixa)
            perc_variavel = random.uniform(0.45, max_perc_variavel)
            perc_tesouro = 1 - perc_fixa - perc_variavel
            individual.append((receita_total, custos_totais, perc_fixa, perc_variavel, perc_tesouro))
        population.append(individual)
    with open('population_z', 'wb') as f:
        pickle.dump(population, f)
    return population


# Função para avaliar o plano financeiro
def eval_plano(plano, renda_total, risco_renda_fixa, risco_renda_variavel, risco_tesouro, custo_total):
    total_reserva = 0
    total_receita = 0
    total_gastos = 0
    total_renda_fixa = 0
    total_renda_variavel = 0
    total_tesouro = 0
    total_valor_aplicado = 0
    total_retorno_aplicado = 0

    for mes in plano:
        _, _, valor_fixo, valor_variavel, valor_tesouro = mes
        reserva_percentual = 0.12 #random.uniform(0.12, max_reserva)
        reserva_total = reserva_percentual * (renda_total - custo_total)
        valor_disponivel = renda_total - custo_total - reserva_total

        # if valor_disponivel < 0:
        #     return float('-inf')  # Penalidade alta se os gastos e reserva excederem a receita

        perc_fixa = random.uniform(0, 0.45)
        perc_variavel = random.uniform(0, 0.35)
        perc_tesouro = 1 - perc_fixa - perc_variavel

        renda_fixa = valor_disponivel * perc_fixa
        renda_variavel = valor_disponivel * perc_variavel
        tesouro = valor_disponivel * perc_tesouro

        renda_fixa *= (1 + random.gauss(0, risco_renda_fixa))
        renda_variavel *= (1 + random.gauss(0, risco_renda_variavel))
        tesouro *= (1 + random.gauss(0, risco_tesouro))

        reserva_total = renda_fixa + renda_variavel + tesouro

        total_reserva += reserva_total
        total_gastos += custo_total
        total_renda_fixa += renda_fixa
        total_renda_variavel += renda_variavel
        total_tesouro += tesouro
        total_receita += renda_total
        total_valor_aplicado += valor_disponivel
        total_retorno_aplicado += reserva_total - valor_disponivel

    for _ in range(random.randint(1, 3)):
        emergencia = random.uniform(0.1, 0.3) * total_reserva
        # if emergencia > total_reserva:
        #     return float('-inf')  # Penalidade alta se a reserva não for suficiente
        total_reserva -= emergencia

    # if total_reserva < meta_reserva:
    #     return float('-inf')  # Penalidade baixa

    return total_reserva, total_receita, total_gastos, total_renda_fixa, total_renda_variavel, total_tesouro, total_valor_aplicado, total_retorno_aplicado, \
           plano


def fitness(individual):
    return individual[0]


# Função para o crossover
def crossover_positions(parent1, parent2):
    # Verifica se ambos os pais têm o mesmo número de meses (tuplas)
    if len(parent1) != len(parent2):
        raise ValueError("parent1 e parent2 devem ter o mesmo comprimento")

    # Cria novos pais para armazenar o resultado do crossover
    child1 = []
    child2 = []

    for (p1, p2) in zip(parent1, parent2):
        # Desempacota as tuplas
        p1_values = list(p1)
        p2_values = list(p2)

        # Troca as posições 4 apenas (renda variavel)
        p1_values[2], p1_values[3],  p1_values[4] = p1_values[4], p1_values[2],  p1_values[3]
        p2_values[2], p2_values[3],  p2_values[4] = p2_values[4], p2_values[2],  p2_values[3]


        p1_values[2], p2_values[2] = p2_values[2], p1_values[2]
        # p1_values[3], p2_values[3] = p2_values[3], p1_values[3]
        p1_values[4] = 1 - p1_values[2] - p1_values[3] #ajustar os 100%
        p2_values[4] = 1 - p2_values[2] - p2_values[3] #ajustar os 100%
        # Adiciona as novas tuplas aos filhos
        child1.append(tuple(p1_values))
        child2.append(tuple(p2_values))

    return child1, child2




def plot_reserve_totals(top_individuals):
    # Extraímos as gerações e os totais de reserva dos top_individuals
    generations = [ind[0] for ind in top_individuals]  # Primeiro valor da tupla
    reserve_totals = [ind[1] for ind in top_individuals]  # Segundo valor da tupla

    plt.figure(figsize=(10, 4))
    plt.plot(generations, reserve_totals, marker='x')
    plt.title('Reservas Totais por Geração')
    plt.xlabel('Geração')
    plt.ylabel('Reserva Total (R$)')
    plt.grid(True)

    # Adiciona anotações para cada ponto
    # min_reserve_total = min(reserve_totals)
    # max_reserve_total = max(reserve_totals)
    # plt.xlim(min_reserve_total - (min_reserve_total % 20), max_reserve_total + (20 - max_reserve_total % 20))
    #
    # Configurar ticks no eixo y em incrementos de 100
    #plt.yticks(range(int(plt.ylim()[0]), int(plt.ylim()[1]) + 1, 100))

    plt.show()


def process_best_individuals_history(best_individuals_history):
    generations = []
    for gen, reserva_total in best_individuals_history:
        generations.append((gen, reserva_total[0]))
    return generations
# Função principal para execução do algoritmo genético
def run_genetic_algorithm(num_generations, population_size, num_months, renda_total, custos_fixos,
                          custos_variaveis, risco_renda_fixa, risco_renda_variavel,
                          risco_tesouro, mutation_rate, population):
    best_individuals_history = []

    for generation in range(num_generations):
        logging.info(f"Generation {generation + 1} - Evaluating Population")

        score = [(eval_plano(ind, renda_total, risco_renda_fixa, risco_renda_variavel, risco_tesouro,
                             (custos_fixos - custos_variaveis)))
                 for ind in population]


        individuos_ordenados = sorted(score, key=lambda x: x[0], reverse=True)
        best_individual = individuos_ordenados[0]

        reserva_atual = best_individual[0]

        if best_individuals_history:
            ultima_melhor = best_individuals_history[-1][1]
            ultima_melhor_reserva = ultima_melhor[0]


        #vai mantendo o melhor resultado de reserva
        if len(best_individuals_history) == 0 or reserva_atual > ultima_melhor_reserva:
            best_individuals_history.append(( generation + 1, best_individual))
        else:
            best_individuals_history.append((generation + 1, ultima_melhor))


        #elitismo
        new_population = [best_individuals_history[-1][1][8]]  # mantem o melhor the best individual: ELITISM   É guardado a mlehor condição até o momento, se tirar isso ele pode perder a melhor opção

        while len(new_population) < population_size:
            # selection
            # simple selection based on first 10 best solutions
            parent1, parent2 = random.choices(population[:10], k=2)

            child1,_ = crossover_positions(parent1, parent2)

           # child1 = mutate(child1, mutation_rate)

            new_population.append(child1)

        population = new_population


       # population_sem_best = individuos_ordenados[1]
      #  randomizar_2 = random.sample(population_sem_best, 2)

        #
        #
        # parent1 = individuos_ordenados[0][8] #pega o pior
        # parent2 = individuos_ordenados[-1][8] #pega o melhor
        #
        # parent12, parent21 = crossover_positions(parent1, parent2)
        # # troca entre o par1 e par2 a posição 3,4 de cada mes para os valores de fixa e variavel
        #
        #
        # #pegar 2 aleatórios
        # # random.sample(sorted_population, 2)
        # list = [best_individual[8],parent12,parent21]
        # for ind in individuos_ordenados[2:len(individuos_ordenados)-1]:
        #     list.append(ind[8])
        #
        #
        # population =  list



    generations = process_best_individuals_history(best_individuals_history)
    # top_individuals = get_top_individuals(generations)
    #
    # if best_individuals_history:
    #     detailed_report(best_individuals_history[-1], renda_total, risco_renda_fixa, risco_renda_variavel,
    #                     risco_tesouro, meta_reserva, min_gastos_essenciais, max_gastos_essenciais,
    #                     min_gastos_nao_essenciais, max_gastos_nao_essenciais)

    #ultimos 2 melhores
    print(best_individuals_history[-1])
    print(best_individuals_history[-2])
    generations = [item for item in generations if item[1] != 0]
    plot_reserve_totals(generations)


# Configurações do algoritmo genético e parâmetros financeiros
config = configparser.ConfigParser()
config.read('config.ini')

salario_fixo = config.getfloat('finance', 'salario_fixo')
outras_receitas = config.getfloat('finance', 'outras_receitas')
meta_reserva = config.getfloat('finance', 'meta_reserva')
custos_fixos = config.getfloat('finance', 'custos_fixos')
custos_variaveis = custos_fixos * 0.12
num_meses = config.getint('finance', 'num_meses')
min_gastos_essenciais = config.getfloat('finance', 'min_gastos_essenciais') / 100
max_gastos_essenciais = config.getfloat('finance', 'max_gastos_essenciais') / 100
min_gastos_nao_essenciais = config.getfloat('finance', 'min_gastos_nao_essenciais') / 100
max_gastos_nao_essenciais = config.getfloat('finance', 'max_gastos_nao_essenciais') / 100
max_reserva = config.getfloat('finance', 'max_reserva') / 100

# Parâmetros fixos do risco
risco_renda_fixa = 0.01
risco_renda_variavel = 0.1
risco_tesouro = 0.05

population_size = config.getint('genetic_algorithm', 'population_size')
num_generations = config.getint('genetic_algorithm', 'ngen')
mutation_rate = config.getfloat('genetic_algorithm', 'mutation_rate')

# Gerar população inicial de gastos
population = generate_population(population_size, num_meses, salario_fixo + outras_receitas,
                                 custos_fixos - custos_variaveis)
# Executar o algoritmo genético
run_genetic_algorithm(num_generations, population_size, num_meses, salario_fixo + outras_receitas, custos_fixos,
                      custos_variaveis, risco_renda_fixa, risco_renda_variavel, risco_tesouro, mutation_rate,
                      population)