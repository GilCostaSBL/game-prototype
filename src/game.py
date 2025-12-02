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
RED = (200, 50, 50)
PANEL_BG = (60, 60, 60)
BUTTON_COLOR = (100, 180, 100)
# NEW: Scrollbar colors
SCROLL_TRACK_COLOR = (120, 120, 120)
SCROLL_THUMB_COLOR = (190, 190, 190)
RESULTS_BOX_BG = (40, 40, 40) # New background for the movie list box
RESET_BUTTON_COLOR = (50, 50, 150) # New color for the reset button

# --- Game States ---
TITLE_SCREEN = 0
RUNNING = 1
DONE = 2

# --- Game setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pick Your Favorite Movie!")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# NEW: Dedicated fonts for game experience
TITLE_FONT = pygame.font.SysFont('Consolas', 72, bold=True) # Pixel-art style font simulation
INSTRUCTION_FONT = pygame.font.Font(None, 30)
SUMMARY_TITLE_FONT = pygame.font.SysFont('Consolas', 48, bold=True) # Similar style for results
RESET_SYMBOL_FONT = pygame.font.Font(None, 40) # Font for the arrow symbol

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

def load_image_from_url(url, width, height_limit):
    """Downloads an image from a URL and returns a scaled Pygame Surface."""
    try:
        # --- CRITICAL CHANGE: Added verify=False here ---
        response = requests.get(url, verify=False)
        response.raise_for_status() # Check for bad status codes
        
        image_file = BytesIO(response.content)
        image_surface = pygame.image.load(image_file).convert_alpha()

        # NEW SCALING LOGIC
        original_width = image_surface.get_width()
        original_height = image_surface.get_height()
        
        # 1. Calculate new height based on fixed width (216) and aspect ratio
        new_height = int(width * (original_height / original_width))
        # 2. Apply the height limit (320)
        final_height = min(new_height, height_limit)
        
        # 3. Scale the image
        return pygame.transform.scale(image_surface, (width, final_height))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image from URL {url}: {e}")
    except pygame.error as e:
        print(f"Error loading image into Pygame: {e}")
    
    # Return a default colored surface on failure
    default_surface = pygame.Surface((width, height_limit))
    default_surface.fill(GRAY)
    return default_surface


