"""Portal entities with near-identical visuals but different behavior."""

import math
import random
import pygame
import config


class Portal:
    """Generic portal; behavior decided by kind (real or trap)."""

    def __init__(self, position: pygame.Vector2, kind: str = "real"):
        self.pos = pygame.Vector2(position)
        self.kind = kind
        self.radius = config.PORTAL_RADIUS
        self.phase = random.random() * math.pi
        self.tint_shift = random.randint(-8, 8)
    
    def draw(self, surface: pygame.Surface, camera, time_ms: int):
        # Couleur de base avec légère variation
        base_color = tuple(max(0, min(255, c + self.tint_shift)) for c in config.PORTAL_BASE_COLOR)
        color = base_color
    
        # En mode DEBUG, forcer une couleur très visible
        if getattr(config, "DEBUG", False):
            color = getattr(config, "PORTAL_DEBUG_COLOR", (255, 0, 255))
    
        # Pulsation
        pulse = 2 + int(2 * math.sin(time_ms * 0.005 + self.phase))
    
        # Rect monde -> écran
        world_rect = pygame.Rect(
            self.pos.x - self.radius - pulse,
            self.pos.y - self.radius - pulse,
            2 * (self.radius + pulse),
            2 * (self.radius + pulse),
        )
        screen_rect = camera.apply(world_rect)
        cx, cy = screen_rect.center
    
        # HALO blanc (visible de jour comme de nuit)
        pygame.draw.circle(surface, (255, 255, 255), (cx, cy), self.radius + 8, 3)
    
        # 3 anneaux épais
        for i in range(3):
            rr = int(self.radius + i * 6 + 3 * math.sin(self.phase + i + time_ms * 0.005))
            pygame.draw.circle(surface, color, (cx, cy), rr, 3)
    
        # Point central
        pygame.draw.circle(surface, (255, 255, 255), (cx, cy), 4)
    
        # --- DEBUG : croix magenta au centre (immanquable)
        if getattr(config, "DEBUG", False):
            pygame.draw.line(surface, (255, 0, 255), (cx - 12, cy), (cx + 12, cy), 3)
            pygame.draw.line(surface, (255, 0, 255), (cx, cy - 12), (cx, cy + 12), 3)

    def collides_with(self, player_rect: pygame.Rect) -> bool:
        distance = pygame.Vector2(player_rect.center).distance_to(self.pos)
        return distance <= self.radius + max(player_rect.width, player_rect.height) / 2


def place_portals(spawn: pygame.Vector2):
    angle = random.uniform(0, math.tau)
    dist = random.randint(config.PORTAL_MIN_R, config.PORTAL_MAX_R)
    true_pos = pygame.Vector2(
        spawn.x + dist * math.cos(angle),
        spawn.y + dist * math.sin(angle),
    )

    angle2 = random.uniform(0, math.tau)
    dist2 = random.randint(config.PORTAL_MIN_R, config.PORTAL_MAX_R)
    trap_pos = pygame.Vector2(
        spawn.x + dist2 * math.cos(angle2),
        spawn.y + dist2 * math.sin(angle2),
    )
    return Portal(true_pos, "real"), Portal(trap_pos, "trap")
