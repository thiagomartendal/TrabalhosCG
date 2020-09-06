from PyQt5.QtGui import *
from PyQt5.QtCore import *
from objeto.objeto import *

class Linha(Objeto):

    # Construtor
    def __init__(self, nome, pontos):
        super(Linha, self).__init__(nome, pontos)

    # Desenha o objeto
    def desenhar(self, cena):
        linha = QLineF(self.getPontos()[0].X(), self.getPontos()[0].Y(), self.getPontos()[1].X(), self.getPontos()[1].Y()) # dois pontos
        cena().scene().addLine(linha, QPen(QColor(0, 0, 0), 1, Qt.SolidLine))

    # Retorna o tipo físico do objeto
    def tipo(self):
        return 1
