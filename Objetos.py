import pygame

class ladrao(pygame.sprite.Sprite):
    # This class represents a car. It derives from the "Sprite" class in Pygame.
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(620/31, 261/13, 16, 16)
        self.image = pygame.image.load("images\\ladrao.png")


class moeda(pygame.sprite.Sprite):
    # This class represents a car. It derives from the "Sprite" class in Pygame.
    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((620/31)*3 * x, (261/13) * y, 16, 16)
        self.image = pygame.image.load("images\\moeda.png")

class policia(pygame.sprite.Sprite):
    # This class represents a car. It derives from the "Sprite" class in Pygame.
    def __init__(self):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((620/31)*20, (261/13)*5, 16, 16)
        self.image = pygame.image.load("images\\pol.png")