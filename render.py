import pygame
import numpy as np
from math import *


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WIDTH, HEIGHT = 800, 600

scale = 100
pos = [WIDTH/2, HEIGHT/2]
x_angle = 0.61
y_angle = 0.79



screen = pygame.display.set_mode((WIDTH, HEIGHT))

points = []

points.append(np.matrix([-1, -1, 1]))
points.append(np.matrix([1, -1, 1]))
points.append(np.matrix([1,  1, 1]))
points.append(np.matrix([-1, 1, 1]))
points.append(np.matrix([-1, -1, -1]))
points.append(np.matrix([1, -1, -1]))
points.append(np.matrix([1, 1, -1]))
points.append(np.matrix([-1, 1, -1]))

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
])

projected_points = [
    [n, n] for n in range(len(points))
]

clock = pygame.time.Clock()
while True:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()


    x_rotation_matrix = np.matrix([
        [1, 0, 0],
        [0, cos(x_angle), -sin(x_angle)],
        [0, sin(x_angle), cos(x_angle)],
    ])

    y_rotation_matrix = np.matrix([
        [cos(y_angle), 0, sin(y_angle)],
        [0, 1, 0],
        [-sin(y_angle), 0, cos(y_angle)],
    ])


    screen.fill(WHITE)

    i = 0
    for point in points:
        rotated2d = np.dot(y_rotation_matrix, point.reshape((3, 1)))
        rotated2d = np.dot(x_rotation_matrix, rotated2d)
        projected2d = np.dot(projection_matrix, rotated2d)
        x = int(projected2d[0][0] * scale) + pos[0]
        y = int(projected2d[1][0] * scale) + pos[1]
        pygame.draw.circle(screen, BLACK, (x, y), 5)
        projected_points[i] = [x, y]
        i += 1

    top_points = [projected_points[0], projected_points[1], projected_points[5], projected_points[4]]
    left_points = [projected_points[7], projected_points[6], projected_points[5], projected_points[4]]
    right_points = [projected_points[2], projected_points[6], projected_points[5], projected_points[1]]
    pygame.draw.polygon(screen, RED, top_points)
    pygame.draw.polygon(screen, BLUE, left_points)
    pygame.draw.polygon(screen, GREEN, right_points)

    pygame.display.update()