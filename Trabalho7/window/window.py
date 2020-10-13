class Window():
    # Coordenadas da Window
    __X1 = 0
    __Y1 = 0
    __X2 = 0
    __Y2 = 0
    __Z = 0
    __anguloZ = 0   # rotacoes no 2D
    __anguloY = 0
    __anguloX = 0

    # Define as coordenadas
    def setDimensao(self, largura, altura):
        self.__X1 = -largura/2
        self.__Y1 = -altura/2
        self.__X2 = largura/2
        self.__Y2 = altura/2
        self.__dimensao = [largura, altura]
        self.__calculoCentro()

    # Altera a coordenada X1
    def setX1(self, x):
        self.__X1 = x
        self.__calculoCentro()

    # Altera a coordenada Y1
    def setY1(self, y):
        self.__Y1 = y
        self.__calculoCentro()

    # Altera a coordenada X2
    def setX2(self, x):
        self.__X2 = x
        self.__calculoCentro()

    # Altera a coordenada Y2
    def setY2(self, y):
        self.__Y2 = y
        self.__calculoCentro()

    def setCentro(self, centro):
        self.__centro = centro

    # Altera a coordenada X2
    def setZ(self, z):
        self.__Z = z

    # Adiciona graus ao angulo da window
    def addAnguloZ(self, angulo):
        self.__anguloZ += angulo

    # Retorna o angulo da window
    def getAnguloZ(self):
        return self.__anguloZ
    
    # Adiciona graus ao angulo da window
    def addAnguloY(self, angulo):
        self.__anguloY += angulo

    # Retorna o angulo da window
    def getAnguloY(self):
        return self.__anguloY

    # Adiciona graus ao angulo da window
    def addAnguloX(self, angulo):
        self.__anguloX += angulo

    # Retorna o angulo da window
    def getAnguloX(self):
        return self.__anguloX

    # Retorna um vetor com o tamanho no eixo X e no eixo Y
    def getSize(self):
        return [(self.__X2 - self.__X1), (self.__Y2 - self.__Y1)]

    # Retorna um vetor com as coordenadas da window
    def coordenadas(self):
        return [self.__X1, self.__Y1, self.__X2, self.__Y2]
    
    # Retorna um vetor com as coordenadas da window
    def coordenadas3D(self):
        return [self.__X1, self.__Y1, self.__X2, self.__Y2, self.__Z]

    # Calcula o centro da window
    def __calculoCentro(self):
        self.__centro = [(self.__X1+self.__X2)/2, (self.__Y1+self.__Y2)/2]

    # Retorna o centro da window
    def centro(self):
        return self.__centro
        
    # Calcula o centro da window
    def centro3D(self):
        return [(self.__X1+self.__X2)/2, (self.__Y1+self.__Y2)/2, self.__Z]

    # Retorna o tamanho da window
    def dimensao(self):
        return self.__dimensao
