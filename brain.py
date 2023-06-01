import random
import pygame
from pygame import sprite
from neat.nn import FeedForwardNetwork
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


class RandomBrain:
    BirdBrain

    def __init__(self):
        pass

    def shouldJump(self, state: GameState):
        int_random = random.randint(0, 1)
        if int_random == 1:
            return True
        return False


class NeuralNetBrain:
    BirdBrain

    def __init__(self, net: FeedForwardNetwork):
        self.net = net

    def shouldJump(self, state: GameState):
        if not state.bird or not state.pipes:
            return False

        closest_pipe = self.__find_closest_pipe(state.bird, state.pipes)

        inputForNet = [state.bird.rect.x,
                       state.bird.rect.y,
                       closest_pipe.rect.x,
                       closest_pipe.rect.y]
        # print("inputForNet: ", inputForNet)
        output = self.net.activate(inputForNet)
        if output[0] >= 0.5:
            return True
        return False

    @staticmethod
    def __find_closest_pipe(bird: sprite.Sprite, pipes: sprite.Group):
        closest_pipe = None
        for pipe in pipes:
            x = pipe.rect.x + pipe.rect.width
            if bird.rect.x <= x and pipe.rect.y > 0:
                if not closest_pipe:
                    closest_pipe = pipe
                elif pipe.rect.x < closest_pipe.rect.x:
                    closest_pipe = pipe
        return closest_pipe


class NeuralNetWithAllPipesBrain:
    BirdBrain

    def __init__(self, net: FeedForwardNetwork):
        self.net = net

    def shouldJump(self, state: GameState):
        if not state.bird or not state.pipes or len(state.pipes) < 6:
            return False

        pipes = []
        for pipe in state.pipes:
            pipes.append(pipe.rect.x)
            pipes.append(pipe.rect.y)

        inputForNet = [state.bird.rect.x,  state.bird.rect.y] + pipes
        # print("inputForNet: ", inputForNet)
        output = self.net.activate(inputForNet)
        if output[0] >= 0.5:
            return True
        return False