def get_poster_image(title, api_key, poster_width=216, poster_height_limit=320):
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

                # NEW LOCAL SCALING LOGIC
                new_height = int(poster_width * (image_surface.get_height() / image_surface.get_width()))
                final_height = min(new_height, poster_height_limit)

                return pygame.transform.scale(image_surface, (poster_width, final_height))
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
            # UPDATED: Pass width and height_limit to loader
            return load_image_from_url(poster_url, poster_width, poster_height_limit)
        else:
            print(f"API Failed: Poster not found for {title}. OMDb response: {data.get('Error', 'N/A')}")

    except Exception as e:
        print(f"API Failed: An error occurred during OMDb lookup for {title}: {e}")

    # ----------------------------------------------------
    # 3. RETURN FALLBACK (if both failed)
    # ----------------------------------------------------
    # Fallback: return a randomly colored surface
    print(f"Using default fallback surface for {title}")
    # UPDATED: Use width and height_limit for fallback surface size
    default_surface = pygame.Surface((poster_width, poster_height_limit))
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
        
        # CHANGED: Align the poster by its bottom edge, starting it at Y=0 (the top of the screen).
        # Pygame automatically calculates rect.y = rect.bottom - rect.height.
        self.rect.bottom = 0
        
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
        # self.selected_titles = []       # Removed: use all_selected_titles for full list
        self.all_selected_titles = []   # full history
        self.font = pygame.font.Font(None, 28)
        self.done_button_rect = pygame.Rect(x + 20, SCREEN_HEIGHT - 60, width - 40, 40)
        self.is_done = False

        # NEW SCROLLING VARIABLES
        self.scroll_y = 0
        self.scroll_speed = 30
        
        # Define the viewport for the list content
        self.LIST_MARGIN = 10
        self.VIEWPORT_Y_START = 40
        # VIEWPORT_HEIGHT is calculated based on screen height minus margins and button height
        self.VIEWPORT_HEIGHT = SCREEN_HEIGHT - self.VIEWPORT_Y_START - self.done_button_rect.height - 40
        self.VIEWPORT_WIDTH = self.width - self.LIST_MARGIN * 2 - 10 # 10px buffer for scrollbar
        self.VIEWPORT_RECT = pygame.Rect(
            self.x + self.LIST_MARGIN,
            self.VIEWPORT_Y_START,
            self.width - self.LIST_MARGIN * 2,
            self.VIEWPORT_HEIGHT
        )

    def add_title(self, title):
        self.all_selected_titles.append(title)
        # Note: No need to limit the list size here.

    def draw(self, screen):
        # 1. Draw Panel Background
        pygame.draw.rect(screen, PANEL_BG, (self.x, 0, self.width, SCREEN_HEIGHT))
        
        # 2. Draw Done Button
        pygame.draw.rect(screen, BUTTON_COLOR, self.done_button_rect)
        btn_text = self.font.render("Done!", True, BLACK)
        text_rect = btn_text.get_rect(center=self.done_button_rect.center)
        screen.blit(btn_text, text_rect)

        # 3. Content Rendering (Scrolling Logic)
        
        # --- Calculate Total Content Height ---
        total_content_height = 0
        list_font = self.font
        
        for t in self.all_selected_titles:
            lines = wrap_text_multi(t, list_font, self.VIEWPORT_WIDTH)
            entry_height = sum(list_font.size(line)[1] + 4 for line in lines)
            total_content_height += entry_height + 8 # 8px spacing between entries

        # --- Clamping scroll_y ---
        max_scroll_down = max(0, total_content_height - self.VIEWPORT_HEIGHT)
        self.scroll_y = max(min(self.scroll_y, 0), -max_scroll_down)

        # --- Draw List within Viewport (Clipping) ---
        
        # Set a clipping rectangle 
        clip_rect = self.VIEWPORT_RECT.copy()
        clip_rect.x += 1
        clip_rect.y += 1
        clip_rect.width -= 2
        clip_rect.height -= 2
        screen.set_clip(clip_rect)

        current_y_render = self.VIEWPORT_Y_START + self.scroll_y
        
        # Draw the list, applying the scroll offset
        for t in self.all_selected_titles:
            lines = wrap_text_multi(t, list_font, self.VIEWPORT_WIDTH)
            y_line = current_y_render
            
            # Render and draw lines
            for line in lines:
                text = list_font.render(line, True, WHITE)
                screen.blit(text, (self.x + self.LIST_MARGIN, y_line))
                y_line += text.get_height() + 4
            
            current_y_render = y_line + 4 # Spacing between entries
        
        # Reset clipping
        screen.set_clip(None)

        # --- Draw Scrollbar ---
        if total_content_height > self.VIEWPORT_HEIGHT:
            SCROLLBAR_WIDTH = 8
            # Position scrollbar on the far right of the content area
            SCROLLBAR_X = self.x + self.width - self.LIST_MARGIN - SCROLLBAR_WIDTH 
            
            # Calculate bar height and position relative to the VIEWPORT_RECT
            scrollbar_height_ratio = self.VIEWPORT_HEIGHT / total_content_height
            scrollbar_display_height = max(15, self.VIEWPORT_HEIGHT * scrollbar_height_ratio) # min height
            
            # Calculate bar position: map scroll_y (negative) to a positive position
            scroll_ratio = -self.scroll_y / max_scroll_down
            bar_y_offset = (self.VIEWPORT_HEIGHT - scrollbar_display_height) * scroll_ratio
            
            scrollbar_rect = pygame.Rect(
                SCROLLBAR_X,
                self.VIEWPORT_Y_START + bar_y_offset,
                SCROLLBAR_WIDTH,
                scrollbar_display_height
            )
            
            # Draw the scrollbar track (background)
            pygame.draw.rect(screen, SCROLL_TRACK_COLOR, (SCROLLBAR_X, self.VIEWPORT_Y_START, SCROLLBAR_WIDTH, self.VIEWPORT_HEIGHT), border_radius=4)
            # Draw the scrollbar thumb
            pygame.draw.rect(screen, SCROLL_THUMB_COLOR, scrollbar_rect, border_radius=4)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.done_button_rect.collidepoint(event.pos):
                self.is_done = True

