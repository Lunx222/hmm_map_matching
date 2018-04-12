import pickle

import _thread
import threading

from map.RoadNetwork import get_coords_on_connected_edges, find_edge_by_id, draw_edges_on_map, is_same_road_seg
from processor.MatchedSegMerger import merge_sub_path_v1, merge_sub_path_v2
from trajectory.GPSTrajectory import read_trajectory_from_csv
from MapMatchingFactory import *
from processor.GroundTruthComparor import *
import time

TIME_FORMAT = '%H:%M:%S'


class MultiLoader():
    def __load_edges(self):
        f_edge = open('data/expanded_edges', 'rb')
        self.edges = pickle.load(f_edge)
        print('Total ' + str(len(self.edges)) + ' edges.')

    def __load_a_star_map(self):
        f_map = open('data/A_star_map', 'rb')
        print('Loading A* map...')
        self.a_star_road_map = pickle.load(f_map)

    def __load_fast_map(self):
        print('Loading fast query map...')
        f_fast_map = open('data/fast_query_map_v4', 'rb')
        self.fast_query_map = pickle.load(f_fast_map)

    def __load_raw_data(self):
        self.raw_traj = read_trajectory_from_csv('data/gps_data.csv', TIME_FORMAT, 0, 300)
        self.raw_traj.calculate_features()
        print('Total ' + str(len(self.raw_traj.gps_points)) + ' original gps observations.')

    def load_data(self):
        t_set = []
        t_set.append(threading.Thread(target=self.__load_edges, args=()))
        t_set.append(threading.Thread(target=self.__load_a_star_map, args=()))
        t_set.append(threading.Thread(target=self.__load_fast_map, args=()))
        t_set.append(threading.Thread(target=self.__load_raw_data, args=()))
        for t in t_set:
            t.start()
        for t in t_set:
            if t.isAlive:
                t.join()
        return self.edges, self.a_star_road_map, self.fast_query_map, self.raw_traj



# f_edge = open('data/expanded_edges', 'rb')
# edges = pickle.load(f_edge)
# print('Total '+str(len(edges))+' edges.')
# f_map = open('data/A_star_map', 'rb')
# print('Loading A* map...')
# a_star_road_map = pickle.load(f_map)
# print('Loading fast query map...')
# f_fast_map = open('data/fast_query_map', 'rb')
# fast_query_map = pickle.load(f_fast_map)
# raw_traj = read_trajectory_from_csv('data/gps_data.csv', TIME_FORMAT)
# raw_traj.calculate_features()

loader = MultiLoader()

edges, a_star_road_map, fast_query_map, raw_traj = loader.load_data()


print('Total '+str(len(raw_traj.gps_points))+' original gps observations.')
print('Pre-processing...')
start_time = time.clock()
preprocessed_trajs = preprocessing([raw_traj,], max_distance=20, max_time_interval=370, time_format=TIME_FORMAT)
print('Cleaned and segmented trajectory '+str(len(preprocessed_trajs)))
print('Candidate searching...')
matched_points_set, cleaned_traj_set = candidate_searching(preprocessed_trajs, fast_query_map,
                                                           offset_lon=0.0003, offset_lat=0.0003,
                                                           delta=0.001,
                                                           k_nearest=3,
                                                           max_offset_threshold=0.001,
                                                           step=0.0007)

