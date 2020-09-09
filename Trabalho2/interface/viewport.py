from PyQt5.QtWidgets import *
from transformacao.primeiraTransformacao import *
from transformacao.normalizacao import *

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

    # Retorna o painel do viewport
    def painel(self):
        return self.__viewport

    # Renderiza os objetos na viewport
    def renderizar(self, objetos):
        self.__viewport.update()
        self.__viewport.scene().clear()
        # transformada de viewport
        primaeiraTransformacao = PrimeiraTransformacao(objetos, self.__window, self.__coordenadas)
        primaeiraTransformacao.transformadaViewport()
        # normalizacao
        n = Normalizacao(self.__window, self.__coordenadas)
        for objeto in objetos:
            n.normalizar(objeto)
            n.view(objeto)
        # desenhar na tela
        for objeto in objetos:
            objeto.desenhar(self.painel)

    # Retorna coordenadas da viewport
    def coordenadas(self):
        return self.__coordenadas
