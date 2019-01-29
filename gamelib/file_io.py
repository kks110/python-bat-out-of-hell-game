import fileinput
import os
import pygame
from pygame.locals import *
import yaml


# If the scores file doesn't exist, it creates it
# Then appent the score to the file
def save_score(score):
    score_path_check()
    score = str(score)
    score = score + '\n'
    f = open('data/top.scores', 'a')
    f.write(score)
    f.close()

# Reads each line and saves to a list
# Turns them back to ints to sorts them correctly
# Returns the top 5 and changes back to string to be displayed
def load_scores():
    score_path_check()
    top_scores = []
    scores = [line.rstrip('\n') for line in open('data/top.scores')]
    scores = [int(x) for x in scores]
    scores.sort(reverse = True)
    top_scores = scores[:5]
    top_scores = [str(x) for x in top_scores]
    return top_scores

# Checks that the data directory exists, and that the top scores file exists
def score_path_check():
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.isfile('data/top.scores'):
        f = open('data/top.scores', 'w')
        f.write('0\n0\n0\n0\n0')
        f.close()

# Loads the config file for the game
def config_load():
    config_file = 'data/config.yaml'
    with open(config_file) as f:
        config_map = yaml.safe_load(f)
        return config_map

# Is used to load the sprite sheets
class Spritesheet(object):
    # confirms file is readable, throws error if not
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error:
            print ('Unable to load spritesheet image:' + filename)
            raise SystemExit

    # Returns a single image from the sprite sheet
    def image_at(self, rectangle, colorkey):
        # Loads image from x,y,x+offset,y+offset
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]

    # Gets the first rect size, then multiplys that across, then uses the other functions to get the other images
    def load_strip(self, rect, image_count, colorkey = None):
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(tups, colorkey)
