from abc import ABC, abstractmethod
from objeto.segmentoReta import *

class Objeto3D(ABC):
    __cor = (0,0,0)

    # Construtor
    def __init__(self, nome, pontos3D):
        self.__nome = nome
        self.__pontos3D = [p for p in pontos3D]
        self.__pontos3DFixos = [p for p in pontos3D]

    # Atualiza a lista de pontos
    def setPontos(self, novosPontos):
        self.__pontos3D.clear()
        self.__pontos3D = [p for p in novosPontos]

    # Atualiza a lista de pontos fixos
    def setPontosFixos(self, novosPontos):
        self.__pontos3DFixos.clear()
        self.__pontos3DFixos = [p for p in novosPontos]

    # Retorna os vetor de pontos3D
    def getPontos(self):
        return self.__pontos3D

    # Retorna os vetor de pontos3D iniciais
    def getPontosFixos(self):
        return self.__pontos3DFixos

    # Atualiza a cor
    def setCor(self, r, g, b):
        self.__cor = (r, g, b)

    # Retorna a cor
    def getCor(self):
        return self.__cor

    # Retorna o nome
    def getNome(self):
        return self.__nome

    # Converte pontos 3D em segmentos de reta
    def __transformarSegmentos(self):
        segmentos = []
        if len(self.__pontos3D) % 2 == 0:
            for i in range(0, len(self.__pontos3D), 2):
                p1 = self.__pontos3D[i]
                p2 = self.__pontos3D[i+1]
                s = SegmentoReta(p1, p2)
                segmentos.append(s)
        return segmentos

    # Retorna lista de segmentos baseada nos pontos 3D
    def coverterPontosEmSegmentos(self):
        return self.__transformarSegmentos()

    # Desenha o objeto
    @abstractmethod
    def desenhar(self, cena):
        pass

    # Retorna o tipo físico do objeto
    @abstractmethod
    def tipo(self):
        pass

    # Define um objeto 3D
    def dimensao(self):
        return 3
