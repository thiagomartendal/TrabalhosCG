from numpy import matmul
from math import radians, cos, sin
from objeto.estruturaPonto import *
from objeto.ponto3D import *
from objeto.segmentoReta import *

class Projecao():

    # Construtor
    def __init__(self, window):
        self.__window = window

    def segmentosProjParalelaOrtogonal(self, objeto):
        segmentosFixos = objeto.getSegmentosFixos()
        segmentosProj = objeto.aplicarMatSegmentos(self.__matParalelaOrtogonal(),  segmentosFixos)
        return segmentosProj

    def segmentosProjPerspectiva(self, objeto):
        segmentosFixos = objeto.getSegmentosFixos()
        segmentosProj = objeto.aplicarMatSegmentos(self.__matPerspectiva(), objeto.getSegmentosFixos())
        segmentosProj = self.__segmentosFrenteWindow(segmentosProj)
        segmentosProj = objeto.aplicarMatSegmentos(self.__matPerpectiva(), segmentosProj)
        return segmentosProj

    def __matParalelaOrtogonal(self):
        wcX, wcY, wcZ = self.__window.centro3D()
        matTransOrig = self.__gerarMatrizTranslacao(-wcX, -wcY, -wcZ)
        matRotXAlin = self.gerarMatrizRotacaoX(-self.__window.getAnguloX())
        matRotYAlin = self.gerarMatrizRotacaoY(-self.__window.getAnguloY())
        matRot = self.gerarMatrizRotacaoY(-30)
        matResult = self.calcularMatrizResultante([
                                                    matTransOrig,
                                                    matRotXAlin,
                                                    matRotYAlin,
                                                    matRot
                                                    ])
        return matResult

    def __matPerspectiva(self):
        copX, copY, copZ = self.posCOP()
        matTransOrig = self.__gerarMatrizTranslacao(-copX, -copY, -copZ)
        matRotXAlin = self.gerarMatrizRotacaoX(-self.__window.getAnguloX())
        matRotYAlin = self.gerarMatrizRotacaoY(-self.__window.getAnguloY())
        matResult = self.calcularMatrizResultante([
                                                    matTransOrig,
                                                    matRotXAlin,
                                                    matRotYAlin
                                                    ])
        return matResult

    # Retorna a posicao do COP
    def posCOP(self):
        wx, wy, wz = self.__window.centro3D()
        p = self.participacaoEixo(0, 0, -1, self.__window.getDistanciaCOP())
        return [wx+p[0], wy+p[1], wz+p[2]]

    def __matPerpectiva(self):
        d = self.__window.getDistanciaCOP()
        return [[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 1/d],
                [0, 0, 0, 0]]

    def __segmentosFrenteWindow(self, segmentos):
        wz = 0
        segmentosFrenteWindow = []
        for s in segmentos:
            p1 = s.P1()
            p2 = s.P2()
            if p1.Z() >= wz and p2.Z() >= wz:
                segmentosFrenteWindow.append(s)
            elif p1.Z() < wz and p2.Z() < wz:
                continue
            else:
                # menor z fica como p1
                if p1.Z() > p2.Z():
                    trocados = True
                    tempP1 = p2
                    tempP2 = p1
                else:
                    trocados = False
                    tempP1 = p1
                    tempP2 = p2
                #
                t = (wz - tempP1.Z()) / (tempP1.Z() - tempP2.Z())
                x = tempP1.X() + ( (tempP2.X() - tempP1.X()) * t )
                y = tempP1.Y() + ( (tempP2.Y() - tempP1.Y()) * t )
                novoP = Ponto3D(x, y, wz)
                if trocados:
                    novoS = SegmentoReta(p1, novoP)
                else:
                    novoS = SegmentoReta(novoP, p2)

                segmentosFrenteWindow.append(novoS)
        return segmentosFrenteWindow


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

    # Vetor com a participacao de cada eixo no movimento
    def participacaoEixo(self, x, y, z, qtd):
        x *= qtd
        y *= qtd
        z *= qtd
        matQtd = [x, y, z, 1]
        mrx = self.gerarMatrizRotacaoX(self.__window.getAnguloX())
        mry = self.gerarMatrizRotacaoY(self.__window.getAnguloY())
        mrz = self.gerarMatrizRotacaoZ(self.__window.getAnguloZ())
        mresult = self.calcularMatrizResultante([mrx, mry, mrz])
        participacao = matmul(matQtd, mresult)
        return participacao[:-1]