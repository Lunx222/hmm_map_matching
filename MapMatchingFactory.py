from processor.Preprocessor import traj_preprocessor
from processor.QueryForCandidates import  \
    find_candidate_edges_of_a_trajectory_accelerated
from processor.WorkSpaceDividor import matched_set_and_traj_segmentation, heavy_point_segmentation
from hmm.HMMProcess import Hmm
from util.MapPainter import draw_lines_on_map

def preprocessing(raw_trajs, max_distance,  max_time_interval, time_format):
    # 按照两点间时间间隔的大小分割轨迹
    print('Segmenting by time interval...' + str(max_time_interval) + 's')
    segmented_trajs = traj_preprocessor.segmentation_by_time_interval(raw_trajs, max_time_interval)
    # 在一定距离之内只保留一个坐标点
    print('Down sampling...' + str(max_distance) + 'm')
    sampled_trajs = traj_preprocessor.down_sample_by_dis_interval(segmented_trajs, max_distance, time_format)
    print('Sampled trajectory '+ str(len(sampled_trajs)))
    for traj in sampled_trajs:
        print(str(len(traj.gps_points)),end=' ')
    print()
    # # kalman filter 平滑轨迹
    # print('Kalman filtering...')
    # filtered_trajs = traj_preprocessor.filtering(sampled_trajs,time_format)
    return sampled_trajs


def candidate_searching(trajs, fast_query_map, offset_lon, offset_lat, delta, k_nearest, max_offset_threshold, step):
    matched_points_set = []
    cleaned_traj_set = []
    for traj in trajs:
        matched_points, cleaned_traj = find_candidate_edges_of_a_trajectory_accelerated(traj, fast_query_map, offset_lon, offset_lat, delta, k_nearest, max_offset_threshold, step)
        matched_points_set.append(matched_points)
        cleaned_traj_set.append(cleaned_traj)
    return matched_points_set, cleaned_traj_set


def work_space_segmentation_for_one_traj(matched_points, cleaned_traj, maximum_size):
    # sub_matched_sets, sub_trajs_corresponding_to_sub_matched_sets = matched_set_and_traj_segmentation(matched_points, cleaned_traj, maximum_size)
    print("HPS segmenting...")
    sub_matched_sets, sub_trajs_corresponding_to_sub_matched_sets = heavy_point_segmentation(matched_points, cleaned_traj, maximum_size)
    return sub_matched_sets, sub_trajs_corresponding_to_sub_matched_sets


def hmm_opt_path_calculating_for_one_traj(matched_points, a_star_map, ob_traj, real_edges):
    print('HMM building...')
    hmm_processor = Hmm(matched_points, a_star_map, real_edges)
    print('Optimal searching...')
    score, opt_cand_path, traversed_edges_id = hmm_processor.find_optimal_path()
    final_opt_path = []
    matched_coords = []
    matched_edges = []
    for cand in opt_cand_path:
        final_opt_path.append(cand)
        matched_coords.append(cand.projected_coordinate)
        matched_edges.append(cand.edge.edge_id)
    raw_coords = []
    for gps_p in ob_traj.gps_points:
        raw_coords.append(gps_p.coordinate)
    # draw_lines_on_map([matched_coords, raw_coords], ['matched', 'raw'], 'Comparison', center_point=matched_gps_traj[0])
    return matched_coords, raw_coords, traversed_edges_id, matched_edges