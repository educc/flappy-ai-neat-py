import pygame
import random
from sprites import Bird, GameState, Pipe
from brain import UserBrain

# Dimensiones de la ventana del juego
WIDTH = 288
HEIGHT = 512

# Colores
WHITE = (255, 255, 255)

# Inicialización de Pygame

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Carga de recursos
background_img = pygame.image.load("assets/background.png").convert()
bird_img = pygame.image.load("assets/bird.png").convert_alpha()
pipe_img = pygame.image.load("assets/pipe.png").convert_alpha()


font = pygame.font.Font(None, 36)

# Función para mostrar el puntaje en pantalla


def show_score(score):
    score_surface = font.render(str(score), True, WHITE)
    score_rect = score_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(score_surface, score_rect)

# Función principal del juego


def start_game_loop():

    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    pipes = pygame.sprite.Group()

    # Creación del jugador
    bird = Bird(HEIGHT, bird_img, UserBrain())
    all_sprites.add(bird)

    running = True
    score = 0

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            bird.makeJumpIfNecessary(GameState(event, None, None))

        # Actualización de los sprites
        all_sprites.update()

        # Generación de nuevos obstáculos
        if len(pipes) < 5:
            if len(pipes) == 0:
                x = WIDTH
            else:
                x = pipes.sprites()[-1].rect.x + 150
            y = random.randint(200, 350)
            pipe_top = Pipe(x, y - 620, False, pipe_img)
            pipe_bottom = Pipe(x, y, True, pipe_img)
            pipes.add(pipe_top, pipe_bottom)
            all_sprites.add(pipe_top, pipe_bottom)

        # Verificación de colisiones
        if pygame.sprite.spritecollide(bird, pipes, False):
            running = False

        if bird.rect.y >= HEIGHT or bird.rect.y <= 0:
            running = False

        # Eliminación de los obstáculos que salen de la pantalla
        for pipe in pipes:
            if pipe.rect.right < 0:
                pipes.remove(pipe)
                all_sprites.remove(pipe)

        score = score + 1

        # Dibujado de la pantalla
        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)
        show_score(score)
        pygame.display.flip()
        clock.tick(60)

    # pygame.quit()
