# src/core/isam_tree.py

# Capacidade máxima definida pelo escopo (2 registros por página folha/overflow)
CAPACIDADE_PAGINA = 2

def construir_arvore_estatica():
    """
    Constrói a estrutura ISAM inicial usando listas aninhadas.
    Retorna a raiz da árvore e uma lista com as folhas para facilitar a varredura.
    """
    
    # PÁGINAS FOLHA PRIMÁRIAS [ [registros], [overflows] ]
    folha_A = [ [(10, "R10"), (15, "R15")], [] ]
    folha_B = [ [(20, "R20"), (27, "R27")], [] ]
    folha_C = [ [(33, "R33"), (37, "R37")], [] ]
    folha_D = [ [(40, "R40"), (46, "R46")], [] ]
    folha_E = [ [(51, "R51"), (55, "R55")], [] ]
    folha_F = [ [(63, "R63"), (97, "R97")], [] ]
    
    lista_folhas = [folha_A, folha_B, folha_C, folha_D, folha_E, folha_F]

    # 2. NÍVEL INTERMEDIÁRIO [ [chaves], [filhos] ]
    no1_esq = [ [20, 33], [folha_A, folha_B, folha_C] ]
    
    # Nó direito
    no1_dir = [ [51, 63], [folha_D, folha_E, folha_F] ]

    # 3. RAIZ [ [chaves], [filhos] ]
    raiz = [ [40], [no1_esq, no1_dir] ]

    return raiz, lista_folhas

# testes
if __name__ == "__main__":
    arvore, folhas = construir_arvore_estatica()
    print("=== Estrutura ISAM Inicializada ===")
    print(f"Raiz: {arvore[0]}")
    print(f"Filhos da Raiz (Chaves dos nós intermediários): {arvore[1][0][0]} e {arvore[1][1][0]}")
    print(f"Primeira Folha (Primários): {folhas[0][0]}")
    print(f"Primeira Folha (Overflows): {folhas[0][1]}")