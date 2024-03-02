import numpy as np
import pygame

pygame.init()
cell_size = 5  # Size of each cell in pixels

matrix = np.zeros((100, 100), dtype=bool)

# Calculate screen dimensions based on matrix size and cell size
width, height = cell_size * matrix.shape[1], cell_size * matrix.shape[0]
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game")
clock = pygame.time.Clock()

def update_matrix():
    matrix[np.random.randint(0, 100), np.random.randint(0, 100)] = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update_matrix()

    # clear screen
    screen.fill((0, 0, 0))

    # Option 1: Reshape the color values (corrected)
    color_matrix = np.where(
        matrix[:, :, None],
        np.full((matrix.shape[0], matrix.shape[1], 3), 255),
        np.full((matrix.shape[0], matrix.shape[1], 3), 0),
    )

    # Draw the grid using cell_size
    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            # Calculate top-left corner of the cell based on its position and cell size
            top_left_x, top_left_y = x * cell_size, y * cell_size

            # Draw a rectangle representing the cell using the corresponding color from color_matrix
            pygame.draw.rect(
                screen,
                color_matrix[y, x],
                (top_left_x, top_left_y, cell_size, cell_size),
            )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
