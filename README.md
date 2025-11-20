# Desert Portals

Petit jeu 2D procédural en Pygame : trouvez le vrai portail dans un désert mouvant tout en évitant le faux portail. Inclut menus, sauvegarde JSON, boussole et effet mirage optionnel.

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
Le jeu ouvre une fenêtre redimensionnable. Si le plein écran est activé dans les paramètres, `Alt+Entrée` ou le toggle de menu basculeront l'état.

## Commandes
- Flèches ou WASD : déplacer le héros
- Échap : pause (depuis le jeu) ou retour depuis les sous-menus
- Entrée/Espace : valider un choix de menu

## Sauvegarde/chargement
- La sauvegarde JSON se fait via le menu pause (option "Sauvegarder") et crée `save.json`.
- "Charger" sur le menu principal restaure joueur, portails, paramètres et inventaire.

## Paramétrage rapide
- `config.py` regroupe les valeurs clés :
  - `PORTAL_MIN_R` / `PORTAL_MAX_R` : distance du vrai/faux portail au spawn.
  - `PLAYER_SPEEDS` + `DEFAULT_SPEED_INDEX` : paliers de vitesse du héros.
  - `WORLD_WIDTH` / `WORLD_HEIGHT` : taille du monde.
  - Couleurs (`PLAYER_COLOR`, `TRUE_PORTAL_COLOR`, etc.) et tailles (`PORTAL_RADIUS`, `PICKUP_SIZE`).
  - Effet de mirage : `HEAT_HAZE_ENABLED`, `HEAT_HAZE_AMPLITUDE`, `HEAT_HAZE_WAVELENGTH`, `HEAT_HAZE_SPEED`.

## Désactiver le heat haze
Dans `config.py`, mettez `HEAT_HAZE_ENABLED = False`, ou passez par le menu Paramètres en jeu.

## Architecture
- `main.py` : boucle principale et gestion des états (menus, jeu, victoire).
- `config.py` : constantes et paramètres.
- `world.py` : génération du décor sableux, pickups et caméra.
- `player.py` : déplacement et inventaire du héros.
- `portals.py` : placement et rendu des portails gagnant/faux.
- `menu.py` : menus principal/pause/paramètres.
- `hud.py` : HUD, boussole vers le vrai portail, inventaire.
- `effects.py` : effet de mirage optionnel.
- `saveio.py` : sérialisation JSON pour save/load.

## Packaging macOS (option)
```
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```
L'exécutable sera disponible dans `dist/`.
