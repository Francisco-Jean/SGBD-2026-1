from src.core.isam_tree import ISAMTree


class Menu:
    def __init__(self, arvore_isam):
        self.arvore = arvore_isam
        self.show_menu()

    def show_menu(self):
        while True:
            print("=" * 60 + "\n")
            print("Qual operação deseja realizar?\n")
            print("[1] Visualizar árvore atual\n" + 
                  "[2] Inserir nó manual\n" + 
                  "[3] Remover nó\n" + 
                  "[4] Buscar nó\n" + 
                  "[5] Exibir Métricas de Overflow\n" +
                  "[6] Executar Inserções Obrigatórias (Lote)\n" +
                  "[7] Sair\n")
            print("\n" + "=" * 60)
            option = input("Digite a opção desejada: ")

            if option == "1":
                self.arvore.get_tree()
                
            elif option == "2":
                key = input("Digite a chave para inserir: ")
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
                # Chaves obrigatórias
                chaves_obrigatorias = [18, 22, 27, 35, 41, 44, 63, 67, 83, 86, 121, 145]
                print("\nIniciando carga obrigatória...")
                for key in chaves_obrigatorias:
                    value = f"R{key}"
                    if self.arvore.insert(key, value):
                        print(f"Inserido: ({key}, '{value}')")
                    else:
                        print(f"Falha ao inserir: {key}")
                print("Carga obrigatória concluída com sucesso!")
                
            elif option == "7":
                print("Encerrando...")
                break
