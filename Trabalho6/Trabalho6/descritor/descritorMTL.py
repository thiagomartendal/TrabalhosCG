from objeto.objeto import *

class DescritorMTL:

    # Construtor
    def __init__(self):
        self.__materiais = []   # lista de duplas (cor, texto)

    # Retorna o nome do material com base na cor (r,g,b) se precisar criando um novo material
    def material(self, cor):
        for m in self.__materiais:
            if m[0] == cor:
                return self.__getMaterialNome(m[1])
        # material novo
        nomeMaterial = "material"+str(len(self.__materiais))
        r = cor[0]/255
        g = cor[1]/255
        b = cor[2]/255
        texto = "newmtl "+nomeMaterial+"\n"
        texto += "Ka 0 0 0"+"\n"
        texto += "Kd "+str(r)+" "+str(g)+" "+str(b)+"\n"
        texto += "illum 1" + "\n"
        self.__materiais.append((cor, texto))
        return nomeMaterial

    # Escreve os materiais no arquivo materiais.mtl
    def gerarArquivo(self):
        texto = ""
        for m in self.__materiais:
            texto += m[1]
        with open('Wavefront.mtl','w') as f:
            f.write(texto)
    
    # Retorna o nome do material
    def __getMaterialNome(self, texto):
        linhas = texto.split("\n")
        linhaNewmtl = linhas[0].split(" ")
        return linhaNewmtl[1]

    # Retorna a cor (r,g,b) do Kd de um determinado material
    def extrairCor(self, nomeArquivo, nomeMaterial):
        with open(nomeArquivo, 'r') as f:
            materiais = f.read().split("newmtl ")[1:]
            r, g, b = (0,0,0)
            for material in materiais:
                linhas = material.split("\n")
                if linhas[0] == nomeMaterial:
                    for linha in linhas[1:]:
                        palavras = linha.split(" ")
                        if palavras[0] == 'Kd':
                            r = min(int( float(palavras[1]) *255), 255)
                            g = min(int( float(palavras[2]) *255), 255)
                            b = min(int( float(palavras[3]) *255), 255)
        return (r,g,b)