from PyQt5.QtWidgets import *
from transformacao.primeiraTransformacao import *

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
        self.__coordenadas = [20, 20, self.__viewport.width()-20, self.__viewport.height()-20]
        self.__window = window

    # Retorna o painel do viewport
    def painel(self):
        return self.__viewport

    # Renderiza os objetos na viewport
    def renderizar(self, objetos):
        self.__viewport.update()
        self.__viewport.scene().clear()
        primaeiraTransformacao = PrimeiraTransformacao(objetos, self.__window, self.__coordenadas)
        primaeiraTransformacao.transformadaViewport()
        for objeto in objetos:
            objeto.desenhar(self.painel)

    def coordenadas(self):
        return self.__coordenadas
