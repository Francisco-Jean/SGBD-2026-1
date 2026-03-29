# Relatorio - Buscas Obrigatorias (ISAM)

## Operacoes executadas

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
  - encontrado: `False`
  - registro: `None`
  - paginas visitadas: `['raiz', 'intermediario_esquerdo', 'folha_2']`
  - custo: `3` nos
- `buscar(35)`
  - encontrado: `False`
  - registro: `None`
  - paginas visitadas: `['raiz', 'intermediario_esquerdo', 'folha_3']`
  - custo: `3` nos
- `buscar(44)`
  - encontrado: `False`
  - registro: `None`
  - paginas visitadas: `['raiz', 'intermediario_direito', 'folha_4']`
  - custo: `3` nos
- `buscar(90)`
  - encontrado: `False`
  - registro: `None`
  - paginas visitadas: `['raiz', 'intermediario_direito', 'folha_6']`
  - custo: `3` nos

### Buscas por intervalo
- `buscar_intervalo(20, 50)`
  - registros: `[(20, 'R20'), (27, 'R27'), (33, 'R33'), (37, 'R37'), (40, 'R40'), (46, 'R46')]`
  - paginas visitadas: `['raiz', 'intermediario_esquerdo', 'folha_2', 'folha_3', 'folha_4', 'folha_5']`
  - custo: `6` nos
- `buscar_intervalo(60, 90)`
  - registros: `[(63, 'R63')]`
  - paginas visitadas: `['raiz', 'intermediario_direito', 'folha_5', 'folha_6']`
  - custo: `4` nos
- `buscar_intervalo(120, 150)`
  - registros: `[]`
  - paginas visitadas: `['raiz', 'intermediario_direito', 'folha_6']`
  - custo: `3` nos

## Metricas de igualdade
- `total_buscas_igualdade`: `4`
- `encontradas`: `0`
- `nao_encontradas`: `4`
- `nos_percorridos_total`: `12`
- `nos_percorridos_medio`: `3.0`
- `overflow_visitadas_total`: `0`
- `overflow_visitadas_media`: `0.0`

## Exemplos de caminho
- Igualdade (`buscar(44)`): `raiz -> intermediario_direito -> folha_4` (custo `3`)
- Intervalo (`buscar_intervalo(60, 90)`): `raiz -> intermediario_direito -> folha_5 -> folha_6` (custo `4`)
