"""Player entity with movement and inventory."""

import pygame
import config


class Player:
    """Controllable hero with adjustable speed and inventory."""

    def __init__(self, position=None, speed_index=None):
        self.pos = pygame.Vector2(position or config.PLAYER_SPAWN)
        self.speed_index = speed_index if speed_index is not None else config.DEFAULT_SPEED_INDEX
        self.rect = pygame.Rect(0, 0, config.PLAYER_SIZE, config.PLAYER_SIZE)
        self.inventory = {"water": 0, "torch": 0}

    @property
    def speed(self):
        return config.PLAYER_SPEEDS[self.speed_index]

    def handle_input(self, keys, dt):
        direction = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y += 1
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.pos += direction * self.speed * dt
        self.pos.x = max(0, min(self.pos.x, config.WORLD_WIDTH))
        self.pos.y = max(0, min(self.pos.y, config.WORLD_HEIGHT))
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def draw(self, surface, camera):
        draw_rect = camera.apply(self.rect)
        pygame.draw.rect(surface, config.PLAYER_COLOR, draw_rect)

    def collect(self, pickup):
        if pickup:
            self.inventory[pickup["type"]] += 1

    def to_dict(self):
        return {
            "pos": [self.pos.x, self.pos.y],
            "speed_index": self.speed_index,
            "inventory": self.inventory,
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(position=data.get("pos"), speed_index=data.get("speed_index"))
        player.inventory = data.get("inventory", {"water": 0, "torch": 0})
        return player
