import uuid


class Bezier(object):
    def __init__(self, controlPoints, frameType='Frenet'):
        if controlPoints is not None and len(controlPoints) > 0:
            self.ControlPoints = controlPoints
        else:
            self.ControlPoints = []
        if frameType is not None:
            self.FrameType = frameType
        self.discriminator = 'Elements.Geometry.Bezier'


class Vector3(object):
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z
        self.discriminator = 'Elements.Geometry.Vector3'


class Line(object):
    def __init__(self, start, end):
        self.Start = start
        self.End = end
        self.discriminator = 'Elements.Geometry.Line'


class Polygon(object):
    def __init__(self, vertices):
        if vertices is not None and len(vertices) > 0:
            self.Vertices = vertices
        else:
            self.Vertices = []
        self.discriminator = 'Elements.Geometry.Polygon'


class Element(object):
    def __init__(self, id=None, name=None):
        if id is not None:
            self.Id = id
        else:
            self.Id = str(uuid.uuid4())
        self.Name = name


class Color():
    def __init__(self, red, green, blue, alpha):
        self.Red = red
        self.Green = green
        self.Blue = blue
        self.Alpha = alpha


class Material(Element):
    def __init__(self, name=None,  color=None):
        Element.__init__(self)
        self.discriminator = 'Elements.Material'
        if name is not None:
            self.Name = name
        else:
            self.Name = 'default'
        self.Name = name
        if color is not None:
            self.Color = color
        else:
            self.Color = Color(1.0, 0.0, 0.0, 0.0)
        self.SpecularFactor = 0.0
        self.GlossinessFactor = 0.0
        self.Unlit = False
        self.DoubleSided = False


class ModelCurve(Element):
    def __init__(self, curve, material):
        Element.__init__(self)
        self.discriminator = 'Elements.ModelCurve'
        self.Curve = curve
        if material is not None:
            self.Material = material
        else:
            self.Material = Material()
        self.Transform = Transform(Matrix(None))
        self.IsElementDefinition = False
        self.Representation = None


class ModelPoints(Element):
    def __init__(self, locations, material):
        Element.__init__(self)
        self.discriminator = 'Elements.ModelPoints'
        self.Locations = locations
        if material is not None:
            self.Material = material
        else:
            self.Material = Material()
        self.Transform = Transform(Matrix(None))
        self.IsElementDefinition = False
        self.Representation = None


class Model(object):
    def __init__(self, transform, elements):
        if transform is not None:
            self.Transform = transform
        else:
            self.Transform = transform
        if elements is not None:
            self.Elements = elements
        else:
            self.Elements = elements

    def add_element(self, element):
        self.Elements[element.Id] = element


class Transform(object):
    def __init__(self, matrix):
        if matrix is not None:
            self.Matrix = matrix
        else:
            self.Matrix = matrix


class Matrix(object):
    def __init__(self, components):
        if components is not None:
            self.Components = components
        else:
            self.Components = [1.0,
                               0.0,
                               0.0,
                               0.0,
                               0.0,
                               1.0,
                               0.0,
                               0.0,
                               0.0,
                               0.0,
                               1.0,
                               0.0]


class DirectionalLight(Element):
    def __init__(self, color, intensity, transform, id=None, name=None):
        Element.__init__(self, id, name)
        self.Color = color
        self.Intensity = intensity
        self.Transform = transform
