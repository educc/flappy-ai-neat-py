import neat
import pygame
from pygame import sprite
import random
from sprites import Bird, GameState, Pipe
from brain import BirdBrain, NeuralNetBrain, RandomBrain

# Dimensiones de la ventana del juego
WIDTH = 288
HEIGHT = 512
FRAME_RATE = 60
GAP_BETWEEN_PIPES = 100

# Colores
WHITE = (255, 255, 255)


class FlappyBirdNeat:

    def __init__(self) -> None:
        # Inicialización de Pygame
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # Carga de recursos
        self.background_img = pygame.image.load(
            "assets/background.png").convert()
        self.bird_img = pygame.image.load("assets/bird.png").convert_alpha()
        self.pipe_img = pygame.image.load("assets/pipe.png").convert_alpha()

        self.font = pygame.font.Font(None, 36)
        self.all_sprites = pygame.sprite.Group()
        self.generation = 0

    def show_text(self, score: int):
        texts = [
            f"Generación: {self.generation}",
            f"Puntaje: {score}",
        ]
        y = 0
        for text in texts:
            y += 30
            surface = self.font.render(text, True, WHITE)
            # my_rect = surface.get_rect(center=(WIDTH // 2, 50))
            my_rect = surface.get_rect(center=(WIDTH // 2, y))

            self.screen.blit(surface, my_rect)

    def eval_genomes(self, genomes, config):
        # Grupos de sprites
        pipes = pygame.sprite.Group()

        # Creación del jugador
        self.all_sprites = pygame.sprite.Group()
        self.generation += 1

        birds = []
        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)

            bird = Bird(HEIGHT, self.bird_img, NeuralNetBrain(net))
            bird.genome = genome
            birds.append(bird)

            self.all_sprites.add(bird)

        score = 0

        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)

            for bird in birds:
                bird.jump(GameState(None, bird, pipes))

            # Actualización de los sprites
            self.all_sprites.update()

            self.__add_new_pipes(pipes)

            # Verificación de colisiones
            for bird in birds:
                collided = self.__check_collisions(bird, pipes)
                if collided:
                    bird.genome.fitness = score
                    birds.remove(bird)
                    self.all_sprites.remove(bird)

            self.__remove_pipes(pipes, self.all_sprites)

            score = score + 1

            running = len(birds) > 0
            # print(f"Running: {running} - Score: {score} - Generación: {self.generation}")

            self.__draw(score)

        # pygame.quit()

    def __draw(self, score: int):
        # Dibujado de la pantalla
        self.screen.blit(self.background_img, (0, 0))
        self.all_sprites.draw(self.screen)
        self.show_text(score)
        pygame.display.flip()
        self.clock.tick(FRAME_RATE)

    def __add_new_pipes(self, pipes: sprite.Group):
        # Generación de nuevos obstáculos
        if len(pipes) < 5:
            if len(pipes) == 0:
                x = WIDTH
            else:
                x = pipes.sprites()[-1].rect.x + 150
            y = random.randint(200, 350)

            pipe_bottom = Pipe(x, y, True, self.pipe_img)

            height = pipe_bottom.rect.height
            pipe_top = Pipe(
                x, y - (height + GAP_BETWEEN_PIPES), False, self.pipe_img)

            pipes.add(pipe_top, pipe_bottom)
            self.all_sprites.add(pipe_top, pipe_bottom)

    @staticmethod
    def __remove_pipes(pipes: sprite.Group, all_sprites: sprite.Group):
        # Eliminación de los obstáculos que salen de la pantalla
        for pipe in pipes:
            if pipe.rect.right < 0:
                pipes.remove(pipe)
                all_sprites.remove(pipe)

    @staticmethod
    def __check_collisions(bird: sprite.Sprite, pipes: sprite.Group):
        if pygame.sprite.spritecollide(bird, pipes, False):
            return True

        if bird.rect.y >= HEIGHT or bird.rect.y <= 0:
            return True

        return False
# end-class


def run_game_and_train():
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'net.config')

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    # p.add_reporter(neat.StdOutReporter(False))

    # Run until a solution is found.
    game = FlappyBirdNeat()
    winner = p.run(game.eval_genomes)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
# end-def


if __name__ == "__main__":
    run_game_and_train()
