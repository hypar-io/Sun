import Elements
from ladybug.location import Location
from ladybug.sunpath import Sunpath
from ladybug_geometry.geometry3d import Vector3D
import json
import math
import sys
from datetime import datetime


def execute(models, inputs):
    radius = inputs['Radius']

    location_model = models.get('location')
    if location_model is None:
        raise Exception('The location model was not provided.')

    latitude = 0.0
    longitude = 0.0

    elements = location_model['Elements']
    for id in elements:
        e = elements[id]
        d = e.get('discriminator')
        if d is not None:
            if d == 'Elements.Origin':
                longitude = e['Position'][0]
                latitude = e['Position'][1]

    sp = Sunpath(latitude, longitude)

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
                    x = math.cos(elevation) * math.sin(azimuth)
                    y = math.cos(elevation) * math.cos(azimuth)
                    z = math.sin(elevation)

                    if dt.hour == hour:
                        vertices.append(Elements.Vector3(
                            x * radius, y * radius, z * radius))
                    else:
                        vertices_back.append(Elements.Vector3(
                            x * radius, y * radius, z * radius))

                    # If the current date time corresponds to the input
                    # date time, then create a light
                    if dt.month == month and dt.day == day and dt.hour == hour:
                        v = Vector3D.from_array([x, y, z]).normalize()
                        tmp = Vector3D.from_array([0.0, 0.0, 1.0]).normalize()
                        right = v.cross(tmp).normalize()
                        up = right.cross(v).normalize()

                        em = Elements.Matrix([])
                        em.Components = [right.x, up.x, v.x, 0,
                                         right.y, up.y, v.y, 0,
                                         right.z, up.z, v.z, 0]
                        light = Elements.DirectionalLight(Elements.Color(
                            1.0, 1.0, 1.0, 1.0), 1.0, Elements.Transform(em))
                        model.add_element(light)

                        sun_vector = Elements.Line(Elements.Vector3(
                            x * radius, y * radius, z * radius), Elements.Vector3(0, 0, 0))
                        sun_model_curve = Elements.ModelCurve(
                            sun_vector, material)
                        model.add_element(sun_model_curve)
            except:
                continue

    model.add_element(Elements.ModelPoints(vertices, material.Id))
    model.add_element(Elements.ModelPoints(vertices_back, material_back.Id))

    return {'Model': model}
