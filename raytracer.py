"""
My goal in writing this was, firstly, to have a side project, because I was
getting a little antsy, which usually means I've been bored as shit, but have
been denying it. And secondly, because I've always wanted to get into graphics
in a very real way. Every time I've tried to sit down and write a raytracer,
I've been overwhelmed by the maths.

And it's been no different this time. I ain't giving up, anymore, though. Fuck
it, I'll figure out what's needed on my own, then later on I can understand it
through the filter of maths.

Anyway, with that in mind, I'm going to build the raytracer using things that
are familiar to me. After all, that's how the first raytracer must have been
built. And in order to understand something really, really well, I've learned
understanding the development of the idea is crucial. It becomes instinct to
recognize why things are done (because they'll solve a problem I ran into).

Right, so I'm going to begin by tracing every (1,1) point in a ray's path. I'm
going to begin with a relatively small space: a 100x100 screen with a 200x200
world space. I'll have one sphere with a radius of 40 in the center of the
world, and one spherical light source r=20 diagonally to the top-left of the
object sphere. x is screen x, y is depth, and z is screen y.

Starting very simply, rays which hit nothing (reach y=150) will be black; rays
which hit an object and can reach a light source will be white; rays which hit
an object and no light source will be gray.
"""

import math
import pygame
import sys

pygame.init()


class Vector(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector((other.x + self.x), (other.y + self.y), (other.z + self.z))

    def __sub__(self, other):
        return other + (-self)

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __len__(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __div__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar, self.z / scalar)

    def normalize(self):
        return self / len(self)


class Sphere(Vector):
    def __init__(self, x, y, z, r):
        super(Sphere, self).__init__(x, y, z)
        self.radius = r

    def __contains__(self, vector):
        return math.sqrt((vector.x - self.x)**2 +
                         (vector.y - self.y)**2 +
                         (vector.z - self.z)**2) < self.radius


class Ray(object):
    """
    I'm making this a point with a direction, and iterating over it adds the
    `direction` vector. I've really muddled what Vector and Point means, but
    I really, really don't care at this point. I'm aware of my lack of
    distinction, but FUCK IT. They're both three floats, and the ease at which
    they're represented as the same data in programming-language-speak makes
    their utility non-obvious, so fuck it. I'm doing this experiment for
    myself, anyway... I don't know why I keep forgetting that.

    I'm totally gonna end up a bitter hermit.
    """

    def __init__(self, point, direction):
        self.point = point
        self.direction = direction

    def __iter__(self):
        return RayIter(self)


class RayIter(object):
    def __init__(self, ray):
        self.ray = ray

    def next(self):
        self.ray.point += self.ray.direction
        return self.ray.point


class World(object):
    def __init__(self, width, depth, height):
        self.width = width
        self.depth = depth
        self.height = height

    def __contains__(self, point):
        return (0 < point.x < self.width and
                0 < point.y < self.depth and
                0 < point.z < self.height)


if __name__ == '__main__':
    # The world space is 200x200. (0, 0) is bottom-left of the screen, depth
    # closer to 0 being closer to the screen.
    world_size = (200, 200, 200)
    world = World(*world_size)

    # Top-left quadrant (roughly), just past center of world (in depth), 20 rad
    light = Sphere(40, 170, 40, 20)

    # Dead-center, 4 radius
    object = Sphere(100, 100, 100, 40)

    w = pygame.display.set_mode((100, 100))

    RAY_NOTHING = pygame.Color('orange')
    RAY_OBJ_LIGHT = pygame.Color('MintCream')  # Oh, yeah, my kind of colour name
    RAY_OBJECT = pygame.Color('DarkGray')

    def trace_object(ray, object):
        for point in ray:
            if point not in world:
                return None
            if point in object:
                return point
        else:
            return None

    def trace_ray(x, y, z):
        v = Vector(x, y, z)
        hit = trace_object(Ray(v, Vector(0, 1, 0)), object)
        if hit:
            # I don't know how to find the vector between the point hit and the
            # light source. I do want the normalized (i.e. length=1) vector.
            # Shit, I'm really out of my element here. I'm searching the nets.
            # I'm hitting the maths wall hard, to the point where I'm going to
            # have to suck up all my pride and learn some real maths, because
            # it will save me lots of time. Fuck. Fuck. FUCK. :(      :'(
            #
            # Alright, gonna try just subtracting
            if trace_object(Ray(hit, (hit - light).normalize()), light):
                return RAY_OBJ_LIGHT
            else:
                return RAY_OBJECT
        else:
            return RAY_NOTHING

    # I don't even care to determine the relationship between this. Gawsh, I'm
    # so lazy. Oh, well.
    WORLD_SIZE = 200
    WORLD_VIEW = 100
    VIEW_START = 50
    for z in xrange(VIEW_START, world_size[2] - VIEW_START):
        for x in xrange(VIEW_START, world_size[0] - VIEW_START):
            color = trace_ray(x, 0, z)
            #print x, z, color#####################
            w.set_at((x - VIEW_START, z - VIEW_START), color)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                else:
                    print event

    # Boilerplate, just wanna get shit running
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            else:
                print event
