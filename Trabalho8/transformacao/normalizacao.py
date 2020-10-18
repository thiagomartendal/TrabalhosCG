from numpy import matmul
from math import radians, cos, sin
from objeto.estruturaPonto import *
from objeto.ponto3D import *
from objeto.segmentoReta import *
from transformacao.projecao import *

class Normalizacao:

    # Construtor
    def __init__(self, window, viewportCoordenadas):
        self.__window = window
        self.__viewportCoordenadas = viewportCoordenadas
        self.__proj = Projecao(self.__window)

    # Ajusta os PontosNormalizados do objeto para a posicao atual da window
    def normalizar(self, objeto):
        if objeto.dimensao() == 2:
            pontos = self.__normalizacao2D(objeto)
            objeto.setPontosNormalizados(pontos)
        elif objeto.dimensao() == 3:
            #segmentosProj = self.__proj.segmentosProjParalelaOrtogonal(objeto)
            segmentosProj = self.__proj.segmentosProjPerspectiva(objeto)
            segmentosNorm = self.__normalizacao3D(objeto, segmentosProj)
            objeto.setSegmentosNormalizados(segmentosNorm)

    # Normalização para objetos 2D
    def __normalizacao2D(self, objeto):
        pontos = []
        for ponto in objeto.getPontosFixos():
            matrizPonto = [ponto.X(), ponto.Y(), 1]
            matrizRes = matmul(matrizPonto, self.__matrizGeral())
            p = EstruturaPonto(matrizRes[0], matrizRes[1])
            pontos.append(p)
        return pontos

    # Normalização para objetos 3D
    def __normalizacao3D(self, objeto, segmentosEntrada):
        segmentos = []
        for segmento in segmentosEntrada:
            matrizPonto1 = [segmento.P1().X(), segmento.P1().Y(), 1]
            matrizPonto2 = [segmento.P2().X(), segmento.P2().Y(), 1]
            matrizRes1 = matmul(matrizPonto1, self.__matrizGeral3D())
            matrizRes2 = matmul(matrizPonto2, self.__matrizGeral3D())
            p1 = EstruturaPonto(matrizRes1[0], matrizRes1[1])
            p2 = EstruturaPonto(matrizRes2[0], matrizRes2[1])
            segmentos.append(SegmentoReta(p1, p2))
        return segmentos

    # Ajusta os Pontos do objeto para serem desenhados com base nos PontosNormalizados do objeto
    def view(self, objeto):
        largura = self.__viewportCoordenadas[2] - self.__viewportCoordenadas[0]
        altura = self.__viewportCoordenadas[3] - self.__viewportCoordenadas[1]
        if objeto.dimensao() == 2:
            self.__view2D(objeto, largura, altura)
        elif objeto.dimensao() == 3:
            self.__view3D(objeto, largura, altura)

    # Calcula a view 2D
    def __view2D(self, objeto, largura, altura):
        pontos = []
        for ponto in objeto.getPontosNormalizados():
            matrizPonto = [ponto.X(), -ponto.Y(), 1]
            matrizEscal = [[largura/2,0,0],[0,altura/2,0],[0,0,1]]
            matrizResul = matmul(matrizPonto, matrizEscal)
            p = EstruturaPonto(matrizResul[0]+largura/2, matrizResul[1]+altura/2)
            pontos.append(p)
        objeto.setPontos(pontos)

    # Calcula a view 3D
    def __view3D(self, objeto, largura, altura):
        segmentos = []
        for segmento in objeto.getSegmentosNormalizados():
            ponto1 = segmento.P1()
            ponto2 = segmento.P2()
            matrizPonto1 = [ponto1.X(), -ponto1.Y(), 1]
            matrizPonto2 = [ponto2.X(), -ponto2.Y(), 1]
            matrizEscal = [[largura/2,0,0],[0,altura/2,0],[0,0,1]]
            matrizResul1 = matmul(matrizPonto1, matrizEscal)
            matrizResul2 = matmul(matrizPonto2, matrizEscal)
            p1 = EstruturaPonto(matrizResul1[0]+largura/2, matrizResul1[1]+altura/2)
            p2 = EstruturaPonto(matrizResul2[0]+largura/2, matrizResul2[1]+altura/2)
            segmento = SegmentoReta(p1, p2)
            segmentos.append(segmento)
        objeto.setSegmentos(segmentos)

    # Matriz de translacao
    def __translacao(self):
        wcX, wcY = self.__window.centro()
        return [[1,0,0],
                [0,1,0],
                [-wcX, -wcY, 1]]

    # Matriz de rotacao
    def __rotacao(self):
        angulo = radians(-self.__window.getAnguloZ())
        return [[cos(angulo), sin(angulo), 0],
                [-sin(angulo), cos(angulo), 0],
                [0, 0, 1]]

    # Matriz de escalonamento
    def __escalonamento(self):
        largura, altura = self.__window.getSize()
        return [[2/largura, 0, 0],
                [0, 2/altura, 0],
                [0, 0, 1]]

    # Matriz geral obtida pela multiplicacao da translacao, rotacao e escalonamento
    def __matrizGeral(self):
        m = matmul(self.__translacao(), self.__rotacao())
        return matmul(m, self.__escalonamento())

    # Matriz geral obtida pela multiplicacao da translacao, rotacao e escalonamento
    def __matrizGeral3D(self):
        return matmul(self.__rotacao(), self.__escalonamento())
