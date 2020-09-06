from PyQt5.QtGui import *
from PyQt5.QtCore import *
from objeto.objeto import *

class Ponto(Objeto):

    # Construtor
    def __init__(self, nome, pontos):
        super(Ponto, self).__init__(nome, pontos)

    # Desenha o objeto
    def desenhar(self, cena):
        ponto = QLineF(self.getPontos()[0].X(), self.getPontos()[0].Y(), self.getPontos()[0].X(), self.getPontos()[0].Y()) # um ponto
        cena().scene().addLine(ponto, QPen(QColor(0, 0, 0), 3, Qt.SolidLine))

    # Retorna o tipo físico do objeto
    def tipo(self):
        return 2
