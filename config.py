"""Configuration constants for Desert/Forest worlds and gameplay."""

import pygame

# Screen settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60
TITLE = "Desert Portals"

# World settings
WORLD_WIDTH = 8000
WORLD_HEIGHT = 6000
BG_TILE = 32

# Player settings (pixels per second)
PLAYER_SPEEDS = [120, 140, 180]
DEFAULT_SPEED_INDEX = 1
PLAYER_SIZE = 20
PLAYER_COLOR = (40, 110, 180)
PLAYER_SPAWN = (WORLD_WIDTH // 2, WORLD_HEIGHT // 2)

# Portal settings
PORTAL_RADIUS = 24
PORTAL_MIN_R = 1200
PORTAL_MAX_R = 2400
PORTAL_BASE_COLOR = (170, 120, 230)
PORTAL_EDGE_COLOR = (240, 230, 255)
PORTAL_PULSE_SPEED = 2
PORTAL_RING_ALPHA = 130

# Pickups
PICKUP_COUNT_RANGE = (10, 20)
PICKUP_TYPES_DESERT = ["water", "torch"]
PICKUP_TYPES_FOREST = ["water", "torch", "lamp"]
PICKUP_COLORS = {
    "water": (60, 170, 230),
    "torch": (255, 180, 70),
    "lamp": (180, 240, 120),
}
PICKUP_MIN_DIST_FROM_SPAWN = 160
PICKUP_SIZE = 12

# Camera/HUD
HUD_COLOR = (20, 20, 20)
HUD_TEXT_COLOR = (250, 240, 220)
HUD_BG_ALPHA = 170

# Heat haze effect
HEAT_HAZE_ENABLED = True
HEAT_HAZE_AMPLITUDE = 3
HEAT_HAZE_WAVELENGTH = 120
HEAT_HAZE_SPEED = 0.6

# Day/Night cycle
DAY_DURATION = 120.0  # seconds
NIGHT_DURATION = 120.0  # seconds
NIGHT_LEVELS = [0.55, 0.7, 0.9]  # lower is darker
DEFAULT_NIGHT_LEVEL_INDEX = 1
NIGHT_VISIBILITY_RADIUS = 320
NIGHT_FADE_WIDTH = 220
NIGHT_COLOR = (0, 0, 0)

# Rock/obstacle density
DESERT_ROCK_DENSITY = 0.00008  # proportion of world area
FOREST_ROCK_DENSITY = 0.0001
ROCK_SIZE_RANGE = (22, 48)

# Biomes
BIOMES = {
    "desert": {
        "name": "Désert",
        "base_colors": [(227, 200, 140), (200, 170, 120), (245, 220, 170)],
        "dune_color": (215, 190, 140),
        "rock_color": (160, 140, 110),
        "pickup_types": PICKUP_TYPES_DESERT,
    },
    "forest": {
        "name": "Forêt",
        "base_colors": [(90, 150, 90), (70, 130, 70), (110, 170, 110)],
        "dune_color": (80, 130, 90),
        "rock_color": (60, 90, 60),
        "pickup_types": PICKUP_TYPES_FOREST,
    },
}

# Save file
SAVE_FILE = "save.json"

pygame.font.init()
DEFAULT_FONT = pygame.font.get_default_font()
