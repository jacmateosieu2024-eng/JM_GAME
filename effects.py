"""Visual effects including heat haze and day/night vignette."""

import math
import pygame
import config


def apply_heat_haze(surface: pygame.Surface, time_ms: int) -> pygame.Surface:
    """Apply a subtle horizontal displacement to mimic heat haze."""
    if not config.HEAT_HAZE_ENABLED:
        return surface
    amplitude = config.HEAT_HAZE_AMPLITUDE
    wavelength = config.HEAT_HAZE_WAVELENGTH
    speed = config.HEAT_HAZE_SPEED
    width, height = surface.get_size()
    displaced = surface.copy()
    for y in range(height):
        shift = int(amplitude * math.sin((y / wavelength) + time_ms * 0.001 * speed))
        row = surface.subsurface((0, y, width, 1))
        displaced.blit(row, (shift, y))
    return displaced


def is_night(time_of_day: float) -> bool:
    phase = time_of_day % (config.DAY_DURATION + config.NIGHT_DURATION)
    return phase >= config.DAY_DURATION


def apply_day_night(surface: pygame.Surface, player_screen_pos: pygame.Vector2, time_of_day: float, brightness: float, has_lamp: bool):
    """Darken the scene at night with a vignette unless lamp is active."""
    if not is_night(time_of_day) or has_lamp:
        return surface

    radius = config.NIGHT_VISIBILITY_RADIUS
    fade = config.NIGHT_FADE_WIDTH
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    base_alpha = int(220 * (1.0 - brightness))
    overlay.fill((*config.NIGHT_COLOR, base_alpha))

    # radial gradient for visibility cone
    for step in range(0, fade, 12):
        alpha = max(0, base_alpha - int((step / fade) * base_alpha))
        pygame.draw.circle(
            overlay,
            (0, 0, 0, alpha),
            (int(player_screen_pos.x), int(player_screen_pos.y)),
            radius + fade - step,
        )
    pygame.draw.circle(overlay, (0, 0, 0, 0), (int(player_screen_pos.x), int(player_screen_pos.y)), radius)
    surface.blit(overlay, (0, 0))
    return surface
