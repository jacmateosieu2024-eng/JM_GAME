"""Entry point for the Desert Portals game."""

import random
import sys
import pygame

import config
import effects
import hud
import menu
import player
import portals
import saveio
import world


class Game:
    """High-level game controller handling states and rendering."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"

        self.settings = {
            "speed_index": config.DEFAULT_SPEED_INDEX,
            "fullscreen": False,
            "heat_haze": config.HEAT_HAZE_ENABLED,
        }

        self.hud = hud.HUD()
        self.main_menu = menu.Menu(
            "Desert Portals",
            ["Nouvelle partie", "Charger", "Paramètres", "Quitter"],
        )
        self.pause_menu = menu.Menu(
            "Pause",
            ["Reprendre", "Sauvegarder", "Paramètres", "Quitter au menu"],
        )

        self._start_new_game()

    def _start_new_game(self):
        self.world = world.World()
        self.player = player.Player(speed_index=self.settings["speed_index"])
        self.true_portal, self.fake_portal = portals.place_portals(pygame.Vector2(config.PLAYER_SPAWN))
        self.camera = world.Camera(self.world.width, self.world.height)
        self.victory = False

    def _toggle_fullscreen(self):
        self.settings["fullscreen"] = not self.settings["fullscreen"]
        if self.settings["fullscreen"]:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)

    def run(self):
        while self.running:
            dt = self.clock.tick(config.FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

            if self.state == "menu":
                self.handle_main_menu(events)
            elif self.state == "running":
                self.update_gameplay(dt, events)
            elif self.state == "paused":
                self.handle_pause_menu(events)
            elif self.state == "victory":
                self.draw_victory(events)
            pygame.display.flip()
        pygame.quit()
        sys.exit()

    def handle_main_menu(self, events):
        choice = self.main_menu.update(events)
        if choice == 0:
            self._start_new_game()
            self.state = "running"
        elif choice == 1:
            loaded = saveio.load_game(player.Player, world.World, portals.Portal)
            if loaded:
                self.player, self.world, (self.true_portal, self.fake_portal), settings = loaded
                self.settings.update(settings)
                config.HEAT_HAZE_ENABLED = self.settings.get("heat_haze", config.HEAT_HAZE_ENABLED)
                self.state = "running"
        elif choice == 2:
            self.state = "settings"
        elif choice == 3:
            self.running = False

        self.screen.fill((0, 0, 0))
        self.main_menu.draw(self.screen)
        if self.state == "settings":
            self.settings["open"] = True
            while self.settings.get("open"):
                events = pygame.event.get()
                self.screen.fill((0, 0, 0))
                self.settings = menu.settings_menu(self.screen, self.settings, events)
                pygame.display.flip()
                self.clock.tick(30)
                config.HEAT_HAZE_ENABLED = self.settings["heat_haze"]
                self.player.speed_index = self.settings["speed_index"]
                if self.settings["fullscreen"] != pygame.display.is_fullscreen():
                    self._toggle_fullscreen()
            self.state = "menu"

    def update_gameplay(self, dt, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.state = "paused"
            return
        self.player.handle_input(keys, dt)
        self.camera.update(self.player.pos, self.screen.get_rect())
        pickup = self.world.remove_pickup_at(self.player.pos)
        self.player.collect(pickup)

        if self.true_portal and self.true_portal.collides_with(self.player.rect):
            self.victory = True
            self.state = "victory"
        elif self.fake_portal and self.fake_portal.collides_with(self.player.rect):
            self.player.pos = pygame.Vector2(config.PLAYER_SPAWN)
            self.player.rect.center = self.player.pos

        self.draw_game(dt)

    def handle_pause_menu(self, events):
        choice = self.pause_menu.update(events)
        if choice == 0:
            self.state = "running"
        elif choice == 1:
            saveio.save_game(
                self.player,
                self.world,
                (self.true_portal, self.fake_portal),
                self.settings,
            )
            self.state = "running"
        elif choice == 2:
            self.settings["open"] = True
            while self.settings.get("open"):
                events = pygame.event.get()
                self.screen.fill((0, 0, 0))
                self.settings = menu.settings_menu(self.screen, self.settings, events)
                pygame.display.flip()
                self.clock.tick(30)
                config.HEAT_HAZE_ENABLED = self.settings["heat_haze"]
                self.player.speed_index = self.settings["speed_index"]
                if self.settings["fullscreen"] != pygame.display.is_fullscreen():
                    self._toggle_fullscreen()
            self.state = "paused"
        elif choice == 3:
            self.state = "menu"

        self.screen.fill((0, 0, 0))
        self.pause_menu.draw(self.screen)

    def draw_game(self, dt):
        canvas = pygame.Surface(self.screen.get_size())
        self.world.draw(canvas, self.camera)
        if self.true_portal:
            self.true_portal.draw(canvas, self.camera, pygame.time.get_ticks())
        if self.fake_portal:
            self.fake_portal.draw(canvas, self.camera, pygame.time.get_ticks())
        self.player.draw(canvas, self.camera)
        self.hud.draw(canvas, self.player, self.true_portal, self.camera, dt)

        if config.HEAT_HAZE_ENABLED:
            canvas = effects.apply_heat_haze(canvas, pygame.time.get_ticks())
        self.screen.blit(canvas, (0, 0))

    def draw_victory(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._start_new_game()
                self.state = "running"
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = "menu"
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        font = pygame.font.Font(config.DEFAULT_FONT, 36)
        text = font.render("Victoire! Entrée pour recommencer", True, (255, 255, 255))
        rect = text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(text, rect)


if __name__ == "__main__":
    Game().run()
