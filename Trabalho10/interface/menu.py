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
        objetos2D = inserir.addMenu("Objetos 2D")
        objetos3D = inserir.addMenu("Objetos 3D")
        self.__menuPoligono2D = QAction('Polígono', self)
        self.__menuLinha2D = QAction('Linha', self)
        self.__menuPonto2D = QAction('Ponto', self)
        self.__menuCurva2D = QAction('Curva', self)
        self.__menuBSpline2D = QAction('BSpline', self)
        self.__menuModeloArame = QAction('Modelo de Arame', self)
        self.__bezier = QAction('Bézier', self)
        self.__spline = QAction('Spline', self)
        objetos2D.addAction(self.__menuPoligono2D)
        objetos2D.addAction(self.__menuLinha2D)
        objetos2D.addAction(self.__menuPonto2D)
        objetos2D.addAction(self.__menuCurva2D)
        objetos2D.addAction(self.__menuBSpline2D)
        objetos3D.addAction(self.__menuModeloArame)
        superficiesBicubicas = objetos3D.addMenu('Superfícies Bicúbicas')
        superficiesBicubicas.addAction(self.__bezier)
        superficiesBicubicas.addAction(self.__spline)

    # Retorna menu abrir
    def menuAbrir(self):
        return self.__menuAbrir

    # Retorna menu salvar
    def menuSalvar(self):
        return self.__menuSalvar

    # Retorna menu poligo2D
    def menuPoligo2D(self):
        return self.__menuPoligono2D

    # Retorna menu linha2D
    def menuLinha2D(self):
        return self.__menuLinha2D

    # Retorna menu ponto2D
    def menuPonto2D(self):
        return self.__menuPonto2D

    # Retorna menu curva2D
    def menuCurva2D(self):
        return self.__menuCurva2D

    # Retorna menu curvaBSpline2D
    def menuBSpline2D(self):
        return self.__menuBSpline2D

    # Retorna menu poligo3D
    def menuPoligo3D(self):
        return self.__menuModeloArame

    # Retorna menu bezier
    def menuBezier(self):
        return self.__bezier

    # Retorna menu spline
    def menuSpline(self):
        return self.__spline
