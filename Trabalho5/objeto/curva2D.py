from numpy import matmul, arange
from numpy.linalg import inv
from math import radians, cos, sin, pi
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from objeto.objeto import *
from objeto.estruturaPonto import *

class Curva2D(Objeto):

    # Construtor
    def __init__(self, nome, pontos):
        self.__pontos = pontos
        self.__definirColunas()
        tmp = self.__transformar()
        super(Curva2D, self).__init__(nome, tmp)

    # Define as matrizes coluna dos coeficientes X e Y
    def __definirColunas(self):
        self.__GX = []
        self.__GY = []
        for p in self.__pontos:
            self.__GX.append(p.X())
            self.__GY.append(p.Y())

    # Matriz genérica com os coeficientes de t
    def __matrizT(self, t):
        T = []
        i = len(self.__pontos)-1
        while i >= 0:
            T.append(t**i)
            i -= 1
        return T

    # Define-se a matriz com as tangentes de Hermite
    def __matrizTangente(self, t):
        T = []
        i = len(self.__pontos)-1
        j = i-1
        while i >= 0:
            T.append(i*(t**(j if j >= 0 else 1)))
            i -= 1
            j -= 1
        return T

    # Definida a matriz de bezier para se encontrar as coordenadas X e Y
    def __matrizMB(self):
        Pinicial = self.__matrizT(0)
        PFinal = self.__matrizT(1)
        Rinicial = self.__matrizTangente(0)
        Rfinal = self.__matrizTangente(1)
        MH = [Pinicial, PFinal, Rinicial, Rfinal]
        MHB = [] # Encontrar
        # self.__MB = inv(matmul(MH, MHB)) # Deve-se encontrar a matriz MHB para multiplicar com MH e formar uma matriz MB genérica
        self.__MB = [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]]

    # Transformação para calcular os pontos no intervalo [0, 1]
    def __transformar(self):
        self.__matrizMB()
        novosPontos = [] #[self.__pontos[0], self.__pontos[1], self.__pontos[2], self.__pontos[3], self.__resultadoBezier]
        novosPontos.append(self.__pontos[0])
        i = 0.0
        while i <= 1.0:
            T = self.__matrizT(i)
            mat = matmul(T, self.__MB)
            X = matmul(mat, self.__GX)
            Y = matmul(mat, self.__GY)
            resultadoBezier = EstruturaPonto(X, Y)
            novosPontos.append(resultadoBezier)
            i += 0.01
        novosPontos.append(self.__pontos[len(self.__pontos)-1])
        return novosPontos

    # Desenha o objeto
    def desenhar(self, cena):
        if len(self.getPontos()) > 0:
            cor = QColor(self.getCor()[0], self.getCor()[1], self.getCor()[2])
            pontos = []
            for p in self.getPontos():
                pontos.append(QPointF(p.X(), p.Y()))
            curva = QPolygonF(pontos)
            cena().scene().addPolygon(curva, QPen(cor, 1, Qt.SolidLine), QBrush(Qt.NoBrush))

    # Retorna o tipo físico do objeto
    def tipo(self):
        return 3
