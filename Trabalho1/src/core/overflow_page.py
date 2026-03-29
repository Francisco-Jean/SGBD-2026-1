class OverflowPage:
    """
    Representa uma página de overflow da árvore ISAM.
    Armazena registros que não cabem mais na página primária.
    Mantém referência à próxima página de overflow (encadeamento).
    """
    
    def __init__(self, records=None):
        """
        Inicializa uma página de overflow.
        
        Args:
            records: Lista de tuplas (chave, valor) armazenadas na página.
                     Se None, inicia vazia.
        """
        self.records = records if records is not None else []
        self.next_page = None  # Referência à próxima página de overflow
    
    def add_record(self, key, value):
        """
        Adiciona um registro (chave, valor) à página de overflow.
        
        Args:
            key: Chave do registro (inteiro)
            value: Valor associado à chave (string)
        """
        self.records.append((key, value))
        self.records.sort(key=lambda x: x[0])
    
    def remove_record(self, key):
        """
        Remove um registro pela chave.
        
        Args:
            key: Chave do registro a remover
            
        Returns:
            True se removeu, False se não encontrou
        """
        for i, (k, v) in enumerate(self.records):
            if k == key:
                self.records.pop(i)
                return True
        return False
    
    def search_record(self, key):
        """
        Busca um registro pela chave nesta página de overflow.
        
        Args:
            key: Chave a buscar
            
        Returns:
            Tupla (chave, valor) se encontrar, None caso contrário
        """
        for k, v in self.records:
            if k == key:
                return (k, v)
        return None
    
    def get_records(self):
        """Retorna a lista de todos os registros."""
        return self.records
    
    def set_next_page(self, next_page):
        """Define a próxima página de overflow."""
        self.next_page = next_page
    
    def get_next_page(self):
        """Obtém a próxima página de overflow."""
        return self.next_page
    
    def is_full(self, capacity=2):
        """
        Verifica se a página está cheia.
        
        Args:
            capacity: Número máximo de registros (padrão: 2)
            
        Returns:
            True se está cheia, False caso contrário
        """
        return len(self.records) >= capacity
    
    def __repr__(self):
        has_next = "yes" if self.next_page else "no"
        return f"OverflowPage(records={self.records}, has_next={has_next})"
