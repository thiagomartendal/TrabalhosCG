from PyQt5.QtGui import *
from PyQt5.QtCore import *
from objeto.objeto import *

class Linha(Objeto):

    # Construtor
    def __init__(self, nome, pontos):
        super(Linha, self).__init__(nome, pontos)

    # Desenha o objeto
    def desenhar(self, cena):
        linha = QLineF(self.getPontos()[0], self.getPontos()[1], self.getPontos()[2], self.getPontos()[3]) # dois pontos
        cena().scene().addLine(linha, QPen(QColor(0, 0, 0), 1, Qt.SolidLine))

    # Retorna o tipo físico do objeto
    def tipo(self):
        return 1
