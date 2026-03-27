# lógica: vai ser passada a chave pra remover e eu tenho que buscar a chave pra remover e vão ter essas situações: 
# 1 - existe o nó sem filhos (só remove o nó)
# 2 - existe o nó com um filho (substitui o nó pelo filho)

from ..core import isam_tree

def search_key(isam_tree, key):
    """
    Função para buscar a chave na árvore ISAM.
    Retorna o nó folha onde a chave está localizada ou None se não for encontrada.
    """
    raiz = isam_tree[0][0]

    if key<=raiz:
        subtree = isam_tree[1][0]
    elif key>raiz:
        subtree = isam_tree[1][1]
    
    # Subtree tem formato: [[51, 63], [[[(40, 'R40'), (46, 'R46')], []], [[(51, 'R51'), (55, 'R55')], []], [[(63, 'R63'), (97, 'R97')], []]]]
    left, right = subtree[0]
    if key<left:
        primary_page = subtree[1][0]
    elif left<=key<right:
        primary_page = subtree[1][1]
    elif left<=key<right:
        primary_page = subtree[1][2]

    print(primary_page)
    


        



# def remove_key(isam_tree, key):

