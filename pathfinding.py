"""
Path finding algorithm

Roughly based on https://github.com/Alexander-Wilms/Robotics-simulation/tree/master/Termin%206%20-%20Breitensuche
"""

from copy import deepcopy
from pprint import pprint

import pygame

queue: list[list[int]] = []


def pathfinding(start_x, start_y, goal_x, goal_y):
    global queue, obstacle_map, pathfinding_map

    pathfinding_map[start_x, start_y] = [255, 0, 0]
    pathfinding_map[goal_x, goal_y] = [0, 0, 255]

    next_node_to_search = [start_x, start_y]
    queue.append(next_node_to_search)

    # Main game loop
    clock = pygame.time.Clock()

    done = False
    count = 0
    while not done:
        count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Breadth First Search: pop(0)
        # Depth First Search: pop(-1)
        current_node = queue.pop(0)

        for x_delta in [-1, 0, 1]:
            for y_delta in [-1, 0, 1]:
                # 8-neighborhood
                if x_delta != 0 or y_delta != 0:
                    # next_node_to_search = list(map(add, current_node, [x_delta, y_delta]))
                    next_node_to_search = [current_node[0] + x_delta, current_node[1] + y_delta]

                    if next_node_to_search[0] == goal_x and next_node_to_search[1] == goal_y:
                        pprint(next_node_to_search)
                        print("found")
                        done = True

                    if next_node_to_search not in queue:
                        if next_node_to_search[0] >= 0 and next_node_to_search[0] < 360 and next_node_to_search[1] >= 0 and next_node_to_search[1] < 360:
                            if pathfinding_map[next_node_to_search[0], next_node_to_search[1]][0] == 255 and \
                                pathfinding_map[next_node_to_search[0], next_node_to_search[1]][1] == 255 and \
                                    pathfinding_map[next_node_to_search[0], next_node_to_search[1]][2] == 255:
                                queue.append(next_node_to_search)
                                pathfinding_map[next_node_to_search[0], next_node_to_search[1]] = [count % 256, count % 256, count % 256]

        if count % 100 == 0:
            # Update the image with the modified array
            pygame.surfarray.blit_array(image, pathfinding_map)

            # Display the updated image on the surface
            display_surface.blit(image, (0, 0))
            pygame.display.update()

            # Control the frame rate
            clock.tick(60)

    # show result
    done = False
    count = 0
    while not done:
        count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        # Update the image with the modified array
        pygame.surfarray.blit_array(image, pathfinding_map)

        # Display the updated image on the surface
        display_surface.blit(image, (0, 0))
        pygame.display.update()

        # Control the frame rate
        clock.tick(60)

    return pathfinding_map


if __name__ == "__main__":
    global obstacle_map, pathfinding_map

    # Initialize pygame
    pygame.init()

    # Load the PNG image
    image = pygame.image.load("obstacle_map.png")
    start_x = 100
    start_y = 300

    goal_x = 300
    goal_y = 20

    # Create a display surface
    display_width = image.get_width()
    display_height = image.get_height()
    display_surface = pygame.display.set_mode((display_width, display_height))

    # Convert the image to RGB mode (if necessary)
    image = image.convert()

    # Create a numpy array from the image
    obstacle_map = pygame.surfarray.array3d(image)

    pathfinding_map = deepcopy(obstacle_map)

    pathfinding(start_x, start_y, goal_x, goal_y)

    # Quit pygame
    pygame.quit()
