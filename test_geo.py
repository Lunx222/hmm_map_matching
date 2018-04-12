import util.GeoHelper as geo

dist = geo.get_distance_between_coordinates(geo.Coordinate('-122.342188954353', '47.661389708519'), geo.Coordinate('-122.341580092907', '47.661389708519'))
print(dist)