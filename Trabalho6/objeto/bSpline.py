# coding: utf-8

from numpy import matmul
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from objeto.objeto import *
from objeto.estruturaPonto import *

class BSpline(Objeto):
    
    # Construtor
    def __init__(self, nome, pontos):
        self.__pontos = pontos
        tmp  = self.__calcularSegmentos()
        super(BSpline, self).__init__(nome, tmp)

    # 10 10 20 30 30 0 40 10
    # 10 10 20 30 30 0 40 10 50 20 40 40 60 40 70 40 60 20 70 10
    # -620 -170 -440 190 -260 -350 -80 -170 100 10 -80 370 280 370 460 370 280 10 460 -17

    # Calcula os segmentos da reta a cada 4 pontos
    def __calcularSegmentos(self):
        self.__matrizMbs()
        delta = 0.1
        self.__matrizME(delta)
        n = 1 / delta
        todosPontos = []
        for i in range(len(self.__pontos)-3):
            # G
            Gx, Gy = self.__G(i)
            # C
            Cx = matmul(self.__Mbs, Gx)
            Cy = matmul(self.__Mbs, Gy)
            # F
            Fx = matmul(self.__ME, Cx)
            Fy = matmul(self.__ME, Cy)
            # fwd Diff
            todosPontos += self.fwdDiff(n, Fx[0], Fx[1], Fx[2], Fx[3], Fy[0], Fy[1], Fy[2], Fy[3])
        return todosPontos

    # Retorna Gx, Gy para 4 pontos partindo do indice start
    def __G(self, start):
        Gx, Gy = [], []
        for i in range(start, start+4):
            Gx.append(self.__pontos[i].X())
            Gy.append(self.__pontos[i].Y())
        return (Gx, Gy)

    # Definida a matriz de bezier para a spline
    def __matrizMbs(self):
        Mb = [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]]
        self.__Mbs = [[x/6 for x in y] for y in Mb]

    # matriz E de deltas
    def __matrizME(self, delta):
        d = delta
        d2 = d**2
        d3 = d**3
        self.__ME = [[0, 0, 0, 1], [d3, d2, d, 0], [6*d3, 2*d2, 0, 0], [6*d3, 0, 0, 0]]

    # forward differences
    def fwdDiff(self, n, x, Dx, D2x, D3x, y, Dy, D2y, D3y):
        pontos = [EstruturaPonto(x, y)]
        i = 0
        xVelho = x
        yVelho = y
        while i < n:
            i += 1
            x = x + Dx
            Dx = Dx + D2x
            D2x = D2x + D3x
            y = y + Dy
            Dy = Dy + D2y
            D2y = D2y + D3y
            pontos.append(EstruturaPonto(x, y))
            xVelho = x
            yVelho = y
        return pontos

    # Desenha o objeto
    def desenhar(self, cena):
        if len(self.getPontos()) > 0:
            cor = QColor(self.getCor()[0], self.getCor()[1], self.getCor()[2])
            for i in range(len(self.getPontos())-1):
                p1 = self.getPontos()[i]
                p2 = self.getPontos()[i+1]
                if p1 != -1 and p2 != -1:
                    linha = QLineF(p1.X(), p1.Y(), p2.X(), p2.Y())
                    cena().scene().addLine(linha, QPen(cor, 1, Qt.SolidLine))

    # pontos de controle passados na criacao da curva
    def getPontosControle(self):
        return self.__pontos

    # Retorna o tipo físico do objeto
    def tipo(self):
        return 4
