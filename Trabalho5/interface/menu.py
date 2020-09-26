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
        arquivo = self.__menuPrincipal.addMenu("Arquivo")
        self.__menuAbrir = QAction('Abrir Obj', self)
        self.__menuSalvar = QAction('Salvar Obj', self)
        arquivo.addAction(self.__menuAbrir)
        arquivo.addAction(self.__menuSalvar)
        inserir = self.__menuPrincipal.addMenu("Inserir")
        self.__menuPoligono = QAction('Polígono', self)
        self.__menuLinha = QAction('Linha', self)
        self.__menuPonto = QAction('Ponto', self)
        self.__menuCurva = QAction('Curva', self)
        inserir.addAction(self.__menuPoligono)
        inserir.addAction(self.__menuLinha)
        inserir.addAction(self.__menuPonto)
        inserir.addAction(self.__menuCurva)

    # Retorna menu abrir
    def menuAbrir(self):
        return self.__menuAbrir

    # Retorna menu salvar
    def menuSalvar(self):
        return self.__menuSalvar

    # Retorna menu poligo
    def menuPoligo(self):
        return self.__menuPoligono

    # Retorna menu linha
    def menuLinha(self):
        return self.__menuLinha

    # Retorna menu ponto
    def menuPonto(self):
        return self.__menuPonto

    # Retorna menu curva
    def menuCurva(self):
        return self.__menuCurva
