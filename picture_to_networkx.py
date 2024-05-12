import math
import os
from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx


def ppm_to_nx_graph(map_file: os.PathLike) -> tuple[nx.Graph, dict]:
    with open(map_file, "r", encoding="utf8") as f:
        data = f.read().split("\n")
        pprint(data)

    width = int(data[2].split()[0])
    height = int(data[2].split()[1])
    pixels = data[4]

    G = nx.Graph()
    pos = {}

    def get_color(x: int, y: int, width: int) -> tuple[int, int, int]:
        index = (x + y * width) * 3

        r = ord(pixels[index])
        g = ord(pixels[index + 1])
        b = ord(pixels[index + 2])

        return r, g, b

    # add nodes
    for y in range(height):
        for x in range(width):
            r, g, b = get_color(x, y, width)

            print(chr(min(r, g, b)).replace("ÿ", " "), end="")

            node = f"{x},{y}"
            if r == g == b == 255:
                G.add_node(node)
                pos[node] = (x, height - y)

        print()

    # add edges
    for y in range(height):
        for x in range(width):
            node = f"{x},{y}"
            for delta_x in [-1, 0, 1]:
                for delta_y in [-1, 0, 1]:
                    if not (delta_x == 0 and delta_y == 0):
                        neighbor = f"{x+delta_x},{y+delta_y}"
                        if G.has_node(node) and G.has_node(neighbor):
                            G.add_edge(node, neighbor)

    return G, pos


def pathfinding(G: nx.Graph, pos: dict[str, list[int]]) -> None:
    start_x = int(100 / 3.6 / 2)
    start_y = int(300 / 3.6 / 2)

    goal_x = int(300 / 3.6 / 2)
    goal_y = int(20 / 3.6 / 2)

    source = f"{start_x},{start_y}"
    target = f"{goal_x},{goal_y}"

    print("Computing distances between nodes")
    distances = {}
    for u, pos_u in pos.items():
        for v, pos_v in pos.items():
            if u != v:
                if G.has_edge(u, v):
                    distances[(u, v)] = math.sqrt((pos_u[0] - pos_v[0]) ** 2 + (pos_u[1] - pos_v[1]) ** 2)

    # Add weights to edges based on distances
    G.add_weighted_edges_from([(u, v, distance) for (u, v), distance in distances.items()])

    path_dijkstra = nx.dijkstra_path(G, source, target)

    def heuristic(u, v):
        [x1, y1] = pos[u]
        [x2, y2] = pos[v]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    path_a_star = nx.astar_path(G, source, target, heuristic=heuristic)

    _, axes = plt.subplots()
    axes.set_aspect(1)

    nx.draw_networkx_edges(G, pos, width=0.5, edge_color="#cccccc")
    nx.draw_networkx_edges(G, pos, list(nx.utils.pairwise(path_dijkstra)), width=2, edge_color="#ff0000")
    nx.draw_networkx_edges(G, pos, list(nx.utils.pairwise(path_a_star)), width=2, edge_color="#00ff00")

    plt.show()


if __name__ == "__main__":
    G, pos = ppm_to_nx_graph("obstacle_map_50px.ppm")

    pathfinding(G, pos)
