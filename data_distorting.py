# 对轨迹点下采样
import csv

from trajectory.GPSTrajectory import read_trajectory_from_csv
from util.ChaosMaker import down_sample, add_gaussian_noise
from util.MapPainter import draw_lines_on_map, draw_lines_on_map_gps_version


def write_processed_gps_data_to_csv(gps_points, filename):
    # 加上 newline 参数后，使得写入的csv文件中行与行之间不会出现一行额外的空白行
    with open(filename, "w",newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name
        writer.writerow(["time", "latitude", "longitude"])
        # 写入多行用writerows
        rows = []
        for gps in gps_points:
            rows.append([gps.timestamp.strftime('%H:%M:%S'), gps.coordinate.latitude, gps.coordinate.longitude])
        writer.writerows(rows)


raw_traj = read_trajectory_from_csv('data/gps_data.csv', '%H:%M:%S')
gps_points = raw_traj.gps_points

coords_sampled_at_10s = down_sample(gps_points, 10)
# add_gaussian_noise(coords_sampled_at_10s)
write_processed_gps_data_to_csv(coords_sampled_at_10s, 'data/test_gps_data/down_sampled/s_10.csv')
draw_lines_on_map_gps_version([gps_points, coords_sampled_at_10s],['original','10'],'10',gps_points[0].coordinate)

coords_sampled_at_20s = down_sample(gps_points, 20)
# add_gaussian_noise(coords_sampled_at_20s)
write_processed_gps_data_to_csv(coords_sampled_at_20s, 'data/test_gps_data/down_sampled/s_20.csv')
draw_lines_on_map_gps_version([gps_points, coords_sampled_at_20s],['original','20'],'20',gps_points[0].coordinate)

coords_sampled_at_30s = down_sample(gps_points, 30)
# add_gaussian_noise(coords_sampled_at_30s)
write_processed_gps_data_to_csv(coords_sampled_at_30s, 'data/test_gps_data/down_sampled/s_30.csv')
draw_lines_on_map_gps_version([gps_points, coords_sampled_at_30s],['original','30'],'30',gps_points[0].coordinate)

coords_sampled_at_60s = down_sample(gps_points, 60)
# add_gaussian_noise(coords_sampled_at_60s)
write_processed_gps_data_to_csv(coords_sampled_at_60s, 'data/test_gps_data/down_sampled/s_60.csv')
draw_lines_on_map_gps_version([gps_points, coords_sampled_at_60s],['original','60'],'60',gps_points[0].coordinate)

coords_sampled_at_120s = down_sample(gps_points, 120)
# add_gaussian_noise(coords_sampled_at_120s)
write_processed_gps_data_to_csv(coords_sampled_at_120s, 'data/test_gps_data/down_sampled/s_120.csv')
draw_lines_on_map_gps_version([gps_points, coords_sampled_at_120s],['original','120'],'120',gps_points[0].coordinate)

coords_sampled_at_180s = down_sample(gps_points, 180)
# add_gaussian_noise(coords_sampled_at_180s)
write_processed_gps_data_to_csv(coords_sampled_at_180s, 'data/test_gps_data/down_sampled/s_180.csv')
draw_lines_on_map_gps_version([gps_points, coords_sampled_at_180s],['original','180'],'180',gps_points[0].coordinate)

coords_sampled_at_240s = down_sample(gps_points, 240)
# add_gaussian_noise(coords_sampled_at_240s)
write_processed_gps_data_to_csv(coords_sampled_at_240s, 'data/test_gps_data/down_sampled/s_240.csv')
draw_lines_on_map_gps_version([gps_points, coords_sampled_at_240s],['original','240'],'240',gps_points[0].coordinate)

coords_sampled_at_300s = down_sample(gps_points, 300)
# add_gaussian_noise(coords_sampled_at_300s)
write_processed_gps_data_to_csv(coords_sampled_at_300s, 'data/test_gps_data/down_sampled/s_300.csv')
draw_lines_on_map_gps_version([gps_points, coords_sampled_at_300s],['original','300'],'300',gps_points[0].coordinate)

coords_sampled_at_360s = down_sample(gps_points, 360)
# add_gaussian_noise(coords_sampled_at_360s)
write_processed_gps_data_to_csv(coords_sampled_at_360s, 'data/test_gps_data/down_sampled/s_360.csv')
draw_lines_on_map_gps_version([gps_points, coords_sampled_at_360s],['original','360'],'360',gps_points[0].coordinate)



