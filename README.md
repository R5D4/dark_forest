# The Dark Forest
Simple text-based dungeon crawler with a D&D-inspired combat system. For learning python.

## How To Run
```bash
python game.py
```

## Unofficial Story
Middle-Earth inspired.
In a world where an ancient evil stirs and the sky grows dark, only one man
can unite the free lands and fulfil the prophesy... 
> Renewed shall be blade that was broken,
> The crownless again shall be king.

You're not playing as him, so relax. You play as ranger who was sent to
patrol the area near the south-east of Mirkwood. You know, getting kittens out
of trees and chasing down escaped swans, etc. But there was more trouble than
you expected and you were "volunteered" for a more dangerous task.

## Current Features
1. Map
  * 9 predefined areas
  * Boss encounter based on probability (different for each area)
  * Movement between areas 
  * Simple predefined interactions (look, climb up trees, climb down trees)
  * Can quit game early if you find exits in the map (you lose tho)
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
1. Map
  * More environmental interaction
  * Help messages
  * Tracking/hunting system (procedurally generated environmental clues)
  * Procedurally-generated map?!
2. Characters
  * Items
  * Equipment
  * Procedural generation of items and equipment
3. Combat
  * Conditions
  * Use of items
  * Environmental interaction
  * More nuanced battle system (allow reaction actions)
  * Movement/distance?

## How to Play
### Map Commands
  * 'l' - lowercase 'L' to look around
  * 'climb' - to climb any climbable trees in the area
  * 'down' - to come down from a tree once you're up
  * 'n', 'e', 's', 'w', etc. - to move out to another area in that direction
  * 'attack' - to attack the enemy once you see it

### Combat Commands
  * The player currently has three attacks. Type them once you're in combat.
  * 'shoot' - shoot an arrow from your longbow
  * 'slash' - slash with your elven long-knife
  * 'stab' - stab with your hunting knife
