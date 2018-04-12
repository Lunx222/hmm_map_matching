import pickle

from map.RoadNetwork import find_edge_by_id, get_coords_on_connected_edges
from trajectory.GPSTrajectory import get_bounding_box, read_trajectory_from_csv
from util.MapPainter import draw_lines_on_map

TIME_FORMAT = '%H:%M:%S'
traj = read_trajectory_from_csv('data/traj_1_200.csv', TIME_FORMAT)

bbox = get_bounding_box(traj, 0.001)
b_lines = bbox.get_lines()
coords = []
for gps in traj.gps_points:
    coords.append(gps.coordinate)

f_edge = open('data/expanded_edges', 'rb')
edges = pickle.load(f_edge)

passed_es = [find_edge_by_id(edges, '884147800801'),
             find_edge_by_id(edges, '884147800802'),
             find_edge_by_id(edges, '884147800421'),
             find_edge_by_id(edges, '884147800422'),
             find_edge_by_id(edges, '884147800423'),
             find_edge_by_id(edges, '884147800805'),
             find_edge_by_id(edges, '884147800804'),
             find_edge_by_id(edges, '884147800806')]
edge_coords = []
get_coords_on_connected_edges(passed_es, edge_coords)

draw_lines_on_map([coords, edge_coords, b_lines[0], b_lines[1], b_lines[2], b_lines[3],],'Candidate Searching', coords[0])