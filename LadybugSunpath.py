import Elements
from ladybug.location import Location
from ladybug.sunpath import Sunpath
import json
import math
import sys


def execute(models, inputs):

    # TODO: Do we need to set the time zone?
    sp = Sunpath(inputs['Location']['coordinates'][1],
                 inputs['Location']['coordinates'][0])
    radius = 100

    material = Elements.Material(
        'day_color', Elements.Color(1.0, 1.0, 0.0, 1.0))
    model = Elements.Model(Elements.Transform(Elements.Matrix(None)), {})
    model.add_element(material)

    for month in range(1, 12):
        # print('Calculating month {}'.format(month))
        for day in range(1, 28):
            # print('Calculating day {}'.format(day))
            vertices = []
            for hour in range(0, 24):
                sun = sp.calculate_sun(month=month, day=day, hour=hour)
                azimuth = sun.azimuth_in_radians
                elevation = sun.altitude_in_radians

                # https://en.wikipedia.org/wiki/Spherical_coordinate_system
                x = radius * math.cos(elevation) * math.sin(azimuth)
                y = radius * math.cos(elevation) * math.cos(azimuth)
                z = radius * math.sin(elevation)
                vertices.append(Elements.Vector3(x, y, z))

            model_curve = Elements.ModelPoints(vertices, material.Id)
            model.add_element(model_curve)

    return {'Model': model}
