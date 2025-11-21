# Desert Portals

Petit jeu 2D procédural en Pygame : explorez un désert ou une forêt miroir, trouvez le vrai portail et évitez le faux qui vous fait basculer d'un monde à l'autre. Inclut menus, sauvegarde JSON, cycle jour/nuit, collisions avec rochers, lampe, boussole et effet mirage optionnel.

## Installation
1. Assurez-vous d'avoir Python 3.10+.
2. Installez les dépendances :
   ```bash
   python -m pip install -r requirements.txt
   ```

## Lancer le jeu
```bash
python main.py
```
La fenêtre est redimensionnable. Activez/désactivez le plein écran via le menu Paramètres.

## Commandes
- Flèches ou WASD : déplacer le héros
- Échap : pause (depuis le jeu) ou retour depuis les sous-menus
- Entrée/Espace : valider un choix de menu

## Gameplay et nouveautés
- **Deux portails presque identiques** : l'un mène à la victoire, l'autre change de monde (désert ↔ forêt). Dans la forêt, réemprunter le portail piégé ramène au désert.
- **Cycle jour/nuit** : 2 min de jour, 2 min de nuit ; la nuit est assombrie par un vignettage (visible sauf si vous avez la lampe).
- **Lampe** : pickup unique à trouver dans la forêt ; rend la nuit claire dans les deux mondes. Affiché dans le HUD.
- **Rochers** : obstacles générés procéduralement, infranchissables dans les deux mondes.
- **Monde étendu** : carte 8000×6000, portails éloignés du spawn (1200–2400 px).
- **Vitesse ajustable** : 120/140/180 px/s via Paramètres.

## Sauvegarde/chargement
- La sauvegarde JSON se fait via le menu pause (option "Sauvegarder") et crée `save.json`.
- "Charger" sur le menu principal restaure joueur, monde actuel (désert/forêt), portails, paramètres (vitesse, plein écran, heat haze, luminosité nuit) et inventaire (eau/torche/lampe).

## Paramétrage rapide
- `config.py` regroupe les valeurs clés :
  - `PORTAL_MIN_R` / `PORTAL_MAX_R` : distance des portails au spawn.
  - `PLAYER_SPEEDS` + `DEFAULT_SPEED_INDEX` : paliers de vitesse du héros.
  - `WORLD_WIDTH` / `WORLD_HEIGHT` : taille du monde.
  - Cycle jour/nuit : `DAY_DURATION`, `NIGHT_DURATION`, `NIGHT_LEVELS`, `NIGHT_VISIBILITY_RADIUS`, `NIGHT_FADE_WIDTH`.
  - Rochers : `DESERT_ROCK_DENSITY`, `FOREST_ROCK_DENSITY`, `ROCK_SIZE_RANGE`.
  - Couleurs/biomes : `BIOMES` (désert/forêt), `PORTAL_BASE_COLOR`.
  - Effet de mirage : `HEAT_HAZE_ENABLED`, `HEAT_HAZE_AMPLITUDE`, `HEAT_HAZE_WAVELENGTH`, `HEAT_HAZE_SPEED`.

## Désactiver le heat haze
Dans `config.py`, mettez `HEAT_HAZE_ENABLED = False`, ou passez par le menu Paramètres en jeu.

## Architecture
- `main.py` : boucle principale, gestion des états, changement de monde.
- `config.py` : constantes et paramètres.
- `world.py` : génération désert/forêt, pickups (lampe en forêt), rochers, caméra.
- `player.py` : déplacement (vitesse en px/s), collisions rochers, inventaire.
- `portals.py` : placement/rendu de deux portails visuellement similaires, logique vrai/piège.
- `menu.py` : menus principal/pause/paramètres (vitesse, plein écran, heat haze, luminosité nuit).
- `hud.py` : HUD, boussole vers le vrai portail, indicateur jour/nuit, inventaire (lampe).
- `effects.py` : effet de mirage optionnel et vignette nuit.
- `saveio.py` : sérialisation JSON incluant monde actuel et lampe.

## Packaging macOS (option)
```
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```
L'exécutable sera disponible dans `dist/`.

## Changelog
- Ajout d'un monde forêt miroir et bascule via portail piégé.
- Cycle jour/nuit avec vignette et option de luminosité.
- Vitesse réduite (paliers 120/140/180 px/s) et collisions avec rochers.
- Lampe ramassable (forêt) qui supprime l'assombrissement nocturne.
- Sauvegardes enrichies (monde actuel, lampe, paramètres nuit) et HUD mis à jour.
