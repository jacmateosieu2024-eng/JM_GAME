"""Portal entities: winning and fake teleport portals."""

import random
import pygame
import config


class Portal:
    """Generic portal used for both winning and fake variants."""

    def __init__(self, position: pygame.Vector2, is_true: bool = False):
        self.pos = pygame.Vector2(position)
        self.is_true = is_true
        self.radius = config.PORTAL_RADIUS
        self.phase = random.random() * 3.14

    def draw(self, surface: pygame.Surface, camera, time_ms: int):
        color = config.TRUE_PORTAL_COLOR if self.is_true else config.FAKE_PORTAL_COLOR
        pulse = 2 + int(2 * pygame.math.sin(time_ms * 0.005 + self.phase))
        rect = pygame.Rect(
            self.pos.x - self.radius - pulse,
            self.pos.y - self.radius - pulse,
            2 * (self.radius + pulse),
            2 * (self.radius + pulse),
        )
        rect = camera.apply(rect)
        pygame.draw.ellipse(surface, color, rect, width=4)
        inner = rect.inflate(-8, -8)
        pygame.draw.ellipse(surface, (255, 255, 255), inner, width=2)

    def collides_with(self, player_rect: pygame.Rect) -> bool:
        distance = pygame.Vector2(player_rect.center).distance_to(self.pos)
        return distance <= self.radius + max(player_rect.width, player_rect.height) / 2


def place_portals(spawn: pygame.Vector2):
    angle = random.uniform(0, 6.28)
    dist = random.randint(config.PORTAL_MIN_R, config.PORTAL_MAX_R)
    true_pos = spawn + pygame.Vector2(dist, 0).rotate_rad(angle)

    angle2 = random.uniform(0, 6.28)
    dist2 = random.randint(config.PORTAL_MIN_R, config.PORTAL_MAX_R)
    fake_pos = spawn + pygame.Vector2(dist2, 0).rotate_rad(angle2)
    return Portal(true_pos, True), Portal(fake_pos, False)
