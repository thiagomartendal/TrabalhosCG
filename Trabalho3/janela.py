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
from transformacao.primeiraTransformacao import *
from transformacao.segundaTransformacao import *
from transformacao.normalizacao import *
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
        self.__renderizar()

    # Definição da window para o sistema gráfico interativo
    def __definirWindow(self):
        screen = QDesktopWidget().screenGeometry()
        self.__window.setDimensao(screen.width(), screen.width())
        #self.__window.setDimensao(200, 200)

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
            objeto = inserirPoligono.getObj()
            self.__objetos.append(objeto)
            self.__renderizar()
            self.__painelL.atualizarLista(self.__objetos)

    # Dialogo para inserção de linha
    def __inserirLinha(self):
        inserirLinha = InserirObjeto(1)
        inserirLinha.exec_()
        if inserirLinha.getSinal() == 0:
            objeto = inserirLinha.getObj()
            self.__objetos.append(objeto)
            self.__renderizar()
            self.__painelL.atualizarLista(self.__objetos)

    # Dialogo para inserção de ponto
    def __inserirPonto(self):
        inserirPonto = InserirObjeto(2)
        inserirPonto.exec_()
        if inserirPonto.getSinal() == 0:
            objeto = inserirPonto.getObj()
            self.__objetos.append(objeto)
            self.__renderizar()
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
        self.__painelL.getBotoesTranslacao()[0].clicked.connect(lambda: self.__transladarTodos())
        self.__painelL.getBotoesTranslacao()[1].clicked.connect(lambda: self.__transladarObjeto())
        self.__painelL.getBotoesEscalonamento()[0].clicked.connect(lambda: self.__escalonarObjeto())
        self.__painelL.getBotoesRotacao()[0].clicked.connect(lambda: self.__rotacaoMundo())
        self.__painelL.getBotoesRotacao()[1].clicked.connect(lambda: self.__rotacaoCentroObjeto())
        self.__painelL.getBotoesRotacao()[2].clicked.connect(lambda: self.__rotacaoPontoQualquer())
        self.__painelL.getBotoesRotacao()[3].clicked.connect(lambda: self.__rotacaoWindow())

    # Cada um dos métodos abaixo deve ter uma instancia propria de PrimeiraTransformacao, para atualizar os dados
    # Função para chamada de zoomIn
    def __zoomIn(self):
        p = PrimeiraTransformacao(self.__objetos, self.__window, self.__viewport.coordenadas())
        p.zoomIn()
        self.__renderizar()
        self.__painelL.setZoom(10)

    # Função para chamada de zoomOut
    def __zoomOut(self):
        p = PrimeiraTransformacao(self.__objetos, self.__window, self.__viewport.coordenadas())
        p.zoomOut()
        self.__renderizar()
        self.__painelL.setZoom(-10)

    # Função para chamada de Up
    def __up(self):
        p = PrimeiraTransformacao(self.__objetos, self.__window, self.__viewport.coordenadas())
        p.up()
        self.__renderizar()

    # Função para chamada de Left
    def __left(self):
        p = PrimeiraTransformacao(self.__objetos, self.__window, self.__viewport.coordenadas())
        p.left()
        self.__renderizar()

    # Função para chamada de Right
    def __right(self):
        p = PrimeiraTransformacao(self.__objetos, self.__window, self.__viewport.coordenadas())
        p.right()
        self.__renderizar()

    # Função para chamada de Down
    def __down(self):
        p = PrimeiraTransformacao(self.__objetos, self.__window, self.__viewport.coordenadas())
        p.down()
        self.__renderizar()

    # Adição da viewport
    def __painelViewport(self):
        self.__viewport = Viewport(self.__window)
        self.__layoutHorizontal.addWidget(self.__viewport)

    # Ação para realizar a translação de um objeto
    def __transladarObjeto(self):
        pos = self.__painelL.getValoresTranslacao()[0]
        if pos == -1:
            QMessageBox.question(self, 'Atenção', 'Selecione um objeto para ser transladado.', QMessageBox.Ok)
        else:
            objeto = self.__objetos[pos]
            dx = self.__painelL.getValoresTranslacao()[1]
            dy = self.__painelL.getValoresTranslacao()[2]
            s = SegundaTransformacao()
            s.transladar(objeto, dx, dy)
            self.__renderizar()

    # Ação para realizar a translação de todos os objetos
    def __transladarTodos(self):
        for objeto in self.__objetos:
            dx = self.__painelL.getValoresTranslacao()[1]
            dy = self.__painelL.getValoresTranslacao()[2]
            s = SegundaTransformacao()
            s.transladar(objeto, dx, dy)
        self.__renderizar()

    # Ação para escalonar um objeto
    def __escalonarObjeto(self):
        pos = self.__painelL.getValoresEscalonamento()[0]
        if pos == -1:
            QMessageBox.question(self, 'Atenção', 'Selecione um objeto para ser escalonado.', QMessageBox.Ok)
        else:
            objeto = self.__objetos[pos]
            sx = self.__painelL.getValoresEscalonamento()[1]
            sy = self.__painelL.getValoresEscalonamento()[2]
            s = SegundaTransformacao()
            s.escalonarCentro(objeto, sx, sy)
            self.__renderizar()

    # Ação de rotação do mundo
    def __rotacaoMundo(self):
        pos = self.__painelL.getValoresRotacao()[0]
        if pos == -1:
            QMessageBox.question(self, 'Atenção', 'Selecione um objeto para ser Rotacionado.', QMessageBox.Ok)
        else:
            objeto = self.__objetos[pos]
            angulo = self.__painelL.getValoresRotacao()[1]
            s = SegundaTransformacao()
            s.rotacionarCentroMundo(objeto, angulo)
            self.__renderizar()

    # Ação de rotação do centro de um objeto
    def __rotacaoCentroObjeto(self):
        pos = self.__painelL.getValoresRotacao()[0]
        if pos == -1:
            QMessageBox.question(self, 'Atenção', 'Selecione um objeto para ser Rotacionado.', QMessageBox.Ok)
        else:
            objeto = self.__objetos[pos]
            angulo = self.__painelL.getValoresRotacao()[1]
            s = SegundaTransformacao()
            s.rotacionarCentroObjeto(objeto, angulo)
            self.__renderizar()

    # Ação de rotação de um objeto em relação a um ponto
    def __rotacaoPontoQualquer(self):
        pos = self.__painelL.getValoresRotacao()[0]
        if pos == -1:
            QMessageBox.question(self, 'Atenção', 'Selecione um objeto para ser Rotacionado.', QMessageBox.Ok)
        else:
            objeto = self.__objetos[pos]
            angulo = self.__painelL.getValoresRotacao()[1]
            x = self.__painelL.getValoresRotacao()[2]
            y = self.__painelL.getValoresRotacao()[3]
            s = SegundaTransformacao()
            s.rotacionarPontoGraus(objeto, [x, y], angulo)
            self.__renderizar()

    def __rotacaoWindow(self):
        angulo = self.__painelL.getValoresRotacao()[1]
        self.__window.addAngulo(angulo)
        self.__renderizar()

    # Acao de renderizar todos os objetos e eixos e a window
    def __renderizar(self):
        self.__viewport.renderizar(self.__objetos)
