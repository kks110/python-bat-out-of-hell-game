import pygame
from pygame.locals import *
import random


# Define the player and call super to give it the properties of pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, display_size):
        super(Player, self).__init__()
        # Loads the image, sets the background colour
        self.image = pygame.image.load('images/jet.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(0, (display_size["display_h"] / 2)))

    # These are the keys to move the player
    def update(self, pressed_keys, display_size):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep the player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > display_size["display_w"]:
            self.rect.right = display_size["display_w"]
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= display_size["display_h"]:
            self.rect.bottom = display_size["display_h"]

class Enemy(pygame.sprite.Sprite):
    # Keeps track of player score
    score = 0

    def __init__(self, display_size):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('images/missile.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(display_size["display_w"] + 50, random.randint(0, display_size["display_h"])))
        self.speed = random.randint(5, 20)

    def update(self, alive):
        # Will move toward the left, when it hits the left, it will increase the score by 1
        # if the player is alive (requires alive to be passed in)
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            alive = alive
            if alive:
                Enemy.score += 1

class Cloud(pygame.sprite.Sprite):
    def __init__(self, display_size):
        super(Cloud, self).__init__()
        self.image = pygame.image.load('images/cloud.png').convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(center=(display_size["display_w"] + 50, random.randint(0, display_size["display_h"])))

    def update(self):
        self.rect.move_ip(-8, 0)
        if self.rect.right < 0:
            self.kill()


class TextSurface():
    pygame.font.init()
    myfont = pygame.font.SysFont('Arial ', 40)

    def score(score):
        return TextSurface.myfont.render("Score: " + score, False, (0, 0, 0))

    def exit():
        return TextSurface.myfont.render("Press Esc to exit", False, (0, 0, 0))

    def restart():
        return TextSurface.myfont.render("Press space-bar to restart", False, (0, 0, 0))

    def top_scores_text():
        return TextSurface.myfont.render("Top Scores: ", False, (0, 0, 0))

    def top_scores_number(score):
        return TextSurface.myfont.render(f" {score}  ", False, (0, 0, 0))
