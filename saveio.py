"""Save/load helpers for JSON persistence."""

import json
import os
import pygame
import config
import world as world_module


def save_game(player, worlds: dict, current_world: str, portals, settings, time_of_day: float):
    data = {
        "player": player.to_dict(),
        "worlds": {name: w.to_dict() for name, w in worlds.items()},
        "current_world": current_world,
        "portals": {
            "real": [portals[0].pos.x, portals[0].pos.y] if portals[0] else None,
            "trap": [portals[1].pos.x, portals[1].pos.y] if portals[1] else None,
        },
        "settings": settings,
        "time_of_day": time_of_day,
    }
    with open(config.SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_game(player_cls, portal_cls):
    if not os.path.exists(config.SAVE_FILE):
        return None
    with open(config.SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    player = player_cls.from_dict(data.get("player", {}))
    worlds_data = data.get("worlds", {})
    worlds = {}
    for name, wdata in worlds_data.items():
        worlds[name] = world_module.World.from_dict(wdata)
    if not worlds:
        return None
    portals_data = data.get("portals", {})
    real_portal = portal_cls(pygame.Vector2(portals_data["real"]), "real") if portals_data.get("real") else None
    trap_portal = portal_cls(pygame.Vector2(portals_data["trap"]), "trap") if portals_data.get("trap") else None
    settings = data.get("settings", {})
    current_world = data.get("current_world", "desert")
    time_of_day = data.get("time_of_day", 0.0)
    return player, worlds, (real_portal, trap_portal), settings, current_world, time_of_day
