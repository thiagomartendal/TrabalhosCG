from PyQt5.QtWidgets import *
from transformacao.primeiraTransformacao import *
from transformacao.normalizacao import *
from interface.clipping import *
from objeto.linha import *
from objeto.poligono import *
from objeto.modeloArame import *
from transformacao.projecao import *
from interface.zBuffer import *

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
        self.__eixos = self.__criarEixos()
        self.__viewportRetangulo = self.__criarViewportRetangulo(self.__coordenadas)
        self.__zBuffer = ZBuffer(self.painel)

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
        objetos = self.__eixos + objetos
        for objeto in objetos:
            n.normalizar(objeto)
            n.view(objeto)
            self.__clipping.clip(objeto)

        # desenhar o retangulo da viewport
        self.__viewportRetangulo.desenhar(self.painel)

        # desenha os objetos
        objetos3D = [o for o in objetos if (o.dimensao() == 3)]
        objetos2D = [o for o in objetos if (o.dimensao() == 2)]

        for objeto in objetos2D:
            objeto.desenhar(self.painel)

        self.__zBuffer.renderizar(objetos3D)


    # Retorna coordenadas da viewport
    def coordenadas(self):
        return self.__coordenadas

     # Retorna uma lista com eixos X e Y do mundo em cinza
    def __criarEixos(self):
        tamanho = 100
        eixoX1 = ModeloArame('EixoX1', [Ponto3D(-tamanho,0,0), Ponto3D(0,0,0)])
        eixoX2 = ModeloArame('EixoX2', [Ponto3D(0,0,0), Ponto3D(tamanho,0,0)])
        eixoX1.setCor(255,150,150)
        eixoX2.setCor(255,150,150)
        eixoY1 = ModeloArame('EixoY1', [Ponto3D(0,-tamanho,0), Ponto3D(0,0,0)])
        eixoY2 = ModeloArame('EixoY2', [Ponto3D(0,0,0), Ponto3D(0,tamanho,0)])
        eixoY1.setCor(150,255,150)
        eixoY2.setCor(150,255,150)
        eixoZ1 = ModeloArame('EixoZ1', [Ponto3D(0,0,-tamanho), Ponto3D(0,0,0)])
        eixoZ2 = ModeloArame('EixoZ2', [Ponto3D(0,0,0), Ponto3D(0,0,tamanho)])
        eixoZ1.setCor(150,150,255)
        eixoZ2.setCor(150,150,255)
        return [eixoX1, eixoX2, eixoY1, eixoY2, eixoZ1, eixoZ2]

    # Retorna uma lista com a viewport em vermelho
    def __criarViewportRetangulo(self, c):
        view = Poligono('Window', [])
        view.setPontos([EstruturaPonto(c[0],c[1]), EstruturaPonto(c[2],c[1]), EstruturaPonto(c[2],c[3]), EstruturaPonto(c[0],c[3])])
        view.setCor(200,100,100)
        return view
