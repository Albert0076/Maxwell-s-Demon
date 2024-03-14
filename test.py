import pygame
import pymunk
from pymunk import pygame_util
import sys
import random


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Join. Just wait and the L will top over.")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 900.0)

    lines = add_static_L(space)
    balls = []
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    ticks_to_next_ball = 10
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y < 0:
                balls_to_remove.append(ball)

        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        space.step(1 / 50.0)

        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(60)


def add_ball(space):
    mass = 3
    radius = 25
    body = pymunk.Body()
    x = random.randint(120, 300)
    body.position = x, 50
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.friction = 1
    space.add(body, shape)
    return shape


def draw_ball(screen, ball):
    p = int(ball.body.position.x), int(ball.body.position.y)
    pygame.draw.circle(screen, (0, 0, 255), p, int(ball.radius), 2)


def add_static_L(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (300, 300)
    l1 = pymunk.Segment(body, (-150, 0), (225, 0), 5)
    l2 = pymunk.Segment(body, (-150, 0), (-150, 50), 5)
    l1.friction = 1
    l2.friction = 2

    space.add(body, l1, l2)
    return l1, l2


if __name__ == "__main__":
    main()
