# src/player.py
import pygame
from src.settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill((0, 200, 255))
        self.rect = self.image.get_rect()
        
        # Define lanes
        self.lanes = [
            SCREEN_WIDTH // 4,           # left lane center
            (SCREEN_WIDTH * 3) // 4      # right lane center
        ]
        
        # Start in the middle-bottom of the screen, left lane by default
        self.current_lane = 0
        self.rect.centerx = self.lanes[self.current_lane]
        self.rect.bottom = SCREEN_HEIGHT - 100

    def update(self, keys):
        # Move only if there is a lane to switch to
        if keys[pygame.K_LEFT] and self.current_lane > 0:
            self.current_lane -= 1
        elif keys[pygame.K_RIGHT] and self.current_lane < len(self.lanes) - 1:
            self.current_lane += 1

        # Update x position based on lane
        self.rect.centerx = self.lanes[self.current_lane]
