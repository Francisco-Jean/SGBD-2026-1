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
        return PageManager.insert_with_overflow_details(
            primary_page, key, value, capacity
        )["success"]

    @staticmethod
    def insert_with_overflow_details(primary_page, key, value, capacity=2):
        overflow_pages_visited = 0
        overflow_pages_created = 0

        if not primary_page.is_full(capacity):
            primary_page.add_record(key, value)
            return {
                "success": True,
                "overflow_pages_visited": overflow_pages_visited,
                "overflow_pages_created": overflow_pages_created,
            }
        
        overflow = primary_page.get_next_overflow()
        
        if not overflow:
            overflow = OverflowPage()
            primary_page.add_overflow(overflow)
            overflow_pages_created += 1

        overflow_pages_visited += 1
        
        while overflow.is_full(capacity):
            next_page = overflow.get_next_page()
            if not next_page:
                next_page = OverflowPage()
                overflow.set_next_page(next_page)
                overflow_pages_created += 1
            overflow = next_page
            overflow_pages_visited += 1
        
        overflow.add_record(key, value)
        primary_page.sync_overflow_index()
        return {
            "success": True,
            "overflow_pages_visited": overflow_pages_visited,
            "overflow_pages_created": overflow_pages_created,
        }
    
    @staticmethod
    def remove_with_reorganization(primary_page, key):
        return PageManager.remove_with_reorganization_details(primary_page, key)["success"]

    @staticmethod
    def remove_with_reorganization_details(primary_page, key):
        
        removed = False
        overflow_pages_visited = 0

        # Tenta remover da página primária
        if primary_page.remove_record(key):
            removed = True
        
        if not removed:
            # Tenta remover das páginas de overflow
            overflow = primary_page.get_next_overflow()
            
            while overflow:
                overflow_pages_visited += 1
                if overflow.remove_record(key):
                    removed = True
                    break
                
                overflow = overflow.get_next_page()
        
        if not removed:
            return {
                "success": False,
                "overflow_pages_visited": overflow_pages_visited,
            }

        # Reorganiza para manter primária mais preenchida e cadeia limpa
        overflow_pages_visited += PageManager._reorganize_after_removal(primary_page)
        overflow_pages_visited += PageManager._clean_empty_overflows(primary_page)
        primary_page.sync_overflow_index()
        return {
            "success": True,
            "overflow_pages_visited": overflow_pages_visited,
        }
    
    @staticmethod
    def _reorganize_after_removal(primary_page):
        capacity = 2
        overflow_pages_touched = 0

        while not primary_page.is_full(capacity):
            overflow = primary_page.get_next_overflow()
            if not overflow:
                break

            # Elimina overflows vazias no início da cadeia
            while overflow and not overflow.get_records():
                overflow_pages_touched += 1
                primary_page.set_next_overflow(overflow.get_next_page())
                overflow = primary_page.get_next_overflow()

            if not overflow:
                break

            overflow_pages_touched += 1
            key, value = overflow.get_records().pop(0)
            primary_page.add_record(key, value)

            if not overflow.get_records():
                primary_page.set_next_overflow(overflow.get_next_page())

        return overflow_pages_touched
    
    @staticmethod
    def _clean_empty_overflows(primary_page):
        """
        Remove páginas de overflow que ficaram vazias.
        Mantém a página primária intacta mesmo se vazia.
        """
        head = primary_page.get_next_overflow()
        overflow_pages_touched = 0

        # Ajusta cabeça da cadeia
        while head and not head.get_records():
            overflow_pages_touched += 1
            head = head.get_next_page()

        current = head
        while current:
            overflow_pages_touched += 1
            while current.get_next_page() and not current.get_next_page().get_records():
                overflow_pages_touched += 1
                current.set_next_page(current.get_next_page().get_next_page())
            current = current.get_next_page()

        primary_page.set_next_overflow(head)
        return overflow_pages_touched
    
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
