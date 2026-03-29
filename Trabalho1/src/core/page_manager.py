from .primary_page import PrimaryPage
from .overflow_page import OverflowPage


class PageManager:
    """
    Gerenciador de operações entre páginas primárias e de overflow.
    Trata inserções, remoções e buscas considerando ambos os tipos de páginas.
    """
    
    @staticmethod
    def search_record_in_all_pages(primary_page, key):

        # Busca na página primária
        record = primary_page.search_record(key)
        if record:
            return ("primary", record)
        
        # Busca nas páginas de overflow
        overflow = primary_page.get_next_overflow()
        while overflow:
            record = overflow.search_record(key)
            if record:
                return ("overflow", record)
            overflow = overflow.get_next_page()
        
        return (None, None)
    
    @staticmethod
    def insert_with_overflow(primary_page, key, value, capacity=2):
        if not primary_page.is_full(capacity):
            primary_page.add_record(key, value)
            return True
        
        overflow = primary_page.get_next_overflow()
        
        if not overflow:
            overflow = OverflowPage()
            primary_page.add_overflow(overflow)
        
        while overflow.is_full(capacity):
            next_page = overflow.get_next_page()
            if not next_page:
                next_page = OverflowPage()
                overflow.set_next_page(next_page)
            overflow = next_page
        
        overflow.add_record(key, value)
        primary_page.sync_overflow_index()
        return True
    
    @staticmethod
    def remove_with_reorganization(primary_page, key):
        
        removed = False

        # Tenta remover da página primária
        if primary_page.remove_record(key):
            removed = True
        
        if not removed:
            # Tenta remover das páginas de overflow
            overflow = primary_page.get_next_overflow()
            
            while overflow:
                if overflow.remove_record(key):
                    removed = True
                    break
                
                overflow = overflow.get_next_page()
        
        if not removed:
            return False

        # Reorganiza para manter primária mais preenchida e cadeia limpa
        PageManager._reorganize_after_removal(primary_page)
        PageManager._clean_empty_overflows(primary_page)
        primary_page.sync_overflow_index()
        return True
    
    @staticmethod
    def _reorganize_after_removal(primary_page):
        capacity = 2

        while not primary_page.is_full(capacity):
            overflow = primary_page.get_next_overflow()
            if not overflow:
                break

            # Elimina overflows vazias no início da cadeia
            while overflow and not overflow.get_records():
                primary_page.set_next_overflow(overflow.get_next_page())
                overflow = primary_page.get_next_overflow()

            if not overflow:
                break

            key, value = overflow.get_records().pop(0)
            primary_page.add_record(key, value)

            if not overflow.get_records():
                primary_page.set_next_overflow(overflow.get_next_page())
    
    @staticmethod
    def _clean_empty_overflows(primary_page):
        """
        Remove páginas de overflow que ficaram vazias.
        Mantém a página primária intacta mesmo se vazia.
        """
        head = primary_page.get_next_overflow()

        # Ajusta cabeça da cadeia
        while head and not head.get_records():
            head = head.get_next_page()

        current = head
        while current:
            while current.get_next_page() and not current.get_next_page().get_records():
                current.set_next_page(current.get_next_page().get_next_page())
            current = current.get_next_page()

        primary_page.set_next_overflow(head)
    
    @staticmethod
    def get_all_records(primary_page):
        """
        Lista todos os registros de uma página primária e suas overflows.
        """
        records = primary_page.get_records()[:]
        
        overflow = primary_page.get_next_overflow()
        while overflow:
            records.extend(overflow.get_records())
            overflow = overflow.get_next_page()
        
        return sorted(records, key=lambda x: x[0])
