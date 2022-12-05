# app/serialization/stats_geometry.py
import json


class StatsGeometry:
    def __int__(self, postal_code, description, age, gender, total_amount, month, year, geo_json):
        self.postal_code = postal_code
        self.description = description
        self.age = age
        self.gender = gender
        self.total_amount = total_amount
        self.month = month
        self.year = year

    @staticmethod
    def stats_geometry_to_json(rows):
        data_json = []
        for row in rows:
            data = {
                'postal_code': row.postal_code,
                'description': row.description,
                'age': row.age,
                'gender': row.gender,
                'total_amount': row.total_amount,
                'month': row.month,
                'year': row.year,
                'geo_json': json.loads(row.geo_json)
            }
            data_json.append(data)

        return data_json
