import pygame
import rpyc
import Objetos
import  numpy as np
"""
LIXO
    #jog1 = pygame.image.load("images\\pol.png")
    #jog1rect = jog1.get_rect().move([620/31, 261/13])
    #moeda = pygame.image.load("images\\moeda.png")
    #moedarect = moeda.get_rect().move([(620/31)*3, 261/13])

K_UP                  up arrow
K_DOWN                down arrow
K_RIGHT               right arrow
K_LEFT                left arrow
K_w           w       w
K_a           a       a
K_s           s       s
K_d           d       d
car1rect = car1rect.move(speed)
campo2 = 13 x 31.
"""
linha = 620/31
coluna = (261/13)

def cria_Paredes(paredes):
    for i in range (2,5):
        parede = Objetos.wall(i*(620/31),2*(261/13))
        paredes.add(parede)

def block(pos_x, pos_y):
    if pos_y - (261/13) == (261/13)*2 and pos_x == (3*620/31):
        return True
    else:
        return False


def main():
    #c = rpyc.connect("localhost", 18861)
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.__PYGAMEinit__
    pygame.init()
    relogio = pygame.time.Clock()
    campo2 = 620, 261


    #Movimentação
    dir = [620 / 31, 0]
    esq = [-620 / 31, 0]
    up = [0, -261 / 13]
    down = [0, 261 / 13]


    screen = pygame.display.set_mode(campo2)
    pygame.display.set_caption("PoliciaLadrao")
    black = 0, 0, 0
    pos_x = 620/31
    pos_y = 261/13
    campo2 = pygame.image.load("images\\campo2.png")
    camporect = campo2.get_rect().move([0, 0])

    paredes = pygame.sprite.Group()
    cria_Paredes(paredes)

    jog1 = Objetos.ladrao()
    policia = Objetos.policia()
    jogadores = pygame.sprite.Group()
    jogadores.add(policia)
    jogadores.add(jog1)
    ladroes = pygame.sprite.Group()
    policias = pygame.sprite.Group()
    ladroes.add(jog1)
    policias.add(policia)
    moedas = pygame.sprite.Group()
    for i in range (0,7):
        moeda = Objetos.moeda(i, i)
        moedas.add(moeda)
    #posicao = pos_x,pos_y
    x = True
    cont = 0
    pygame.key.set_repeat(1, 50)
    while x:
        for event in pygame.event.get():
            pygame.key.get_repeat()
            if event.type == pygame.QUIT:
                x = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP and not (pos_y - 261/13) <= 0 and not block(pos_x,pos_y):
                    jog1.rect = jog1.rect.move(up)
                    pos_y = pos_y - 261/13
                if event.key == pygame.K_DOWN and not(pos_y + 261/13 > 261 - (2*261/13)):
                    jog1.rect = jog1.rect.move(down)
                    pos_y = pos_y + 261/13
                if event.key == pygame.K_RIGHT and not(pos_x  >= 620 - (2*620/31)):
                    jog1.rect = jog1.rect.move(dir)
                    pos_x = pos_x + 620/31
                if event.key == pygame.K_LEFT and not (pos_x - 620/31 <  620/31):
                    jog1.rect = jog1.rect.move(esq)
                    pos_x = pos_x - 620/31

        #for moeda in moedas:
         #   if pygame.sprite.collide_rect(jog1, moeda):
          #      moeda.kill()
                cont = cont + 1
        for ladrao in ladroes:
            if pygame.sprite.spritecollide(ladrao,policias,True):
                cont = cont + 1
                #policia.kill()
            #x =False

        screen.fill(black)
        screen.blit(campo2, camporect)
        for moeda in moedas:
            screen.blit(moeda.image,moeda.rect)
        #screen.blit(jog1.image, jog1.rect)
        for jogador in jogadores:
            screen.blit(jogador.image,jogador.rect)
        pygame.display.flip()
        relogio.tick(10)


    pygame.quit()
    print(cont)

main()