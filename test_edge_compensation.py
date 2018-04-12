import pickle

from map.RoadNetwork import get_coords_on_connected_edges
from processor.Preprocessor import map_preprocessor
from util.MapPainter import draw_lines_on_map
print('loading')
f_edge = open('data/edges_from_road_network', 'rb')
edges = pickle.load(f_edge)

print('processing')
map_preprocessor.points_supplement_on_edges(edges, 50)
edge_part = edges[1502:1568]
print('collecting')
coords_seq = []
for edge in edge_part:
    edge_coord = []
    get_coords_on_connected_edges([edge,], edge_coord)
    coords_seq.append(edge_coord)
print('drawing')
draw_lines_on_map(coords_seq, 'Edges', center_point=coords_seq[0][0])
