import pygame
import rpyc
import Objetos
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

def main():
    #c = rpyc.connect("localhost", 18861)
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.__PYGAMEinit__
    pygame.init()
    jogador = 1
    cont = 0
    relogio = pygame.time.Clock()
    campo1 = 1200, 633
    campo2 = 620, 261
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
    jog1 = Objetos.pol()
    moeda = Objetos.moeda()
    moedas = pygame.sprite.Group()
    moedas.add(moeda)
    x = True
    pygame.key.set_repeat(1, 50)
    while x:
        for event in pygame.event.get():
            pygame.key.get_repeat()
            if event.type == pygame.QUIT:
                x = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not (pos_y - 261/13 <= 0):
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

        for moeda in moedas:
            if pygame.sprite.collide_rect(jog1, moeda):
                moeda.kill()
                cont = cont + 1

        screen.fill(black)
        screen.blit(campo2, camporect)
        for moeda in moedas:
            screen.blit(moeda.image,moeda.rect)
        screen.blit(jog1.image, jog1.rect)
        pygame.display.flip()
        relogio.tick(10)


    pygame.quit()

main()