import xml.etree.ElementTree as ET
from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()

# https://www.openstreetmap.org/export#map=17/16.74881/-62.22840
osm_file = "montserrat_salem_old_town.osm"
tree = ET.parse(osm_file)
root = tree.getroot()
pprint(root.attrib)

pos = {}

print("Iterating through XML and adding nodes and edges to networkx graph")
node_count = 0
way_count = 0
for child in root:
    match child.tag:
        case "node":
            node_count += 1
            node = child.attrib
            node_id = node["id"]
            # pprint(node)
            print(f"Adding node {node_id}")
            G.add_node(node_id)

            # cooridnated need to be cast to float, otherwise the following error occurs:
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
                        this_node_id = child_of_way.attrib["ref"]

                        if previous_node_id != -1:
                            if previous_node_id in G.nodes and this_node_id in G.nodes:
                                print(f"Adding edge {previous_node_id} - {this_node_id}")
                                G.add_edge(previous_node_id, this_node_id)
                        previous_node_id = this_node_id


print(f"{node_count=}")
print(f"{way_count=}")

# https://stackoverflow.com/a/48820766/2278742
G.remove_nodes_from(list(nx.isolates(G)))
pprint(G.nodes)
pprint(G.edges)
pprint(pos)

print("Drawing graph")
nx.draw(G, pos=pos)
plt.show()
