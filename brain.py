import pygame
from sprites import BirdBrain, GameState


class UserBrain:
    BirdBrain

    def __init__(self):
        pass

    def shouldJump(self, state: GameState):
        if not state.event:
            return False

        event = state.event
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return True

        return False
