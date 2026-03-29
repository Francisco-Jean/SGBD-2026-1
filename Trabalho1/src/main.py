from src.core.isam_tree import ISAMTree
from src.operations.required_searches import (
    REQUIRED_INSERTIONS,
    REQUIRED_REMOVALS,
    print_required_searches_report,
)


class Menu:
    def __init__(self, arvore_isam):
        self.arvore = arvore_isam
        self.show_menu()

    def _print_header(self):
        print("=" * 70)
        print("Qual operação deseja realizar?\n")
        print("[1] Visualizar árvore atual")
        print("[2] Inserir nó manual (com custo)")
        print("[3] Remover nó (com custo)")
        print("[4] Buscar por igualdade (com custo)")
        print("[5] Buscar por intervalo (com custo)")
        print("[6] Exibir métricas (overflow + buscas)")
        print("[7] Executar inserções obrigatórias (lote)")
        print("[8] Executar remoções obrigatórias (lote)")
        print("[9] Executar relatório de buscas obrigatórias")
        print("[10] Sair")
        print("=" * 70)

    def _print_operation_cost(self, result):
        print(f"  páginas visitadas: {result['visited_pages']}")
        print(f"  nós da árvore: {result['nodes_visited']}")
        print(f"  páginas de overflow visitadas: {result['overflow_pages_visited']}")
        print(f"  custo aproximado total: {result['cost']} nós")

    def show_menu(self):
        while True:
            self._print_header()
            option = input("Digite a opção desejada: ").strip()

            if option == "1":
                self.arvore.get_tree()

            elif option == "2":
                key = input("Digite a chave para inserir: ").strip()
                value = input("Digite o valor (enter para usar R<chave>): ").strip()
                if not value:
                    value = f"R{key}"

                result = self.arvore.insert_with_cost(int(key), value)
                status = "Sucesso" if result["success"] else "Falha"
                print(f"{status}: ({key}, '{value}')")
                self._print_operation_cost(result)
                print(
                    f"  novas páginas de overflow criadas: {result.get('overflow_pages_created', 0)}"
                )

            elif option == "3":
                key = input("Qual chave deseja remover? ").strip()
                result = self.arvore.remove_with_cost(int(key))
                status = "Removido" if result["success"] else "Não encontrado"
                print(f"{status}: chave {key}")
                self._print_operation_cost(result)

            elif option == "4":
                key = input("Qual chave deseja buscar? ").strip()
                result = self.arvore.search_with_cost(int(key))
                print(f"Encontrado: {result['found']}")
                print(f"Registro: {result['record']}")
                print(f"Localização: {result['location']}")
                print(f"Páginas visitadas: {result['visited_pages']}")
                print(f"Custo aproximado: {result['nodes_visited']} nós")

            elif option == "5":
                start_key = input("Início do intervalo: ").strip()
                end_key = input("Fim do intervalo: ").strip()
                result = self.arvore.search_interval_with_cost(int(start_key), int(end_key))
                print(f"Intervalo consultado: {result['range']}")
                print(f"Registros encontrados: {result['records']}")
                print(f"Páginas visitadas: {result['visited_pages']}")
                print(f"Custo aproximado: {result['nodes_visited']} nós")

            elif option == "6":
                overflow_metrics = self.arvore.get_overflow_metrics()
                equality_metrics = self.arvore.get_equality_search_metrics()

                print("\nMétricas de Estrutura / Overflow")
                for key, value in overflow_metrics.items():
                    print(f"- {key}: {value}")

                print("\nMétricas de Busca por Igualdade (sessão atual)")
                for key, value in equality_metrics.items():
                    print(f"- {key}: {value}")

            elif option == "7":
                print("\nExecutando inserções obrigatórias...")
                total_cost = 0
                for key in REQUIRED_INSERTIONS:
                    value = f"R{key}"
                    result = self.arvore.insert_with_cost(key, value)
                    total_cost += result["cost"]
                    status = "ok" if result["success"] else "falha"
                    print(
                        f"- inserir {key}: {status} | custo={result['cost']} nós | overflow_visitadas={result['overflow_pages_visited']}"
                    )
                print(f"Custo total do lote de inserções: {total_cost} nós")

            elif option == "8":
                print("\nExecutando remoções obrigatórias...")
                total_cost = 0
                for key in REQUIRED_REMOVALS:
                    result = self.arvore.remove_with_cost(key)
                    total_cost += result["cost"]
                    status = "ok" if result["success"] else "não encontrada"
                    print(
                        f"- remover {key}: {status} | custo={result['cost']} nós | overflow_visitadas={result['overflow_pages_visited']}"
                    )
                print(f"Custo total do lote de remoções: {total_cost} nós")

            elif option == "9":
                print_required_searches_report()

            elif option == "10":
                print("Encerrando...")
                break

            else:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    Menu(ISAMTree())
