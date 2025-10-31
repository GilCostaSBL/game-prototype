# src/obstacle.py
import pygame
import random
from src.settings import *

class MoviePoster(pygame.sprite.Sprite):
    def __init__(self, lane, title):
        super().__init__()
        self.image = pygame.Surface((100, 150))
        self.image.fill((random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
        self.rect = self.image.get_rect()
        
        # Position based on lane
        if lane == "left":
            self.rect.centerx = SCREEN_WIDTH // 4
        else:
            self.rect.centerx = (SCREEN_WIDTH * 3) // 4

        self.rect.y = -150  # start above the screen
        self.speed = 2  # slower drop for readability
        self.title = title

        # Font for title
        self.font = pygame.font.SysFont(None, 24)
        self.text_surface = self.font.render(title, True, WHITE)
        self.text_rect = self.text_surface.get_rect(center=(self.rect.centerx, self.rect.bottom + 15))

    def update(self):
        self.rect.y += self.speed
        self.text_rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
