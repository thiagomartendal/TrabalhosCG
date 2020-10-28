from PyQt5.QtGui import *
from PyQt5.QtCore import *

class ZBuffer():

    def __init__(self, painel):
        self.__painel = painel

    def renderizar(self, objetos):
        for obj in objetos:
            corR, corG, corB = obj.getCor()
            cor = QColor(corR, corG, corB)
            for s in obj.getSegmentos2():
                self.desenhar(s, cor)

    # Desenha o segmento de reta
    def desenhar(self, s, cor):
        cena = self.__painel
        if s.P1() != None and s.P2() != None:
            linha = QLineF(s.P1().X(), s.P1().Y(), s.P2().X(), s.P2().Y()) # dois pontos
            cena().scene().addLine(linha, QPen(cor, 1, Qt.SolidLine))
            
            rect = QRectF(s.P1().X(), s.P1().Y(), 1, 1)
            #rect = QRectF(0, 0, 1, 1)
            cena().scene().addRect(rect, QPen(cor, 1, Qt.SolidLine))