def load_movie_categories():
    json_path = os.path.join(os.path.dirname(__file__), "data", "movies_by_category.json")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def draw_title_screen(screen):
    """Draws the main title screen with instructions, now with centered text."""
    screen.fill(BLACK) # Black screen for dramatic intro

    # 1. Draw Title (Already Centered)
    title_text = TITLE_FONT.render("MOVIE MANIA RUNNER", True, RED)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_text, title_rect)

    # 2. Instruction Box Setup (Already Centered)
    box_width = 500
    box_height = 250
    box_rect = pygame.Rect(0, 0, box_width, box_height)
    box_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

    # Draw the instruction box background and border
    pygame.draw.rect(screen, PANEL_BG, box_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, box_rect, 3, border_radius=10) 

    # 3. Draw Instructions inside the box (Now Centered)
    instruction_lines = [
        "BUILD YOUR FAVORITE FILMOGRAPHY!",
        "",
        "Use the Left/Right Arrow Keys to move and",
        "collide with the poster of the movie you prefer.",
        "The selection is added to your film list, and ",
        "click 'Done!' when you've made enough choices.",
        "",
        "PRESS SPACEBAR TO BEGIN"
    ]
    
    y_offset = box_rect.top + 20

    for line in instruction_lines:
        color = WHITE
        if "PRESS SPACEBAR" in line:
            color = RED
        
        text_surface = INSTRUCTION_FONT.render(line, True, color)
        
        # Calculate X position for centering the text within the instruction box
        centered_x = box_rect.left + (box_rect.width - text_surface.get_width()) // 2
        
        screen.blit(text_surface, (centered_x, y_offset))
        y_offset += text_surface.get_height() + 5

# --- Game Loop ---

