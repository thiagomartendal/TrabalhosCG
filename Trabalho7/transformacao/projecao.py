from numpy import matmul
from math import radians, cos, sin
from objeto.estruturaPonto import *
from objeto.ponto3D import *
from objeto.segmentoReta import *

class Projecao():

    # Construtor
    def __init__(self, window):
        self.__window = window

    def projecaoParalelaOrtogonal(self):
        wcX, wcY, wcZ = self.__window.centro3D()
        matTransOrig = self.__gerarMatrizTranslacao(-wcX, -wcY, -wcZ)
        matRotXAlin = self.gerarMatrizRotacaoX(-self.__window.getAnguloX())
        matRotYAlin = self.gerarMatrizRotacaoY(-self.__window.getAnguloY())
        matRot = self.gerarMatrizRotacaoY(30)
        matResult = self.calcularMatrizResultante([
                                                    matTransOrig,
                                                    matRotXAlin,
                                                    matRotYAlin,
                                                    matRot
                                                    ])
        return matResult

    # Retorna uma matriz 4x4 de translacao para x, y, z
    def __gerarMatrizTranslacao(self, x, y, z):
        return [[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [x, y, z, 1]]

    # Retorna uma matriz 4x4 no eixo Z de rotacao por graus
    def gerarMatrizRotacaoZ(self, graus):
        angulo = radians(graus)
        return [[cos(angulo), sin(angulo), 0, 0],
                [-sin(angulo), cos(angulo), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]]

    # Retorna uma matriz 4x4 no eixo Y de rotacao por graus
    def gerarMatrizRotacaoY(self, graus):
        angulo = radians(graus)
        return [[cos(angulo), 0, -sin(angulo), 0],
                [0, 1, 0, 0],
                [sin(angulo), 0, cos(angulo), 0],
                [0, 0, 0, 1]]

    # Retorna uma matriz 4x4 no eixo X de rotacao por graus
    def gerarMatrizRotacaoX(self, graus):
        angulo = radians(graus)
        return [[1, 0, 0, 0],
                [0, cos(angulo), sin(angulo), 0],
                [0, -sin(angulo), cos(angulo), 0],
                [0, 0, 0, 1]]

    # Retorna a matriz resultante da multiplicacao da lista
    def calcularMatrizResultante(self, matrizes):
        resultante = matrizes.pop(0)
        for mat in matrizes:
            resultante = matmul(resultante, mat)
        return resultante
