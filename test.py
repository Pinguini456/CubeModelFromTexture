import pygame
import cv2
import numpy as np

# Initialize
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Perfect Perspective Warp")

# Load and prepare image
image = cv2.imread("stonebrick.png", cv2.IMREAD_UNCHANGED)

if image.shape[2] == 3:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
else:
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

h, w = image.shape[:2]

# Define source points (image corners)
src_pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]])

# Define destination points (screen polygon)
dst_pts = np.float32([
    [259.0, 218.0],    # top-right
    [400.0, 300.0],   # bottom-right
    [541.0, 219.0],   # top-left
    [400.0, 138.0]    # bottom-left
])

points = [
    [259.0, 218.0],    # top-right
    [400.0, 300.0],   # bottom-right
    [541.0, 219.0],   # top-left
    [400.0, 138.0]
]

# Compute perspective transform matrix
matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)

# Create a full-screen transparent canvas (RGBA)
canvas = np.zeros((600, 800, 4), dtype=np.uint8)

# Warp the image directly into the final canvas
cv2.warpPerspective(image, matrix, (800, 600), dst=canvas, borderMode=cv2.BORDER_TRANSPARENT, flags=cv2.INTER_NEAREST)

# Convert to pygame surface
canvas = np.ascontiguousarray(canvas)
surface = pygame.image.frombuffer(canvas.tobytes(), (800, 600), 'RGBA')

# Display loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))  # Background
    screen.blit(surface, (0, 0))# Blit whole canvas
    for i in points:
        pygame.draw.circle(screen, (0, 0, 0), (i[0], i[1]), 5)
    pygame.display.flip()

pygame.quit()
