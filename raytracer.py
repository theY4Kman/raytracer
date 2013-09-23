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

    def normalize(self):
        """
        I don't really know what "normalize" means in the mathematical sense.
        What little I've gathered and what I could see as being useful is
        changing each x, y, and z to be ratios of 1. And the way that seems
        obvious to do that is to find the maximum of the three and divide them
        all by it.

        The internet says that's wholly wrong, though I do not fully understand
        why. What sticks out to me as bad (not very useful) in my solution is
        that one component would always end up as 1, and so it seems two
        different vectors, in wholly different directions, could end up seeming
        very similar with my method.

        Boy, I'm really coming to the point where I just want to trust the
        maths and get on with it, BUT THAT'S QUITTER TALK! I WILL WIN THIS! I
        WILL UNDERSTAND THESE MATHS AND STILL KEEP MY OWN METHOD OF UNDER-
        STANDING. I WILL NOT LET THEM WIN!

        I actually have no idea why I wrote this method. It just seemed like
        the thing you put on a Vector class. Well, fuck, I'm already not
        solving my problem, and doing things which look like solving it. Pshhh.
        """


class Sphere(Vector):
    def __init__(self, x, y, z, r):
        super(Sphere, self).__init__(x, y, z)
        self.radius = r

    def __contains__(self, vector):
        return math.sqrt((vector.x - self.x)**2 +
                         (vector.y - self.y)**2 +
                         (vector.z - self.z)**2) < self.radius


if __name__ == '__main__':
    # The world space is 200x200. (0, 0) is bottom-left of the screen, depth
    # closer to 0 being closer to the screen.
    world_size = (200, 200, 200)

    # Top-left quadrant (roughly), just past center of world (in depth), 20 rad
    light = Sphere(40, 170, 40, 20)

    # Dead-center, 4 radius
    object = Sphere(100, 100, 100, 40)

    w = pygame.display.set_mode((100, 100))

    RAY_NOTHING = pygame.Color('orange')
    RAY_OBJ_LIGHT = pygame.Color('MintCream')  # Oh, yeah, my kind of colour name
    RAY_OBJECT = pygame.Color('DarkGray')

    def trace_ray(x, y, z):
        v = Vector(x, y, z)
        while v.y < world_size[1]:
            if v in object:
                return RAY_OBJECT
            elif v in light:
                return RAY_OBJ_LIGHT
            v.y += 1.0
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
