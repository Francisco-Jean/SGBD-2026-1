from src.core.isam_tree import ISAMTree
from src.operations import searcher


def run_required_searches(tree=None):
    """
    Executa as buscas obrigatorias para medicao de custo.
    Retorna um dicionario com resultados e metricas de igualdade.
    """
    arvore = tree if tree is not None else ISAMTree()

    igualdade_keys = [22, 35, 44, 90]
    intervalos = [(20, 50), (60, 90), (120, 150)]

    resultados_igualdade = []
    for key in igualdade_keys:
        resultado = searcher.search_equal(arvore.get_raiz(), key, metrics=arvore.search_metrics)
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
        "metricas_igualdade": arvore.get_equality_search_metrics(),
    }


def print_required_searches_report(tree=None):
    """Imprime um resumo simples das buscas obrigatorias."""
    resultado = run_required_searches(tree)

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


if __name__ == "__main__":
    print_required_searches_report()
