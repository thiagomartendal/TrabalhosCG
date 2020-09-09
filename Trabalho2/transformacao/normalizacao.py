from numpy import matmul
from math import radians, cos, sin
from objeto.estruturaPonto import *

class Normalizacao:

    # Construtor
    def __init__(self, window, viewportCoordenadas):
        self.__window = window
        self.__viewportCoordenadas = viewportCoordenadas

    # Ajusta os PontosNormalizados do objeto para a posicao atual da window
    def normalizar(self, objeto):
        pontos = []
        for ponto in objeto.getPontosFixos():
            matrizPonto = [ponto.X(), ponto.Y(), 1]
            matrizRes = matmul(matrizPonto, self.__matrizGeral())
            p = EstruturaPonto(matrizRes[0], matrizRes[1])
            pontos.append(p)
        objeto.setPontosNormalizados(pontos)

    # Ajusta os Pontos do objeto para serem desenhados com base nos PontosNormalizados do objeto
    def view(self, objeto):
        largura = self.__viewportCoordenadas[2] - self.__viewportCoordenadas[0]
        altura = self.__viewportCoordenadas[3] - self.__viewportCoordenadas[1]
        pontos = []
        for ponto in objeto.getPontosNormalizados():
            matrizPonto = [ponto.X(), -ponto.Y(), 1]
            matrizEscal = [[largura/2,0,0],[0,altura/2,0],[0,0,1]]
            matrizResul = matmul(matrizPonto, matrizEscal)
            p = EstruturaPonto(matrizResul[0]+largura/2, matrizResul[1]+altura/2)
            pontos.append(p)
        objeto.setPontos(pontos)

    # Matriz de translacao
    def __translacao(self):
        wcX, wcY = self.__window.centro()
        return [[1,0,0],[0,1,0],[-wcX, -wcY, 1]]

    # Matriz de rotacao
    def __rotacao(self):
        angulo = radians(-self.__window.getAngulo())
        return [[cos(angulo), sin(angulo), 0], [-sin(angulo), cos(angulo), 0], [0, 0, 1]]

    # Matriz de escalonamento
    def __escalonamento(self):
        largura, altura = self.__window.getSize()
        return [[2/largura, 0, 0], [0, 2/altura, 0], [0, 0, 1]]

    # Matriz geral obtida pela multiplicacao da translacao, rotacao e escalonamento
    def __matrizGeral(self):
        m = matmul(self.__translacao(), self.__rotacao())
        return matmul(m, self.__escalonamento())
