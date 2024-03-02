import numpy as np
import pygame

pygame.init()
cell_size = 5  # Size of each cell in pixels

GRID_SIZE = 200

matrix = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)

# Calculate screen dimensions based on matrix size and cell size
width, height = cell_size * matrix.shape[1], cell_size * matrix.shape[0]
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game")
clock = pygame.time.Clock()


def initialize_matrix():
    global matrix
    print("initialize_matrix()")
    ratio = 0.1
    for i in range(int(ratio * GRID_SIZE * GRID_SIZE)):
        matrix[np.random.randint(0, GRID_SIZE), np.random.randint(0, GRID_SIZE)] = True


def update_matrix():
    global matrix

    print("update_matrix()")
    next_generation = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)

    # iterate over all cells
    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            living_neighbors = 0
            # iterate over neighbors
            for neighbor_y in [-1, 0, 1]:
                for neighbor_x in [-1, 0, 1]:
                    if neighbor_y == 0 and neighbor_x == 0:
                        continue
                    try:
                        if matrix[y + neighbor_y, x + neighbor_x]:
                            living_neighbors += 1
                    except Exception:
                        pass

            # Rules
            if matrix[y, x]:
                # live cell
                if living_neighbors < 2:
                    next_generation[y, x] = False
                elif living_neighbors in [2, 3]:
                    next_generation[y, x] = True
                else:
                    next_generation[y, x] = False
            else:
                # dead cell
                if living_neighbors == 3:
                    next_generation[y, x] = True

    matrix = next_generation


initialize_matrix()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update_matrix()

    # clear screen
    screen.fill((0, 0, 0))

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
