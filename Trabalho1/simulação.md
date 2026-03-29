# Simulação das Operações Obrigatórias (ISAM)

## Estado da carga
- Inserções efetivas: `12`
- Inserções rejeitadas: `0`
- Remoções efetivas: `5`
- Remoções falhas: `0`
- Custo total das inserções obrigatórias: `66` nós
- Custo total das remoções obrigatórias: `39` nós

## Custos das inserções obrigatórias
| Ordem | Registro inserido | Custo (nós) | Overflow visitadas | Overflow criadas |
| :--- | :--- | :---: | :---: | :---: |
| 1 | `(18, 'R18')` | 5 | 1 | 1 |
| 2 | `(22, 'R22')` | 5 | 1 | 1 |
| 3 | `(27, 'R27')` | 5 | 1 | 0 |
| 4 | `(35, 'R35')` | 5 | 1 | 1 |
| 5 | `(41, 'R41')` | 5 | 1 | 1 |
| 6 | `(44, 'R44')` | 5 | 1 | 0 |
| 7 | `(63, 'R63')` | 5 | 1 | 1 |
| 8 | `(67, 'R67')` | 5 | 1 | 0 |
| 9 | `(83, 'R83')` | 6 | 2 | 1 |
| 10 | `(86, 'R86')` | 6 | 2 | 0 |
| 11 | `(121, 'R121')` | 7 | 3 | 1 |
| 12 | `(145, 'R145')` | 7 | 3 | 0 |

## Custos das remoções obrigatórias
| Ordem | Registro alvo removido | Custo (nós) | Overflow visitadas |
| :--- | :--- | :---: | :---: |
| 1 | chave `27` (registro `R27`) | 6 | 2 |
| 2 | chave `44` (registro `R44`) | 6 | 2 |
| 3 | chave `67` (registro `R67`) | 8 | 4 |
| 4 | chave `83` (registro `R83`) | 9 | 5 |
| 5 | chave `145` (registro `R145`) | 10 | 6 |

## Operações executadas

### Igualdade
- `buscar(22)`
- `buscar(35)`
- `buscar(44)`
- `buscar(90)`

### Intervalo
- `buscar_intervalo(20, 50)`
- `buscar_intervalo(60, 90)`
- `buscar_intervalo(120, 150)`

## Resultados

### Buscas por igualdade
- `buscar(22)`
  - encontrado: `True`
  - registro: `(22, 'R22')`
  - páginas visitadas: `['raiz', 'intermediario_n1_esquerdo[20,33]', 'intermediario_n2[20,27]', 'folha_2']`
  - custo: `4` nós
- `buscar(35)`
  - encontrado: `True`
  - registro: `(35, 'R35')`
  - páginas visitadas: `['raiz', 'intermediario_n1_esquerdo[20,33]', 'intermediario_n2[33,37]', 'folha_3', 'overflow_3_1']`
  - custo: `5` nós
- `buscar(44)`
  - encontrado: `False`
  - registro: `None`
  - páginas visitadas: `['raiz', 'intermediario_n1_direito[51,63]', 'intermediario_n2[40,46]', 'folha_4', 'overflow_4_1']`
  - custo: `5` nós
- `buscar(90)`
  - encontrado: `False`
  - registro: `None`
  - páginas visitadas: `['raiz', 'intermediario_n1_direito[51,63]', 'intermediario_n2[63,97]', 'folha_6', 'overflow_6_1', 'overflow_6_2', 'overflow_6_3']`
  - custo: `7` nós

### Buscas por intervalo
- `buscar_intervalo(20, 50)`
  - registros: `[(20, 'R20'), (22, 'R22'), (27, 'R27'), (33, 'R33'), (35, 'R35'), (37, 'R37'), (40, 'R40'), (41, 'R41'), (46, 'R46')]`
  - páginas visitadas: `['raiz', 'intermediario_n1_esquerdo[20,33]', 'intermediario_n2[20,27]', 'folha_2', 'overflow_2_1', 'folha_3', 'overflow_3_1', 'folha_4', 'overflow_4_1', 'folha_5']`
  - custo: `10` nós
- `buscar_intervalo(60, 90)`
  - registros: `[(63, 'R63'), (63, 'R63'), (86, 'R86')]`
  - páginas visitadas: `['raiz', 'intermediario_n1_direito[51,63]', 'intermediario_n2[51,55]', 'folha_5', 'folha_6', 'overflow_6_1', 'overflow_6_2', 'overflow_6_3']`
  - custo: `8` nós
- `buscar_intervalo(120, 150)`
  - registros: `[(121, 'R121')]`
  - páginas visitadas: `['raiz', 'intermediario_n1_direito[51,63]', 'intermediario_n2[63,97]', 'folha_6', 'overflow_6_1', 'overflow_6_2', 'overflow_6_3']`
  - custo: `7` nós

## Métricas

### Métricas de igualdade
- `total_buscas_igualdade`: `4`
- `encontradas`: `2`
- `nao_encontradas`: `2`
- `nos_percorridos_total`: `21`
- `nos_percorridos_medio`: `5.25`
- `overflow_visitadas_total`: `5`
- `overflow_visitadas_media`: `1.25`

### Métricas experimentais
- `quantidade_paginas_folha`: `6`
- `quantidade_paginas_overflow`: `7`
- `tamanho_medio_cadeias_overflow`: `1.4`
- `quantidade_registros_removidos`: `5`
- `custo_aproximado_buscas_nos_medio`: `6.57`
- `custo_aproximado_buscas_nos_total`: `46`
