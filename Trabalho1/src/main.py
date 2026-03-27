from src.core.isam_tree import ISAMTree
from src.core.page_manager import PageManager
from src.core.overflow_page import OverflowPage


class Menu:

    def __init__(self, arvore_isam):
        self.arvore = arvore_isam
        self.show_menu()

    def show_menu(self):
        print("=" * 60 + "\n")
        print("Qual operação deseja realizar?\n")
        print("[1] Visualizar árvore atual\n" + 
              "[2] Inserir nó\n" + 
              "[3] Remover nó" + "\n" + 
              "[4] Buscar nó\n" + 
              "[5] Sair\n")
        print("\n" + "=" * 60)
        option = input("Digite a opção desejada: ")

        if option == "1":
            self.arvore.get_tree()
        # elif option == "2":
        elif option == "3":
            key = input("Qual chave deseja remover?\n")
            self.arvore.remove(key)
        elif option == "4":
            key = input("Qual chave deseja buscar?\n")
            tuple = self.arvore.search(key)
            print(tuple)