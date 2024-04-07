"""
Path finding algorithm

Roughly based on https://github.com/Alexander-Wilms/Robotics-simulation/tree/master/Termin%206%20-%20Breitensuche
"""

import math
from pprint import pprint
from random import shuffle

import numpy as np
import pandas as pd
import pygame

queue: list[list[int]] = []


def draw():
    global clock, cost_map, backtracking_map, start_x, start_y, goal_x, goal_y
    max_val = np.amax(cost_map)
    range_mapped_cost_map = cost_map * 128 / max_val + 128
    range_mapped_cost_map = np.where(cost_map == 0, cost_map, range_mapped_cost_map)
    rgb_cost_map = np.stack((range_mapped_cost_map,) * 3, axis=-1).astype(np.uint8)

    additional_arrays = np.zeros_like(backtracking_map)
    rgb_backtracking_map = np.stack([backtracking_map] + [additional_arrays] * 2, axis=-1)

    cost_and_backtracking_map = np.where(
        np.any(rgb_backtracking_map != [0, 0, 0], axis=-1, keepdims=True),
        rgb_backtracking_map,
        rgb_cost_map,
    )

    # start and goal
    cost_and_backtracking_map[start_x, start_y] = [0, 255, 0]
    cost_and_backtracking_map[goal_x, goal_y] = [0, 0, 255]

    # Display the updated image on the surface
    pygame.surfarray.blit_array(image, cost_and_backtracking_map)
    image_scaled = pygame.transform.scale(image, (display_width, display_height))
    display_surface.blit(image_scaled, (0, 0))

    pygame.display.update()

    # Control the frame rate
    clock.tick(60)


cost_checked_nodes = []


def find_goal():
    global queue, obstacle_map, cost_map, binary_obstacle_map, width, height, display_width, display_height, image, clock, start_x, start_y, goal_x, goal_y, neighborhood_delta

    print(f"find_goal({start_x}, {start_y}, {goal_x}, {goal_y})")

    next_node_to_search = [start_x, start_y]
    queue.append(next_node_to_search)
    cost_checked_nodes.append(next_node_to_search)
    goal_found = False
    quit_event = False
    count = 0
    while not (goal_found or quit_event):
        count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_event = True

        # Breadth First Search: pop(0)
        # Depth First Search: pop(-1)
        current_node = queue.pop(0)

        if current_node == [goal_x, goal_y]:
            pprint(current_node)
            print("found goal")
            goal_found = True
            break

        for delta in neighborhood_delta:
            if current_node[0] + delta[0] >= 0 and current_node[0] + delta[0] < width and current_node[1] + delta[1] >= 0 and current_node[1] + delta[1] < height:
                next_node_to_search = [
                    current_node[0] + delta[0],
                    current_node[1] + delta[1],
                ]

                if next_node_to_search not in queue:
                    if binary_obstacle_map[next_node_to_search[0], next_node_to_search[1]]:
                        if next_node_to_search not in cost_checked_nodes:
                            cost_checked_nodes.append(next_node_to_search)
                            queue.append(next_node_to_search)
                            cost_map[next_node_to_search[0], next_node_to_search[1]] = cost_map[current_node[0], current_node[1]] + 1 + abs(delta[0] * delta[1]) * (math.sqrt(2) - 1)
        if count % 100 == 0:
            # to speed up rendering, draw one frame every 100 nodes
            draw()

    export_cost_map_as_xlsx()


