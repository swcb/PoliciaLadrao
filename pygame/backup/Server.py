import rpyc
import random

class MyServer(rpyc.Service):
    
    def __init__(self):
        self.cont1 = 0
        self.cont2 = 0
        self.num_jogs = 0
        self.end = 15
        self.winner = 0
        self.seq1 = []
        self.seq2 = []
        self.exposed_gera_seq(1)
        self.exposed_gera_seq(2)

    def exposed_comeca(self):
        self.cont1 = 0
        self.cont2 = 0
        self.winner = 0
    
    def on_connect(self, conn):
        self.num_jogs = self.num_jogs+1
        print("Jogador "+str(self.num_jogs) + " Conectado")
        pass

    def on_disconnect(self, conn):
        print("Desconectado")
        pass

    def exposed_gera_seq(self, n_jog):
        seq = []
        
        if(n_jog == 1):
            for i in range(3):
                a = random.randint(1,3)
                seq.append(a)

            self.seq1 = seq
        else:
            for i in range(3):
                a = random.randint(4,6)
                seq.append(a)
            
            self.seq2 = seq

    def exposed_get_jogador(self):
        return self.num_jogs
        
    def exposed_get_seq(self, n_jog):
        if(n_jog == 1):
            return self.seq1
        return self.seq2

    def exposed_anda(self, n_jog):
        if(n_jog == 1):
            self.cont1 = self.cont1 + 1
            if(self.cont1 == self.end):
                self.winner = 1
            self.exposed_gera_seq(n_jog)
        else:
            self.cont2 = self.cont2 + 1
            if(self.cont2 == self.end):
                self.winner = 2
            self.exposed_gera_seq(n_jog)

    def exposed_get_cont(self, n_jog):
        if(n_jog == 1):
            return self.cont1
        return self.cont2
    
    def exposed_get_winner(self):
        return self.winner

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(MyServer(), port=18861)
    t.start()
