from PyQt5.QtWidgets import *
from transformacao.primeiraTransformacao import *
from transformacao.normalizacao import *
from interface.clipping import *
from objeto.linha import *
from objeto.poligono import *
from objeto.objeto3D import *

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
        tamanho = 100
        eixoX = Objeto3D('EixoX', [SegmentoReta(Ponto3D(-tamanho,0,0), Ponto3D(tamanho,0,0))])
        eixoX.setCor(255,150,150)
        eixoY = Objeto3D('EixoY', [SegmentoReta(Ponto3D(0,-tamanho,0), Ponto3D(0,tamanho,0))])
        eixoY.setCor(150,255,150)
        eixoZ = Objeto3D('EixoZ', [SegmentoReta(Ponto3D(0,0,-tamanho), Ponto3D(0,0,tamanho))])
        eixoZ.setCor(150,150,255)
        return [eixoX, eixoY, eixoZ]

    # Retorna uma lista com a viewport em vermelho
    def __criarViewportRetangulo(self, c):
        view = Poligono('Window', [])
        view.setPontos([EstruturaPonto(c[0],c[1]), EstruturaPonto(c[2],c[1]), EstruturaPonto(c[2],c[3]), EstruturaPonto(c[0],c[3])])
        view.setCor(200,100,100)
        return [view]