def export_cost_map_as_xlsx():
    global cost_map

    df = pd.DataFrame(cost_map)
    df = df.transpose()

    writer = pd.ExcelWriter("cost_map.xlsx", engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Cost map")
    worksheet = writer.sheets["Cost map"]
    (max_row, max_col) = df.shape
    # https://xlsxwriter.readthedocs.io/working_with_conditional_formats.html
    worksheet.conditional_format(1, 1, max_row, max_col, {"type": "2_color_scale", "min_color": "#ffffff", "max_color": "#63BE7B"})
    writer.close()


backtrack_queue: list[list[int]] = []
backtrack_already_checked: list[list[int]] = []


def backtrack():
    global queue, backtrack_queue, obstacle_map, cost_map, binary_obstacle_map, width, height, display_width, display_height, image, clock, backtracking_map, start_x, start_y, goal_x, goal_y, neighborhood_delta

    print(f"backtrack({start_x}, {start_y}, {goal_x}, {goal_y})")

    start_found = False
    quit_event = False
    backtrack_queue.append([goal_x, goal_y])

    while not (start_found or quit_event):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_event = True

        current_node = backtrack_queue.pop(0)
        print("checking neighbors of ", end="")
        pprint(current_node)
        print(f"cost at current node: {cost_map[current_node[0], current_node[1]]}")
        # required for first node
        backtracking_map[current_node[0], current_node[1]] = 255

        best_cost_so_far = math.inf
        best_node_so_far = [-1, -1]
        found_next_node = False
        for delta in neighborhood_delta:
            if not start_found:
                next_node_to_search = [
                    current_node[0] + delta[0],
                    current_node[1] + delta[1],
                ]

                if next_node_to_search not in backtrack_already_checked:
                    if next_node_to_search in cost_checked_nodes:
                        backtrack_already_checked.append(next_node_to_search)
                        if next_node_to_search[0] >= 0 and next_node_to_search[0] < width and next_node_to_search[1] >= 0 and next_node_to_search[1] < height:
                            if binary_obstacle_map[next_node_to_search[0], next_node_to_search[1]]:
                                cost_of_this_neighbor = cost_map[next_node_to_search[0], next_node_to_search[1]]
                                print(f"checking neighbor. cost: {cost_of_this_neighbor}")
                                if cost_of_this_neighbor < best_cost_so_far:
                                    best_cost_so_far = cost_map[next_node_to_search[0], next_node_to_search[1]]
                                    best_node_so_far = next_node_to_search
                                    found_next_node = True

        if found_next_node:
            # check all neighbors of the start node before concluding search, so don't take a suboptimal path at the last step
            if best_node_so_far == [start_x, start_y]:
                start_found = True
                found_next_node = True
                print("found start")
                break

            backtrack_queue.append(best_node_so_far)
            # required for last node
            backtracking_map[best_node_so_far[0], best_node_so_far[1]] = 255

        draw()


def show_result():
    quit_event = False
    while not quit_event:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_event = True


def pathfinding():
    global queue, obstacle_map, cost_map, binary_obstacle_map, width, height, display_width, display_height, image, clock, start_x, start_y, goal_x, goal_y

    clock = pygame.time.Clock()

    find_goal()

    backtrack()

    show_result()

    return cost_map


if __name__ == "__main__":
    global obstacle_map, pathfinding_map, width, height, display_width, display_height, image, neighborhood_delta

    pygame.init()

    # Use downscaled map, since Python is not fast enough for the 360 px version
    image = pygame.image.load("obstacle_map_100px.png")
    width = image.get_width()
    height = image.get_height()

    start_x = int(100 / 3.6)
    start_y = int(300 / 3.6)

    goal_x = int(300 / 3.6)
    goal_y = int(20 / 3.6)

    # Create a display surface
    display_width = image.get_width() * 4
    display_height = image.get_height() * 4
    display_surface = pygame.display.set_mode((display_width, display_height), 0, 64)

    # Convert the image to RGB mode
    image = image.convert()

    # Create a numpy array from the image
    obstacle_map = pygame.surfarray.array3d(image)

    binary_obstacle_map = np.ndarray((360, 360), dtype=bool)

    # cost matrix must be of type float, otherwise the cost of diagonal movements, i.e. sqrt(2) can't be accurately represented
    cost_map = np.ndarray((width, height), dtype=float)
    backtracking_map = np.ndarray((width, height), dtype=int)

    for x in range(width):
        for y in range(height):
            binary_obstacle_map[x, y] = obstacle_map[x, y, 0] == 255 and obstacle_map[x, y, 1] == 255 and obstacle_map[x, y, 2] == 255
            cost_map[x, y] = 0
            backtracking_map[x, y] = 0

    n_neighborhood = 8
    neighborhood_delta = []
    match n_neighborhood:
        case 4:
            for delta_x in [-1, 0, 1]:
                for delta_y in [-1, 0, 1]:
                    if not (delta_x == 0 and delta_y == 0):
                        if abs(delta_x) != abs(delta_y):
                            neighborhood_delta.append([delta_x, delta_y])
        case 8:
            for delta_x in [-1, 0, 1]:
                for delta_y in [-1, 0, 1]:
                    if not (delta_x == 0 and delta_y == 0):
                        neighborhood_delta.append([delta_x, delta_y])

    shuffle(neighborhood_delta)
    pprint(neighborhood_delta)

    pathfinding()

    # Quit pygame
    pygame.quit()
