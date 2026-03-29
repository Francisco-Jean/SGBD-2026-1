# src/core/isam_tree.py
from ..operations import remover
from ..operations import searcher
from ..metrics.search_metrics import SearchMetrics
from .page_manager import PageManager
from .primary_page import PrimaryPage

# Capacidade máxima definida pelo escopo (2 registros por página folha/overflow)
CAPACIDADE_PAGINA = 2


class ISAMTree:
    """
    Classe que representa uma árvore ISAM (Indexed Sequential Access Method).
    """
    
    def __init__(self):
        """Inicializa a árvore ISAM com estrutura predefinida."""
        self.raiz = None
        self.folhas = []
        self.search_metrics = SearchMetrics()
        self._construir_arvore_estatica()
    
    def _construir_arvore_estatica(self):
        """
        Constrói a estrutura ISAM inicial usando listas aninhadas.
        Define a raiz e a lista com as folhas para facilitar a varredura.
        """
        
        # PÁGINAS FOLHA PRIMÁRIAS [ [registros], [overflows] ]
        folha_A = [ [(10, "R10"), (15, "R15")], [] ]
        folha_B = [ [(20, "R20"), (27, "R27")], [] ]
        folha_C = [ [(33, "R33"), (37, "R37")], [] ]
        folha_D = [ [(40, "R40"), (46, "R46")], [] ]
        folha_E = [ [(51, "R51"), (55, "R55")], [] ]
        folha_F = [ [(63, "R63"), (97, "R97")], [] ]
        
        self.folhas = [folha_A, folha_B, folha_C, folha_D, folha_E, folha_F]
        no1_esq = [ [20, 33], [folha_A, folha_B, folha_C] ]
        no1_dir = [ [51, 63], [folha_D, folha_E, folha_F] ]
        self.raiz = [ [40], [no1_esq, no1_dir] ]
    
    def get_raiz(self):
        return self.raiz
    
    def get_folhas(self):
        return self.folhas
    
    def get_tree(self):
        print("\nRaiz:")
        print(f"  Chaves: {self.get_raiz()[0]}")
        print(f"  Filhos: {len(self.get_raiz()[1])}")

        print("\nNós Intermediários:")
        for i, no in enumerate(self.get_raiz()[1]):
            print(f"  Nó {i + 1}:")
            print(f"    Chaves: {no[0]}")
            print(f"    Filhos (folhas): {len(no[1])}")

        print("\nFolhas Primárias:")
        for i, folha in enumerate(self.get_folhas()):
            print(f"  Folha {i + 1}: {folha[0]}")

        print("\n" + "=" * 60)
    
    def remove(self, key):
        primary_page = self._navigate_to_primary_page(key)
        if primary_page:
            return PageManager.remove_with_reorganization(primary_page, key)
        return False
    
    def search(self, key):
        result = searcher.search_equal(self.raiz, key, metrics=self.search_metrics)
        return (result["location"], result["record"])

    def search_interval(self, start_key, end_key):
        return searcher.search_range(self.raiz, start_key, end_key)

    def get_equality_search_metrics(self):
        return self.search_metrics.get_equality_metrics()
    
    def _navigate_to_primary_page(self, key):
        """
        Navega pela árvore até encontrar a página primária correta para a chave.
        """
        raiz = self.raiz[0][0]
        
        # Escolhe qual nó intermediário seguir
        if int(key) <= raiz:
            no_intermediario = self.raiz[1][0]
        else:
            no_intermediario = self.raiz[1][1]
        
        # Encontra a folha primária correta baseado nas chaves do nó intermediário
        chaves = no_intermediario[0]
        folhas = no_intermediario[1]
        
        key_int = int(key)
        
        if key_int < chaves[0]:
            folha_lista = folhas[0]
        elif key_int < chaves[1]:
            folha_lista = folhas[1]
        else:
            folha_lista = folhas[2]
        
        # Converte a lista para uma instância de PrimaryPage
        return PrimaryPage(folha_lista[0])
