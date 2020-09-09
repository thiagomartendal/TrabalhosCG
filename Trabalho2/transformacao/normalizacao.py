from numpy import matmul
from math import radians, cos, sin
from objeto.estruturaPonto import *

class Normalizacao:

    def __init__(self, objeto, altura, largura, windowCenter):
        self.__altura = altura
        self.__largura = largura
        self.__WC = windowCenter
        pontos = []
        for ponto in objeto.getPontosFixos():
            matrizPonto = [ponto.X(), ponto.Y(), 1]
            matrizRes = matmul(matrizPonto, self.__matrizGeral())
            p = EstruturaPonto(matrizRes[0], matrizRes[1])
            pontos.append(p)
        objeto.setPontosFixos(pontos)

    def __translacao(self):
        return [[1,0,0],[0,1,0],[-self.__WC[0], -self.__WC[1], 1]]

    def __rotacao(self):
        angulo = 0
        return [[cos(angulo), -sin(angulo), 0], [sin(angulo), cos(angulo), 0], [0, 0, 1]]

    def __escalonamento(self):
        # return [[1/(self.__largura/2), 0, 0], [0, 1/(self.__altura/2), 0], [0, 0, 1]]
        return [[self.__largura/2, 0, 0], [0, self.__altura/2, 0], [0, 0, 1]]

    def __matrizGeral(self):
        m = matmul(self.__translacao(), self.__rotacao())
        return matmul(m, self.__escalonamento())
