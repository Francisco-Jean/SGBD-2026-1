
# Relatório de Implementação: Estrutura ISAM

**Disciplina:** Sistemas de Gerenciamento de Banco de Dados - 2026.1
**Integrantes:** Francisco Jean, Anna Beatriz, Lucas Lopes
**Data de Entrega:** 29/03/2026

## 1. Descrição da Modelagem e Decisões de Implementação

Este trabalho implementa uma simulação de um índice ISAM para organizar e recuperar registros com eficiência. A característica central do ISAM orientou toda a modelagem: a estrutura de índice principal é estática, enquanto as atualizações afetam apenas as páginas folha e suas páginas de overflow associadas.

### 1.1. Estrutura de Dados em Python

Optamos por modelar a árvore ISAM utilizando **listas aninhadas** em Python, aproveitando a permissão do escopo para usar estruturas simples com capacidade limitada. Não implementamos persistência em arquivo ou acesso a disco; os ponteiros são referências diretas em memória.

A arquitetura foi definida da seguinte forma:

* **Nós Intermediários e Raiz:** Representados como `[ [chaves_separadoras], [filhos] ]`.
* **Páginas Folha:** Representadas como `[ [registros_primarios], [paginas_de_overflow] ]`. A capacidade máxima foi fixada em 2 registros por página.
* **Estrutura Estática:** A árvore foi inicializada exatamente conforme a especificação, com a raiz (40) separando a busca em dois ramos, seguidos por dois níveis intermediários que apontam para 6 páginas folha primárias.

### 1.2. Divisão de Arquitetura e Prevenção de Conflitos

O projeto foi modularizado para facilitar o desenvolvimento assíncrono da equipe:

* **Francisco Jean:** Responsável pelo módulo de inserção e pela lógica de criação/encadeamento de páginas de overflow quando a folha primária atinge sua capacidade máxima. Também responsável pelas métricas de overflow.
* **Anna Beatriz:** Responsável pelo módulo de remoção de registros e liberação (garbage collection) de páginas de overflow que fiquem vazias, além das métricas de páginas folha.
* **Lucas Lopes:** Responsável pelo módulo de buscas (igualdade e intervalo) e pela medição do custo computacional (nós visitados).

---

## 2. Resultados Experimentais

### 2.1. Carga e Inserções

A partir da configuração inicial, o sistema processou o lote de 12 inserções obrigatórias (chaves 18 a 145). Como as folhas primárias atingiram rapidamente sua capacidade, o sistema passou a criar e encadear páginas de overflow para absorver os novos registros.

### 2.2. Remoções

O sistema processou o lote de 5 remoções obrigatórias (chaves 27, 44, 67, 83, 145). Durante este processo, [PREENCHER: descrever se alguma página de overflow ficou vazia e foi liberada com sucesso].

---

## 3. Análise de Comportamento e Percurso

### 3.1. Rastreamento de Busca por Igualdade

Para ilustrar a navegação, analisamos o caminho percorrido durante a busca pela chave **90**:

* **Caminho percorrido:** Raiz -> Nó Intermediário Direito -> Folha 6.
* **Custo:** 3 nós percorridos.
* **Explicação:** A busca iniciou na raiz, avaliando se a chave era menor ou maior que o separador. Como 90 > 40, seguiu para o ramo direito. Em seguida, no nó intermediário direito (51, 63), como 90 >= 63, a navegação chegou à Folha 6. Não houve acesso a overflow nesse caso.

### 3.2. Rastreamento de Busca por Intervalo

Analisamos a operação `buscar_intervalo(60, 90)`:

* **Caminho percorrido:** Raiz -> Nó Intermediário Direito -> Folha 5 -> Folha 6
* **Custo:** 4 nós percorridos.
* **Explicação:** A busca começa na raiz (chave separadora 40). Como o início do intervalo é 60 e 60 > 40, a navegação desce para o nó intermediário direito (separadores 51 e 63). Nesse nó, a chave 60 fica entre 51 e 63, então a primeira folha candidata é a Folha 5.
Na Folha 5, os registros são (51, R51) e (55, R55), ambos menores que 60, então nenhum entra no resultado. Em seguida, a busca continua sequencialmente para a Folha 6, onde encontra (63, R63), que está dentro do intervalo [60, 90], e (97, R97), que já ultrapassa o limite superior. Com isso, o resultado final é [(63, 'R63')], sem necessidade de visitar páginas de overflow.

---

## 4. Métricas Finais Observadas

Abaixo estão as métricas coletadas após a execução completa de todas as inserções e remoções obrigatórias:

| Métrica                                         | Objetivo da Observação                                          | Resultado Final              |
| :----------------------------------------------- | :---------------------------------------------------------------- | :--------------------------- |
| **Quantidade de páginas folha**           | Avaliar a estrutura primária ocupada.                            | 6 (Estático)                |
| **Quantidade de páginas de overflow**     | Medir o impacto das inserções após o preenchimento das folhas. | [PREENCHER]                  |
| **Tamanho médio das cadeias de overflow** | Avaliar a degradação potencial da busca.                        | [PREENCHER]                  |
| **Quantidade de registros removidos**      | Observar a manutenção das páginas e liberação de overflow.   | 5                            |
| **Custo aproximado das buscas**            | Comparar o efeito do crescimento das cadeias de overflow.         | [PREENCHER] nós (em média) |

---

## 5. Conclusão

A simulação evidenciou claramente a natureza da estrutura ISAM. A eficiência de busca na árvore estática é extremamente alta (garantindo apenas 3 saltos até a folha primária). No entanto, ao submeter o índice a um volume de inserções além de sua capacidade primária, observamos um crescimento nas cadeias de overflow.

Isso confirma que, embora o ISAM seja excelente para cenários com dados estáticos ou poucas inserções, a falta de balanceamento dinâmico (divisão de páginas) causa uma degradação linear no custo da busca à medida que as listas de overflow crescem.
