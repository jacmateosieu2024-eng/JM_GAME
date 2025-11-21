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
        base_color = tuple(max(0, min(255, c + self.tint_shift)) for c in config.PORTAL_BASE_COLOR)
        color = base_color
        pulse = 2 + int(2 * math.sin(time_ms * 0.005 + self.phase))
        rect = pygame.Rect(
            self.pos.x - self.radius - pulse,
            self.pos.y - self.radius - pulse,
            2 * (self.radius + pulse),
            2 * (self.radius + pulse),
        )
        rect = camera.apply(rect)
        ring = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(ring, (*color, config.PORTAL_RING_ALPHA), ring.get_rect(), width=6)
        pygame.draw.ellipse(ring, config.PORTAL_EDGE_COLOR, ring.get_rect().inflate(-8, -8), width=2)
        surface.blit(ring, rect.topleft)

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
