from objeto.estruturaPonto import *

class PrimeiraTransformacao:

    # Construtor
    def __init__(self, objetos, window, coordenadasV):
        self.__objetos = objetos
        self.__window = window
        self.__coordenadasV = coordenadasV
        self.__coordenadasW = self.__window.coordenadas()

    # Calculo da transformada de viewport
    def transformadaViewport(self):
        xwmin = self.__coordenadasW[0]
        ywmin = self.__coordenadasW[1]
        xwmax = self.__coordenadasW[2]
        ywmax = self.__coordenadasW[3]
        xvmin = self.__coordenadasV[0]
        yvmin = self.__coordenadasV[1]
        xvmax = self.__coordenadasV[2]
        yvmax = self.__coordenadasV[3]
        for objeto in self.__objetos:
            pontos = []
            for p in objeto.getPontosFixos():
                xw = p.X()
                yw = p.Y()
                xv = ((xw-xwmin)/(xwmax-xwmin))*(xvmax-xvmin)
                yv = (1-((yw-ywmin)/(ywmax-ywmin)))*(yvmax-yvmin)
                pontos.append(EstruturaPonto(xv, yv))
            objeto.setPontos(pontos)

    # Operação de zoomIn na window
    def zoomIn(self):
        qnt = [100, 100]
        self.__window.setX1(self.__coordenadasW[0] + qnt[0]/2)
        self.__window.setX2(self.__coordenadasW[2] - qnt[0]/2)
        self.__window.setY1(self.__coordenadasW[1] + qnt[1]/2)
        self.__window.setY2(self.__coordenadasW[3] - qnt[1]/2)

    # Operação de zoomOut na window
    def zoomOut(self):
        qnt = [100, 100]
        self.__window.setX1(self.__coordenadasW[0] - qnt[0]/2)
        self.__window.setX2(self.__coordenadasW[2] + qnt[0]/2)
        self.__window.setY1(self.__coordenadasW[1] - qnt[1]/2)
        self.__window.setY2(self.__coordenadasW[3] + qnt[1]/2)

    # Move a window para cima
    def up(self):
        qnt = 100
        self.__window.setY1(self.__coordenadasW[1] - qnt)
        self.__window.setY2(self.__coordenadasW[3] - qnt)

    # Move a window para esquerda
    def left(self):
        qnt = 100
        self.__window.setX1(self.__coordenadasW[0] + qnt)
        self.__window.setX2(self.__coordenadasW[2] + qnt)

    # Move a window para direita
    def right(self):
        qnt = 100
        self.__window.setX1(self.__coordenadasW[0] - qnt)
        self.__window.setX2(self.__coordenadasW[2] - qnt)

    # Move a window para baixo
    def down(self):
        qnt = 100
        self.__window.setY1(self.__coordenadasW[1] + qnt)
        self.__window.setY2(self.__coordenadasW[3] + qnt)
