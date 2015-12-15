# The Dark Forest
Text-based dungeon crawler with tracking/hunting system and D&D-inspired combat.

## How To Run
```bash
python game.py
```

## How to Play

### Goal
  * Track down and eliminate the terror in the Dark Forest.
  * You start with a knife, search your surroundings for things that will help.

### Map Commands
  * 'look' - Look around. Lists items you can pick up and their item IDs.
  * 'n', 'e', 's', 'w', etc. - Move out to another area in that direction
  * 'map' - Draw the map
  * 'attack' - Attack the enemy once you see it
  * 'time' - Tell the time of day
  * 'wait' - Wait for 1 hour
  * 'rest' - Rest for 3 hours (heals hp)
  * 'sleep' - Sleep for 8 hours (heals hp)
  * 'pray' - Pray to Elbereth (takes 1 hour - does nothing currently)
  * 'stats' - Print character stats
  * 'inventory' - Print inventory and item ID
  * 'equip' - Print equipped items
  * 'equip <item ID>' - Equip item specified by ID
  * 'unequip <slot>' - Unequip item from equipment slot
  * 'examine <item ID>' - Examine item in inventory (specify item ID)
  * 'search' - Search the scene for loot (takes 1 hour)
  * 'take <item ID>' - Take an item from the area (specify item ID)
  * 'drop <item ID>' - Drop an item from inventory into the scene
  * 'help' - Show all available commands

### Combat Commands
  * 'stats' - Print character stats
  * 'inventory' - Print inventory and item ID
  * 'run' - Run from the fight to a random adjacent area
  * 'help' - Print all available commands
  * Attack command (varies depending on weapon, e.g. 'pierce' w/ dagger)

### Gameplay tips
  * Search discarded item piles, you might get lucky!
  * It might take a few tries to get something from your search, but there's 
  always something there
  * Follow clues, recent clues will be "fresh"
  * There's a chance that the boss will attack you when encountered
  * 'run' from combat and 'rest' or 'sleep' if you are low on HP
  * The boss heals naturally outside of battle
  * Certain commands take time to perform, the enemy might sneak up on you
  * Game commands have shortened forms, use the 'help' command in-game to see.

## Unofficial Story
Middle-Earth inspired.
* Age of the world at this point is unclear
* Somehow you've found yourself trying to take out a monstrous beast in a 
gloomy forest. And you've only got a knife on ya.

## Current Features
1. Map
  * Procedurally generated topography
  * 24-hour game clock with day/night cycle
  * Explore and find better equipment
2. Characters
  * One Player character and one Boss character
  * Randomly generated character attributes
3. Items
  * Weapon and armor available to be found as treasure
  * Certain items require base stats of a certain level to be equipped
  * Equipping items gives stat bonuses
  * Equip different weapons to use different attacks
3. Tracking
  * Agent-based tracking: the boss moves across the map as an individual entity
  * Boss leaves clues as it moves
3. Combat
  * Loosely based on D&D 3.5e
  * Boss has a chance of initiating combat if encountered
  * Boss has a chance to run from combat at low HP
  * Player can run from combat (incur extra enemy attack)
  * One action per character per turn, alternating turns

## Planned Features
4. Map/Environment
  * More coherent environment generation (rivers connect across scenes, etc.)
  * More environments (currently only mixed forest)
  * Weather (includes phase of the moon)
2. Gameplay
  * More realistic behaviour model for the boss (based on real-life wild boars)
  * Environmental features have bigger impact on gameplay
1. Flavour text (descriptions)
  * Extract all flavour text into own file
  * Expand on descriptions
2. Items
  * Consummables
1. Character Update
  * Character classes
  * More boss types
4. Interface
  * Graphical (ASCII-based) game interface

## Next Major Update
  * Core gameplay update: boss movement behavior update

## Next Minor Update
