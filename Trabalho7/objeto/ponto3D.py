class Ponto3D:

    # Construtor
    def __init__(self, x, y, z):
        self.__x = x
        self.__y = y
        self.__z = z
        self.__w = 1.0

    # Define coordenada X
    def setX(self, x):
        self.__x = x

    # Define coordenada Y
    def setY(self, y):
        self.__y = y
        
    # Define coordenada Y
    def setZ(self, z):
        self.__z = z

    # Retorna coordenada X
    def X(self):
        return self.__x

    # Retorna coordenada Y
    def Y(self):
        return self.__y
    
    # Retorna coordenada Z
    def Z(self):
        return self.__z

    # Define coordenada W
    def W(self):
        return self.__w

    def pontosStr(self):
        print(str(self.__x) + " " + str(self.__y)+ " " + str(self.__z))
