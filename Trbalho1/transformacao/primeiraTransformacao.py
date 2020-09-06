class PrimeiraTransformacao():

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
            for i in range(0, len(objeto.getPontos())):
                if i % 2 != 0:
                    xw = objeto.getPontosFixos()[i-1]
                    yw = objeto.getPontosFixos()[i]
                    xv = ((xw-xwmin)/(xwmax-xwmin))*(xvmax-xvmin)
                    yv = (1-((yw-ywmin)/(ywmax-ywmin)))*(yvmax-yvmin)
                    pontos.append(xv)
                    pontos.append(yv)
                    i+1
            objeto.setPontos(pontos)

    # Operação de zoomIn na window
    def zoomIn(self):
        self.__window.setX2(self.__coordenadasW[2]*0.7)
        self.__window.setY2(self.__coordenadasW[3]*0.7)

    # Operação de zoomOut na window
    def zoomOut(self):
        self.__window.setX2(self.__coordenadasW[2]*1.3)
        self.__window.setY2(self.__coordenadasW[3]*1.3)

    # Move a window para cima
    def up(self):
        self.__window.setY1(self.__coordenadasW[1]-100)
        self.__window.setY2(self.__coordenadasW[3]-100)

    # Move a window para esquerda
    def left(self):
        self.__window.setX1(self.__coordenadasW[0]+100)
        self.__window.setX2(self.__coordenadasW[2]+100)

    # Move a window para direita
    def right(self):
        self.__window.setX1(self.__coordenadasW[0]-100)
        self.__window.setX2(self.__coordenadasW[2]-100)

    # Move a window para baixo
    def down(self):
        self.__window.setY1(self.__coordenadasW[1]+100)
        self.__window.setY2(self.__coordenadasW[3]+100)
