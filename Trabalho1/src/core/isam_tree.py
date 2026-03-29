# src/core/isam_tree.py
from ..operations import remover
from .page_manager import PageManager
from .primary_page import PrimaryPage
from .overflow_page import OverflowPage

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
        total_paginas = 0
        total_registros = 0
        for folha in self.folhas:
            total_paginas += len(folha[1])
            for pagina_lista in folha[1]:
                total_registros += len(pagina_lista)
        if total_paginas == 0:
            return 0.0
        return round(total_registros / total_paginas, 2)
    
    def remove(self, key):
        primary_page, folha_lista = self._navigate_to_primary_page(key)
        if primary_page:
            resultado = PageManager.remove_with_reorganization(primary_page, key)
            self._sync_page_to_list(primary_page, folha_lista)
            return resultado
        return False
    
    def search(self, key):
        # Navega até a página primária correta
        primary_page, _ = self._navigate_to_primary_page(key)
        if primary_page:
            return PageManager.search_record_in_all_pages(primary_page, key)
        return (None, None)
    
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
        page = PrimaryPage(folha_lista[0].copy())
        
        previous_overflow = None
        for over_list in folha_lista[1]:
            over_page = OverflowPage(over_list.copy())
            if previous_overflow is None:
                page.add_overflow(over_page)
            else:
                previous_overflow.set_next_page(over_page)
                page.overflows.append(over_page)
            previous_overflow = over_page
            
        return page, folha_lista

    def _sync_page_to_list(self, primary_page, folha_lista):
        folha_lista[0] = primary_page.get_records()
        
        overflows_list = []
        over_page = primary_page.get_next_overflow()
        while over_page:
            if over_page.get_records():
                overflows_list.append(over_page.get_records())
            over_page = over_page.get_next_page()
            
        folha_lista[1] = overflows_list