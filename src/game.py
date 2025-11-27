import pygame
import random
import sys
import json
import os
import requests
from io import BytesIO
from requests.packages.urllib3.exceptions import InsecureRequestWarning

pygame.init()

# Suppress the warning caused by setting verify=False
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# --- API Configuration ---
# !!! IMPORTANT: Replace this placeholder with your actual OMDb API key
OMDB_API_KEY = "70e7e6d9" 
OMDB_URL = "http://www.omdbapi.com"


# --- Screen and layout ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_WIDTH = int(SCREEN_WIDTH * 0.65)
PANEL_X = GAME_WIDTH
PANEL_WIDTH = SCREEN_WIDTH - GAME_WIDTH
LANE_COUNT = 2
LANE_WIDTH = GAME_WIDTH // LANE_COUNT

# --- Local Asset Path ---
# Points to a folder named 'assets/posters' one directory up from 'src'
POSTER_ASSET_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "posters")

# --- Colors ---
GREEN = (80, 150, 80)  # grassy background
GRAY = (90, 90, 90)    # pavement lanes
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PANEL_BG = (60, 60, 60)
BUTTON_COLOR = (100, 180, 100)
# NEW: Scrollbar colors
SCROLL_TRACK_COLOR = (120, 120, 120)
SCROLL_THUMB_COLOR = (190, 190, 190)

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

# --- HELPER FUNCTIONS ---

def load_image_from_url(url, width, height):
    """Downloads an image from a URL and returns a scaled Pygame Surface."""
    try:
        # --- CRITICAL CHANGE: Added verify=False here ---
        response = requests.get(url, verify=False)
        response.raise_for_status() # Check for bad status codes
        
        image_file = BytesIO(response.content)
        image_surface = pygame.image.load(image_file).convert_alpha()
        # Scale the image to the new poster size (200x280)
        return pygame.transform.scale(image_surface, (width, height))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from URL {url}: {e}")
    except pygame.error as e:
        print(f"Error loading image into Pygame: {e}")
    
    # Return a default colored surface on failure
    default_surface = pygame.Surface((width, height))
    default_surface.fill(GRAY)
    return default_surface


