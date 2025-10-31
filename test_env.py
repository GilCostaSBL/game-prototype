import sys
import pygame

print("Python version:", sys.version)
print("Pygame version:", pygame.__version__)

try:
    pygame.display.init()
    screen = pygame.display.set_mode((100, 100))
    pygame.display.set_caption("Environment Check")
    print("Environment verified ✅")
except Exception as e:
    print("Environment test failed ❌", e)
finally:
    pygame.quit()
