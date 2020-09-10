class Window():
    # Coordenadas da Window
    __X1 = 0
    __Y1 = 0
    __X2 = 0
    __Y2 = 0
    __angulo = 0

    # Define as coordenadas
    def setDimensao(self, largura, altura):
        self.__X1 = -largura/2
        self.__Y1 = -altura/2
        self.__X2 = largura/2
        self.__Y2 = altura/2

    # Altera a coordenada X1
    def setX1(self, x):
        self.__X1 = x

    # Altera a coordenada Y1
    def setY1(self, y):
        self.__Y1 = y

    # Altera a coordenada X2
    def setX2(self, x):
        self.__X2 = x

    # Altera a coordenada Y2
    def setY2(self, y):
        self.__Y2 = y

    # Adiciona graus ao angulo da window
    def addAngulo(self, angulo):
        self.__angulo += angulo

    # Retorna o angulo da window
    def getAngulo(self):
        return self.__angulo

    # Retorna um vetor com o tamanho no eixo X e no eixo Y
    def getSize(self):
        return [(self.__X2 - self.__X1), (self.__Y2 - self.__Y1)]

    # Retorna um vetor com as coordenadas da window
    def coordenadas(self):
        return [self.__X1, self.__Y1, self.__X2, self.__Y2]

    # Retorna o centro da window
    def centro(self):
        return [(self.__X1+self.__X2)/2, (self.__Y1+self.__Y2)/2]
