import random
import matplotlib.pyplot as plt
import configparser
import logging
import pickle
import numpy as np
import pygame
import sys
import io

# Configurações de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para gerar uma população inicial
def generate_population(size, num_meses, receita_total, custos_totais):
    population = []

    try:
        with open('population_z', 'rb') as f:
            population = pickle.load(f)
    except (FileNotFoundError, EOFError):
        pass

    if len(population) > 0:
        return population

    max_perc_fixa = 0.30
    max_perc_variavel = 0.70

    for _ in range(size):
        individual = []
        for _ in range(num_meses):
            perc_fixa = random.uniform(0, max_perc_fixa)
            perc_variavel = random.uniform(0, max_perc_variavel)
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
        reserva_percentual = 0.12
        reserva_total = reserva_percentual * (renda_total - custo_total)
        valor_disponivel = renda_total - custo_total - reserva_total

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
        total_reserva -= emergencia

    return total_reserva, total_receita, total_gastos, total_renda_fixa, total_renda_variavel, total_tesouro, total_valor_aplicado, total_retorno_aplicado, plano

def fitness(individual):
    return individual[0]

# Função para o crossover
def crossover_positions(parent1, parent2):
    if len(parent1) != len(parent2):
        raise ValueError("parent1 e parent2 devem ter o mesmo comprimento")

    child1 = []
    child2 = []

    for (p1, p2) in zip(parent1, parent2):
        p1_values = list(p1)
        p2_values = list(p2)

        p1_values[2], p1_values[3], p1_values[4] = p1_values[4], p1_values[2], p1_values[3]
        p2_values[2], p2_values[3], p2_values[4] = p2_values[4], p2_values[2], p2_values[3]

        p1_values[2], p2_values[2] = p2_values[2], p1_values[2]
        p1_values[4] = 1 - p1_values[2] - p1_values[3]
        p2_values[4] = 1 - p2_values[2] - p2_values[3]

        child1.append(tuple(p1_values))
        child2.append(tuple(p2_values))

    return child1, child2

def process_best_individuals_history(best_individuals_history):
    generations = []
    for gen, reserva_total in best_individuals_history:
        generations.append((gen, reserva_total[0]))
    return generations
