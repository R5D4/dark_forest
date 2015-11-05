# The Dark Forest
Simple text-based dungeon crawler with a D&D-inspired combat system. For learning python.

## How To Run
```bash
python game.py
```

## Unofficial Story
Middle-Earth inspired.
Update - new background story:
* Class/race/background TBD
* Enter forest with minimal equipment
* Evil power prevents you from leaving, must defeat boss

## Current Features
1. Map
  * All scenes and map topography are procedurally generated!
  * 24-hour game clock with gradual day/night cycle
  * Boss encounter chance depends on your natural surroundings and time
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
  * Hit chance and damage based on character and attack attributes
  * Critical hits
  * Enemy bloodied when HP < 30% 
  * Ignores distance

## Planned Features
1. Exploration System
  * Certain map areas provide randomized equipment
1. Character Update
  * Character classes
2. Items
  * 2H weapons
  * Armor and consummables
3. Hunting System 
  * Ability for boss or player to "hunt" if other party runs from combat
  * Limited to certain number of scene transitions
1. Flavour text (descriptions)
  * Extract all flavour text into own file
  * Expand on descriptions
4. Weather (includes phase of the moon)
  * Weather-based special actions
4. Interface
  * Interactive game interface with curses

## Next Action
* Design healing system

## How to Play
### Map Commands
  * 'look' - look around (hint: you get a better view from high up)
  * 'n', 'e', 's', 'w', etc. - to move out to another area in that direction
  * 'map' - draw the map
  * 'attack' - to attack the enemy once you see it
  * 'time' - tell the time of day
  * 'wait' - Wait for 1 hour
  * 'rest' - Rest for 3 hours
  * 'pray' - Pray to Elbereth (takes 1 hour)
  * 'stats' - Print character stats
  * 'inventory' - Print inventory and item ID
  * 'equip' - Print equipped items
  * 'equip <item ID>' - Equip item specified by ID
  * 'unequip <slot>' - Unequip item from equipment slot
  * 'examine <item ID>' - Examine the item specified by ID

### Combat Commands
  * Simplified verion of DnD 3.5e/Pathfinder
  * The player currently has three attacks. Type them once you're in combat.
  * 'shoot' - shoot an arrow from your longbow
  * 'slash' - slash with your elven long-knife
  * 'stab' - stab with your hunting knife
