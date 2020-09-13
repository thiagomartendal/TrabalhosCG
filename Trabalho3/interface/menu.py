from PyQt5.QtWidgets import *
from interface.inserir.inserirObjeto import *

class Menu(QMenuBar):

    # Construtor
    def __init__(self, menu):
        super(Menu, self).__init__()
        self.__menuPrincipal = menu
        self.__menusInternos()
        self.__larguraMenu()

    # Largura da barra de menu
    def __larguraMenu(self):
        screen = QDesktopWidget().screenGeometry()
        self.__menuPrincipal.setFixedWidth(screen.width())

    # Menus de controle para adição de objetos
    def __menusInternos(self):
        inserir = self.__menuPrincipal.addMenu("Inserir")
        self.__menuPoligono = QAction('Polígono', self)
        self.__menuLinha = QAction('Linha', self)
        self.__menuPonto = QAction('Ponto', self)
        inserir.addAction(self.__menuPoligono)
        inserir.addAction(self.__menuLinha)
        inserir.addAction(self.__menuPonto)

    # Retorna menu poligo
    def menuPoligo(self):
        return self.__menuPoligono

    # Retorna menu linha
    def menuLinha(self):
        return self.__menuLinha

    # Retorna menu ponto
    def menuPonto(self):
        return self.__menuPonto
