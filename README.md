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
2. Characters
  * 1 Player character and 1 Boss character
  * Predefined character attacks
  * Randomly generated character attributes
3. Combat
  * D&D-inspired, in that virtual dice are rolled
  * Roll for initiative
  * One action per character per turn, alternating turns
  * Boss will randomly use one of its predefined attacks
  * Combat continues until one opponent expires (then the game is over)
  * Hit chance and damage based on character and attack attributes
  * Critical hits
  * Enemy bloodied when HP < 30% 
  * Ignores distance

## Planned Features
1. Exploration System
  * Certain map areas provide randomized equipment
1. Character Update
  * Ability to acquire new equipment and attacks
2. Combat System Update
  * Run from combat
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
* Make game support items and equipment

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

### Combat Commands
  * The player currently has three attacks. Type them once you're in combat.
  * 'shoot' - shoot an arrow from your longbow
  * 'slash' - slash with your elven long-knife
  * 'stab' - stab with your hunting knife
