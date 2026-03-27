"""
Trabalho1 - Sistema de Gerenciamento de Banco de Dados (SGBD)
Módulo principal para testes da árvore ISAM
"""

from src.core.isam_tree import ISAMTree
from src.main import Menu

# Criar instância da árvore ISAM
arvore_isam = ISAMTree()

# Testes
# arvore_isam.get_tree()

menu = Menu(arvore_isam)