# src/core/isam_tree.py
from ..operations import searcher
from ..metrics.search_metrics import SearchMetrics
from .page_manager import PageManager
from .primary_page import PrimaryPage
from .overflow_page import OverflowPage


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

        # Nível intermediário 2: cada nó aponta para uma folha primária específica
        no2_A = [[10, 15], [folha_A]]
        no2_B = [[20, 27], [folha_B]]
        no2_C = [[33, 37], [folha_C]]
        no2_D = [[40, 46], [folha_D]]
        no2_E = [[51, 55], [folha_E]]
        no2_F = [[63, 97], [folha_F]]

        # Nível intermediário 1
        no1_esq = [[20, 33], [no2_A, no2_B, no2_C]]
        no1_dir = [[51, 63], [no2_D, no2_E, no2_F]]

        # Raiz
        self.raiz = [ [40], [no1_esq, no1_dir] ]
    
    def get_raiz(self):
        return self.raiz
    
    def get_folhas(self):
        return self.folhas
    
    def get_tree(self):
        print("\nRaiz:")
        print(f"  Chaves: {self.get_raiz()[0]}")
        print(f"  Filhos: {len(self.get_raiz()[1])}")

        print("\nNós Intermediários - Nível 1:")
        for i, no_n1 in enumerate(self.get_raiz()[1]):
            print(f"  Nó N1.{i + 1}:")
            print(f"    Chaves: {no_n1[0]}")
            print(f"    Filhos (nós N2): {len(no_n1[1])}")

        print("\nNós Intermediários - Nível 2:")
        for i, no_n1 in enumerate(self.get_raiz()[1]):
            for j, no_n2 in enumerate(no_n1[1]):
                print(f"  Nó N2.{i + 1}.{j + 1}:")
                print(f"    Chaves: {no_n2[0]}")
                print(f"    Filhos (folhas): {len(no_n2[1])}")

        print("\nFolhas Primárias:")
        for i, folha in enumerate(self.get_folhas()):
            print(f"  Folha {i + 1}: {folha[0]}")
            if folha[1]:
                print(f"    Overflows: {folha[1]}")

        print("\n" + "=" * 60)
    
    def insert(self, key, value):
        primary_page, folha_lista = self._navigate_to_primary_page(key)
        if primary_page:
            sucesso = PageManager.insert_with_overflow(primary_page, int(key), value)
            if sucesso:
                self._sync_page_to_list(primary_page, folha_lista)
            return sucesso
        return False

    def count_overflow_pages(self):
        total_overflows = 0
        for folha in self.folhas:
            total_overflows += len(folha[1])
        return total_overflows

    def average_overflow_length(self):
        """
        Tamanho médio das cadeias de overflow (em páginas por folha com overflow).
        """
        cadeias = [len(folha[1]) for folha in self.folhas if folha[1]]
        if not cadeias:
            return 0.0
        return round(sum(cadeias) / len(cadeias), 2)

    def count_leaf_pages(self):
        return len(self.folhas)
    
    def remove(self, key):
        primary_page, folha_lista = self._navigate_to_primary_page(key)
        if primary_page:
            resultado = PageManager.remove_with_reorganization(primary_page, key)
            self._sync_page_to_list(primary_page, folha_lista)
            return resultado
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
        if int(key) < raiz:
            no_intermediario = self.raiz[1][0]
        else:
            no_intermediario = self.raiz[1][1]
        
        # Nível intermediário 1 -> escolhe nó intermediário 2
        chaves = no_intermediario[0]
        nos_n2 = no_intermediario[1]
        
        key_int = int(key)
        
        if key_int < chaves[0]:
            no_n2 = nos_n2[0]
        elif key_int < chaves[1]:
            no_n2 = nos_n2[1]
        else:
            no_n2 = nos_n2[2]

        # Nível intermediário 2 -> folha primária
        folha_lista = no_n2[1][0] if not self._is_leaf_page(no_n2) else no_n2

        # Converte a lista para uma instância de PrimaryPage
        page = PrimaryPage(folha_lista[0].copy())
        
        for over_list in folha_lista[1]:
            over_page = OverflowPage(over_list.copy())
            page.add_overflow(over_page)
            
        return page, folha_lista

    @staticmethod
    def _is_leaf_page(node):
        if not isinstance(node, list) or len(node) != 2:
            return False
        records = node[0]
        if not isinstance(records, list):
            return False
        if not records:
            return True
        return isinstance(records[0], tuple)

    def _sync_page_to_list(self, primary_page, folha_lista):
        folha_lista[0] = primary_page.get_records()
        
        overflows_list = []
        over_page = primary_page.get_next_overflow()
        while over_page:
            if over_page.get_records():
                overflows_list.append(over_page.get_records())
            over_page = over_page.get_next_page()
            
        folha_lista[1] = overflows_list
