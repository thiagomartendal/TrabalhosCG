from PyQt5.QtGui import *
from PyQt5.QtCore import *
from objeto.objeto import *

class Ponto(Objeto):

    # Construtor
    def __init__(self, nome, pontos):
        super(Ponto, self).__init__(nome, pontos)

    # Desenha o objeto
    def desenhar(self, cena):
        if len(self.getPontos()) > 0:
            cor = QColor(self.getCor()[0], self.getCor()[1], self.getCor()[2])
            ponto = QLineF(self.getPontos()[0].X(), self.getPontos()[0].Y(), self.getPontos()[0].X(), self.getPontos()[0].Y()) # um ponto
            cena().scene().addLine(ponto, QPen(cor, 1, Qt.SolidLine))

    # Retorna o tipo físico do objeto
    def tipo(self):
        return 2
