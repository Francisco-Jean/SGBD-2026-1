from src.core.isam_tree import ISAMTree
from src.core.page_manager import PageManager
from src.core.overflow_page import OverflowPage


class Menu:

    def __init__(self, arvore_isam):
        self.arvore = arvore_isam
        self.show_menu()

    def show_menu(self):
        while True:
            print("=" * 60 + "\n")
            print("Qual operação deseja realizar?\n")
            print("[1] Visualizar árvore atual\n" + 
                  "[2] Inserir nó\n" + 
                  "[3] Remover nó" + "\n" + 
                  "[4] Buscar nó\n" + 
                  "[5] Exibir Métricas de Overflow\n" +
                  "[6] Sair\n")
            print("\n" + "=" * 60)
            option = input("Digite a opção desejada: ")

            if option == "1":
                self.arvore.get_tree()
                
            elif option == "2":
                key = input("Digite a chave para inserir: ")
                # Valor gerado automaticamente no padrão "RX"
                value = f"R{key}"
                self.arvore.insert(key, value)
                print(f"Sucesso: Nó ({key}, '{value}') processado!")
                
            elif option == "3":
                key = input("Qual chave deseja remover?\n")
                self.arvore.remove(int(key))
                
            elif option == "4":
                key = input("Qual chave deseja buscar?\n")
                tuple_rec = self.arvore.search(int(key))
                print(tuple_rec)
                
            elif option == "5":
                print(f"Páginas de overflow: {self.arvore.count_overflow_pages()}")
                print(f"Tamanho médio das cadeias: {self.arvore.average_overflow_length()}")
                
            elif option == "6":
                print("Encerrando...")
                break