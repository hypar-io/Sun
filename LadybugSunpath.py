import Elements
from ladybug.location import Location
from ladybug.sunpath import Sunpath
from ladybug_geometry.geometry3d import Vector3D

import json
import math
import sys
from datetime import datetime
# from scipy.spatial.transform import Rotation


def execute(models, inputs):

    # TODO: Do we need to set the time zone?
    sp = Sunpath(inputs['Location']['coordinates'][1],
                 inputs['Location']['coordinates'][0])
    radius = 100

    dt = datetime.fromisoformat(inputs['Date'])

    material = Elements.Material(
        'day_color', Elements.Color(1.0, 1.0, 0.0, 1.0))
    material_back = Elements.Material(
        'day_color_back', Elements.Color(0.6, 0.6, 0.6, 1.0))

    model = Elements.Model(Elements.Transform(Elements.Matrix(None)), {})

    model.add_element(material)
    model.add_element(material_back)

    vertices = []
    vertices_back = []
    for month in range(1, 13):
        for day in range(1, 32):
            try:
                for hour in range(0, 24):
                    sun = sp.calculate_sun(month=month, day=day, hour=hour)
                    azimuth = sun.azimuth_in_radians
                    elevation = sun.altitude_in_radians

                    # https://en.wikipedia.org/wiki/Spherical_coordinate_system
                    x = radius * math.cos(elevation) * math.sin(azimuth)
                    y = radius * math.cos(elevation) * math.cos(azimuth)
                    z = radius * math.sin(elevation)

                    if dt.hour == hour:
                        vertices.append(Elements.Vector3(x, y, z))
                    else:
                        vertices_back.append(Elements.Vector3(x, y, z))

                    # If the current date time corresponds to the input
                    # date time, then create a light
                    if dt.month == month and dt.day == day and dt.hour == hour:
                        v = Vector3D.from_array([x, y, z]).reverse()
                        up = Vector3D.from_array([0, 0, 1])
                        right = v.cross(up)

                        em = Elements.Matrix([])
                        em.Components = [right.x, right.y, right.z, 0,
                                         v.x, v.y, v.z, 0,
                                         up.x, up.y, up.z, 0,
                                         x, y, z, 1]
                        light = Elements.DirectionalLight(Elements.Color(
                            1.0, 1.0, 1.0, 1.0), 1.0, Elements.Transform(em))
                        model.add_element(light)
                        sun_vector = Elements.Line(Elements.Vector3(
                            x, y, z), Elements.Vector3(0, 0, 0))
                        sun_model_curve = Elements.ModelCurve(
                            sun_vector, material)
                        model.add_element(sun_model_curve)
            except:
                continue

    model.add_element(Elements.ModelPoints(vertices, material.Id))
    model.add_element(Elements.ModelPoints(vertices_back, material_back.Id))

    return {'Model': model}
