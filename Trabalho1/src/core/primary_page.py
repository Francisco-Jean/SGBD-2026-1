class PrimaryPage:
    """
    Representa uma página folha primária da árvore ISAM.
    Contém registros primários e referências para páginas de overflow.
    
    Estrutura: [ [records], [overflows] ]
    """
    
    def __init__(self, records=None):
        """
        Inicializa uma página folha primária.
        
        Args:
            records: Lista de tuplas (chave, valor) armazenadas na página.
                     Se None, inicia vazia.
        """
        self.records = records if records is not None else []
        self.overflows = []  # Lista de páginas de overflow
        self.next_overflow = None  # Referência à primeira página de overflow (encadeamento)
    
    def add_record(self, key, value):
        """
        Adiciona um registro (chave, valor) à página primária.
        
        Args:
            key: Chave do registro (inteiro)
            value: Valor associado à chave (string, ex: "R10")
        """
        self.records.append((key, value))
        # Ordena os registros por chave
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
        Busca um registro pela chave.
        
        Args:
            key: Chave a buscar
            
        Returns:
            Tupla (chave, valor) se encontrar, None caso contrário
        """
        for k, v in self.records:
            if k == key:
                return (k, v)
        return None
    
    def add_overflow(self, overflow_page):
        """
        Adiciona uma página de overflow.
        
        Args:
            overflow_page: Instância de OverflowPage
        """
        if overflow_page is None:
            return

        if not self.next_overflow:
            self.next_overflow = overflow_page
            self.sync_overflow_index()
            return

        tail = self.next_overflow
        visited = {id(tail)}

        # Evita loop acidental no encadeamento
        while tail.get_next_page() and id(tail.get_next_page()) not in visited:
            tail = tail.get_next_page()
            visited.add(id(tail))

        tail.set_next_page(overflow_page)
        self.sync_overflow_index()

    def set_next_overflow(self, overflow_page):
        """Define explicitamente a primeira página de overflow."""
        self.next_overflow = overflow_page
        self.sync_overflow_index()

    def sync_overflow_index(self):
        """
        Reconstrói a lista auxiliar de overflows com base no encadeamento.
        Mantém `overflows` e `next_overflow` consistentes.
        """
        self.overflows = []
        current = self.next_overflow
        seen = set()

        while current and id(current) not in seen:
            seen.add(id(current))
            self.overflows.append(current)
            current = current.get_next_page()
    
    def get_next_overflow(self):
        """Obtém a primeira página de overflow."""
        return self.next_overflow
    
    def get_records(self):
        """Retorna a lista de todos os registros."""
        return self.records
    
    def get_overflows(self):
        """Retorna a lista de todas as páginas de overflow."""
        return self.overflows
    
    def is_full(self, capacity=2):
        """
        Verifica se a página atingiu a capacidade máxima.
        
        Args:
            capacity: Número máximo de registros (padrão: 2)
            
        Returns:
            True se está cheia, False caso contrário
        """
        return len(self.records) >= capacity
    
    def get_structure_content(self):
        """Retorna a estrutura compatível com a representação anterior."""
        return [self.records, self.overflows]
    
    def __repr__(self):
        return f"PrimaryPage(records={self.records}, overflows={len(self.overflows)})"
