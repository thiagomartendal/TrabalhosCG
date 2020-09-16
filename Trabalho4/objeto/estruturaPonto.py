class EstruturaPonto:

    # Cosntrutor
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__w = 1.0

    # Define coordenada X
    def setX(self, x):
        self.__x = x

    # Define coordenada Y
    def setY(self, y):
        self.__y = y

    # Retorna coordenada X
    def X(self):
        return self.__x

    # Retorna coordenada Y
    def Y(self):
        return self.__y

    # Define coordenada W
    def W(self):
        return self.__w

    def pontosStr(self):
        print(str(self.__x) + " " + str(self.__y))