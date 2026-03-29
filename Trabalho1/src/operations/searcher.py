def _normalize_key(key):
    """Converte a chave para inteiro."""
    return int(key)


def _get_tree_parts(isam_tree):
    """
    Extrai partes fixas da estrutura ISAM em listas.
    Formato esperado:
    raiz = [[40], [no_esq, no_dir]]
    no = [[sep1, sep2], [folha1, folha2, folha3]]
    """
    root_key = isam_tree[0][0]
    left_node = isam_tree[1][0]
    right_node = isam_tree[1][1]
    return root_key, left_node, right_node


def _navigate_to_leaf(isam_tree, key):
    """
    Navega pela árvore e retorna a folha alvo com metadados do caminho.
    """
    key = _normalize_key(key)
    root_key, left_node, right_node = _get_tree_parts(isam_tree)

    visited_pages = ["raiz"]
    nodes_visited = 1

    if key <= root_key:
        inter_node = left_node
        inter_label = "intermediario_esquerdo"
        base_index = 0
    else:
        inter_node = right_node
        inter_label = "intermediario_direito"
        base_index = 3

    visited_pages.append(inter_label)
    nodes_visited += 1

    sep1, sep2 = inter_node[0]
    leaves = inter_node[1]

    if key < sep1:
        local_leaf_index = 0
    elif key < sep2:
        local_leaf_index = 1
    else:
        local_leaf_index = 2

    global_leaf_index = base_index + local_leaf_index
    leaf = leaves[local_leaf_index]

    visited_pages.append(f"folha_{global_leaf_index + 1}")
    nodes_visited += 1

    return {
        "leaf": leaf,
        "global_leaf_index": global_leaf_index,
        "visited_pages": visited_pages,
        "nodes_visited": nodes_visited,
    }


def _iter_overflow_pages(leaf):
    """
    Itera páginas de overflow da folha.
    Suporta:
    - listas de registros (modelo simples)
    - objetos com get_records()/get_next_page() (modelo OO)
    """
    overflows = leaf[1] if len(leaf) > 1 else []

    for overflow in overflows:
        if hasattr(overflow, "get_records"):
            current = overflow
            while current:
                yield current
                current = current.get_next_page()
        else:
            yield overflow


def _get_records_from_overflow(overflow):
    if hasattr(overflow, "get_records"):
        return overflow.get_records()
    return overflow


def search_equal(isam_tree, key, metrics=None):
    """
    Busca por igualdade.
    Retorna detalhes do percurso e custo aproximado (nós visitados).
    """
    key = _normalize_key(key)
    nav = _navigate_to_leaf(isam_tree, key)
    leaf = nav["leaf"]

    # Busca na folha primária
    for record in leaf[0]:
        if record[0] == key:
            if metrics:
                metrics.register_equality_search(
                    found=True,
                    nodes_visited=nav["nodes_visited"],
                    overflow_pages_visited=0,
                )
            return {
                "found": True,
                "location": "primary",
                "record": record,
                "visited_pages": nav["visited_pages"],
                "nodes_visited": nav["nodes_visited"],
                "overflow_pages_visited": 0,
            }

    # Busca nas páginas de overflow
    overflow_pages_visited = 0
    visited_pages = nav["visited_pages"][:]
    nodes_visited = nav["nodes_visited"]

    for index, overflow in enumerate(_iter_overflow_pages(leaf), start=1):
        overflow_pages_visited += 1
        nodes_visited += 1
        visited_pages.append(f"overflow_{nav['global_leaf_index'] + 1}_{index}")

        for record in _get_records_from_overflow(overflow):
            if record[0] == key:
                if metrics:
                    metrics.register_equality_search(
                        found=True,
                        nodes_visited=nodes_visited,
                        overflow_pages_visited=overflow_pages_visited,
                    )
                return {
                    "found": True,
                    "location": "overflow",
                    "record": record,
                    "visited_pages": visited_pages,
                    "nodes_visited": nodes_visited,
                    "overflow_pages_visited": overflow_pages_visited,
                }

    if metrics:
        metrics.register_equality_search(
            found=False,
            nodes_visited=nodes_visited,
            overflow_pages_visited=overflow_pages_visited,
        )

    return {
        "found": False,
        "location": None,
        "record": None,
        "visited_pages": visited_pages,
        "nodes_visited": nodes_visited,
        "overflow_pages_visited": overflow_pages_visited,
    }


def _flatten_leaves_in_order(isam_tree):
    _, left_node, right_node = _get_tree_parts(isam_tree)
    return left_node[1] + right_node[1]


def search_range(isam_tree, start_key, end_key):
    """
    Busca por intervalo [start_key, end_key].
    Retorna registros encontrados em ordem crescente e custo aproximado.
    """
    start_key = _normalize_key(start_key)
    end_key = _normalize_key(end_key)

    if start_key > end_key:
        start_key, end_key = end_key, start_key

    nav = _navigate_to_leaf(isam_tree, start_key)
    leaves = _flatten_leaves_in_order(isam_tree)

    results = []
    visited_pages = nav["visited_pages"][:-1]  # raiz + nó intermediário inicial
    nodes_visited = 2

    for leaf_index in range(nav["global_leaf_index"], len(leaves)):
        leaf = leaves[leaf_index]
        visited_pages.append(f"folha_{leaf_index + 1}")
        nodes_visited += 1

        for record in leaf[0]:
            if start_key <= record[0] <= end_key:
                results.append(record)

        for overflow_pos, overflow in enumerate(_iter_overflow_pages(leaf), start=1):
            nodes_visited += 1
            visited_pages.append(f"overflow_{leaf_index + 1}_{overflow_pos}")
            for record in _get_records_from_overflow(overflow):
                if start_key <= record[0] <= end_key:
                    results.append(record)

        # Como as folhas estão em ordem, se o menor registro da folha já passou do fim, pode parar
        if leaf[0] and leaf[0][0][0] > end_key:
            break

    results.sort(key=lambda x: x[0])
    return {
        "range": (start_key, end_key),
        "records": results,
        "visited_pages": visited_pages,
        "nodes_visited": nodes_visited,
    }
