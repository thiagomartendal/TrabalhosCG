from numpy import matmul
from math import radians, cos, sin
from objeto.estruturaPonto import *
from objeto.objeto3D import *

class SegundaTransformacao:

    # Translada o objeto dado uma distancia x, y
    def transladar(self, objeto, x, y):
        if objeto.dimensao() == 3:
            z = 0
            objeto.transladar(x, y, z)
        else:
            matT = self.__gerarMatrizTranslacao(x, y)
            self.__aplicarMatObj(matT, objeto)

    # Escalona o objeto por um coeficiente sX, sY
    def escalonarCentro(self, objeto, sX, sY):
        if objeto.dimensao() == 3:
            sZ = 1
            objeto.escalonarCentro(sX, sY, sZ)
        else:
            centro = objeto.getMediaPontosFixos()
            matTransParaOrigem = self.__gerarMatrizTranslacao(-centro[0], -centro[1])
            matEscalonamento = self.__gerarMatrizEscalonamento(sX, sY)
            matTransDeVolta = self.__gerarMatrizTranslacao(centro[0], centro[1])
            matResult = self.__calcularMatrizResultante([matTransParaOrigem, matEscalonamento, matTransDeVolta])
            self.__aplicarMatObj(matResult, objeto)

    # Rotaciona o objeto ao redor do seu centro por determinados graus
    def rotacionarCentroObjeto(self, objeto, graus):
        if objeto.dimensao() == 3:
            objeto.rotacionarGraus(graus)
        else:
            centro = objeto.getMediaPontosFixos()
            self.rotacionarPontoGraus(objeto, centro, graus)

    # Rotaciona o objeto ao redor do ponto [0, 0] do mundo por determinados graus
    def rotacionarCentroMundo(self, objeto, graus):
        if objeto.dimensao() == 3:
            objeto.rotacionarGraus(graus)
        else:
            centro = [0, 0]
            self.rotacionarPontoGraus(objeto, centro, graus)

    # Rotaciona o objeto por um ponto por determinados graus
    def rotacionarPontoGraus(self, objeto, ponto, graus):
        if objeto.dimensao() == 3:
            objeto.rotacionarGraus(graus)
        else:
            matTransParaPonto = self.__gerarMatrizTranslacao(-ponto[0], -ponto[1])
            matRotacao = self.__gerarMatrizRotacao(graus)
            matTransDeVolta = self.__gerarMatrizTranslacao(ponto[0], ponto[1])
            matResult = self.__calcularMatrizResultante([matTransParaPonto, matRotacao, matTransDeVolta])
            self.__aplicarMatObj(matResult, objeto)

    # Retorna uma matriz 3x3 de translacao para x, y
    def __gerarMatrizTranslacao(self, x, y):
        return [[1, 0, 0],
                [0, 1, 0],
                [x, y, 1]]

    # Retorna uma matriz 3x3 de rotacao por graus
    def __gerarMatrizRotacao(self, graus):
        angulo = radians(graus)
        return [[cos(angulo), sin(angulo), 0],
                [-sin(angulo), cos(angulo), 0],
                [0, 0, 1]]

    # Retorna uma matriz 3x3 de escalonamento por sX, sY
    def __gerarMatrizEscalonamento(self, sX, sY):
        return [[sX, 0, 0],
                [0, sY, 0],
                [0, 0, 1]]

    # Retorna a matriz resultante da multiplicacao da lista
    def __calcularMatrizResultante(self, matrizes):
        resultante = matrizes.pop(0)
        for mat in matrizes:
            resultante = matmul(resultante, mat)
        return resultante

    # Todos os pontos do objeto sao multiplicados pela matriz
    def __aplicarMatObj(self, mat, objeto):
        pontos = objeto.getPontosFixos()
        novosPontos = []
        for p in pontos:
            np = [p.X(), p.Y(), 1]
            novoP = matmul(np, mat)
            novosPontos.append(EstruturaPonto(novoP[0], novoP[1]))
        objeto.setPontosFixos(novosPontos)
