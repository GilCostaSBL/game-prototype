import pygame
import random
import sys
import json
import os

pygame.init()

# --- Screen and layout ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_WIDTH = int(SCREEN_WIDTH * 0.65)
PANEL_X = GAME_WIDTH
PANEL_WIDTH = SCREEN_WIDTH - GAME_WIDTH
LANE_COUNT = 2
LANE_WIDTH = GAME_WIDTH // LANE_COUNT

# --- Colors ---
GREEN = (80, 150, 80)  # grassy background
GRAY = (90, 90, 90)    # pavement lanes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL_BG = (60, 60, 60)
BUTTON_COLOR = (100, 180, 100)

# --- Game setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pick Your Favorite Movie!")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def wrap_text_multi(text, font, max_width):
    """
    Splits text into as many lines as needed to fit within max_width.
    Returns a list of lines.
    """
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = (current_line + " " + word).strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


# --- Classes ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill((255, 200, 50))
        self.rect = self.image.get_rect()
        self.lane = 0
        self.update_position()

    def update_position(self):
        lane_center = self.lane * LANE_WIDTH + LANE_WIDTH // 2
        self.rect.center = (lane_center, SCREEN_HEIGHT - 80)

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.update_position()

    def move_right(self):
        if self.lane < LANE_COUNT - 1:
            self.lane += 1
            self.update_position()


class Poster(pygame.sprite.Sprite):
    def __init__(self, lane, title):
        super().__init__()
        self.image = pygame.Surface((100, 140))
        self.image.fill((random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)))
        self.rect = self.image.get_rect()
        self.lane = lane
        self.title = title
        self.rect.centerx = lane * LANE_WIDTH + LANE_WIDTH // 2
        self.rect.y = -140
        self.speed = 2
        self.title_surface = font.render(self.title, True, WHITE)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def draw(self, surface):
        # --- Poster rectangle ---
        surface.blit(self.image, self.rect)
    
        # --- Title box dimensions ---
        title_box_width = self.rect.width
        title_box_height = 60  # can be adjusted
        title_box_x = self.rect.left
        title_box_y = self.rect.bottom + 15
    
        # Draw the title box (transparent look)
        title_box_rect = pygame.Rect(
            title_box_x,
            title_box_y,
            title_box_width,
            title_box_height
        )
    
        # Optional: faint background to help reading
        overlay = pygame.Surface((title_box_rect.width, title_box_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 80))  # transparent black
        surface.blit(overlay, (title_box_x, title_box_y))
    
        # --- Wrapped text inside the title box ---
        max_text_width = title_box_rect.width - 10  # small padding
        lines = wrap_text_multi(self.title, font, max_text_width)
    
        # Top-aligned text
        y_offset = title_box_y + 5
        for line in lines:
            line_surface = font.render(line, True, WHITE)
            surface.blit(line_surface, (title_box_x + 5, y_offset))
            y_offset += line_surface.get_height() + 2


class SelectionPanel:
    def __init__(self, x, width):
        self.x = x
        self.width = width
        self.selected_titles = []       # last 5 shown
        self.all_selected_titles = []   # full history
        self.font = pygame.font.Font(None, 28)
        self.done_button_rect = pygame.Rect(x + 20, SCREEN_HEIGHT - 60, width - 40, 40)
        self.is_done = False

    def add_title(self, title):
        self.all_selected_titles.append(title)
        self.selected_titles.insert(0, title)
        if len(self.selected_titles) > 5:
            self.selected_titles.pop()

    def draw(self, screen):
        pygame.draw.rect(screen, PANEL_BG, (self.x, 0, self.width, SCREEN_HEIGHT))
        y = 40
        for title in self.selected_titles:
            lines = wrap_text_multi(title, self.font, self.width - 40)

            y_start = y
            for line in lines:
                text = self.font.render(line, True, WHITE)
                screen.blit(text, (self.x + 20, y_start))
                y_start += text.get_height() + 2

            y = y_start + 8  # spacing between entries

        pygame.draw.rect(screen, BUTTON_COLOR, self.done_button_rect)
        btn_text = self.font.render("Done!", True, BLACK)
        text_rect = btn_text.get_rect(center=self.done_button_rect.center)
        screen.blit(btn_text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.done_button_rect.collidepoint(event.pos):
                self.is_done = True

def load_movie_categories():
    json_path = os.path.join(os.path.dirname(__file__), "data", "movies_by_category.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


# --- Game Loop ---
def main():
    player = Player()
    all_sprites = pygame.sprite.Group(player)
    posters = pygame.sprite.Group()
    panel = SelectionPanel(PANEL_X, PANEL_WIDTH)

    movie_categories = load_movie_categories()

    # Flatten all movies into a single list (for now)
    all_movies = []
    for category, movies in movie_categories.items():
        all_movies.extend(movies)

    # Shuffle movies and make pairs
    random.shuffle(all_movies)
    movie_pairs = list(zip(all_movies[0::2], all_movies[1::2]))  # pair every 2 items

    current_pair_index = 0
    pair_active = False

    running = True
    game_done = False
    title_screen = True

    while running:
        screen.fill(GREEN)
        pygame.draw.rect(screen, GRAY, (0, 0, GAME_WIDTH, SCREEN_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_done:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        player.move_right()

                panel.handle_event(event)

        # Title screen
        if title_screen:
            title_text = font.render("Pick your favorite movie from each pair!", True, WHITE)
            text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(title_text, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            title_screen = False
            continue

        if not pair_active and current_pair_index < len(movie_pairs):
            pair_active = True
            left_movie, right_movie = movie_pairs[current_pair_index]
            left_poster = Poster(0, left_movie)
            right_poster = Poster(1, right_movie)
            posters.add(left_poster, right_poster)
            all_sprites.add(left_poster, right_poster)

        all_sprites.update()

        # Collision detection
        for poster in posters:
            if player.rect.colliderect(poster.rect):
                panel.add_title(poster.title)
                for other in list(posters):
                    other.kill()
                pair_active = False
                current_pair_index += 1
                break

        # Draw everything
        for poster in posters:
            poster.draw(screen)

        all_sprites.draw(screen)
        panel.draw(screen)

        # Check done
        if panel.is_done or current_pair_index >= len(movie_pairs):
            game_done = True

        # Final screen
        if game_done:
            screen.fill(PANEL_BG)
            y = 100
            summary_font = pygame.font.Font(None, 40)
            title = summary_font.render("Your Favorite Movies:", True, WHITE)
            screen.blit(title, (100, 40))

            # Show the full persistent list of all selected movies
            for t in panel.all_selected_titles:
                lines = wrap_text_multi(t, summary_font, 600)
                y_line = y
                for line in lines:
                    text = summary_font.render(line, True, WHITE)
                    screen.blit(text, (100, y_line))
                    y_line += text.get_height() + 4
                y = y_line + 12

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
