"""HUD elements including compass and inventory display."""

import pygame
import config


class HUD:
    """Draws on-screen hints, inventory, and compass."""

    def __init__(self):
        self.font = pygame.font.Font(config.DEFAULT_FONT, 18)
        self.small_font = pygame.font.Font(config.DEFAULT_FONT, 14)

    def draw(self, surface, player, true_portal, camera, dt_ms):
        width, height = surface.get_size()
        overlay = pygame.Surface((width, 60), pygame.SRCALPHA)
        overlay.fill((*config.HUD_COLOR, config.HUD_BG_ALPHA))
        surface.blit(overlay, (0, 0))

        hint = "Flèches/WASD: bouger | Échap: pause"
        text = self.font.render(hint, True, config.HUD_TEXT_COLOR)
        surface.blit(text, (10, 10))

        inv_text = f"Eau: {player.inventory['water']} | Torche: {player.inventory['torch']}"
        inv = self.font.render(inv_text, True, config.HUD_TEXT_COLOR)
        surface.blit(inv, (10, 34))

        self._draw_compass(surface, player, true_portal, width, dt_ms)

    def _draw_compass(self, surface, player, true_portal, screen_width, dt_ms):
        center = (screen_width - 70, 40)
        radius = 26
        pygame.draw.circle(surface, (80, 70, 60), center, radius)
        pygame.draw.circle(surface, (240, 220, 200), center, radius, width=2)

        if true_portal:
            direction = pygame.Vector2(true_portal.pos) - player.pos
            angle = direction.angle_to(pygame.Vector2(1, 0))
            endpoint = (
                center[0] + radius * 0.9 * pygame.math.cos(pygame.math.radians(angle)),
                center[1] - radius * 0.9 * pygame.math.sin(pygame.math.radians(angle)),
            )
            blink = direction.length() < 40 and (pygame.time.get_ticks() // 400) % 2 == 0
            color = (230, 80, 50) if blink else (255, 150, 90)
            pygame.draw.line(surface, color, center, endpoint, width=3)
            pygame.draw.circle(surface, color, endpoint, 3)

        label = self.small_font.render("Nord", True, (200, 200, 190))
        surface.blit(label, (center[0] - label.get_width() // 2, center[1] - radius - 12))
