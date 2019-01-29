# First attempt at making a python game
Followed [this Guide](https://realpython.com/pygame-a-primer/), then added my own little extras to it.

The idea of the game it to avoid the fireballs and get as high score as you can.

## Controls
* Arrow keys or WASD to move
* Space to restart
* Return to show help page (return again to close)
* Escape to close the game

## Extra features added
**Extra features include:**
* Different sprites
* Sprites have animations
* You can press space to restart
* It keeps track of your score
* Score increases when a fireball hits the left hand side of the screen
* Added gems, these also give you score. Different gems give different scores
* Gems are spawned at different frequencies depending on value
* It saves your score to a file, and at the end, will display the top five in that file
* Has a life system and displays that as hearts
* You can collect water droplets to increase your life
* Has a starting splash screen
* If you press enter, it will display more info about the objects in the
* Added code to read sprite sheets
* Converting some of the images to sprite sheets, rather than lots of separate files
* Update the text with the game font
* Final scores also now in game font, pulling from a number sprite sheet
* A message to say if you are beating the high score / in the top 5
* A modifiable config file to change things such as screen res, enemy speeds, ect..

## Modifying the game
In the data folder, there is a file called config.yaml. This is what the game reads to load the config.
It can be edited to change parts of the game.
Please see the file for more info.
config.backup contains a complete copy of the file, so you can refer to that to changes things back to default.

## Python packages needed
```
py -m pip install pygame
```
```
py -m pip install PyYAML
```
