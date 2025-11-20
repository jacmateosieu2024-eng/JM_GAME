"""Save/load helpers for JSON persistence."""

import json
import os
import pygame
import config


def save_game(player, world, portals, settings):
    data = {
        "player": player.to_dict(),
        "world": world.to_dict(),
        "portals": {
            "true": [portals[0].pos.x, portals[0].pos.y] if portals[0] else None,
            "fake": [portals[1].pos.x, portals[1].pos.y] if portals[1] else None,
        },
        "settings": settings,
    }
    with open(config.SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_game(player_cls, world_cls, portal_cls):
    if not os.path.exists(config.SAVE_FILE):
        return None
    with open(config.SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    player = player_cls.from_dict(data.get("player", {}))
    world = world_cls.from_dict(data.get("world", {}))
    portals_data = data.get("portals", {})
    true_portal = portal_cls(pygame.Vector2(portals_data["true"])) if portals_data.get("true") else None
    fake_portal = portal_cls(pygame.Vector2(portals_data["fake"])) if portals_data.get("fake") else None
    settings = data.get("settings", {})
    return player, world, (true_portal, fake_portal), settings
