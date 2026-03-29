from src.core.isam_tree import ISAMTree
from src.metrics.search_metrics import SearchMetrics
from src.operations import searcher

REQUIRED_INSERTIONS = [18, 22, 27, 35, 41, 44, 63, 67, 83, 86, 121, 145]
REQUIRED_REMOVALS = [27, 44, 67, 83, 145]


def _empty_workload_stats():
    return {
        "inserted_ok": 0,
        "inserted_failed": 0,
        "removed_ok": 0,
        "removed_failed": 0,
    }


def _apply_required_workload(tree):
    """
    Aplica inserções e remoções obrigatórias na árvore informada.
    """
    stats = _empty_workload_stats()

    for key in REQUIRED_INSERTIONS:
        if tree.insert(key, f"R{key}"):
            stats["inserted_ok"] += 1
        else:
            stats["inserted_failed"] += 1

    for key in REQUIRED_REMOVALS:
        if tree.remove(key):
            stats["removed_ok"] += 1
        else:
            stats["removed_failed"] += 1

    return stats


def _build_required_workload_tree():
    """
    Monta a árvore no estado esperado para as buscas obrigatórias:
    estrutura inicial + inserções obrigatórias + remoções obrigatórias.
    """
    arvore = ISAMTree()
    stats = _apply_required_workload(arvore)
    return arvore, stats


def _compute_experimental_metrics(arvore, igualdade, intervalo, workload_stats):
    custos = [item["nodes_visited"] for item in igualdade + intervalo]
    custo_total = sum(custos)
    custo_medio = round(custo_total / len(custos), 2) if custos else 0.0

    return {
        "quantidade_paginas_folha": arvore.count_leaf_pages(),
        "quantidade_paginas_overflow": arvore.count_overflow_pages(),
        "tamanho_medio_cadeias_overflow": arvore.average_overflow_length(),
        "quantidade_registros_removidos": workload_stats["removed_ok"],
        "custo_aproximado_buscas_nos_medio": custo_medio,
        "custo_aproximado_buscas_nos_total": custo_total,
    }


def run_required_searches(tree=None, apply_workload=True):
    """
    Executa as buscas obrigatorias para medicao de custo.
    Retorna um dicionario com resultados e metricas de igualdade.
    """
    if tree is None:
        arvore, workload_stats = _build_required_workload_tree()
    else:
        arvore = tree
        workload_stats = _empty_workload_stats()
        if apply_workload:
            workload_stats = _apply_required_workload(arvore)

    metrics = SearchMetrics()

    igualdade_keys = [22, 35, 44, 90]
    intervalos = [(20, 50), (60, 90), (120, 150)]

    resultados_igualdade = []
    for key in igualdade_keys:
        resultado = searcher.search_equal(arvore.get_raiz(), key, metrics=metrics)
        resultados_igualdade.append({"operacao": f"buscar({key})", **resultado})

    resultados_intervalo = []
    for inicio, fim in intervalos:
        resultado = searcher.search_range(arvore.get_raiz(), inicio, fim)
        resultados_intervalo.append(
            {
                "operacao": f"buscar_intervalo({inicio}, {fim})",
                "records": resultado["records"],
                "visited_pages": resultado["visited_pages"],
                "nodes_visited": resultado["nodes_visited"],
            }
        )

    return {
        "igualdade": resultados_igualdade,
        "intervalo": resultados_intervalo,
        "metricas_igualdade": metrics.get_equality_metrics(),
        "metricas_experimentais": _compute_experimental_metrics(
            arvore, resultados_igualdade, resultados_intervalo, workload_stats
        ),
        "workload_stats": workload_stats,
    }


def print_required_searches_report(tree=None, apply_workload=True):
    """Imprime um resumo simples das buscas obrigatorias."""
    resultado = run_required_searches(tree, apply_workload=apply_workload)

    print("== Buscas por Igualdade ==")
    for item in resultado["igualdade"]:
        print(f"- {item['operacao']}")
        print(f"  encontrado: {item['found']}")
        print(f"  registro: {item['record']}")
        print(f"  paginas visitadas: {item['visited_pages']}")
        print(f"  custo (nos): {item['nodes_visited']}")

    print("\n== Buscas por Intervalo ==")
    for item in resultado["intervalo"]:
        print(f"- {item['operacao']}")
        print(f"  registros: {item['records']}")
        print(f"  paginas visitadas: {item['visited_pages']}")
        print(f"  custo (nos): {item['nodes_visited']}")

    print("\n== Metricas de Igualdade ==")
    for chave, valor in resultado["metricas_igualdade"].items():
        print(f"- {chave}: {valor}")

    print("\n== Metricas Experimentais ==")
    for chave, valor in resultado["metricas_experimentais"].items():
        print(f"- {chave}: {valor}")


if __name__ == "__main__":
    print_required_searches_report()
