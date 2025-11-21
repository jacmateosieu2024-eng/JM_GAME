"""Player entity with movement, collision, and inventory."""

import pygame
import config


class Player:
    """Controllable hero with adjustable speed, collision, and inventory."""

    def __init__(self, position=None, speed_index=None):
        self.pos = pygame.Vector2(position or config.PLAYER_SPAWN)
        self.speed_index = speed_index if speed_index is not None else config.DEFAULT_SPEED_INDEX
        self.rect = pygame.Rect(0, 0, config.PLAYER_SIZE, config.PLAYER_SIZE)
        self.inventory = {"water": 0, "torch": 0, "lamp": False}
        self._update_rect()

    @property
    def speed(self):
        return config.PLAYER_SPEEDS[self.speed_index]

    def _update_rect(self):
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def handle_input(self, keys, dt_ms, world):
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
        dt = dt_ms / 1000.0
        velocity = direction * self.speed * dt

        # Move on X
        self.pos.x += velocity.x
        self._update_rect()
        for rock in world.colliding_rocks(self.rect):
            if velocity.x > 0:
                self.rect.right = rock.left
            elif velocity.x < 0:
                self.rect.left = rock.right
            self.pos.x = self.rect.centerx

        # Move on Y
        self.pos.y += velocity.y
        self._update_rect()
        for rock in world.colliding_rocks(self.rect):
            if velocity.y > 0:
                self.rect.bottom = rock.top
            elif velocity.y < 0:
                self.rect.top = rock.bottom
            self.pos.y = self.rect.centery

        # Clamp to world bounds
        self.pos.x = max(0, min(self.pos.x, world.width))
        self.pos.y = max(0, min(self.pos.y, world.height))
        self._update_rect()

    def draw(self, surface, camera):
        draw_rect = camera.apply(self.rect)
        pygame.draw.rect(surface, config.PLAYER_COLOR, draw_rect)

    def collect(self, pickup):
        if pickup:
            if pickup["type"] == "lamp":
                self.inventory["lamp"] = True
            else:
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
        inv = {"water": 0, "torch": 0, "lamp": False}
        inv.update(data.get("inventory", {}))
        player.inventory = inv
        player._update_rect()
        return player
