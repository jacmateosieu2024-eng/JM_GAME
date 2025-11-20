"""World generation and camera handling for the desert map."""

import random
import pygame
import config


class Camera:
    """Simple camera that follows the player while clamping to world bounds."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.offset = pygame.Vector2(0, 0)

    def update(self, target_pos: pygame.Vector2, screen_rect: pygame.Rect):
        self.offset.x = target_pos.x - screen_rect.width / 2
        self.offset.y = target_pos.y - screen_rect.height / 2
        self.offset.x = max(0, min(self.offset.x, self.width - screen_rect.width))
        self.offset.y = max(0, min(self.offset.y, self.height - screen_rect.height))

    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        return rect.move(-self.offset.x, -self.offset.y)


class World:
    """Procedurally generated desert world with pickups."""

    def __init__(self, seed: int | None = None):
        self.seed = seed or random.randint(0, 999999)
        random.seed(self.seed)
        self.width = config.WORLD_WIDTH
        self.height = config.WORLD_HEIGHT
        self.background = self._generate_background()
        self.pickups = self._generate_pickups()

    def _generate_background(self) -> pygame.Surface:
        surf = pygame.Surface((self.width, self.height))
        base_color = pygame.Color(227, 200, 140)
        darker = pygame.Color(200, 170, 120)
        lighter = pygame.Color(245, 220, 170)

        for y in range(0, self.height, config.BG_TILE):
            for x in range(0, self.width, config.BG_TILE):
                choice = random.random()
                if choice < 0.4:
                    color = base_color
                elif choice < 0.7:
                    color = darker
                else:
                    color = lighter
                pygame.draw.rect(surf, color, (x, y, config.BG_TILE, config.BG_TILE))

        # Add dunes as horizontal sine-wave bands
        for band in range(8):
            amplitude = random.randint(4, 8)
            wavelength = random.randint(120, 200)
            color = (210 + band % 2 * 8, 185 + band % 3 * 5, 130)
            for x in range(self.width):
                y = int(self.height * (band + 1) / 9 + amplitude * pygame.math.sin(x / wavelength))
                pygame.draw.line(surf, color, (x, y), (x, y + 2))

        # Add rocks as small circles
        for _ in range(350):
            rx = random.randint(0, self.width)
            ry = random.randint(0, self.height)
            radius = random.randint(1, 3)
            pygame.draw.circle(surf, (160, 140, 110), (rx, ry), radius)
        return surf

    def _generate_pickups(self):
        pickups = []
        count = random.randint(*config.PICKUP_COUNT_RANGE)
        spawn = pygame.Vector2(config.PLAYER_SPAWN)
        for _ in range(count):
            ptype = random.choice(config.PICKUP_TYPES)
            while True:
                pos = pygame.Vector2(
                    random.randint(0, self.width),
                    random.randint(0, self.height),
                )
                if pos.distance_to(spawn) > config.PICKUP_MIN_DIST_FROM_SPAWN:
                    break
            pickups.append({"type": ptype, "pos": pos})
        return pickups

    def draw(self, surface: pygame.Surface, camera: Camera):
        surface.blit(self.background, (-camera.offset.x, -camera.offset.y))
        for pickup in self.pickups:
            color = config.PICKUP_COLORS[pickup["type"]]
            rect = pygame.Rect(
                pickup["pos"].x - config.PICKUP_SIZE / 2,
                pickup["pos"].y - config.PICKUP_SIZE / 2,
                config.PICKUP_SIZE,
                config.PICKUP_SIZE,
            )
            pygame.draw.rect(surface, color, camera.apply(rect))

    def remove_pickup_at(self, pos: pygame.Vector2, radius: float = 12):
        for pickup in list(self.pickups):
            if pickup["pos"].distance_to(pos) <= radius:
                self.pickups.remove(pickup)
                return pickup
        return None

    def to_dict(self):
        return {
            "seed": self.seed,
            "pickups": [
                {"type": p["type"], "pos": [p["pos"].x, p["pos"].y]} for p in self.pickups
            ],
        }

    @classmethod
    def from_dict(cls, data: dict):
        world = cls(seed=data.get("seed"))
        world.pickups = [
            {"type": p["type"], "pos": pygame.Vector2(p["pos"][0], p["pos"][1])}
            for p in data.get("pickups", [])
        ]
        return world
