from PyQt5.QtGui import *
from PyQt5.QtCore import *
from objeto.ponto3D import *
from objeto.segmentoReta import *
from numpy import matmul
from math import sin, cos, radians, acos, degrees

class Objeto3D():
    __segmentos = [] # Vetor de segmentos de reta
    __segmentosFixos = []
    __segmentosNormalizados = []
    __cor = (0,0,0)

# 0 0 0 100 0 0 100 100 0 0 100 0
# 0 0 0 100 0 0 100 100 0 0 100 0 0 100 200 100 100 200 0 100 200 0 0 200
# 0 0 0 100 0 0 100 0 100 0 0 100 0 100 100 0 100 0 0 0 0 0 0 100 0 100 100 100 100 100 100 0 100 100 100 100 100 100 0 100 0 0 100 100 0 0 100 0



    # Construtor
    def __init__(self, nome, segmentos):
        self.__nome = nome
        self.__segmentosFixos = [s for s in segmentos]

    # Atualiza a lista de pontos
    def setSegmentos(self, novosSegmentos):
        self.__segmentos.clear()
        self.__segmentos = [s for s in novosSegmentos]

    # Atualiza a lista de pontos fixos
    def setSegmentosFixos(self, novosSegmentos):
        self.__segmentosFixos.clear()
        self.__segmentosFixos = [s for s in novosSegmentos]

    # Atualiza a lista de pontos normalizados
    def setSegmentosNormalizados(self, novosSegmentos):
        self.__segmentosNormalizados.clear()
        self.__segmentosNormalizados = [s for s in novosSegmentos]

    # Atualiza a cor
    def setCor(self, r, g, b):
        self.__cor = (r, g, b)

    # Retorna a cor
    def getCor(self):
        return self.__cor

    # Retorna o nome
    def getNome(self):
        return self.__nome

    # Retorna os vetor de pontos
    def getSegmentos(self):
        return self.__segmentos

    # Retorna os vetor de pontos iniciais
    def getSegmentosFixos(self):
        return self.__segmentosFixos

    # Retorna os pontos normalizados
    def getSegmentosNormalizados(self):
        return self.__segmentosNormalizados

    # Retorna o tipo físico do objeto
    def tipo(self):
        return 5

    # Define um objeto 2D
    def dimensao(self):
        return 3

    # Desenha o objeto
    def desenhar(self, cena):
        if len(self.getSegmentos()) > 0:
            cor = QColor(self.getCor()[0], self.getCor()[1], self.getCor()[2])
            for s in self.getSegmentos():
                s.desenhar(cena, cor)

    # Retorna o vetor [x, y] da média dos pontos
    def getMediaSegmentosFixos(self):
        mediaX = 0
        mediaY = 0
        mediaZ = 0
        for s in self.__segmentosFixos:
            mediaX += s.mediaX()
            mediaY += s.mediaY()
            mediaZ += s.mediaZ()
        return [mediaX/len(self.__segmentosFixos), mediaY/len(self.__segmentosFixos), mediaZ/len(self.__segmentosFixos)]

    # Translada o objeto dado uma distancia x, y
    def transladar(self, x, y, z):
        matT = self.__gerarMatrizTranslacao(x, y, z)
        self.__aplicarMat(matT)

    # Escalona o objeto por um coeficiente sX, sY
    def escalonarCentro(self, sX, sY, sZ):
        centro = self.getMediaSegmentosFixos()
        matTransParaOrigem = self.__gerarMatrizTranslacao(-centro[0], -centro[1], -centro[2])
        matEscalonamento = self.__gerarMatrizEscalonamento(sX, sY, sZ)
        matTransDeVolta = self.__gerarMatrizTranslacao(centro[0], centro[1], centro[2])
        matResult = self.__calcularMatrizResultante([matTransParaOrigem, matEscalonamento, matTransDeVolta])
        self.__aplicarMat(matResult)

    # Eixo X
    def rotacionarEixoX(self, graus):
        centroObj = self.getMediaSegmentosFixos()
        matTransParaPonto = self.__gerarMatrizTranslacao(-centroObj[0], -centroObj[1], -centroObj[2])
        matRot = self.__gerarMatrizRotacaoX(graus)
        matTransDeVolta = self.__gerarMatrizTranslacao(centroObj[0], centroObj[1], centroObj[2])
        matResult = self.__calcularMatrizResultante([matTransParaPonto, matRot, matTransDeVolta])
        self.__aplicarMat(matResult)

    # Eixo Y
    def rotacionarEixoY(self, graus):
        centroObj = self.getMediaSegmentosFixos()
        matTransParaPonto = self.__gerarMatrizTranslacao(-centroObj[0], -centroObj[1], -centroObj[2])
        matRot = self.__gerarMatrizRotacaoY(graus)
        matTransDeVolta = self.__gerarMatrizTranslacao(centroObj[0], centroObj[1], centroObj[2])
        matResult = self.__calcularMatrizResultante([matTransParaPonto, matRot, matTransDeVolta])
        self.__aplicarMat(matResult)

    # Eixo Z
    def rotacionarEixoZ(self, graus):
        centroObj = self.getMediaSegmentosFixos()
        matTransParaPonto = self.__gerarMatrizTranslacao(-centroObj[0], -centroObj[1], -centroObj[2])
        matRot = self.__gerarMatrizRotacaoZ(graus)
        matTransDeVolta = self.__gerarMatrizTranslacao(centroObj[0], centroObj[1], centroObj[2])
        matResult = self.__calcularMatrizResultante([matTransParaPonto, matRot, matTransDeVolta])
        self.__aplicarMat(matResult)

    # Rotaciona o objeto por determinados graus
    def rotacionarGraus(self, graus):
        centroObj = self.getMediaSegmentosFixos()
        matTransParaPonto = self.__gerarMatrizTranslacao(-centroObj[0], -centroObj[1], -centroObj[2])
        p2Obj = self.getSegmentosFixos()[0].P2()
        angulos = self.__findAnguloEixos(centroObj, [p2Obj.X(), p2Obj.Y(), p2Obj.Z()])
        matRotX = self.__gerarMatrizRotacaoX(angulos[0])
        matRotZ = self.__gerarMatrizRotacaoZ(angulos[2])
        matRotGraus = self.__gerarMatrizRotacaoY(graus)
        matRotZrev = self.__gerarMatrizRotacaoZ(-angulos[2])
        matRotXrev = self.__gerarMatrizRotacaoX(-angulos[0])
        matTransDeVolta = self.__gerarMatrizTranslacao(centroObj[0], centroObj[1], centroObj[2])
        matResult = self.__calcularMatrizResultante([matTransParaPonto,
                                                     matRotX,
                                                     matRotZ,
                                                     matRotGraus,
                                                     matRotZrev,
                                                     matRotXrev,
                                                     matTransDeVolta])
        self.__aplicarMat(matResult)

    # retorna lista com angulos do eixos do vetor dado por 2 pontos
    def __findAnguloEixos(self, p1, p2):
        op = [p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]]
        size = (sum([k**2 for k in op]) )**0.5
        angulos = [degrees( acos(k/size) ) for k in op]
        return angulos

    # Retorna uma matriz 4x4 de translacao para x, y, z
    def __gerarMatrizTranslacao(self, x, y, z):
        return [[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [x, y, z, 1]]

    # Retorna uma matriz 4x4 de escalonamento por sX, sY, sZ
    def __gerarMatrizEscalonamento(self, sX, sY, sZ):
        return [[sX, 0, 0, 0],
                [0, sY, 0, 0],
                [0, 0, sZ, 0],
                [0, 0, 0, 1]]

    # Retorna uma matriz 4x4 no eixo Z de rotacao por graus
    def __gerarMatrizRotacaoZ(self, graus):
        angulo = radians(graus)
        return [[cos(angulo), sin(angulo), 0, 0],
                [-sin(angulo), cos(angulo), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]]

    # Retorna uma matriz 4x4 no eixo Y de rotacao por graus
    def __gerarMatrizRotacaoY(self, graus):
        angulo = radians(graus)
        return [[cos(angulo), 0, -sin(angulo), 0],
                [0, 1, 0, 0],
                [sin(angulo), cos(angulo), 0, 0],
                [0, 0, 0, 1]]

    # Retorna uma matriz 4x4 no eixo X de rotacao por graus
    def __gerarMatrizRotacaoX(self, graus):
        angulo = radians(graus)
        return [[1, 0, 0, 0],
                [0, cos(angulo), sin(angulo), 0],
                [0, -sin(angulo), cos(angulo), 0],
                [0, 0, 0, 1]]

    # Retorna a matriz resultante da multiplicacao da lista
    def __calcularMatrizResultante(self, matrizes):
        resultante = matrizes.pop(0)
        for mat in matrizes:
            resultante = matmul(resultante, mat)
        return resultante

    # Retorna os segmentos apos ser aplicada a matriz
    def aplicarMatSegmentos(self, mat, segmentosEntrada):
        segmentos = []
        for s in segmentosEntrada:
            p1 = s.P1()
            p2 = s.P2()
            vp1 = [p1.X(), p1.Y(), p1.Z(), 1]
            vp2 = [p2.X(), p2.Y(), p2.Z(), 1]
            novoP1 = matmul(vp1, mat)
            novoP2 = matmul(vp2, mat)
            ponto1 = Ponto3D(novoP1[0], novoP1[1], novoP1[2])
            ponto2 = Ponto3D(novoP2[0], novoP2[1], novoP2[2])
            segmentos.append( SegmentoReta(ponto1, ponto2))
        return segmentos

    # Todos os pontos do objeto sao multiplicados pela matriz
    def __aplicarMat(self, mat):
        for s in self.__segmentosFixos:
            p1 = s.P1()
            p2 = s.P2()
            vp1 = [p1.X(), p1.Y(), p1.Z(), 1]
            vp2 = [p2.X(), p2.Y(), p2.Z(), 1]
            novoP1 = matmul(vp1, mat)
            novoP2 = matmul(vp2, mat)
            s.setP1(Ponto3D(novoP1[0], novoP1[1], novoP1[2]))
            s.setP2(Ponto3D(novoP2[0], novoP2[1], novoP2[2]))
