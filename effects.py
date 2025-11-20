"""Optional heat haze post-process effect."""

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
        shift = int(amplitude * pygame.math.sin((y / wavelength) + time_ms * 0.001 * speed))
        row = surface.subsurface((0, y, width, 1))
        displaced.blit(row, (shift, y))
    return displaced
