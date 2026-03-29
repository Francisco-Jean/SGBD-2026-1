"""
Trabalho1 - Sistema de Gerenciamento de Banco de Dados (SGBD)
Pacote principal da simulação ISAM.
"""

from src.core.isam_tree import ISAMTree
from src.main import Menu

__all__ = ["ISAMTree", "Menu", "run"]


def run():
    """Ponto de entrada opcional para iniciar o menu interativo."""
    arvore_isam = ISAMTree()
    Menu(arvore_isam)
