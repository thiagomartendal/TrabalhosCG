from PyQt5.QtGui import *
from PyQt5.QtCore import *

class SegmentoReta:

    # Construtor
    def __init__(self, p1, p2):
        # Pontos da classe ponto3D
        self.__p1 = p1
        self.__p2 = p2

    # Modifica o ponto 1
    def setP1(self, p1):
        self.__p1 = p1

    # Modifica o ponto 2
    def setP2(self, p2):
        self.__p2 = p2

    # Retorna o ponto 1
    def P1(self):
        return self.__p1

    # Retorna o ponto 2
    def P2(self):
        return self.__p2

    # Ponto médio de X
    def mediaX(self):
        (self.__p2.X()+self.__p1.X())/2

    # Ponto médio de Y
    def mediaY(self):
        (self.__p2.Y()+self.__p1.Y())/2

    # Ponto médio de Z
    def mediaZ(self):
        (self.__p2.Z()+self.__p1.Z())/2

    # Desenha o segmento de reta
    def desenhar(self, cena, cor):
        linha = QLineF(self.__p1.X(), self.__p1.Y(), self.__p2.X(), self.__p2.Y()) # dois pontos
        cena().scene().addLine(linha, QPen(cor, 1, Qt.SolidLine))
