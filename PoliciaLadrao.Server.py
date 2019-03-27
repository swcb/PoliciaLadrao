import rpyc
import numpy as np


class policiaLadraoServidor(rpyc.Service):

    def __init__(self):
        self.jogadorX = np.array([1, 1]) #guarda a posiçãoX dos jogadores
        self.jogadorY = np.array([8, 2]) #guarda a posiçãoY dos jogadores
        self.limites = (14, 10)
        self.qtChaves = 0 #Variavel de Controle para o Fim do jogo e Atualização do Campo
        self.chavesPega = [] #Guarda a Posição das chaves Pegas
        self.campo = self.exposed_carregaCampo() #Guarda o Campo


    def on_connect(self, conn):
        print('   ~Conectado')
        pass

    def on_disconnect(self, conn):
        print('   ~Desconectado')
        pass

    #Cria o Campo e o Atualiza
    #O campo é Fixo e é retirado dele
    #as chaves ja pegas e em seguida
    #eh atualizada a posição dos jogadores
    def exposed_carregaCampo(self):
        campo = np.ones((10,14), dtype=str)
        campo[:, :] = ' '
        campo[0, :] = campo[5, 2:5] = campo[9, :] = campo[:, 13] = campo[:, 0] = 'X'
        campo[7, 6:10] = campo[7, 11:13] = campo[2:4, 1:2] = campo[4:7, 8] = 'X'
        campo[3, 5] = campo[2, 3] = 'X'
        campo[7:, 2] = 'X'
        campo[1, 5] = campo[2, 9:11] = campo[5, 6] = campo[2, 12] = 'X'
        campo[4, 10:] = 'X'
        campo[7, 7] = campo[2, 2] = campo[5, 3] = campo[7, 12] = '/'
        campo[3, 2] = campo[8, 12] = campo[1, 7] = campo[8, 5] = campo[7, 1] = campo[6, 10] = campo[2, 11] = 'C'
        for n in range(0, len(self.chavesPega)):
            if n % 2 == 0:
                campo[self.chavesPega[n], self.chavesPega[n+1]] = ' '
        campo[self.jogadorX[0], self.jogadorY[0]] = 'L'
        campo[self.jogadorX[1], self.jogadorY[1]] = 'P'
        self.campo = campo
        return campo

    #Manda o campo para o Cliente
    def exposed_getCampo(self):
        return self.campo

    #Verifica se a posição que o jogador
    #deseja ir é permitida
    def verificaMov(self,x,y,z):
        if self.campo[x,y] == 'C':
            if z == 0:
                self.pegaChave(x,y)
            return True
        if self.campo[x,y] == ' ':
            return True
        elif z == 0 and self.campo[x, y] == '/':
            return True
        else:
            return False


    #Verifica se em uma area em formato
    #de cruz ao policial há um ladrao
    #e se o ladrao pegou 5 chaves
    #qualquer um do dois resulta no fim
    def exposed_verificaFim(self):
        if self.jogadorY[1] == self.jogadorY[0] and (self.jogadorX[1]+1 == self.jogadorX[0]   or self.jogadorX[1] - 1 == self.jogadorX[0]):#fixa Y e verifica X -
            return True
        elif  self.jogadorX[1] == self.jogadorX[0] and (self.jogadorY[1] + 1 == self.jogadorY[0] or self.jogadorY[1] - 1 == self.jogadorY[0]):#fixa X e verifica Y !
            return True
        elif self.jogadorX[1] == self.jogadorX[0] and self.jogadorY[1] == self.jogadorY[0]:#Verifica na mesma posicao
            return True
        elif self.qtChaves == 5:
            return True
        return False

    #Aumenta a quantidade de chaves pegas em 1
    #guarda a posição da chave em chavesPegas[]
    def pegaChave(self,x,y):
        self.chavesPega.append(x)
        self.chavesPega.append(y)
        self.qtChaves = self.qtChaves + 1
        self.exposed_carregaCampo()




    #Realiza o movimento para Cima
    # Chama a função Verifica
    # para a possibilidade do movimento
    def exposed_movCima(self,z):
        if self.verificaMov(self.jogadorX[z] - 1, self.jogadorY[z], z) == True:
            self.jogadorX[z] = self.jogadorX[z] - 1
            self.exposed_carregaCampo()

    # Realiza o movimento para Baixo
    # Chama a função Verifica
    # para a possibilidade do movimento
    def exposed_movBaixo(self, z):
        if self.verificaMov(self.jogadorX[z]+1, self.jogadorY[z], z) == True:
            self.jogadorX[z] = self.jogadorX[z] + 1
            self.exposed_carregaCampo()

    #Realiza o movimento para a Esquerda
    #Chama a função Verifica
    #para a possibilidade do movimento
    def exposed_movEsquerda(self, z):
        if self.verificaMov(self.jogadorX[z], self.jogadorY[z] -1, z) == True:
            self.jogadorY[z] = self.jogadorY[z] - 1
            self.exposed_carregaCampo()

    #Realiza o movimento para a Direita
    # Chama a função Verifica
    # para a possibilidade do movimento
    def exposed_movDireita(self, z):
        if self.verificaMov(self.jogadorX[z], self.jogadorY[z] + 1, z) == True:
            self.jogadorY[z] = self.jogadorY[z] + 1
            self.exposed_carregaCampo()




if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(policiaLadraoServidor(), port=18861)
    t.start()
