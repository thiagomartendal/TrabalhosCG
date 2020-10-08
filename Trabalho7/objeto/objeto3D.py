from objeto.ponto3D import *
from math import sin, cos, radians, acos, degrees

class Objeto3D():
    __pontos = [] # Vetor de coordenadas
    __pontosFixos = []
    __pontosNormalizados = []
    __cor = (0,0,0)

    # Construtor
    def __init__(self, nome, pontos):
        self.__nome = nome
        self.__pontos = [p for p in pontos]
        self.__pontosFixos = [p for p in pontos]

    # Zera a lista de pontos
    def clearPontos(self):
        self.__pontos.clear()

    # Atualiza a lista de pontos
    def setPontos(self, novosPontos):
        self.__pontos.clear()
        self.__pontos = [p for p in novosPontos]

    # Atualiza a lista de pontos fixos
    def setPontosFixos(self, novosPontos):
        self.__pontosFixos.clear()
        self.__pontosFixos = [p for p in novosPontos]

    # Atualiza a lista de pontos normalizados
    def setPontosNormalizados(self, novosPontos):
        self.__pontosNormalizados.clear()
        self.__pontosNormalizados = [p for p in novosPontos]

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
    def getPontos(self):
        return self.__pontos

    # Retorna os vetor de pontos iniciais
    def getPontosFixos(self):
        return self.__pontosFixos

    # Retorna os pontos normalizados
    def getPontosNormalizados(self):
        return self.__pontosNormalizados

    # Retorna o tipo físico do objeto
    def tipo(self):
        return 5

    # Desenha o objeto
    def desenhar(self, cena):
        pass

    # Retorna o vetor [x, y] da média dos pontos
    def getMediaPontosFixos(self):
        mediaX = 0
        mediaY = 0
        mediaZ = 0
        for p in self.__pontosFixos:
            mediaX += p.X()
            mediaY += p.Y()
            mediaZ += p.Z()
        return [mediaX/len(self.__pontosFixos), mediaY/len(self.__pontosFixos), mediaZ/len(self.__pontosFixos)]

    # Translada o objeto dado uma distancia x, y
    def transladar(self, x, y, z):
        matT = self.__gerarMatrizTranslacao(x, y, z)
        self.__aplicarMat(matT)

    # Escalona o objeto por um coeficiente sX, sY
    def escalonarCentro(self, sX, sY, sZ):
        centro = self.getMediaPontosFixos()
        matTransParaOrigem = self.__gerarMatrizTranslacao(-centro[0], -centro[1], -centro[2])
        matEscalonamento = self.__gerarMatrizEscalonamento(sX, sY, sZ)
        matTransDeVolta = self.__gerarMatrizTranslacao(centro[0], centro[1], centro[2])
        matResult = self.__calcularMatrizResultante([matTransParaOrigem, matEscalonamento, matTransDeVolta])
        self.__aplicarMat(matResult)

    # Eixo X
    def rotacionarEixoX(self, graus):
        centroObj = self.getMediaPontosFixos()
        matTransParaPonto = self.__gerarMatrizTranslacao(-centroObj[0], -centroObj[1], -centroObj[2])
        matRot = self.__gerarMatrizRotacaoX(graus)
        matTransDeVolta = self.__gerarMatrizTranslacao(centroObj[0], centroObj[1], centroObj[2])
        matResult = self.__calcularMatrizResultante([matTransParaPonto, matRot, matTransDeVolta])
        self.__aplicarMat(matResult)
        
    # Eixo Y
    def rotacionarEixoY(self, graus):
        centroObj = self.getMediaPontosFixos()
        matTransParaPonto = self.__gerarMatrizTranslacao(-centroObj[0], -centroObj[1], -centroObj[2])
        matRot = self.__gerarMatrizRotacaoY(graus)
        matTransDeVolta = self.__gerarMatrizTranslacao(centroObj[0], centroObj[1], centroObj[2])
        matResult = self.__calcularMatrizResultante([matTransParaPonto, matRot, matTransDeVolta])
        self.__aplicarMat(matResult)
        
    # Eixo Z
    def rotacionarEixoZ(self, graus):
        centroObj = self.getMediaPontosFixos()
        matTransParaPonto = self.__gerarMatrizTranslacao(-centroObj[0], -centroObj[1], -centroObj[2])
        matRot = self.__gerarMatrizRotacaoZ(graus)
        matTransDeVolta = self.__gerarMatrizTranslacao(centroObj[0], centroObj[1], centroObj[2])
        matResult = self.__calcularMatrizResultante([matTransParaPonto, matRot, matTransDeVolta])
        self.__aplicarMat(matResult)

    # Rotaciona o objeto por determinados graus
    def rotacionarGraus(self, graus):
        centroObj = self.getMediaPontosFixos()
        matTransParaPonto = self.__gerarMatrizTranslacao(-centroObj[0], -centroObj[1], -centroObj[2])
        p2Obj = self.getPontosFixos()[0]
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

    # Retorna uma matriz 3x3 de translacao para x, y
    def __gerarMatrizTranslacao(self, x, y, z):
        return [[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [x, y, z, 1]]
    
    # Retorna uma matriz 3x3 de escalonamento por sX, sY
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

    # Todos os pontos do objeto sao multiplicados pela matriz
    def __aplicarMat(self, mat):
        pontos = self.getPontosFixos()
        novosPontos = []
        for p in pontos:
            vp = [p.X(), p.Y(), p.Z(), 1]
            novoP = matmul(vp, mat)
            novosPontos.append(Ponto3D(novoP[0], novoP[1]))
        self.setPontosFixos(novosPontos)