import random
import matplotlib.pyplot as plt
import configparser
import logging
import pygame
import sys
import io
import hashlib
from financial_plan import *

# Inicializar Pygame
pygame.init()
window_size = (1800, 600)  # Ajuste o tamanho da janela para acomodar gráfico e texto lado a lado
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Genetic Algorithm Evolution")
font = pygame.font.SysFont(None, 24)

def calculate_hash_individual(individual):
    individual_str = str(individual).encode()
    return hashlib.md5(individual_str).hexdigest()

def plot_reserve_totals(screen, generations, reserve_totals):
    plt.clf()
    plt.plot(generations, reserve_totals, marker='x')
    plt.title('Reservas Totais por Geração')
    plt.xlabel('Geração')
    plt.ylabel('Reserva Total (R$)')
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph_image = pygame.image.load(buf)
    screen.blit(graph_image, (0, 0))
    pygame.display.flip()
    buf.close()

def display_final_results(screen, font, best_individual):
    text_surface = pygame.Surface((window_size[0] // 2, window_size[1]))
    text_surface.fill((255, 255, 255))

    lines = [
        f"Total Reserva acumulada: {best_individual[1][0]:.2f}",
        f"Total Gastos emergenciais: {best_individual[1][9]:.2f}",
        f"Total Receita no período: {best_individual[1][1]:.2f}",
        f"Total Gastos no período: {best_individual[1][2]:.2f}",
        f"Total Renda Fixa: {best_individual[1][3]:.2f}",
        f"Total Renda Variável: {best_individual[1][4]:.2f}",
        f"Total Tesouro: {best_individual[1][5]:.2f}",
        f"Total Valor Aplicado: {best_individual[1][6]:.2f}",
        f"Total Retorno Aplicado: {best_individual[1][7]:.2f}",
    ]
    
    for i, line in enumerate(lines):
        text = font.render(line, True, (0, 0, 0))
        text_surface.blit(text, (10, 20 + 25 * i))

    for j, month in enumerate(best_individual[1][8]):
        month_text = f"Mês {j + 1}: Receita Total: {month[0]:.2f}, Gastos totais: {month[1]:.2f}, Renda Fixa: {month[2]:.2f}, Renda Variável: {month[3]:.2f}, Tesouro: {month[4]:.2f}"
        text = font.render(month_text, True, (0, 0, 0))
        text_surface.blit(text, (10, 250 + 25 * j))

    screen.blit(text_surface, (window_size[0] // 2, 0))
    pygame.display.flip()

def run_genetic_algorithm(num_generations, population_size, num_months, renda_total, custos_fixos,
                          custos_variaveis, risco_renda_fixa, risco_renda_variavel,
                          risco_tesouro, mutation_rate, population):
    best_individuals_history = []
    seen_hashes = set()

    for generation in range(num_generations):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

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

        if len(best_individuals_history) == 0 or reserva_atual > ultima_melhor_reserva:
            best_individuals_history.append((generation + 1, best_individual))
        else:
            best_individuals_history.append((generation + 1, ultima_melhor))

        new_population = [best_individuals_history[-1][1][8]]

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population[:10], k=2)
            child1, _ = crossover_positions(parent1, parent2)

            hash_child1 = calculate_hash_individual(child1)
            if hash_child1 not in seen_hashes:
                seen_hashes.add(hash_child1)
                new_population.append(child1)

        population = new_population

        generations = process_best_individuals_history(best_individuals_history)
        generation_nums = [gen[0] for gen in generations]
        reserve_totals = [gen[1] for gen in generations]

        plot_reserve_totals(screen, generation_nums, reserve_totals)

    print(best_individuals_history[-1])
    print(best_individuals_history[-2])
    display_final_results(screen, font, best_individuals_history[-1])


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

risco_renda_fixa = 0.01
risco_renda_variavel = 0.1
risco_tesouro = 0.05

population_size = config.getint('genetic_algorithm', 'population_size')
num_generations = config.getint('genetic_algorithm', 'ngen')
mutation_rate = config.getfloat('genetic_algorithm', 'mutation_rate')

population = generate_population(population_size, num_meses, salario_fixo + outras_receitas,
                                 custos_fixos - custos_variaveis)

run_genetic_algorithm(num_generations, population_size, num_meses, salario_fixo + outras_receitas, custos_fixos,
                      custos_variaveis, risco_renda_fixa, risco_renda_variavel, risco_tesouro, mutation_rate,
                      population)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

pygame.quit()
sys.exit()
