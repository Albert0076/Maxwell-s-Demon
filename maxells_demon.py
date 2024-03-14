import pygame
import pymunk
from pymunk import pygame_util
import sys
import numpy as np

RADIUS = 4
MAX_SPEED = 150


class Particle:
    def __init__(self, space, position, velocity, weight):
        self.body = pymunk.Body()
        self.body.position = position
        self.body.velocity = velocity
        self.speed = np.sqrt(self.body.velocity.x ** 2 + self.body.velocity.y ** 2)
        self.shape = pymunk.Circle(self.body, RADIUS)
        self.shape.density = weight
        self.shape.elasticity = 1
        self.set_color()

        space.add(self.body, self.shape)

    def set_color(self):
        blue = abs(int(np.floor((MAX_SPEED - self.speed) / MAX_SPEED * 255)))
        if self.speed >= MAX_SPEED:
            red = 255
            blue = 0
        else:
            red = abs(int(np.floor((self.speed / MAX_SPEED) * 255)))
        self.shape.color = pygame.color.Color(red, 0, blue)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0, 0)

    sides = add_walls(space)
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        for particle in particles:
            particle.set_color()
        space.step(1 / 50.0)

        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(60)


def add_walls(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (0, 0)

    sides = [pymunk.Segment(body, (0, 0), (0, 600), 10),
             pymunk.Segment(body, (0, 600), (600, 600), 10),
             pymunk.Segment(body, (600, 600), (600, 0), 10),
             pymunk.Segment(body, (600, 0), (0, 0), 10),
             pymunk.Segment(body, (300, 600), (300, 350), 10),
             pymunk.Segment(body, (300, 0), (300, 250), 10)]

    for side in sides:
        side.elasticity = 1

    space.add(body, *sides)
    return sides


def add_particles(n, mu, sigma, space):
    particles = []
    for i in range(n):
        velocity = np.random.normal(mu, sigma, 2).tolist()
        position = (np.random.randint(10, 590), np.random.randint(10, 590))
        particles.append(Particle(space, position, velocity, 1))

    return particles


if __name__ == '__main__':
    main()
