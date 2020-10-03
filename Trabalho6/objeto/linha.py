from PyQt5.QtGui import *
from PyQt5.QtCore import *
from objeto.objeto import *

class Linha(Objeto):

    # Construtor
    def __init__(self, nome, pontos):
        super(Linha, self).__init__(nome, pontos)

    # Desenha o objeto
    def desenhar(self, cena):
        if len(self.getPontos()) > 0:
            cor = QColor(self.getCor()[0], self.getCor()[1], self.getCor()[2])
            linha = QLineF(self.getPontos()[0].X(), self.getPontos()[0].Y(), self.getPontos()[1].X(), self.getPontos()[1].Y()) # dois pontos
            cena().scene().addLine(linha, QPen(cor, 1, Qt.SolidLine))

    # Retorna o tipo físico do objeto
    def tipo(self):
        return 1
