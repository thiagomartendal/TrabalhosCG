from abc import ABC, abstractmethod

class Objeto(ABC):
    __pontos = [] # Vetor de coordenadas
    __pontosFixos = []

    # Construtor
    def __init__(self, nome, pontos):
        self.__nome = nome
        self.__transformarPontos(pontos)
        self.__pontosFixos = [float(p) for p in pontos]

    # Conversão dos pontos de string para float
    def __transformarPontos(self, pontos):
        self.__pontos = [float(p) for p in pontos]

    # Desenha o objeto
    @abstractmethod
    def desenhar(self, cena):
        pass

    # Atualiza a lista de pontos fixos
    def setPontosFixos(self, novosPontos):
        self.__pontosFixos.clear()
        self.__pontosFixos = [float(p) for p in novosPontos]

    # Atualiza a lista de pontos
    def setPontos(self, novosPontos):
        self.__pontos.clear()
        self.__transformarPontos(novosPontos)

    # Retorna o nome
    def getNome(self):
        return self.__nome

    # Retorna os vetor de pontos
    def getPontos(self):
        return self.__pontos

    # Retorna os vetor de pontos iniciais
    def getPontosFixos(self):
        return self.__pontosFixos

    # Retorna o tipo físico do objeto
    @abstractmethod
    def tipo(self):
        pass

    # Retorna o vetor [x, y] da média dos pontos
    def getMediaPontosFixos(self):
        mediaX = 0
        mediaY = 0
        for i in range(1, len(self.__pontosFixos), 2):
            mediaX += self.__pontosFixos[i-1]
            mediaY += self.__pontosFixos[i]
        return [mediaX*2/len(self.__pontosFixos), mediaY*2/len(self.__pontosFixos)]

