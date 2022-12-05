# app/serialization/stats_geometry_group_by_cp.py
import json
from shapely.geometry import LineString, Point
import numpy as np


class StatsGeometryGroupByCp:
    def __int__(self, postal_code, geo_json, stats_list):
        self.postal_code = postal_code
        self.geom = geo_json
        self.stats_list = stats_list

    @staticmethod
    def get_stats_geometry_group_by_cp(stats_geometry_row):
        stats_group_by_cp = {}
        print(f"stats_geometry: {stats_geometry_row}")
        for stats in stats_geometry_row:
            print(f"stats_geometry: {stats.postal_code}")
            if stats.postal_code not in stats_group_by_cp.keys():
                print(f"stats_geometry: {stats.geo_json}")
                print(f"coordinates: {stats.geo_json}")
                new_cp_list = [[str(stats.geo_json)], [str(stats)]]
                print(f"cp_list: {new_cp_list}")
                stats_group_by_cp.update({stats.postal_code: new_cp_list})
            else:
                cp_stat_list = stats_group_by_cp[stats.postal_code]
                print(f"stats_geometry: {stats.geo_json}")
                geoJson = json.loads(stats.geo_json)
                print(f"coordinates: {geoJson['coordinates']}")
                numpy_array = np.array(geoJson['coordinates'])
                print(f"old coordinates: {cp_stat_list[0]}")
                print(f"old stats: {cp_stat_list[1]}")
                cp_stat_list[0].Append(stats.geo_json)
                cp_stat_list[1].Append(stats)
                print(f"cp_stat_list to add: {str(cp_stat_list)}")
                stats_group_by_cp.update({stats.postal_code: cp_stat_list})

        return stats_group_by_cp

    @staticmethod
    def stats_geometry_group_by_cp_to_json(stats_geometry_object):
        data_json = []
        for row in stats_geometry_object:
            data = {
                'postal_code': row.postal_code,
                'geo_json': json.loads(row.geo_json),
                'stats_list': json.loads(row.stats_list)
            }
            data_json.append(data)

        return data_json
