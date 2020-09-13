from objeto.estruturaPonto import *
from objeto.poligono import *
from objeto.linha import *
from objeto.ponto import *

class DescritorOBJ:
    __arquivoObj = ""
    __vertices = []

    # Passa a window
    def setWindow(self, window):
        self.__window = window

    # Passa a lista de objetos
    def setObjetos(self, objetos):
        self.__objetos = objetos

    # Inicia a lista de vértices com a window
    def __definirVertices(self):
        # Window
        centro = EstruturaPonto(self.__window.centro()[0], self.__window.centro()[1])
        dimensao = EstruturaPonto(self.__window.dimensao()[0], self.__window.dimensao()[1])
        self.__vertices.append(centro) # Pos 1
        self.__vertices.append(dimensao) # Pos 2
        self.__linha = 3

    # Escreve um objeto no arquivo obj
    def escreverOBJ(self, objeto):
        descricaoObj = "o "+objeto.getNome()
        descricaoObj += "\n"
        if objeto.tipo() == 0: # poligono
            descricaoObj += "l "
        elif objeto.tipo() == 1: # linha
            descricaoObj += "l "
        elif objeto.tipo() == 2: # ponto
            descricaoObj += "p "
        for i in range(len(objeto.getPontosFixos())):
            ponto = objeto.getPontosFixos()[i]
            self.__vertices.append(ponto)
            descricaoObj += str(self.__linha)
            if i != len(objeto.getPontosFixos())-1:
                descricaoObj += " "
            self.__linha += 1
        return descricaoObj

    # Escreve a lista de objetos e a window no arquivo obj
    def escreverArquivo(self):
        self.__definirVertices()
        tmpDescricao = ""
        for i in range(len(self.__objetos)):
            objeto = self.__objetos[i]
            tmpDescricao += self.escreverOBJ(objeto)
            if i != len(self.__objetos)-1:
                tmpDescricao += "\n"
        for v in self.__vertices:
            self.__arquivoObj += "v "+str(v.X())+" "+str(v.Y())+" "+str(v.W())+"\n"
        self.__arquivoObj += "o window\n"
        self.__arquivoObj += "w 1 2\n"
        self.__arquivoObj += tmpDescricao
        return self.__arquivoObj

    # Realiza a leitura do arquivo obj, criando os objetos
    def lerArquivo(self, str):
        linhas = str.splitlines()
        tmpVertices = []
        resto = []
        for l in linhas:
            tmpLinha = l.split(" ")
            if tmpLinha[0] == 'v':
                tmpVertices.append(l)
            else:
                resto.append(l)
        for i in range(len(resto)):
            tmpLinha = resto[i].split(" ")
            nome = ""
            if tmpLinha[0] == 'o':
                nome = tmpLinha[1]
                obj = resto[i+1].split(" ")
                if obj[0] == 'w':
                    centro = tmpVertices[int(obj[1])-1].split(" ")
                    dim = tmpVertices[int(obj[2])-1].split(" ")
                    self.__window.setCentro([float(centro[1]), float(centro[2])])
                elif obj[0] == 'p':
                    ponto = tmpVertices[int(obj[1])-1].split(" ")
                    tmpPonto = []
                    tmpPonto.append(EstruturaPonto(float(ponto[1]), float(ponto[2])))
                    p = Ponto(nome, tmpPonto)
                    self.__objetos.append(p)
                elif obj[0] == 'l':
                    if len(obj)-1 == 2:
                        p1 = tmpVertices[int(obj[1])-1].split(" ")
                        p2 = tmpVertices[int(obj[2])-1].split(" ")
                        tmpPonto1 = EstruturaPonto(float(p1[1]), float(p1[2]))
                        tmpPonto2 = EstruturaPonto(float(p2[1]), float(p2[2]))
                        pontos = [tmpPonto1, tmpPonto2]
                        linha = Linha(nome, pontos)
                        self.__objetos.append(linha)
                    elif len(obj)-1 > 2:
                        pontos = []
                        for pos in range(1, len(obj)):
                            p = tmpVertices[int(obj[pos])-1].split(" ")
                            tmpPonto = EstruturaPonto(float(p[1]), float(p[2]))
                            pontos.append(tmpPonto)
                        pol = Poligono(nome, pontos)
                        self.__objetos.append(pol)
