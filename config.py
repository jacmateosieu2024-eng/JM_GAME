"""Configuration constants for Desert Portal game."""

import pygame

# Screen settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60
TITLE = "Desert Portals"

# World settings
WORLD_WIDTH = 2400
WORLD_HEIGHT = 1800
BG_TILE = 32

# Player settings
PLAYER_SPEEDS = [2.5, 3.5, 4.5, 5.5]
DEFAULT_SPEED_INDEX = 1
PLAYER_SIZE = 20
PLAYER_COLOR = (40, 110, 180)
PLAYER_SPAWN = (WORLD_WIDTH // 2, WORLD_HEIGHT // 2)

# Portal settings
PORTAL_RADIUS = 24
PORTAL_MIN_R = 120
PORTAL_MAX_R = 360
FAKE_PORTAL_COLOR = (170, 70, 200)
TRUE_PORTAL_COLOR = (50, 220, 120)
PORTAL_PULSE_SPEED = 2

# Pickups
PICKUP_COUNT_RANGE = (10, 20)
PICKUP_TYPES = ["water", "torch"]
PICKUP_COLORS = {
    "water": (60, 170, 230),
    "torch": (255, 180, 70),
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

# Save file
SAVE_FILE = "save.json"

pygame.font.init()
DEFAULT_FONT = pygame.font.get_default_font()
