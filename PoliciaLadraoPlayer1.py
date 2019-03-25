import pygame
import rpyc
"""
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

#c = rpyc.connect("localhost", 18861)
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.__PYGAMEinit__
pygame.init()
jogador = 1
relogio = pygame.time.Clock()
campo1 = 1200,633
campo2 = 620, 261
dir = [620/31, 0]
esq = [-620/31, 0]
up = [0, -261/13]
down = [0, 261/13]
screen = pygame.display.set_mode(campo2)
pygame.display.set_caption("PoliciaLadrao")
black = 0, 0, 0
pos_x = 620/31
pos_y = 261/13
campo2 = pygame.image.load("images\\campo2.png")
camporect = campo2.get_rect().move([0, 0])
jog1 = pygame.image.load("images\\pol.png")
jog1rect = jog1.get_rect().move([620/31, 261/13])
x = True
pygame.key.set_repeat(1, 50)
while x:

    for event in pygame.event.get():
        pygame.key.get_repeat()
        if event.type == pygame.QUIT:
            x = False
        if event.type == pygame.KEYDOWN:#Movimentacao com Bordas
            if event.key == pygame.K_UP:
                if pos_y - 261/13 <= 0:
                    break
                jog1rect = jog1rect.move(up)
                pos_y = pos_y - 261/13
            if event.key == pygame.K_DOWN:
                if pos_y + 261/13 > 261 - (2*261/13):
                    break
                jog1rect = jog1rect.move(down)
                pos_y = pos_y + 261/13
            if event.key == pygame.K_RIGHT:
                if pos_x  >= 620 - (2*620/31):
                    break
                jog1rect = jog1rect.move(dir)
                pos_x = pos_x + 620/31
            if event.key == pygame.K_LEFT:
                if pos_x - 620/31 <  620/31:
                    break
                jog1rect = jog1rect.move(esq)
                pos_x = pos_x - 620/31


    screen.fill(black)
    screen.blit(campo2, camporect)
    screen.blit(jog1, jog1rect)
    pygame.display.flip()
    relogio.tick(10)

pygame.quit()