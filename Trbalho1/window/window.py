class Window():
    # Coordenadas da Window
    __X1 = 0
    __Y1 = 0
    __X2 = 0
    __Y2 = 0

    # Define as coordenadas
    def setCoordenadas(self, x, y):
        self.__X1 = -1*x
        self.__Y1 = -1*y
        self.__X2 = x
        self.__Y2 = y

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

    # Retorna um vetor com as coordenadas da window
    def coordenadas(self):
        return [self.__X1, self.__Y1, self.__X2, self.__Y2]

    # Retorna o centro da window
    def centro(self):
        return [self.__X2/2, self.__Y2/2]
