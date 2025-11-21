"""HUD elements including compass, inventory, and day/night indicators."""

import math
import pygame
import config
import effects


class HUD:
    """Draws on-screen hints, inventory, and compass."""

    def __init__(self):
        self.font = pygame.font.Font(config.DEFAULT_FONT, 18)
        self.small_font = pygame.font.Font(config.DEFAULT_FONT, 14)

    def draw(self, surface, player, true_portal, camera, dt_ms, time_of_day):
        width, height = surface.get_size()
        overlay = pygame.Surface((width, 70), pygame.SRCALPHA)
        overlay.fill((*config.HUD_COLOR, config.HUD_BG_ALPHA))
        surface.blit(overlay, (0, 0))

        hint = "Flèches/WASD: bouger | Échap: pause"
        text = self.font.render(hint, True, config.HUD_TEXT_COLOR)
        surface.blit(text, (10, 10))

        inv_text = (
            f"Eau: {player.inventory['water']} | Torche: {player.inventory['torch']} | "
            f"Lampe: {'Oui' if player.inventory['lamp'] else 'Non'}"
        )
        inv = self.font.render(inv_text, True, config.HUD_TEXT_COLOR)
        surface.blit(inv, (10, 36))

        self._draw_compass(surface, player, true_portal, width)
        self._draw_time_badge(surface, time_of_day)

    def _draw_compass(self, surface, player, true_portal, screen_width):
        center = (screen_width - 70, 42)
        radius = 26
        pygame.draw.circle(surface, (80, 70, 60), center, radius)
        pygame.draw.circle(surface, (240, 220, 200), center, radius, width=2)

        if true_portal:
            direction = pygame.Vector2(true_portal.pos) - player.pos
            angle = math.atan2(-direction.y, direction.x)
            endpoint = (
                center[0] + radius * 0.9 * math.cos(angle),
                center[1] + radius * 0.9 * math.sin(angle),
            )
            blink = direction.length() < 40 and (pygame.time.get_ticks() // 400) % 2 == 0
            color = (230, 80, 50) if blink else (255, 150, 90)
            pygame.draw.line(surface, color, center, endpoint, width=3)
            pygame.draw.circle(surface, color, (int(endpoint[0]), int(endpoint[1])), 3)

        label = self.small_font.render("Nord", True, (200, 200, 190))
        surface.blit(label, (center[0] - label.get_width() // 2, center[1] - radius - 12))

    def _draw_time_badge(self, surface, time_of_day: float):
        night = effects.is_night(time_of_day)
        icon_color = (255, 220, 120) if not night else (160, 200, 255)
        text = "Jour" if not night else "Nuit"
        badge = self.small_font.render(text, True, icon_color)
        surface.blit(badge, (10, 58))
