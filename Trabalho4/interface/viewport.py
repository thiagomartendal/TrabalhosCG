from PyQt5.QtWidgets import *
from transformacao.primeiraTransformacao import *
from transformacao.normalizacao import *
from interface.clipping import *
from objeto.linha import *
from objeto.poligono import *

class Viewport(QFrame):
    __coordenadas = [] # Coordenadas do viewport

    # Cosntrutor
    def __init__(self, window, parent=None):
        super(Viewport, self).__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.__viewport = QGraphicsView()
        self.__viewport.setScene(QGraphicsScene())
        vp = QLabel("Viewport")
        vp.setStyleSheet("font-weight: bold;")
        layout.addWidget(vp)
        layout.addWidget(self.__viewport)
        self.__coordenadas = [0, 0, self.__viewport.width(), self.__viewport.height()]
        self.__window = window
        self.__clipping = Clipping(self.__coordenadas)
        self.__viewportRetangulo = self.__criarViewportRetangulo(self.__coordenadas)

    # def deslocamento(self, valorDeslocado):
        # self.__clipping.distanciaPontos(valorDeslocado)

    # Retorna o painel do viewport
    def painel(self):
        return self.__viewport

    # Renderiza os objetos na viewport
    def renderizar(self, objetos):
        self.__viewport.update()
        self.__viewport.scene().clear()
        # transformada de viewport
        #primaeiraTransformacao = PrimeiraTransformacao(objetos, self.__window, self.__coordenadas)
        #primaeiraTransformacao.transformadaViewport()

        # normalizacao
        n = Normalizacao(self.__window, self.__coordenadas)
        objetos = self.__eixos() + objetos
        for objeto in objetos:
            n.normalizar(objeto)
            n.view(objeto)
            self.__clipping.clip(objeto)

        # desenhar na tela
        for objeto in self.__viewportRetangulo + objetos:
            objeto.desenhar(self.painel)

    # Retorna coordenadas da viewport
    def coordenadas(self):
        return self.__coordenadas

     # Retorna uma lista com eixos X e Y do mundo em cinza
    def __eixos(self):
        eixoX = Linha('EixoX', [EstruturaPonto(0, -100), EstruturaPonto(0, 100)])
        eixoX.setCor(200,200,200)
        eixoY = Linha('EixoY', [EstruturaPonto(-100, 0), EstruturaPonto(100, 0)])
        eixoY.setCor(200,200,200)
        return [eixoX, eixoY]

    # Retorna uma lista com a viewport em vermelho
    def __criarViewportRetangulo(self, c):
        view = Poligono('Window', [])
        view.setPontos([EstruturaPonto(c[0],c[1]), EstruturaPonto(c[2],c[1]), EstruturaPonto(c[2],c[3]), EstruturaPonto(c[0],c[3])])
        view.setCor(200,100,100)
        return [view]
