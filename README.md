# The Dark Forest
Simple text-based dungeon crawler with a D&D-inspired combat system. 
For learning python.

## How To Run
```bash
python game.py
```

## How to Play
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

### Combat
  * Simplified verion of DnD 3.5e/Pathfinder
  * Attack options depends on the equipped weapon
  * e.g. Default weapon (Hunting Knife) provides the 'pierce' attack
  * Type 'pierce' once in combat to use it

### Gameplay tips
* Search the map for artifacts from ancient battles!
* The boss is more likely to be found where there are signs of its activity
* There's a chance that the boss will attack you when encountered
* 'run' from combat and 'rest' if you are low on HP
* Certain commands take time to perform, an enemy might sneak up on you
* Game commands have shortened forms, use the 'help' command in-game to see.
* The boss will be 'bloodied' when its HP is less than 30% 

## Unofficial Story
Middle-Earth inspired.
* Age of the world at this point is unclear
* Enter forest with minimal equipment
* Evil power prevents you from leaving, must defeat boss

## Current Features
1. Map
  * All scenes and map topography are procedurally generated!
  * 24-hour game clock with day/night cycle
  * Boss encounter chance depends on your natural surroundings and time
  * Explore and find better equipment
2. Characters
  * 1 Player character and 1 Boss character
  * Equip different weapons to use different attacks
  * Randomly generated character attributes
3. Combat
  * D&D-inspired, in that virtual dice are rolled
  * Boss has a chance of initiating combat if encountered
  * Can run from combat
  * One action per character per turn, alternating turns
  * Boss will randomly use one of its predefined attacks
  * Critical hits

## Planned Features
2. Items
  * Implement armor 
  * Implement consummables 
1. Character Update
  * Character classes
  * More boss types
3. Hunting System 
  * Ability for boss or player to "hunt" if other party runs from combat
  * Limited to certain number of scene transitions
1. Flavour text (descriptions)
  * Extract all flavour text into own file
  * Expand on descriptions
4. Map/Environment
  * Weather (includes phase of the moon)
  * Weather-based special actions
4. Interface
  * Interactive game interface with curses

## Next Major Update
  * Gameplay mechanics update
