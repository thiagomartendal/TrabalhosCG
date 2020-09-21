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
