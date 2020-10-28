from PyQt5.QtGui import *
from PyQt5.QtCore import *
from math import ceil

class ZBuffer():

    def __init__(self, painel, coordenadas, window):
        self.__painel = painel
        self.__window = window
        self.__objetos = []
        self.__altura = coordenadas[3] - coordenadas[1]
        self.__largura = coordenadas[2] - coordenadas[0]
        nInf = float("inf")
        self.__zBuffer = [[nInf for _ in range(self.__largura)] for _ in range(self.__altura)]
        self.__intensidade = [[(0,0,0) for _ in range(self.__largura)] for _ in range(self.__altura)]

    def atualizar(self, objetos):
        nInf = float("inf")
        self.__zBuffer = [[nInf for _ in range(self.__largura)] for _ in range(self.__altura)]
        self.__intensidade = [[(0,0,0) for _ in range(self.__largura)] for _ in range(self.__altura)]
        self.ob = objetos
        for objeto in objetos:
            for p in self.__pixelsInterceptamObjeto(objeto):
                x, y = p
                profundidade = self.__profundidade(objeto, x, y)
                if profundidade < self.__zBuffer[y][x]:
                    self.__zBuffer[y][x] = profundidade
                    self.__intensidade[y][x] = objeto.getCor()

    def __profundidade(self, objeto, x, y):
        return 5.0

    def __pixelsInterceptamObjeto(self, objeto):
        pixels = []
        segmentos = objeto.getSegmentosComZ()
        for s in segmentos:
            pixels += self.rastreadorBordas(s)
            p1 = segmentos[0].P1()
            p2 = segmentos[0].P2()
            dx = ceil(p1.X()) - p1.X()
            dy = ceil(p1.Y()) - p1.Y()
            #pixels.append([ceil(p1.X()), ceil(p1.Y())])
        return pixels

    def rastreadorBordas(self, segmento):
        p1 = segmento.P1()
        p2 = segmento.P2()
        Dx = p2.X() - p1.X()
        Dy = p2.Y() - p1.Y()
        Dz = p2.Z() - p1.Z()
        if Dy == 0: Dy = 0.0001
        xd = -(p2.Y()-(p2.Y()-ceil(p2.Y()))) * (Dx / Dy)
        pontoAtual = p1
        return [[int(pontoAtual.X()), int(pontoAtual.Y())]]




    def renderizar(self):
        #for o in self.ob:
        #    o.desenhar(self.__painel)

        
        cena = self.__painel
        corR, corG, corB = (0,0,0)
        for y in range(self.__altura):
            for x in range(self.__largura):
                corR, corG, corB = self.__intensidade[y][x]
                cor = QColor(corR, corG, corB)
                x = int(x)
                #y = int(self.__altura -1 -y)
                y = int(y)
                rect = QRectF(x, y, 1, 1)
                cena().scene().addRect(rect, QPen(cor, 1, Qt.SolidLine))

