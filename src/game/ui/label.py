import pygame


class Label:

    def __init__(self, text, x, y, size=20, color="white"):
        self.font = pygame.font.SysFont("Arial", size)
        self.image = self.font.render(text, True, color)
        _, _, w, h = self.image.get_rect()
        self.screen = None
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def setScreen(self, screen):
        self.screen = screen

    def updateText(self, newtext, color="white"):
        self.image = self.font.render(newtext, 1, color)

    def changeFont(self, font, size, color="white"):
        self.font = pygame.font.SysFont(font, size)
        self.change_text(self.text, color)

    def draw(self):
        self.screen.blit(self.image, (self.rect))