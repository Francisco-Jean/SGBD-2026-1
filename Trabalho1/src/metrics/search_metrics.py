class SearchMetrics:
    """
    Métricas das operações de busca por igualdade.
    """

    def __init__(self):
        self.total_equality_searches = 0
        self.found_equality_searches = 0
        self.not_found_equality_searches = 0
        self.total_nodes_visited_equality = 0
        self.total_overflow_pages_visited_equality = 0

    def register_equality_search(self, found, nodes_visited, overflow_pages_visited):
        self.total_equality_searches += 1
        self.total_nodes_visited_equality += int(nodes_visited)
        self.total_overflow_pages_visited_equality += int(overflow_pages_visited)

        if found:
            self.found_equality_searches += 1
        else:
            self.not_found_equality_searches += 1

    def get_equality_metrics(self):
        if self.total_equality_searches == 0:
            avg_nodes = 0.0
            avg_overflow = 0.0
        else:
            avg_nodes = self.total_nodes_visited_equality / self.total_equality_searches
            avg_overflow = (
                self.total_overflow_pages_visited_equality / self.total_equality_searches
            )

        return {
            "total_buscas_igualdade": self.total_equality_searches,
            "encontradas": self.found_equality_searches,
            "nao_encontradas": self.not_found_equality_searches,
            "nos_percorridos_total": self.total_nodes_visited_equality,
            "nos_percorridos_medio": round(avg_nodes, 2),
            "overflow_visitadas_total": self.total_overflow_pages_visited_equality,
            "overflow_visitadas_media": round(avg_overflow, 2),
        }
