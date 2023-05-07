from pygame import Vector2

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

OVERLAY_POSITIONS = {'tool': (40, SCREEN_HEIGHT - 15), 'seed': (70, SCREEN_HEIGHT - 5)}

LAYERS = {'water': 0, 'ground': 1, 'soil': 2, 'soil_water': 3, 'house_bottom': 4, 'main': 5, 'fruit': 6}

APPLE_POS = {'Small': [(18, 17), (30, 37), (12, 50), (30, 45), (20, 30), (30, 10)],
             'Large': [(30, 24), (60, 65), (50, 50), (16, 40), (45, 40), (42, 70)]}

PLAYER_TOOL_OFFSET = {'left': Vector2(-50, 40), 'right': Vector2(50, 40), 'up': Vector2(0, -10), 'down': Vector2(0, 50)}
