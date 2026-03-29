# ISAM - Trabalho Prático (SGBD 2026.1)

Anna Beatriz Vieira Sousa - 538758
Francisco Jean da Silva de Sousa - 541790
Lucas Lopes de Sousa - 537512

## Como rodar o código
No diretório `Trabalho1`:

```bash
python -m src.operations.required_searches
```

Esse comando executa a carga obrigatória completa e imprime os resultados.

Menu interativo (opcional):

```bash
python -c "from src.core.isam_tree import ISAMTree; from src.main import Menu; Menu(ISAMTree())"
```

## Informações gerais
- Disciplina: Sistemas de Gerenciamento de Banco de Dados (SGBD)
- Linguagem: Python
- Prazo de entrega: 29/03/2026
- Grupo: até 3 integrantes

## Objetivo
Implementar uma simulação funcional de índice ISAM para analisar inserções, remoções, buscas e impacto de páginas de overflow no custo das operações.

## Modelagem implementada
- Estrutura estática com:
  - raiz `40`
  - nível intermediário 1: `20,33` (esquerda) e `51,63` (direita)
  - nível intermediário 2 com seis nós (`A..F`), cada um apontando para uma folha primária
- Folhas primárias iniciais:
  - `A:[10,15]`, `B:[20,27]`, `C:[33,37]`, `D:[40,46]`, `E:[51,55]`, `F:[63,97]`
- Capacidade por página (folha/overflow): `2` registros
- Índice principal não sofre split; atualizações ficam em folha + overflow
- Não há restrição explícita de unicidade no enunciado; duplicatas foram permitidas

## Operações obrigatórias cobertas
- Inserções: `18,22,27,35,41,44,63,67,83,86,121,145`
- Remoções: `27,44,67,83,145`
- Igualdade: `buscar(22)`, `buscar(35)`, `buscar(44)`, `buscar(90)`
- Intervalo: `buscar_intervalo(20,50)`, `buscar_intervalo(60,90)`, `buscar_intervalo(120,150)`

## Métricas finais
- Quantidade de páginas folha: `6`
- Quantidade de páginas de overflow: `7`
- Tamanho médio das cadeias de overflow: `1.4`
- Quantidade de registros removidos: `5`
- Custo aproximado das buscas obrigatórias:
  - total: `46` nós
  - médio: `6.57` nós/busca

## Análise dos resultados
- A estrutura estática do ISAM foi preservada durante toda a carga.
- O aumento de overflow ficou concentrado nas regiões mais acessadas, elevando o custo das buscas que passam por essas cadeias.
- Com duplicatas permitidas, as chaves já existentes na base inicial (`27` e `63`) foram inseridas novamente, aumentando cadeia de overflow e custo médio.
- As remoções obrigatórias foram efetivas (`5/5`) e a reorganização da cadeia manteve o comportamento esperado.

## Exemplo de caminho das buscas
### Exemplo 1 - Busca por igualdade (`buscar(35)`)
- Caminho percorrido:
  - `raiz`
  - `intermediario_n1_esquerdo[20,33]` (35 é menor que 40, então segue para o ramo esquerdo)
  - `intermediario_n2[33,37]` (35 fica na faixa da folha 3)
  - `folha_3`
  - `overflow_3_1` (registro encontrado no overflow)
- Registro retornado: `(35, 'R35')`
- Custo: `5` nós percorridos

### Exemplo 2 - Busca por intervalo (`buscar_intervalo(60,90)`)
- Caminho percorrido:
  - `raiz`
  - `intermediario_n1_direito[51,63]` (início do intervalo 60 é maior que 40)
  - `intermediario_n2[51,55]` (primeira folha candidata para iniciar a varredura)
  - `folha_5`
  - `folha_6`
  - `overflow_6_1 -> overflow_6_2 -> overflow_6_3`
- Registros retornados: `[(63, 'R63'), (63, 'R63'), (86, 'R86')]`
- Custo: `8` nós percorridos

## Simulação detalhada
Os resultados completos da simulação obrigatória estão em:
- [`simulação.md`](./simulação.md)
