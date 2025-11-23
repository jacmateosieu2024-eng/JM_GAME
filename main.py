"""Entry point for the Desert/Forest Portals game."""

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
            "night_level": config.DEFAULT_NIGHT_LEVEL_INDEX,
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

        self.portal_cooldown = 0
        self.time_of_day = 0.0

        self._start_new_game()

    def _start_new_game(self, seed: int | None = None):
        self.seed = seed or random.randint(0, 999999)
        self.worlds = {
            "desert": world.World("desert", self.seed),
            "forest": world.World("forest", self.seed),
        }
        self.current_world = "desert"
        self.player = player.Player(speed_index=self.settings["speed_index"])
        self.true_portal, self.trap_portal = portals.place_portals(pygame.Vector2(config.PLAYER_SPAWN))
                # DEBUG: rapprocher les portails pour les voir tout de suite
        if self.true_portal:
            self.true_portal.pos.update(config.PLAYER_SPAWN[0] + 260, config.PLAYER_SPAWN[1])
        if self.trap_portal:
            self.trap_portal.pos.update(config.PLAYER_SPAWN[0] - 260, config.PLAYER_SPAWN[1])

        self.camera = world.Camera(config.WORLD_WIDTH, config.WORLD_HEIGHT)
        self.victory = False
        self.time_of_day = 0.0
        self.portal_cooldown = 0

    def _toggle_fullscreen(self):
        self.settings["fullscreen"] = not self.settings["fullscreen"]
        if self.settings["fullscreen"]:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        elif:
            self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.RESIZABLE)
                # --- DEBUG TELEPORT PORTALS ---
        elif event.type == pygame.KEYDOWN:
            # 8 : afficher coordonnées dans le terminal
            if event.key == pygame.K_8:
                print("Player:", int(self.player.pos.x), int(self.player.pos.y))
                print("Portal A (real):", int(self.true_portal.pos.x), int(self.true_portal.pos.y))
                print("Portal B (trap):", int(self.trap_portal.pos.x), int(self.trap_portal.pos.y))
    
            # 9 : téléporter près du portail réel
            elif event.key == pygame.K_9:
                self.player.pos.update(self.true_portal.pos.x + 40, self.true_portal.pos.y)
    
            # 0 : téléporter près du portail piège
            elif event.key == pygame.K_0:
                self.player.pos.update(self.trap_portal.pos.x + 40, self.trap_portal.pos.y)


    def run(self):
        while self.running:
            dt = self.clock.tick(config.FPS)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                        # --- DEBUG: touches 8/9/0 (pas besoin de Fn sur Mac) ---
                elif event.type == pygame.KEYDOWN:
                    # 8 : afficher positions dans le Terminal
                    if event.key == pygame.K_8 and self.true_portal and self.trap_portal:
                        print("Player:", int(self.player.pos.x), int(self.player.pos.y))
                        print("Portal A (real):", int(self.true_portal.pos.x), int(self.true_portal.pos.y))
                        print("Portal B (trap):", int(self.trap_portal.pos.x), int(self.trap_portal.pos.y))
            
                    # 9 : téléporter près du portail réel
                    elif event.key == pygame.K_9 and self.true_portal:
                        self.player.pos.update(self.true_portal.pos.x + 40, self.true_portal.pos.y)
            
                    # 0 : téléporter près du portail piège
                    elif event.key == pygame.K_0 and self.trap_portal:
                        self.player.pos.update(self.trap_portal.pos.x + 40, self.trap_portal.pos.y)


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
            loaded = saveio.load_game(player.Player, portals.Portal)
            if loaded:
                (
                    self.player,
                    self.worlds,
                    (self.true_portal, self.trap_portal),
                    settings,
                    current_world,
                    self.time_of_day,
                ) = loaded
                self.settings.update(settings)
                for key, default in [
                    ("speed_index", config.DEFAULT_SPEED_INDEX),
                    ("fullscreen", False),
                    ("heat_haze", config.HEAT_HAZE_ENABLED),
                    ("night_level", config.DEFAULT_NIGHT_LEVEL_INDEX),
                ]:
                    if key not in self.settings:
                        self.settings[key] = default
                self.current_world = current_world
                config.HEAT_HAZE_ENABLED = self.settings.get("heat_haze", config.HEAT_HAZE_ENABLED)
                self.player.speed_index = self.settings.get("speed_index", self.player.speed_index)
                self.state = "running"
        elif choice == 2:
            self.state = "settings"
        elif choice == 3:
            self.running = False

        self.screen.fill((0, 0, 0))
        self.main_menu.draw(self.screen)
        if self.state == "settings":
            self._open_settings_menu()
            self.state = "menu"

    def _open_settings_menu(self):
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

    def update_gameplay(self, dt, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.state = "paused"
            return
        current = self.worlds[self.current_world]
        self.player.handle_input(keys, dt, current)
        self.camera.update(self.player.pos, self.screen.get_rect())
        pickup = current.remove_pickup_at(self.player.pos)
        self.player.collect(pickup)

        now = pygame.time.get_ticks()
        if now > self.portal_cooldown:
            if self.true_portal and self.true_portal.collides_with(self.player.rect):
                self.victory = True
                self.state = "victory"
            elif self.trap_portal and self.trap_portal.collides_with(self.player.rect):
                self._toggle_world()
                self.portal_cooldown = now + 800

        self.time_of_day += dt / 1000.0
        self.draw_game(dt)

    def _toggle_world(self):
        self.current_world = "forest" if self.current_world == "desert" else "desert"
        # Avoid being stuck inside a rock after switching
        if self.worlds[self.current_world].colliding_rocks(self.player.rect):
            self.player.pos = pygame.Vector2(config.PLAYER_SPAWN)
            self.player._update_rect()

    def handle_pause_menu(self, events):
        choice = self.pause_menu.update(events)
        if choice == 0:
            self.state = "running"
        elif choice == 1:
            saveio.save_game(
                self.player,
                self.worlds,
                self.current_world,
                (self.true_portal, self.trap_portal),
                self.settings,
                self.time_of_day,
            )
            self.state = "running"
        elif choice == 2:
            self._open_settings_menu()
            self.state = "paused"
        elif choice == 3:
            self.state = "menu"

        self.screen.fill((0, 0, 0))
        self.pause_menu.draw(self.screen)

    def draw_game(self, dt):
        canvas = pygame.Surface(self.screen.get_size())
        current = self.worlds[self.current_world]
        current.draw(canvas, self.camera)
        if self.true_portal:
            self.true_portal.draw(canvas, self.camera, pygame.time.get_ticks())
        if self.trap_portal:
            self.trap_portal.draw(canvas, self.camera, pygame.time.get_ticks())
        self.player.draw(canvas, self.camera)
        self.hud.draw(canvas, self.player, self.true_portal, self.camera, dt, self.time_of_day)

        brightness = config.NIGHT_LEVELS[self.settings.get("night_level", config.DEFAULT_NIGHT_LEVEL_INDEX)]
        player_screen_pos = pygame.Vector2(
            self.player.pos.x - self.camera.offset.x,
            self.player.pos.y - self.camera.offset.y,
        )
        canvas = effects.apply_day_night(canvas, player_screen_pos, self.time_of_day, brightness, self.player.inventory.get("lamp", False))

        if config.HEAT_HAZE_ENABLED and self.current_world == "desert":
            canvas = effects.apply_heat_haze(canvas, pygame.time.get_ticks())
        self.screen.blit(canvas, (0, 0))

    def draw_victory(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._start_new_game(self.seed)
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
