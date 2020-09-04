# coding: utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from decimal import Decimal
from window.window import *
from interface.viewport import *
from interface.painelLateral import *
from interface.menu import *
from objeto.poligono import *
import sys
import math

class Janela(QWidget):
    __layoutVertical = QVBoxLayout() # Layout Principal vertical
    __layoutHorizontal = QHBoxLayout() # Layout Principal horizontal
    __window = Window() # Instancia da Window
    __objetos = [] # Lista de objetos criados

    # Construtor com definições da classe
    def __init__(self, parent=None):
        super(Janela, self).__init__()
        self.__menuF = self.__menuLateral()
        self.setWindowTitle("Computação Gráfica")
        self.resize(1000, 800)
        self.setLayout(self.__layoutVertical)
        self.__definirWindow()
        self.__painelViewport()
        self.__barraMenu()
        painel = QFrame();
        painel.setLayout(self.__layoutHorizontal)
        self.__layoutVertical.addWidget(painel)

    # Definição da window para o sistema gráfico interativo
    def __definirWindow(self):
        screen = QDesktopWidget().screenGeometry()
        self.__window.setCoordenadas(screen.width(), screen.height())

    # Barra de Menu
    def __barraMenu(self):
        self.__menu = Menu(QMenuBar(self))
        self.__layoutVertical.addWidget(self.__menu)
        self.__menu.menuPoligo().triggered.connect(self.__inserirPoligono)
        self.__menu.menuLinha().triggered.connect(self.__inserirLinha)
        self.__menu.menuPonto().triggered.connect(self.__inserirPonto)

    # Dialogo para inserção de poligono
    def __inserirPoligono(self):
        inserirPoligono = InserirObjeto(0)
        inserirPoligono.exec_()
        if inserirPoligono.getSinal() == 0:
            self.__objetos.append(inserirPoligono.getObj())
            self.__viewport.renderizar(self.__objetos)
            self.__painelL.atualizarLista(self.__objetos)

    # Dialogo para inserção de linha
    def __inserirLinha(self):
        inserirLinha = InserirObjeto(1)
        inserirLinha.exec_()
        if inserirLinha.getSinal() == 0:
            self.__objetos.append(inserirLinha.getObj())
            self.__viewport.renderizar(self.__objetos)
            self.__painelL.atualizarLista(self.__objetos)

    # Dialogo para inserção de ponto
    def __inserirPonto(self):
        inserirPonto = InserirObjeto(2)
        inserirPonto.exec_()
        if inserirPonto.getSinal() == 0:
            self.__objetos.append(inserirPonto.getObj())
            self.__viewport.renderizar(self.__objetos)
            self.__painelL.atualizarLista(self.__objetos)

    # Menu lateral de propriedades
    def __menuLateral(self):
        self.__painelL = PainelLateral()
        self.__layoutHorizontal.addWidget(self.__painelL)
        self.__painelL.getBotoesWindow()[0].clicked.connect(lambda: self.__zoomIn())
        self.__painelL.getBotoesWindow()[1].clicked.connect(lambda: self.__zoomOut())
        self.__painelL.getBotoesWindow()[2].clicked.connect(lambda: self.__up())
        self.__painelL.getBotoesWindow()[3].clicked.connect(lambda: self.__left())
        self.__painelL.getBotoesWindow()[4].clicked.connect(lambda: self.__right())
        self.__painelL.getBotoesWindow()[5].clicked.connect(lambda: self.__down())

    # Cada um dos métodos abaixo deve ter uma instancia propria de PrimeiraTransformacao, para atualizar os dados
    # Função para chamada de zoomIn
    def __zoomIn(self):
        p = PrimeiraTransformacao(self.__objetos, self.__window, self.__viewport.coordenadas())
        p.zoomIn()
        self.__viewport.renderizar(self.__objetos)
        self.__painelL.setZoom(10)

    # Função para chamada de zoomOut
    def __zoomOut(self):
        p = PrimeiraTransformacao(self.__objetos, self.__window, self.__viewport.coordenadas())
        p.zoomOut()
        self.__viewport.renderizar(self.__objetos)
        self.__painelL.setZoom(-10)

    # Função para chamada de Up
    def __up(self):
        p = PrimeiraTransformacao(self.__objetos, self.__window, self.__viewport.coordenadas())
        p.up()
        self.__viewport.renderizar(self.__objetos)

    # Função para chamada de Left
    def __left(self):
        p = PrimeiraTransformacao(self.__objetos, self.__window, self.__viewport.coordenadas())
        p.left()
        self.__viewport.renderizar(self.__objetos)

    # Função para chamada de Right
    def __right(self):
        p = PrimeiraTransformacao(self.__objetos, self.__window, self.__viewport.coordenadas())
        p.right()
        self.__viewport.renderizar(self.__objetos)

    # Função para chamada de Down
    def __down(self):
        p = PrimeiraTransformacao(self.__objetos, self.__window, self.__viewport.coordenadas())
        p.down()
        self.__viewport.renderizar(self.__objetos)

    # Adição da viewport
    def __painelViewport(self):
        self.__viewport = Viewport(self.__window)
        self.__layoutHorizontal.addWidget(self.__viewport)
