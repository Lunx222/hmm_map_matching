import pickle
import map.RoadNetwork as rd_net

from processor.Preprocessor import map_preprocessor,traj_preprocessor
import util.AStarPathSearching as AStar

# edges = rd_net.get_edges_from_file('data/road_network.csv')
#
# f_edge = open('data/edges_from_road_network', 'wb')
# pickle.dump(edges, f_edge)
from trajectory.GPSTrajectory import read_trajectory_from_csv

# f_edge = open('data/edges_from_road_network', 'rb')
# edges = pickle.load(f_edge)
# map_preprocessor.points_supplement_on_edges(edges, 25)
# #
# f_expanded_edges = open('data/expanded_edges_25', 'wb')
# pickle.dump(edges, f_expanded_edges)
#
# f_edge = open('data/edges_from_road_network', 'rb')
# edges = pickle.load(f_edge)
# #
# f_nodes = open('data/nodes_from_road_network', 'rb')
# nodes = pickle.load(f_nodes)

# fast_query_map = map_preprocessor.generate_fast_query_map_v3(edges)
# #
# f_fast_map = open('data/fast_query_map', 'wb')
# pickle.dump(fast_query_map, f_fast_map)

# nodes = rd_net.extract_nodes_from_edges(edges)
# f_node = open('data/nodes_from_road_network', 'wb')
# pickle.dump(nodes, f_node)
#
# road_map = AStar.get_road_map(edges, nodes)
# f_a_star_map = open('data/A_star_map', 'wb')
# pickle.dump(road_map, f_a_star_map)

# for e in edges:
#     e.regain_attrs()
#
# f_expanded_edges = open('data/expanded_edges_man_v', 'wb')
# pickle.dump(edges, f_expanded_edges)