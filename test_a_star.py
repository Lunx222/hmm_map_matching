import pickle

from map.RoadNetwork import find_edge_by_id, get_coords_on_connected_edges
from util.AStarPathSearching import path_finding
from util.MapPainter import draw_lines_on_map

f_map = open('data/A_star_map','rb')
a_map = pickle.load(f_map)
f_edges = open('data/expanded_edges','rb')
edges = pickle.load(f_edges)

start_node_id = '884147800794'
dest_node_id = '884147800998'

result = path_finding(start_node_id, dest_node_id, a_map, edges,1000)
if result == None:
    print('No path is found')
else:
    coords = []
    get_coords_on_connected_edges(result['path_edges'], coords)
    print(result['distance'])
    draw_lines_on_map([coords,], 'Test', coords[0])
