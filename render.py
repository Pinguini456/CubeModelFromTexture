import pygame
import numpy as np
import cv2
from PIL import Image, ImageOps
from math import *
import os


WIDTH, HEIGHT = 512, 512
scale = 100
pos = [WIDTH/2, HEIGHT/2]
x_angle = 0.51
y_angle = 0.79

def make_image_quadrant_transparent(image: str, quadrants: list):
    """creates image with transparent quadrants from image

    :param image: base image
    :param quadrants: quadrants to make transparent e.g [1, 2, 3, 4]
    """

    img = Image.open(image)
    img = img.convert("RGBA")
    width, height = img.size
    pixels = img.load()
    top_left = []
    bottom_right = []

    for quadrant in quadrants:
        match quadrant:
            case 1:
                top_left = (0, 0)
                bottom_right = (width // 2, height // 2)
            case 2:
                top_left = (width // 2, 0)
                bottom_right = (width, height // 2)
            case 3:
                top_left = (0, height // 2)
                bottom_right = (width // 2, height)
            case 4:
                top_left = (width // 2, height // 2)
                bottom_right = (width, height)

        for x in range(top_left[0], bottom_right[0]):
            for y in range(top_left[1], bottom_right[1]):
                r, g, b, a = pixels[x, y]
                pixels[x, y] = (r, g, b, 0)

    img.save('temp/' + str(quadrants) + image.split('/')[-1])


def transform_matrix(matrix: np.matrix[3, 3], w: int, h: int):
    """transforms matrix by width and height

    :param matrix: base matrix
    :param w: width
    :param h: height
    :return: transformed matrix
    """

    t_matrix = np.matrix([
        [w, 0, 0],
        [0, h, 0],
        [0, 0, w]
    ])
    return np.dot(t_matrix, matrix)

def transform_image(source: str, dest: list):
    """transforms an image so that the corners meet specified points

    :param source: image path
    :param dest: destination points
    :return: warped pygame image
    """

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

def render(top_image: str, left_image: str, right_image: str, img_size: tuple[int, int], cube_size: tuple[int, int], output_folder: str):
    """renders cube with texture and size, and saves it as png

    :param top_image: top image texture path
    :param left_image: left image texture path
    :param right_image: right image texture path
    :param img_size: output image size
    :param cube_size: width and height of cube
    :param output_folder: output directory
    """


    pygame.init()

    print('rendering ' + top_image)

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
        transform3d = transform_matrix(point.reshape((3, 1)), cube_size[0] / 100, cube_size[1] / 100)
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

    output_surf.blit(top_surf, (8, 0))
    output_surf.blit(left_surf, (-5, 2))
    output_surf.blit(right_surf, (4, 2))

    output_array_rgb = pygame.surfarray.array3d(output_surf)
    output_array_alpha = pygame.surfarray.pixels_alpha(output_surf)
    output_array = np.dstack((output_array_rgb, output_array_alpha))
    output_image = Image.fromarray(output_array)
    output_image = output_image.rotate(-90)
    output_image = ImageOps.mirror(output_image)
    output_image = output_image.resize((img_size[0], img_size[1]), resample=Image.Resampling.NEAREST)
    output_image.save(output_folder + '/' + top_image.split('/')[-1])

    pygame.quit()

def render_stair(top_texture: str, left_texture: str, right_texture: str, img_size: tuple[int, int], cube_size: tuple[int, int], output_folder: str):
    """renders model with stair shape with texture and size, and saves it as a png

    :param top_texture: top image texture path
    :param left_texture: left image texture path
    :param right_texture: right image texture path
    :param img_size: size of output image
    :param cube_size: width and height of model
    :param output_folder: output directory
    """


    pygame.init()

    os.makedirs('temp', exist_ok=True)

    print('rendering ' + top_texture)

    points = []

    points.append(np.matrix([-1, -1, 1]))
    points.append(np.matrix([1, -1, 1]))
    points.append(np.matrix([1, 1, 1]))
    points.append(np.matrix([-1, 1, 1]))
    points.append(np.matrix([-1, -1, -1]))
    points.append(np.matrix([1, -1, -1]))
    points.append(np.matrix([1, 1, -1]))
    points.append(np.matrix([-1, 1, -1]))

    points.append(np.matrix([0, 1, -1]))
    points.append(np.matrix([0, 1, 1]))
    points.append(np.matrix([0, 0, -1]))
    points.append(np.matrix([0, 0, 1]))
    points.append(np.matrix([1, 0, -1]))
    points.append(np.matrix([1, 0, 1]))
    points.append(np.matrix([0, -1, -1]))
    points.append(np.matrix([0, -1, 1]))
    points.append(np.matrix([-1, 0, -1]))
    points.append(np.matrix([-1, 0, 1]))

    projected_points = [
        [n, n] for n in range(len(points))
    ]

    projection_matrix = np.matrix([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ])

    xz_reflection_matrix = np.matrix([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ])

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
        transformed3d = transform_matrix(point.reshape((3, 1)), cube_size[0] / 100, cube_size[1] / 100)
        reflected3d = np.dot(xz_reflection_matrix, transformed3d)
        rotated3d = np.dot(y_rotation_matrix, reflected3d)
        rotated3d = np.dot(x_rotation_matrix, rotated3d)
        projected2d = np.dot(projection_matrix, rotated3d)
        x = int(projected2d[0][0] * scale) + pos[0]
        y = int(projected2d[1][0] * scale) + pos[1]
        projected_points[i] = [x, y]
        i += 1

    make_image_quadrant_transparent(top_texture, [3, 4])
    make_image_quadrant_transparent(top_texture, [1, 2])
    make_image_quadrant_transparent(left_texture, [2])
    make_image_quadrant_transparent(right_texture, [3, 4])
    make_image_quadrant_transparent(right_texture, [1, 2])

    top_left_surf = transform_image("temp/" + str([3, 4]) + top_texture.split('/')[-1], [projected_points[7], projected_points[3], projected_points[2], projected_points[6]])
    top_right_surf = transform_image("temp/" + str([1, 2]) + top_texture.split('/')[-1], [projected_points[17], projected_points[16], projected_points[12], projected_points[13]])
    left_surf = transform_image('temp/' + str([2]) + left_texture.split('/')[-1], [projected_points[7], projected_points[6], projected_points[5], projected_points[4]])
    right_top_surf = transform_image('temp/' + str([3, 4]) + right_texture.split('/')[-1], [projected_points[8], projected_points[9], projected_points[15], projected_points[14]])
    right_bottom_surf = transform_image('temp/' + str([1, 2]) + right_texture.split('/')[-1], [projected_points[6], projected_points[2], projected_points[1], projected_points[5]])

    left_bright = 34
    right_bright = 63

    left_surf.fill((left_bright, left_bright, left_bright), special_flags=pygame.BLEND_RGB_SUB)
    right_top_surf.fill((right_bright, right_bright, right_bright), special_flags=pygame.BLEND_RGB_SUB)
    right_bottom_surf.fill((right_bright, right_bright, right_bright), special_flags=pygame.BLEND_RGB_SUB)

    output_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    output_surf.fill((0, 0, 0, 0))

    output_surf.blit(top_left_surf, (9, 0))
    output_surf.blit(top_right_surf, (-2, 4))
    output_surf.blit(left_surf, (4, 7))
    output_surf.blit(right_top_surf, (4, 3))
    output_surf.blit(right_bottom_surf, (3, 2))

    output_array_rgb = pygame.surfarray.array3d(output_surf)
    output_array_alpha = pygame.surfarray.pixels_alpha(output_surf)
    output_array = np.dstack((output_array_rgb, output_array_alpha))
    output_image = Image.fromarray(output_array)
    output_image = output_image.rotate(-90)
    output_image = ImageOps.mirror(output_image)
    output_image = output_image.resize((img_size[0], img_size[1]), resample=Image.Resampling.NEAREST)
    output_image.save(output_folder + '/' + top_texture.split('/')[-1])

    pygame.quit()

    for item in os.listdir('temp'):
        item_path = os.path.join('temp', item)
        if os.path.isfile(item_path):
            os.remove(item_path)