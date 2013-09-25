#!/usr/bin/env python
import os
import subprocess
import multiprocessing
import time
import sys


def run_raytracer(wait, n):
    env = os.environ.copy()
    # Rows of 5 windows
    row = (n / 5)
    y = row * 100

    col = (n % 5)
    x = col * 100

    env['SDL_VIDEO_WINDOW_POS'] = '{0},{1}'.format(x, y)
    FNULL = open(os.devnull, 'w')
    subprocess.call(['python', 'raytracer.py', str(wait)], env=env, stdout=FNULL)


def run_multi_raytracers(n=20, stagger=5, wait=10):
    try:
        for x in xrange(n):
            proc = multiprocessing.Process(target=run_raytracer, args=(wait, x))
            proc.start()
            time.sleep(stagger)

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    run_multi_raytracers(stagger=1)
