import math
from copy import deepcopy
from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import defusedxml.ElementTree as ET
from defusedxml.ElementTree import Element


def osm_xml_to_nx_graph(root: Element) -> tuple[nx.Graph, dict]:
    pos = {}

    print("Iterating through XML and adding nodes and edges to networkx graph")
    G = nx.Graph()
    node_count = 0
    way_count = 0
    for child in root:
        match child.tag:
            case "node":
                node_count += 1
                node = child.attrib
                node_id = int(node["id"])
                print(f"Adding node {node_id}")
                G.add_node(node_id)

                # coordinates need to be converted to float, otherwise the following error occurs:
                # numpy.core._exceptions._UFuncNoLoopError: ufunc 'minimum' did not contain a loop with signature matching types (dtype('<U11'), dtype('<U11')) -> None
                pos[node_id] = [float(node["lon"]), float(node["lat"])]

            case "way":
                way_count += 1
                way = child.attrib

                highway = False
                for child_of_way in child:
                    if child_of_way.tag == "tag":
                        tags_dict = child_of_way.attrib
                        if tags_dict["k"] == "highway":
                            highway = True
                            pprint(way)

                if highway:
                    previous_node_id = -1
                    for child_of_way in child:
                        if child_of_way.tag == "nd":
                            # pprint(child_of_way)
                            this_node_id = int(child_of_way.attrib["ref"])

                            if previous_node_id != -1:
                                if previous_node_id in G.nodes and this_node_id in G.nodes:
                                    print(f"Adding edge {previous_node_id} - {this_node_id}")
                                    G.add_edge(previous_node_id, this_node_id)
                            previous_node_id = this_node_id

    print(f"{node_count=}")
    print(f"{way_count=}")

    # https://stackoverflow.com/a/48820766/2278742
    G.remove_nodes_from(list(nx.isolates(G)))
    pprint(pos)
    pprint(G.edges)
    pprint(G.nodes)

    return G, pos


def pathfinding(G: nx.Graph, pos: dict) -> None:
    print("Computing distances between nodes")
    distances = {}
    for u, pos_u in pos.items():
        for v, pos_v in pos.items():
            if u != v:
                if G.has_edge(u, v):
                    distances[(u, v)] = math.sqrt((pos_u[0] - pos_v[0]) ** 2 + (pos_u[1] - pos_v[1]) ** 2)

    # Add weighted edges based on distances
    G_weighted = deepcopy(G)
    G_weighted.add_weighted_edges_from([(u, v, distance) for (u, v), distance in distances.items()])

    # https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.astar.astar_path.html
    def heuristic(u, v):
        [x1, y1] = pos[u]
        [x2, y2] = pos[v]
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    print("Executing A*")
    source = 358027082
    target = 8043782172
    path = nx.astar_path(G, source, target)
    path_weighted_search = nx.astar_path(G_weighted, source, target, heuristic=heuristic)

    print("Drawing graph")
    nx.draw(G, pos=pos, node_size=2, node_color="#000000")

    # nx.draw_networkx_nodes(path, pos=pos, node_size=20, node_color="#ff0000")
    nx.draw_networkx_edges(G, pos, list(nx.utils.pairwise(path)), width=2, edge_color="#ff0000")

    # nx.draw_networkx_nodes(path_weighted_search, pos=pos, node_size=20, node_color="#0000ff")
    nx.draw_networkx_edges(
        G,
        pos,
        list(nx.utils.pairwise(path_weighted_search)),
        width=2,
        edge_color="#0000ff",
    )
    plt.show()


# https://www.openstreetmap.org/export#map=17/16.74881/-62.22840
osm_file = "montserrat_salem_old_town.osm"
tree = ET.parse(osm_file)
root = tree.getroot()

G, pos = osm_xml_to_nx_graph(root)

pathfinding(G, pos)

# display copyright and license
pprint(root.attrib)
