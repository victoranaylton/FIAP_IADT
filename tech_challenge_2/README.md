# Planejamento Financeiro Familiar com Algoritmos Genéticos

## Descrição do Problema

O objetivo deste projeto é utilizar algoritmos genéticos para prever o melhor cenário de planejamento financeiro familiar com objetivo de maximizar a reserva financeira ao longo de um período definido.

## Objetivos

- Exibir um plano de alocação financeira em um determinado numero de meses. Cada mês deve exibir um teto de gastos e o percentual que deve ser investido em cada um dos 3 tipos de investimentos
- O objetivo do plano é maximizar a reserva financeira total após um período definido, considerando 3 diferentes tipos de investimentos.
- O plano leva em consideração os percentual de risco de cada investimento ( parametrizado ) e possíveis emergências financeiras que possam acontecer dentro do período informado e que podem consumir parte da reserva.


## Implementação do Algoritmo Genético

O algoritmo genético implementado neste projeto segue os seguintes passos:

1. **Inicialização da População**: Uma população inicial de indivíduos (planos financeiros) é gerada aleatoriamente. Cada indivíduo representa uma distribuição mensal de gastos e investimentos em renda fixa, renda variável e tesouro.

2. **Avaliação da Aptidão**: A aptidão de cada indivíduo é avaliada com base na reserva financeira total alcançada ao final do período planejado, considerando os riscos associados a cada tipo de investimento e possíveis emergências financeiras.

3. **Seleção**: Os indivíduos mais aptos são selecionados para a próxima geração, com base em sua aptidão relativa.

4. **Crossover**: Pares de indivíduos selecionados são combinados para gerar novos indivíduos (filhos) através de um processo de crossover, onde partes dos planos financeiros dos pais são trocadas.

5. **Mutação**: Os filhos gerados pelo crossover podem sofrer mutações aleatórias, introduzindo variabilidade na população.

6. **Substituição**: A nova população é formada pelos indivíduos mais aptos da geração anterior e pelos filhos gerados pelo crossover e mutação.

7. **Repetição**: Os passos 2 a 6 são repetidos por um número definido de gerações ou até que um critério de parada seja atingido.

Ao final do processo evolutivo, o melhor indivíduo (plano financeiro) é selecionado como a solução para o problema.


## Estrutura do Projeto

`financial_plan.py`

Este arquivo contém a implementação do algoritmo genético e as funções auxiliares necessárias.

`config.ini`

Este arquivo permite ao usuário definir os parâmetros financeiros e os parâmetros do algoritmo genético.

`run.py`

Responsável por executar o algorítmo genético, assim como exibir os resultados em uma interface gráfica

```ini
[finance]
salario_fixo = 4685
outras_receitas = 1240
meta_reserva = 13000
num_meses = 12
custos_fixos = 2650
risco_renda_fixa = 0.01
risco_renda_variavel = 0.1
risco_tesouro = 0.05

[genetic_algorithm]
population_size = 100
ngen = 50
mutation_rate = 0.1
crossover_rate = 0.5
```

#### Parâmetros do Arquivo de Configuração

 - finance
   - salario_fixo: Salário fixo mensal.
   - outras_receitas: Outras receitas mensais.
   - meta_reserva: Meta de reserva financeira a ser alcançada.
   - num_meses: Número de meses para o planejamento.
   - custos_fixos: Custos fixos mensais
   - risco_renda_fixa: Percentual de risco do investimento renda fixa
   - risco_renda_variavel: Percentual de risco do investimento em renda variável
   - risco_tesouro: Percentual de risco do investimento em Tesouro

- genetic_algorithm
   - population_size: Tamanho da população.
   - ngen: Número de gerações.
   - mutation_rate: Taxa de mutação.
   - crossover_rate: Taxa de crossover.

## Execução do Código

Ajuste os valores no arquivo de configuração `config.ini` e execute o script abaixo

> python run.py

### Resultado Esperado

Ao final da execução do algoritmo genético, o melhor plano financeiro será exibido, mostrando a distribuição mensal dos gastos e percentuais de investimentos em renda fixa, renda variável e tesouro. Além disso, será exibida a reserva financeira total após o período planejado.


![](./asset/result.png "Resultado")

