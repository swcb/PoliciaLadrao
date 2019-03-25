import pygame
import rpyc
import sys
import time
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
campo1 = 1200,633
campo2 = 621, 263
speed = [621/31, 0]
screen = pygame.display.set_mode(campo2)
pygame.display.set_caption("PoliciaLadrao")
black = 0, 0, 0
campo2 = pygame.image.load("images\\campo2.png")
camporect = campo2.get_rect().move([0, 0])
jog1 = pygame.image.load("images\\pol.png")
jog1rect = jog1.get_rect().move([1, 1])
x = True
while x:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            x = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                jog1rect = jog1rect.move(speed)
            if event.key == pygame.K_DOWN:
                jog1rect = jog1rect.move(speed)
            if event.key == pygame.K_RIGHT:
                jog1rect = jog1rect.move(speed)
            if event.key == pygame.K_LEFT:
                jog1rect = jog1rect.move(speed)


    screen.fill(black)
    screen.blit(campo2, camporect)
    screen.blit(jog1, jog1rect)
    pygame.display.flip()

pygame.quit()