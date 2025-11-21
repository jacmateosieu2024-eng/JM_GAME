"""World generation, biomes, rocks, and camera handling."""

import math
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
    """Procedurally generated world for a given biome with pickups and rocks."""

    def __init__(self, biome: str = "desert", seed: int | None = None):
        self.biome = biome
        self.seed = seed if seed is not None else random.randint(0, 999999)
        random.seed(self.seed + (1 if biome == "forest" else 0))
        self.width = config.WORLD_WIDTH
        self.height = config.WORLD_HEIGHT
        self.background = self._generate_background()
        self.rocks = self._generate_rocks()
        self.pickups = self._generate_pickups()

    def _generate_background(self) -> pygame.Surface:
        surf = pygame.Surface((self.width, self.height))
        biome_cfg = config.BIOMES[self.biome]
        base_colors = biome_cfg["base_colors"]
        dune_color = biome_cfg["dune_color"]

        for y in range(0, self.height, config.BG_TILE):
            for x in range(0, self.width, config.BG_TILE):
                color = random.choice(base_colors)
                pygame.draw.rect(surf, color, (x, y, config.BG_TILE, config.BG_TILE))

        # Add gentle sine-wave bands
        for band in range(10):
            amplitude = random.randint(4, 8)
            wavelength = random.randint(140, 220)
            for x in range(self.width):
                y = int(self.height * (band + 1) / 11 + amplitude * math.sin(x / wavelength))
                pygame.draw.line(surf, dune_color, (x, y), (x, y + 2))

        # Add speckles for grain/grass
        for _ in range(800):
            rx = random.randint(0, self.width)
            ry = random.randint(0, self.height)
            radius = random.randint(1, 2)
            pygame.draw.circle(surf, dune_color, (rx, ry), radius)
        return surf

    def _generate_rocks(self):
        rocks = []
        density = config.DESERT_ROCK_DENSITY if self.biome == "desert" else config.FOREST_ROCK_DENSITY
        count = int(self.width * self.height * density)
        for _ in range(count):
            w = random.randint(*config.ROCK_SIZE_RANGE)
            h = random.randint(*config.ROCK_SIZE_RANGE)
            x = random.randint(0, self.width - w)
            y = random.randint(0, self.height - h)
            rocks.append(pygame.Rect(x, y, w, h))
        return rocks

    def _generate_pickups(self):
        pickups = []
        count = random.randint(*config.PICKUP_COUNT_RANGE)
        spawn = pygame.Vector2(config.PLAYER_SPAWN)
        available = list(config.BIOMES[self.biome]["pickup_types"])
        # Ensure lamp exists in forest
        if self.biome == "forest" and "lamp" not in available:
            available.append("lamp")
        lamp_added = False
        for _ in range(count):
            ptype = random.choice(available)
            if self.biome == "forest" and not lamp_added:
                ptype = "lamp"
                lamp_added = True
            attempts = 0
            while True:
                pos = pygame.Vector2(
                    random.randint(0, self.width),
                    random.randint(0, self.height),
                )
                attempts += 1
                if pos.distance_to(spawn) > config.PICKUP_MIN_DIST_FROM_SPAWN or attempts > 5:
                    break
            pickups.append({"type": ptype, "pos": pos})
        return pickups

    def draw(self, surface: pygame.Surface, camera: Camera):
        surface.blit(self.background, (-camera.offset.x, -camera.offset.y))
        rock_color = config.BIOMES[self.biome]["rock_color"]
        for rock in self.rocks:
            pygame.draw.rect(surface, rock_color, camera.apply(rock))
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

    def colliding_rocks(self, rect: pygame.Rect):
        return [rock for rock in self.rocks if rect.colliderect(rock)]

    def to_dict(self):
        return {
            "seed": self.seed,
            "biome": self.biome,
            "pickups": [
                {"type": p["type"], "pos": [p["pos"].x, p["pos"].y]} for p in self.pickups
            ],
        }

    @classmethod
    def from_dict(cls, data: dict):
        world = cls(biome=data.get("biome", "desert"), seed=data.get("seed"))
        world.pickups = [
            {"type": p["type"], "pos": pygame.Vector2(p["pos"][0], p["pos"][1])}
            for p in data.get("pickups", [])
        ]
        return world