def reset_game(player, all_sprites, posters, panel, movie_pairs, movie_categories):
    """Resets all game state variables and returns new/reset objects."""
    
    # 1. Reset Display Groups
    all_sprites.empty()
    posters.empty()
    
    # 2. Re-initialize Player
    player = Player()
    all_sprites.add(player)

    # 3. Reset Selection Panel
    panel.all_selected_titles = []
    panel.is_done = False
    panel.scroll_y = 0 # NEW: Reset scroll position
    
    # 4. Re-shuffle Movie Pairs
    all_movies = []
    for category, movies in movie_categories.items():
        all_movies.extend(movies)
        
    random.shuffle(all_movies)
    movie_pairs = list(zip(all_movies[0::2], all_movies[1::2]))
    
    # 5. Return necessary variables for the main loop
    return player, all_sprites, posters, panel, movie_pairs, 0, False, TITLE_SCREEN, 0


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
    game_state = TITLE_SCREEN # Start in the new TITLE_SCREEN state
    
    # Scrolling variables for the final screen (kept separate from panel scroll_y)
    scroll_y = 0
    scroll_speed = 30 

    # Reset button rect (40x40 square, placed near the title)
    RESET_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH - 70, 45, 40, 40)
    
    while running:
        
        # EVENT HANDLING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == TITLE_SCREEN:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_state = RUNNING
            
            elif game_state == RUNNING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        player.move_right()

                panel.handle_event(event)

                # NEW: Mouse wheel scrolling for the side panel
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4: # Scroll Up
                        panel.scroll_y += panel.scroll_speed
                    elif event.button == 5: # Scroll Down
                        panel.scroll_y -= panel.scroll_speed
            
            # Scrolling and Button Input handling when game is done
            elif game_state == DONE:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check for Reset Button click
                    if RESET_BUTTON_RECT.collidepoint(event.pos):
                        (player, all_sprites, posters, panel, movie_pairs, 
                         current_pair_index, pair_active, game_state, scroll_y) = \
                            reset_game(player, all_sprites, posters, panel, movie_pairs, movie_categories)
                        continue # Skip rest of the loop to immediately draw title screen

                    # Mouse wheel scroll handling (for the final results box)
                    # Mouse wheel scroll up = button 4 (scroll list down, increase scroll_y)
                    if event.button == 4:
                        scroll_y += scroll_speed
                    # Mouse wheel scroll down = button 5 (scroll list up, decrease scroll_y)
                    elif event.button == 5:
                        scroll_y -= scroll_speed

        
        # STATE MACHINE DRAWING AND UPDATING
        if game_state == TITLE_SCREEN:
            draw_title_screen(screen)
        
        elif game_state == RUNNING:
            
            # Backgrounds
            screen.fill(GREEN)
            pygame.draw.rect(screen, GRAY, (0, 0, GAME_WIDTH, SCREEN_HEIGHT))

            # Game Logic
            if not pair_active and current_pair_index < len(movie_pairs):
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

            # Check done condition
            if panel.is_done or current_pair_index >= len(movie_pairs):
                game_state = DONE

        
        elif game_state == DONE:
            
            screen.fill(BLACK) # Use black background for final screen

            # 1. Draw Title (Similar style to Intro Screen)
            summary_title_text = SUMMARY_TITLE_FONT.render("YOUR FILMOGRAPHY", True, RED)
            summary_title_rect = summary_title_text.get_rect(center=(SCREEN_WIDTH // 2, 70))
            screen.blit(summary_title_text, summary_title_rect)

            # 1b. Draw Reset Button
            pygame.draw.rect(screen, RESET_BUTTON_COLOR, RESET_BUTTON_RECT, border_radius=5)
            # Draw the left-pointing arrow (<< or a filled triangle)
            arrow_text = RESET_SYMBOL_FONT.render("<<", True, WHITE) # Using double-arrow as symbol
            arrow_rect = arrow_text.get_rect(center=RESET_BUTTON_RECT.center)
            screen.blit(arrow_text, arrow_rect)


            # 2. Define Content Box and Viewport
            CONTENT_BOX_MARGIN = 50
            CONTENT_BOX_WIDTH = SCREEN_WIDTH - CONTENT_BOX_MARGIN * 2
            CONTENT_BOX_HEIGHT = SCREEN_HEIGHT - summary_title_rect.bottom - 40
            
            CONTENT_BOX_RECT = pygame.Rect(
                CONTENT_BOX_MARGIN, 
                summary_title_rect.bottom + 20, 
                CONTENT_BOX_WIDTH, 
                CONTENT_BOX_HEIGHT
            )
            
            # Draw the background for the movie list box
            pygame.draw.rect(screen, RESULTS_BOX_BG, CONTENT_BOX_RECT, border_radius=10)
            pygame.draw.rect(screen, WHITE, CONTENT_BOX_RECT, 2, border_radius=10)

            # Define Viewport and Calculate Total Content Height
            VIEWPORT_X_START = CONTENT_BOX_RECT.left + 20
            VIEWPORT_Y_START = CONTENT_BOX_RECT.top + 20
            VIEWPORT_WIDTH = CONTENT_BOX_RECT.width - 40 # Account for list margins and scrollbar space
            VIEWPORT_HEIGHT = CONTENT_BOX_RECT.height - 40
            
            # The font for the list items
            list_font = pygame.font.Font(None, 36)

            # 1. Calculate the total height of the content
            total_content_height = 0
            for t in panel.all_selected_titles:
                # Use VIEWPORT_WIDTH for wrapping, minus some internal padding
                lines = wrap_text_multi(t, list_font, VIEWPORT_WIDTH - 20) 
                
                entry_height = sum(list_font.size(line)[1] + 4 for line in lines)
                
                total_content_height += entry_height + 12 
            
            # 2. Clamping scroll_y (limits scrolling)
            max_scroll_down = max(0, total_content_height - VIEWPORT_HEIGHT)
            scroll_y = max(min(scroll_y, 0), -max_scroll_down)
            
            # 3. Draw the movie list within the viewport
            
            # Set a clipping rectangle to confine the list to the box
            clip_rect = pygame.Rect(
                CONTENT_BOX_RECT.left + 1, 
                CONTENT_BOX_RECT.top + 1, 
                CONTENT_BOX_RECT.width - 2, 
                CONTENT_BOX_RECT.height - 2
            )
            screen.set_clip(clip_rect)

            current_y_render = VIEWPORT_Y_START + scroll_y
            
            # Draw the list, applying the scroll offset
            for t in panel.all_selected_titles:
                lines = wrap_text_multi(t, list_font, VIEWPORT_WIDTH - 20)
                y_line = current_y_render
                
                # Render and draw lines
                for line in lines:
                    text = list_font.render(line, True, WHITE)
                    screen.blit(text, (VIEWPORT_X_START, y_line))
                    y_line += text.get_height() + 4
                
                current_y_render = y_line + 8 # Spacing between entries
            
            # Reset clipping
            screen.set_clip(None)

            # 4. Draw Scrollbar
            if total_content_height > VIEWPORT_HEIGHT:
                SCROLLBAR_WIDTH = 10
                # Position scrollbar inside the right edge of the content box
                SCROLLBAR_X = CONTENT_BOX_RECT.right - SCROLLBAR_WIDTH - 10 
                
                # Calculate bar height and position relative to the CONTENT_BOX_RECT
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