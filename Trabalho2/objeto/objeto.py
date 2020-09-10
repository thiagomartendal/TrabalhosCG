from abc import ABC, abstractmethod

class Objeto(ABC):
    __pontos = [] # Vetor de coordenadas
    __pontosFixos = []
    __pontosNormalizados = []
    __cor = (0,0,0)

    # Construtor
    def __init__(self, nome, pontos):
        self.__nome = nome
        self.__pontos = [p for p in pontos]
        self.__pontosFixos = [p for p in pontos]

    # Desenha o objeto
    @abstractmethod
    def desenhar(self, cena):
        pass

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
    @abstractmethod
    def tipo(self):
        pass

    # Retorna o vetor [x, y] da média dos pontos
    def getMediaPontosFixos(self):
        mediaX = 0
        mediaY = 0
        for p in self.__pontosFixos:
            mediaX += p.X()
            mediaY += p.Y()
        return [mediaX/len(self.__pontosFixos), mediaY/len(self.__pontosFixos)]
