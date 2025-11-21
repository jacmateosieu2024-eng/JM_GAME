"""Menu system for main, pause, and settings screens."""

import pygame
import config


class Menu:
    """Simple vertical menu navigable via keyboard."""

    def __init__(self, title: str, options: list[str]):
        self.title = title
        self.options = options
        self.index = 0
        self.font = pygame.font.Font(config.DEFAULT_FONT, 28)
        self.small_font = pygame.font.Font(config.DEFAULT_FONT, 20)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    self.index = (self.index + 1) % len(self.options)
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.index = (self.index - 1) % len(self.options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return self.index
        return None

    def draw(self, surface: pygame.Surface):
        width, height = surface.get_size()
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        surface.blit(overlay, (0, 0))

        title_surf = self.font.render(self.title, True, (240, 230, 210))
        surface.blit(title_surf, (width // 2 - title_surf.get_width() // 2, height // 4))

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.index else (180, 170, 150)
            text = self.small_font.render(option, True, color)
            surface.blit(text, (width // 2 - text.get_width() // 2, height // 2 + i * 32))


def settings_menu(surface, current_state, events):
    """Handle settings update and rendering."""
    menu = Menu("Paramètres", ["Vitesse", "Plein écran", "Heat haze", "Luminosité nuit", "Retour"])
    menu.index = current_state.get("index", 0)

    choice = menu.update(events)
    if choice is not None:
        menu.index = choice
    menu.draw(surface)

    width, height = surface.get_size()
    font = pygame.font.Font(config.DEFAULT_FONT, 20)
    info = [
        f"Vitesse: {config.PLAYER_SPEEDS[current_state['speed_index']]} px/s",
        f"Plein écran: {'Oui' if current_state['fullscreen'] else 'Non'}",
        f"Heat haze: {'On' if current_state['heat_haze'] else 'Off'}",
        f"Nuit: niveau {current_state['night_level'] + 1}/{len(config.NIGHT_LEVELS)}",
    ]
    for i, line in enumerate(info):
        text = font.render(line, True, (230, 220, 200))
        surface.blit(text, (width // 2 - text.get_width() // 2, height // 2 + i * 32 + 80))

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if menu.index == 0:
                    current_state["speed_index"] = (current_state["speed_index"] + 1) % len(config.PLAYER_SPEEDS)
                elif menu.index == 1:
                    current_state["fullscreen"] = not current_state["fullscreen"]
                elif menu.index == 2:
                    current_state["heat_haze"] = not current_state["heat_haze"]
                elif menu.index == 3:
                    current_state["night_level"] = (current_state["night_level"] + 1) % len(config.NIGHT_LEVELS)
                elif menu.index == 4:
                    current_state["open"] = False
            elif event.key == pygame.K_ESCAPE:
                current_state["open"] = False
    current_state["index"] = menu.index
    return current_state
