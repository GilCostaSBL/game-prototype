SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TITLE = "Game Prototype"

# Lane system (3-lane runner)
LANE_COUNT = 3
LANE_WIDTH = SCREEN_WIDTH // LANE_COUNT
LANES_X = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(LANE_COUNT)]
PLAYER_Y = SCREEN_HEIGHT - 100  # Fixed Y position near bottom
