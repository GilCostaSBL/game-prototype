# src/game.py
import pygame
import random
from src.settings import *
from src.player import Player
from src.obstacle import MoviePoster


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.posters = pygame.sprite.Group()

        # Player
        self.player = Player()
        self.all_sprites.add(self.player)

        # Fonts
        self.font_big = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 28)

        # Game state
        self.score = 0
        self.show_title = True
        self.title_timer = 2000  # ms for title screen
        self.elapsed = 0
        self.pair_active = False
        self.round_delay = 1000  # ms between pairs

        # Dummy movie data (you’ll replace later)
        self.movies = [
            "Inception", "Avatar", "Titanic", "Interstellar",
            "The Matrix", "The Dark Knight", "Up", "WALL·E",
            "Parasite", "The Godfather"
        ]

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS)
            self.events()
            self.update(dt)
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.elapsed += dt

        # --- Title Screen Phase ---
        if self.show_title:
            if self.elapsed > self.title_timer:
                self.show_title = False
                self.elapsed = 0
            return  # Skip rest of update until title done

        # --- Main Gameplay ---
        self.player.update(keys)
        self.posters.update()

        # Spawn a new pair if none active
        if not self.pair_active and self.elapsed > self.round_delay:
            self.spawn_movie_pair()
            self.elapsed = 0
            self.pair_active = True

        # Handle collision (selection)
        hit = pygame.sprite.spritecollideany(self.player, self.posters)
        if hit:
            chosen = hit.title
            print(f"🎬 You selected: {chosen}")
            self.score += 1

            # Remove all current posters
            for p in list(self.posters):
                p.kill()

            # Prepare next pair
            self.elapsed = 0
            self.pair_active = False

    def spawn_movie_pair(self):
        """Create a left/right movie pair."""
        if len(self.movies) < 2:
            self.movies = [
                "Inception", "Avatar", "Titanic", "Interstellar",
                "The Matrix", "The Dark Knight", "Up", "WALL·E",
                "Parasite", "The Godfather"
            ]
        left_movie, right_movie = random.sample(self.movies, 2)
        left_poster = MoviePoster("left", left_movie)
        right_poster = MoviePoster("right", right_movie)

        self.posters.add(left_poster, right_poster)
        self.all_sprites.add(left_poster, right_poster)

    def draw(self):
        self.screen.fill(BLACK)

        # --- Title screen ---
        if self.show_title:
            title_text = self.font_big.render(
                "Pick your favorite movie from each pair!", True, WHITE
            )
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(title_text, title_rect)
            pygame.display.flip()
            return

        # --- Draw gameplay ---
        self.all_sprites.draw(self.screen)

        # Draw movie names
        for poster in self.posters:
            self.screen.blit(poster.text_surface, poster.text_rect)

        # Draw score at bottom
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(score_text, score_rect)

        pygame.display.flip()

    def quit(self):
        pygame.quit()
