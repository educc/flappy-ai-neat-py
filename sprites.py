from dataclasses import dataclass
import pygame
from pygame import image

# Clase Bird


@dataclass
class GameState:
    event: pygame.event
    bird: pygame.sprite.Sprite
    pipes: pygame.sprite.Group


class BirdBrain:
    def __init__(self):
        pass

    def shouldJump(self, state: GameState):
        return False


class Bird(pygame.sprite.Sprite):
    def __init__(self, heightOfGame: int, bird_img: image, brain: BirdBrain):
        pygame.sprite.Sprite.__init__(self)
        self.brain = brain
        self.image = bird_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = heightOfGame // 2
        self.velocity = 0
        self.gravity = 0.5

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

    def flap(self):
        self.velocity = -8

    def jump(self, state: GameState):
        if self.brain.shouldJump(state):
            self.flap()


# Clase Pipe

class Pipe(pygame.sprite.Sprite):

    def __init__(self, x: float, y: float, flipped: bool, pipe_img: image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.flip(pipe_img, False, flipped)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 2