def get_poster_image(title, api_key, poster_width=200, poster_height=280):
    """
    Attempts to load a poster image: 
    1. From local assets based on title.
    2. From OMDb API if local image is not found.
    3. Returns a fallback surface if both fail.
    """
    
    # ----------------------------------------------------
    # 1. ATTEMPT LOCAL FILE LOAD (PRIORITY)
    # ----------------------------------------------------
    for ext in ['.jpg', '.png']:
        local_path = os.path.join(POSTER_ASSET_DIR, title + ext)
        if os.path.exists(local_path):
            try:
                print(f"Loading local poster for {title}...")
                image_surface = pygame.image.load(local_path).convert_alpha()
                return pygame.transform.scale(image_surface, (poster_width, poster_height))
            except pygame.error as e:
                print(f"Error loading local image {local_path}: {e}. Trying API next.")
                # Continue to API if local load fails
                break

    # ----------------------------------------------------
    # 2. ATTEMPT API LOAD (FALLBACK)
    # ----------------------------------------------------
    try:
        params = {
            't': title,      # Search by exact title
            'apikey': api_key,
            'plot': 'short'
        }
        
        # SSL Bypass is kept here to resolve the certificate error
        response = requests.get(OMDB_URL, params=params, verify=False) 
        data = response.json()

        if data.get('Response') == 'True' and data.get('Poster') not in ('N/A', None):
            poster_url = data['Poster']
            print(f"Fetched poster URL for {title}: {poster_url}")
            return load_image_from_url(poster_url, poster_width, poster_height)
        else:
            print(f"API Failed: Poster not found for {title}. OMDb response: {data.get('Error', 'N/A')}")

    except Exception as e:
        print(f"API Failed: An error occurred during OMDb lookup for {title}: {e}")

    # ----------------------------------------------------
    # 3. RETURN FALLBACK (if both failed)
    # ----------------------------------------------------
    # Fallback: return a randomly colored surface
    print(f"Using default fallback surface for {title}")
    default_surface = pygame.Surface((poster_width, poster_height))
    default_surface.fill((random.randint(100, 200), random.randint(100, 200), random.randint(100, 200)))
    return default_surface

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
    def __init__(self, lane, title, image_surface): 
        super().__init__()
        self.image = image_surface
        self.rect = self.image.get_rect()
        self.lane = lane
        self.title = title
        self.rect.centerx = lane * LANE_WIDTH + LANE_WIDTH // 2
        self.rect.y = -280 
        self.speed = 2
        self.title_surface = font.render(self.title, True, WHITE)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def draw(self, surface):
        # --- Poster image ---
        surface.blit(self.image, self.rect)
    
        # --- Title box constants & preparation ---
        title_box_width = self.rect.width
        title_box_x = self.rect.left
        title_box_y = self.rect.bottom + 15
        
        # Wrapped text preparation
        max_text_width = title_box_width - 10  # small padding
        lines = wrap_text_multi(self.title, font, max_text_width)
        
        line_surfaces = []
        total_text_height = 0
        line_spacing = 2
        vertical_padding = 10 
        
        # 1. Calculate total height and prepare surfaces (Dynamic Height)
        for line in lines:
            line_surface = font.render(line, True, WHITE)
            line_surfaces.append(line_surface)
            total_text_height += line_surface.get_height()
            
        # Add spacing between lines, and top/bottom padding
        if line_surfaces:
            total_text_height += (len(line_surfaces) - 1) * line_spacing
            total_text_height += vertical_padding
            
        title_box_height = max(total_text_height, 20) # Min height
    
        # 2. Draw the title box
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
    
        # 3. Draw Centered Text
        y_offset = title_box_y + (vertical_padding // 2) # Start with top padding (5px)
        for line_surface in line_surfaces:
            # Calculate X position for centering (Centered Text)
            centered_x = title_box_x + (title_box_width - line_surface.get_width()) // 2
            
            surface.blit(line_surface, (centered_x, y_offset))
            y_offset += line_surface.get_height() + line_spacing


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
    
    # Scrolling variables for the final screen
    scroll_y = 0
    scroll_speed = 30 
    
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
            
            # Scrolling input handling when game is done
            if game_done and event.type == pygame.MOUSEBUTTONDOWN:
                # Mouse wheel scroll up = button 4 (scroll list down, increase scroll_y)
                if event.button == 4:
                    scroll_y += scroll_speed
                # Mouse wheel scroll down = button 5 (scroll list up, decrease scroll_y)
                elif event.button == 5:
                    scroll_y -= scroll_speed


        # Title screen
        if title_screen:
            title_text = font.render("Pick your favorite movie from each pair!", True, WHITE)
            text_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(title_text, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            title_screen = False
            continue

        if not pair_active and current_pair_index < len(movie_pairs) and game_done == False:
            pair_active = True
            left_movie, right_movie = movie_pairs[current_pair_index]
            
            # Fetch and load poster images, prioritizing local assets (OMDb call here)
            left_image = get_poster_image(left_movie, OMDB_API_KEY)
            right_image = get_poster_image(right_movie, OMDB_API_KEY)
            
            left_poster = Poster(0, left_movie, left_image)
            right_poster = Poster(1, right_movie, right_image)
            
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
            
            summary_font = pygame.font.Font(None, 40)
            
            # Draw Title
            title = summary_font.render("Your Favorite Movies:", True, WHITE)
            screen.blit(title, (100, 40))

            # Define Viewport and Calculate Total Content Height
            VIEWPORT_Y_START = 80
            VIEWPORT_X_START = 100
            VIEWPORT_WIDTH = SCREEN_WIDTH - VIEWPORT_X_START * 2
            VIEWPORT_HEIGHT = SCREEN_HEIGHT - VIEWPORT_Y_START - 20 # 20px padding at bottom
            
            # 1. Calculate the total height of the content
            total_content_height = 0
            for t in panel.all_selected_titles:
                lines = wrap_text_multi(t, summary_font, 600) 
                
                entry_height = sum(summary_font.size(line)[1] + 4 for line in lines)
                
                total_content_height += entry_height + 12 
            
            # 2. Clamping scroll_y (limits scrolling)
            max_scroll_down = max(0, total_content_height - VIEWPORT_HEIGHT)
            scroll_y = max(min(scroll_y, 0), -max_scroll_down)
            
            # 3. Draw the movie list within the viewport
            
            # Set a clipping rectangle
            clip_rect = pygame.Rect(0, VIEWPORT_Y_START, SCREEN_WIDTH, VIEWPORT_HEIGHT)
            screen.set_clip(clip_rect)

            current_y_render = VIEWPORT_Y_START + scroll_y
            
            # Draw the list, applying the scroll offset
            for t in panel.all_selected_titles:
                lines = wrap_text_multi(t, summary_font, 600)
                y_line = current_y_render
                
                # Render and draw lines
                for line in lines:
                    text = summary_font.render(line, True, WHITE)
                    screen.blit(text, (VIEWPORT_X_START, y_line))
                    y_line += text.get_height() + 4
                
                current_y_render = y_line + 8 # Spacing between entries
            
            # Reset clipping
            screen.set_clip(None)

            # 4. Draw Scrollbar
            if total_content_height > VIEWPORT_HEIGHT:
                SCROLLBAR_WIDTH = 10
                SCROLLBAR_X = SCREEN_WIDTH - 20 # Position near the right edge
                
                # Calculate bar height and position
                scrollbar_height_ratio = VIEWPORT_HEIGHT / total_content_height
                scrollbar_display_height = max(20, VIEWPORT_HEIGHT * scrollbar_height_ratio) # min height 20px
                
                # Calculate bar position: map scroll_y (negative) to a positive position
                scroll_ratio = -scroll_y / max_scroll_down
                bar_y_offset = (VIEWPORT_HEIGHT - scrollbar_display_height) * scroll_ratio
                
                scrollbar_rect = pygame.Rect(
                    SCROLLBAR_X,
                    VIEWPORT_Y_START + bar_y_offset,
                    SCROLLBAR_WIDTH,
                    scrollbar_display_height
                )
                
                # Draw the scrollbar track (background)
                pygame.draw.rect(screen, SCROLL_TRACK_COLOR, (SCROLLBAR_X, VIEWPORT_Y_START, SCROLLBAR_WIDTH, VIEWPORT_HEIGHT), border_radius=5)
                # Draw the scrollbar thumb
                pygame.draw.rect(screen, SCROLL_THUMB_COLOR, scrollbar_rect, border_radius=5)
            
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()