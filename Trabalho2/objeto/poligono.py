from PyQt5.QtGui import *
from PyQt5.QtCore import *
from objeto.objeto import *

class Poligono(Objeto):

    # Construtor
    def __init__(self, nome, pontos):
        super(Poligono, self).__init__(nome, pontos)

    # Desenha o objeto
    def desenhar(self, cena):
        pontos = []
        for i in range(0, len(self.getPontos())):
            pontos.append(QPointF(self.getPontos()[i].X(), self.getPontos()[i].Y()))
        poligono = QPolygonF(pontos) # infinitos pontos
        cena().scene().addPolygon(poligono, QPen(QColor(0, 0, 0), 1, Qt.SolidLine), QBrush(Qt.NoBrush))

    # Retorna o tipo físico do objeto
    def tipo(self):
        return 0
