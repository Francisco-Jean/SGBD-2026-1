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
        return True
    
    @staticmethod
    def remove_with_reorganization(primary_page, key):
        
        # Tenta remover da página primária
        if primary_page.remove(key):

            PageManager._clean_empty_overflows(primary_page)
            return True
        
        # Tenta remover das páginas de overflow
        overflow = primary_page.get_next_overflow()
        
        while overflow:
            if overflow.remove(key):
                # Remove páginas de overflow vazias
                PageManager._clean_empty_overflows(primary_page)
                return True
            
            overflow = overflow.get_next_page()
        
        return False
    
    @staticmethod
    def _reorganize_after_removal(primary_page):
        
        overflow = primary_page.get_next_overflow()
        capacity = 2
        
        while overflow and not primary_page.is_full(capacity):
            # Move registros da primeira página de overflow para primária
            while overflow.get_records() and not primary_page.is_full(capacity):
                key, value = overflow.get_records().pop(0)
                primary_page.add_record(key, value)
            
            # Se overflow ficou vazia, passa para próxima
            if not overflow.get_records():
                overflow = overflow.get_next_page()
                if overflow:
                    primary_page.add_overflow(overflow)
    
    @staticmethod
    def _clean_empty_overflows(primary_page):
        """
        Remove páginas de overflow que ficaram vazias.
        Mantém a página primária intacta mesmo se vazia.
        """
        overflow = primary_page.get_next_overflow()
        previous = None
        
        while overflow:
            if not overflow.get_records():
                # Remove página de overflow vazia
                if previous:
                    previous.set_next_page(overflow.get_next_page())
                else:
                    # Primeira overflow está vazia
                    primary_page.add_overflow(overflow.get_next_page())
                
                overflow = overflow.get_next_page()
            else:
                previous = overflow
                overflow = overflow.get_next_page()
    
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
