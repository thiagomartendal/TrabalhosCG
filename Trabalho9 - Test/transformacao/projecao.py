from objeto.estruturaPonto import *
from objeto.modeloArame import *
from numpy import matmul

class Projecao:

    # Construtor
    def __init__(self, window):
        self.__window = window
        self.__obj = ModeloArame('', [])

    def segmentosProjParalelaOrtogonal(self, objeto):
        segmentosFixos = objeto.getSegmentosFixos()
        segmentosProj = objeto.aplicarMatSegmentos(self.__matParalelaOrtogonal(),  segmentosFixos)
        return segmentosProj

    def segmentosProjPerspectiva(self, objeto):
        retorno = []
        segmentosFixos = objeto.getSegmentosFixos()
        segmentosProj = objeto.aplicarMatSegmentos(self.__matPerspectiva(), segmentosFixos)
        retorno.append(segmentosProj)
        segmentosProj = self.__segmentosFrenteWindow(segmentosProj)
        segmentosProj = objeto.aplicarMatSegmentos(self.__matPerpectiva(), segmentosProj)
        retorno.append(segmentosProj)
        return retorno
        #return segmentosProj

    def __matParalelaOrtogonal(self):
        wcX, wcY, wcZ = self.__window.centro3D()
        matTransOrig = self.__obj.gerarMatrizTranslacao(-wcX, -wcY, -wcZ)
        matRotXAlin = self.__obj.gerarMatrizRotacaoX(-self.__window.getAnguloX())
        matRotYAlin = self.__obj.gerarMatrizRotacaoY(-self.__window.getAnguloY())
        matRot = self.__obj.gerarMatrizRotacaoY(-30)
        matResult = self.__obj.calcularMatrizResultante([
                                                    matTransOrig,
                                                    matRotXAlin,
                                                    matRotYAlin,
                                                    matRot
                                                    ])
        return matResult

    def __matPerspectiva(self):
        copX, copY, copZ = self.posCOP()
        matTransOrig = self.__obj.gerarMatrizTranslacao(-copX, -copY, -copZ)
        matRotXAlin = self.__obj.gerarMatrizRotacaoX(-self.__window.getAnguloX())
        matRotYAlin = self.__obj.gerarMatrizRotacaoY(-self.__window.getAnguloY())
        matResult = self.__obj.calcularMatrizResultante([
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
        return segmentosFrenteWindow

    # Vetor com a participacao de cada eixo no movimento
    def participacaoEixo(self, x, y, z, qtd):
        x *= qtd
        y *= qtd
        z *= qtd
        matQtd = [x, y, z, 1]
        mrx = self.__obj.gerarMatrizRotacaoX(self.__window.getAnguloX())
        mry = self.__obj.gerarMatrizRotacaoY(self.__window.getAnguloY())
        mrz = self.__obj.gerarMatrizRotacaoZ(self.__window.getAnguloZ())
        mresult = self.__obj.calcularMatrizResultante([mrx, mry, mrz])
        participacao = matmul(matQtd, mresult)
        return participacao[:-1]