head_and_tail_cand_set = []
raw_coords_list = []
matched_edges_list = []
for i in range(len(matched_points_set)):
    seg_path = []
    one_traj_raw_coords = []
    one_traj_matched_edges = []
    sub_matched_sets, sub_trajs_corresponding_to_sub_matched_sets = work_space_segmentation_for_one_traj(matched_points_set[i], cleaned_traj_set[i], 100)
    for j in range(len(sub_matched_sets)):
        head_and_tail_cand_set.append([sub_matched_sets[j][0], sub_matched_sets[j][-1]])
        print(str(j+1) + '/' + str(len(sub_matched_sets)) + '...' + str(len(sub_matched_sets[j])))
        matched_coords, raw_coords, traversed_edges_id, can_edge_id_set = hmm_opt_path_calculating_for_one_traj(sub_matched_sets[j], a_star_road_map, sub_trajs_corresponding_to_sub_matched_sets[j], edges)
        seg_path.append(traversed_edges_id)
        for k in range(len(raw_coords)):
            one_traj_raw_coords.append(raw_coords[k])
        for j in range(len(traversed_edges_id)):
            one_traj_matched_edges.append(traversed_edges_id[j])
    # one_traj_matched_edges = merge_sub_path_v2(head_and_tail_cand_set,seg_path, edges, a_star_road_map)
    raw_coords_list.append(one_traj_raw_coords)
    matched_edges_list.append(one_traj_matched_edges)
    # 不分割
    # matched_coords, raw_coords, traversed_edges_id, can_edge_id_set = hmm_opt_path_calculating_for_one_traj(matched_points_set[i], a_star_road_map, cleaned_traj_set[i],edges)
    # result_trajs.append(matched_coords)
    # raw_coords_list.append(raw_coords)
    # matched_edges_list.append(traversed_edges_id)
    print('HMM progress: ' + str(i+1) + '/' + str(len(matched_points_set)))
    # draw_lines_on_map([one_traj_result, one_traj_raw_coords], ['matched', 'raw'], 'Comparison', center_point=one_traj_raw_coords[0])

end_time = time.clock()

cleaned_traversed_edges_id = []
for one_traj_matched_edges in matched_edges_list:
    one_traj_cleaned = [one_traj_matched_edges[0],]
    for i in range(len(one_traj_matched_edges) - 1):
        if is_same_road_seg(one_traj_matched_edges[i], one_traj_matched_edges[i + 1]):
            continue
        one_traj_cleaned.append(one_traj_matched_edges[i+1])
    cleaned_traversed_edges_id.append(one_traj_cleaned)
# 去掉相邻的重复的边id

# cleaned_can_edge_id = []
#
# for can_traj in can_edges_id:
#     if (cleaned_can_edge_id[-1][-1] != can_traj[0]) | (len(cleaned_can_edge_id) == 0):
#         cleaned_can_edge_id.append(can_traj[0])
#     for k in range(len(can_traj)-1):
#         if can_traj[k] == can_traj[k+1]:
#             continue
#         else:
#             cleaned_can_edge_id.append(can_traj[k+1])

cleaned_passed_edges = []
for id in cleaned_traversed_edges_id:
    cleaned_passed_edges.append(find_edge_by_id(edges, id))

# cleaned_can_edges = []
# for id in cleaned_can_edge_id:
#     cleaned_can_edges.append(find_edge_by_id(edges, id))

coords_on_edges_list = []
for one_cleaned in cleaned_traversed_edges_id:
    one_passed_e = []
    one_coords = []
    for id in one_cleaned:
        one_passed_e.append(find_edge_by_id(edges, id))
    get_coords_on_connected_edges(one_passed_e, one_coords)
    coords_on_edges_list.append(one_coords)


for m in range(len(raw_coords_list)):
    draw_lines_on_map([raw_coords_list[m], coords_on_edges_list[m]], 'Comparison', center_point=raw_coords_list[m][0])

# draw_edges_on_map(cleaned_passed_edges)
# print(cleaned_total_traversed_edges_id)
# print(cleaned_can_edge_id)

#   draw_lines_on_map(result_trajs,[lambda x: x in range(len(result_trajs))], 'result trajectories', center_point=result_trajs[0][0])

cleaned_total_eid = [cleaned_traversed_edges_id[0][0]]
for edge_ids in cleaned_traversed_edges_id:
    if edge_ids[0] != cleaned_total_eid[-1]:
        cleaned_total_eid.append(edge_ids[0])
    for i in range(len(edge_ids)-1):
        # if is_same_road_seg(edge_ids[i], edge_ids[i+1]):
        #     continue
        if edge_ids[i] == edge_ids[i+1]:
            continue
        cleaned_total_eid.append(edge_ids[i+1])

print(cleaned_total_eid)

actual_edges_id = read_ground_truth('data/ground_truth_route.csv')
matched_rate = get_accuracy_rate_v2(actual_edges_id, cleaned_total_eid)
print(matched_rate)
print('Execute time:' + str(end_time-start_time) +' s')