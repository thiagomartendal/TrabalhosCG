# coding: utf-8

from numpy import matmul
from numpy.linalg import inv
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from objeto.objeto import *
from objeto.estruturaPonto import *

class Curva2D(Objeto):
    
    # Construtor
    def __init__(self, nome, pontos):
        self.__pontos = pontos
        tmp = self.__calcularSegmentos()
        super(Curva2D, self).__init__(nome, tmp)

    # 0 0 0 100 100 100 100 0
    # 0 0 0 100 100 100 100 0 100 -100 200 -100 200 0 200 100 300 100 300 0

    # pontos de controle passados na criacao da curva
    def getPontosControle(self):
        return self.__pontos

    # Calcula os segmentos da reta a cada 4 pontos mantendo continuidade G(0)
    def __calcularSegmentos(self):
        todosPontos = []
        qtdSegmentos = (len(self.__pontos)-1) //3
        for i in range(qtdSegmentos):
            i *= 3
            self.__definirColunas(i)
            todosPontos += self.__transformar(i)
        return todosPontos

    # Define as matrizes coluna dos coeficientes X e Y
    def __definirColunas(self, start):
        self.__GX = []
        self.__GY = []
        for i in range(start, start+4):
            self.__GX.append(self.__pontos[i].X())
            self.__GY.append(self.__pontos[i].Y())

    # Matriz genérica com os coeficientes de t
    def __matrizT(self, t):
        T = []
        i = 3
        while i >= 0:
            T.append(t**i)
            i -= 1
        return T

    # Define-se a matriz com as tangentes de Hermite
    def __matrizTangente(self, t):
        T = []
        i = 3
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
        #MHB = [] # Encontrar
        #self.__MB = inv(matmul(MH, MHB)) # Deve-se encontrar a matriz MHB para multiplicar com MH e formar uma matriz MB genérica
        self.__MB = [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]]
        
    # Transformação para calcular os pontos no intervalo [0, 1]
    def __transformar(self, start):
        self.__matrizMB()
        novosPontos = [] #[self.__pontos[0], self.__pontos[1], self.__pontos[2], self.__pontos[3], self.__resultadoBezier]
        novosPontos.append(self.__pontos[start])
        i = 0.0
        while i <= 1.0:
            T = self.__matrizT(i)
            mat = matmul(T, self.__MB)
            X = matmul(mat, self.__GX)
            Y = matmul(mat, self.__GY)
            resultadoBezier = EstruturaPonto(X, Y)
            novosPontos.append(resultadoBezier)
            i += 0.01
        novosPontos.append(self.__pontos[start+3])
        return novosPontos

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

    # Retorna o tipo físico do objeto
    def tipo(self):
        return 3
