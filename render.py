from pickle import TUPLE

import pygame
import pygame.gfxdraw
import numpy as np
import cv2
from PIL import Image, ImageOps
from math import *

pygame.init()

def transform_matrix(matrix, w, h):
    t_matrix = np.matrix([
        [w, 0, 0],
        [0, h, 0],
        [0, 0, w]
    ])
    return np.dot(t_matrix, matrix)

def transform_image(source, dest):
    img = cv2.imread(source, cv2.IMREAD_UNCHANGED)

    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    else:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)

    h1, w1 = img.shape[:2]
    src_points = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
    dest_points = np.float32(dest)

    matrix = cv2.getPerspectiveTransform(src_points, dest_points)
    warped = cv2.warpPerspective(img, matrix, (WIDTH, HEIGHT), flags=cv2.INTER_NEAREST)
    warped = np.ascontiguousarray(warped)

    return pygame.image.frombuffer(warped.tobytes(), (WIDTH, HEIGHT), 'RGBA')

WIDTH, HEIGHT = 512, 512
scale = 100
pos = [WIDTH/2, HEIGHT/2]
x_angle = 0.51
y_angle = 0.79

def render(top_image, left_image, right_image, img_size, cube_size, output_folder, stair_shape):

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

    i = 0
    for point in points:
        transform3d = transform_matrix(point.reshape((3, 1)), cube_size[0], cube_size[1])
        rotated3d = np.dot(y_rotation_matrix, transform3d)
        rotated3d = np.dot(x_rotation_matrix, rotated3d)
        projected2d = np.dot(projection_matrix, rotated3d)
        x = int(projected2d[0][0] * scale) + pos[0]
        y = int(projected2d[1][0] * scale) + pos[1]
        projected_points[i] = [x, y]
        i += 1

    left_bright = 34
    right_bright = 63

    top_surf = transform_image(top_image, [projected_points[4], projected_points[0], projected_points[1], projected_points[5]])
    left_surf = transform_image(left_image, [projected_points[5], projected_points[4], projected_points[7], projected_points[6]])
    right_surf = transform_image(right_image, [projected_points[5], projected_points[1], projected_points[2], projected_points[6]])

    left_surf.fill((left_bright, left_bright, left_bright), special_flags=pygame.BLEND_RGB_SUB)
    right_surf.fill((right_bright, right_bright, right_bright), special_flags=pygame.BLEND_RGB_SUB)

    output_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    output_surf.fill((0, 0, 0, 0))

    output_surf.blit(top_surf, (8, 0)) # 100
    output_surf.blit(left_surf, (-5, 2)) # 73
    output_surf.blit(right_surf, (4, 2)) # 50

    output_array_rgb = pygame.surfarray.array3d(output_surf)
    output_array_alpha = pygame.surfarray.pixels_alpha(output_surf)
    output_array = np.dstack((output_array_rgb, output_array_alpha))
    output_image = Image.fromarray(output_array)
    output_image = output_image.rotate(-90)
    output_image = ImageOps.mirror(output_image)
    output_image = output_image.resize((img_size[0], img_size[1]), resample=Image.Resampling.NEAREST)
    output_image.save(output_folder + '/' + 'output.png')

# render('stonebrick.png', 'stonebrick.png', 'stonebrick.png', (64, 64), (1, 1), '', False)