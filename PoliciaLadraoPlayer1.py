import pygame
import rpyc
import Objetos
import numpy as np
import time

"""
pos_x = 620/31*29
    pos_y = 261/13*11
    px = 29
    py = 11

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

fim = False

#Verificacao da movimentacao do policial
def block(px, py, campo):
    if campo[py,px] == 1 or campo[py,px] == 2:
        return True
    else:
        return False


#Verificacao da movimentacao do ladrao
def blockl(px, py, campo):
    if campo[py, px] == 1:
        return True
    else:
        return False




def main():
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

    #Tela e Campo
    screen = pygame.display.set_mode(campo2)
    pygame.display.set_caption("PoliciaLadrao")
    black = 0, 0, 0
    campo2 = pygame.image.load("images\\campo2.png")
    camporect = campo2.get_rect().move([0, 0])


    #Tela de Vitoria e Derrota
    lose = Objetos.lose()
    win = Objetos.win()

    #Posição inicial do jogador
    #trocar para a chamada ao servidor que irá fornecer
    #pos = a posicao usada para desenhar na tela
    #p = posicao na matrix do campo para verificacao da movimentacao
    x1 = 620/31
    y1 = 261/13


    #Campo em matriz para criar as paredes internas.
    campo = np.zeros((13,31))
    campo[2::2,2::2] = 1
    campo[2, 3] = campo[2, 19] = campo[2, 27] = 1
    campo[1, 8] = campo[3, 22] = campo[5, 14] = campo[5, 20] = campo[11, 12] = 1
    campo[4, 3] = campo[4, 13] = campo[4, 27] = 1
    campo[6, 1] = campo[6, 7] = campo[6, 23] = campo[6, 29] = 1
    campo[10, 1] = campo[10, 9] = campo[10, 13] = campo[10, 25] = campo[10, 29] = 1
    campo[2, 1] = campo[2, 9] = campo[4, 23] = campo[4, 29] = campo[5, 16] = campo[6, 11] = 2
    campo[7, 4] = campo[9, 18] = campo[10, 3] = campo[10, 11] = campo[10, 27] = 2

    #Criacao do jogador e dos grupos
    #deverá ser feita no servidor
    #e o jogador recebera o seu sprite
    #e todos os grupos
    ladrao = pygame.image.load("images\\ladrao.png")
    policia = pygame.image.load("images\\pol.png")
    moedas = pygame.sprite.Group()
    pos_xMoeda = [x1, x1*29, x1*18, x1*13, x1*10, x1*24, x1, x1*10]
    pos_yMoeda = [y1*11, y1, y1*7, y1*11, y1*3, y1*5, y1*7, y1*9]
    for i in range(0,7):
        moeda = Objetos.moeda(pos_xMoeda[i],pos_yMoeda[i])
        moedas.add(moeda)

    #Contador de moedas e condicao para fim
    #o contador sera guardado no servidor
    cont = 0

    #repeticao das teclas
    #em mls (pelo menos o segundo)


    conn = rpyc.connect("localhost", 18861)
    indole = conn.root.getIndole()
    indice = conn.root.getIndice()
    pos_x = conn.root.pos_x[indice]
    pos_y = conn.root.pos_y[indice]
    px = conn.root.x[indice]
    py = conn.root.y[indice]
    if indole == 'ladrao':
        jog1 = Objetos.ladrao(pos_x, pos_y)
        pygame.key.set_repeat(150)
    else:
        jog1 = Objetos.policia(pos_x, pos_y)
        pygame.key.set_repeat(50)
    conn.root.getCredenciais(jog1.rect, indole)
    #sons do jogo
    ncont = ["nada", "one", "two", "three", "four", "five"]
    you_sound = pygame.mixer.Sound("sounds\you.wav")
    win_sound = pygame.mixer.Sound("sounds\win.wav")
    lose_sound = pygame.mixer.Sound("sounds\lose.wav")
    soundtrack = 'sounds\open_stage.mp3'
    pygame.mixer_music.load(soundtrack)


    fim = conn.root.getFim()
    start_music = True
    fim1 = False
    winc = 3
    while not fim and not fim1:
        if start_music:
            pygame.mixer_music.set_volume(0.05)
            pygame.mixer_music.play(-1)
            start_music = False
        for event in pygame.event.get():
            pygame.key.get_repeat()
            if event.type == pygame.QUIT:
                fim1 = True
                pygame.mixer_music.pause()
                if indole == 'ladrao':
                    winc = 0
                else:
                    winc = 1

            if event.type == pygame.KEYDOWN:
                if(indole == 'ladrao'):
                    if event.key == pygame.K_UP and not (pos_y - 261/13) <= 0 and not blockl(px,py-1,campo):
                        jog1.rect = jog1.rect.move(up)
                        py = py - 1
                        pos_y = pos_y - 261/13
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_DOWN and not(pos_y + 261/13 > 261 - (2*261/13)) and not blockl(px,py+1,campo):
                        jog1.rect = jog1.rect.move(down)
                        py = py + 1
                        pos_y = pos_y + 261/13
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_RIGHT and not(pos_x  >= 620 - (2*620/31)) and not blockl(px+1,py,campo):
                        jog1.rect = jog1.rect.move(dir)
                        px = px + 1
                        pos_x = pos_x + 620/31
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_LEFT and not (pos_x - 620/31 <  620/31) and not blockl(px-1,py,campo):
                        jog1.rect = jog1.rect.move(esq)
                        px = px - 1
                        pos_x = pos_x - 620/31
                        conn.root.putJogador(indice, jog1.rect)
                else:
                    if event.key == pygame.K_UP and not (pos_y - 261/13) <= 0 and not block(px,py-1,campo):
                        jog1.rect = jog1.rect.move(up)
                        py = py - 1
                        pos_y = pos_y - 261/13
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_DOWN and not(pos_y + 261/13 > 261 - (2*261/13)) and not block(px,py+1,campo):
                        jog1.rect = jog1.rect.move(down)
                        py = py + 1
                        pos_y = pos_y + 261/13
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_RIGHT and not(pos_x  >= 620 - (2*620/31)) and not block(px+1,py,campo):
                        jog1.rect = jog1.rect.move(dir)
                        px = px + 1
                        pos_x = pos_x + 620/31
                        conn.root.putJogador(indice, jog1.rect)
                    if event.key == pygame.K_LEFT and not (pos_x - 620/31 <  620/31) and not block(px-1,py,campo):
                        jog1.rect = jog1.rect.move(esq)
                        px = px - 1
                        pos_x = pos_x - 620/31
                        conn.root.putJogador(indice, jog1.rect)

        #Verifica se o jogador passou por uma moeda
        #O servidor tem q fazer isso verificando
        #se algum ladrao passou por moeda
        aux = conn.root.Killmoeda
        for moeda in moedas:
            if (moeda.rect == aux):
                moeda.kill()
                cont += 1
                son = pygame.mixer.Sound("sounds\\" + ncont[cont] + ".wav")
                son.set_volume(0.7)
                son.play()

        for moeda in moedas:
            if pygame.sprite.collide_rect(jog1, moeda) and indole == 'ladrao':
                moeda.kill()
                cont += 1
                son = pygame.mixer.Sound("sounds\\" + ncont[cont] + ".wav")
                son.set_volume(0.7)
                son.play()
                conn.root.setKillmoeda(moeda.rect)
                conn.root.cont()

        #Verifica se algum larao colidiu com
        #algum policial
        joga = conn.root.getJogadores()
        minha = joga[indice]
        if (indole == 'ladrao'):
            for jog in joga:
                if jog['posicao'] == minha['posicao'] and jog['indole'] == 'policia':
                    conn.root.delJogador(indice)
                    fim1 = True

        #Desenho da tela
        screen.fill(black)
        screen.blit(campo2, camporect)
        for moeda in moedas:
            screen.blit(moeda.image,moeda.rect)
        screen.blit(jog1.image, jog1.rect)
        jogadores = conn.root.getJogadores()
        for jogador in jogadores:
            if(jogador['vivo']):
                if(jogador['indole'] == 'ladrao'):
                    screen.blit(ladrao, jogador['posicao'])
                else:
                    screen.blit(policia, jogador['posicao'])
        pygame.display.flip()
        relogio.tick(30)
        fim = conn.root.getFim()
        if fim:
            pygame.mixer_music.pause()

        winb = conn.root.win



    confirm = False
    c_sound = 0
    while (not confirm):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirm = True
            #if event.type == pygame.KEYDOWN:
            #    confirm = True



        screen.fill(black)
        screen.blit(campo2, camporect)
        for jogador in jogadores:
            if (jogador['vivo']):
                if (jogador['indole'] == 'ladrao'):
                    screen.blit(jog1.image, jogador['posicao'])
                else:
                    screen.blit(policia, jogador['posicao'])
        if indole == 'ladrao':
            if (winb == 0) or (winc == 0):
                screen.blit(lose.image, lose.rect)
                pygame.display.flip()
                if c_sound == 0:
                    c_sound += 1
                    time.sleep(1)
                    you_sound.play(0)
                    time.sleep(1)
                    lose_sound.play(0)
            else:
                screen.blit(win.image, win.rect)
                pygame.display.flip()
                if c_sound == 0:
                    c_sound += 1
                    time.sleep(1)
                    you_sound.play(0)
                    time.sleep(1)
                    win_sound.play(0)
        else:
            if winb == 1 or winc == 1:
                screen.blit(lose.image, lose.rect)
                pygame.display.flip()
            if c_sound == 0:
                c_sound += 1
                time.sleep(1)
                you_sound.play(0)
                time.sleep(1)
                lose_sound.play(0)
            else:
                screen.blit(win.image, win.rect)
                pygame.display.flip()
                if c_sound == 0:
                    c_sound += 1
                    time.sleep(1)
                    you_sound.play(0)
                    time.sleep(1)
                    win_sound.play(0)
        pygame.display.flip()



    #pygame.quit()
    print(cont)
main()