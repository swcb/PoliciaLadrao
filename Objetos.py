import pygame

class pol(pygame.sprite.Sprite):
    # This class represents a car. It derives from the "Sprite" class in Pygame.
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(620/31, 261/13, 16, 16)
        self.image = pygame.image.load("images\\pol.png")


class moeda(pygame.sprite.Sprite):
    # This class represents a car. It derives from the "Sprite" class in Pygame.
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((620/31)*3, 261/13, 16, 16)
        self.image = pygame.image.load("images\\moeda.png")