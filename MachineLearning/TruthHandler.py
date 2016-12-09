from datetime import datetime
from glob import glob
from itertools import chain
from math import floor

import numpy
import pygame
from copy import copy

reverse = {str(pygame.K_UP): str(pygame.K_DOWN),
           str(pygame.K_DOWN): str(pygame.K_UP),
           str(pygame.K_LEFT): str(pygame.K_RIGHT),
           str(pygame.K_RIGHT): str(pygame.K_LEFT),
           str(277): str(277)}


def as_list(state):
    return state.split(',')


def reverse_moves(states):
    reversed_states = []
    for s in states:
        s = as_list(s)
        s[-1] = reverse[s[-1]]
        reversed_states.append(','.join(s))
    return reversed_states


class Recorder:
    states = []
    write_queue = []
    fname = str(datetime.now()) + '.txt'

    @classmethod
    def get_game_state(cls, projectiles):
        serialized = ''
        for projectile in projectiles:
            serialized += ',' + projectile.serialize()
        serialized = serialized[1:]
        return serialized

    xZones = 8
    yZones = 6

    UFO_INDICATOR = 1
    ASTEROID_INDICATOR = 2
    OLD_UFO_INDICATOR = .5
    OLD_ASTEROID_INDICATOR = 1.5
    @classmethod
    def get_grid_game_state(cls, ufo, asteroids, screenX, screenY):
        grid = [[0 for y in range(cls.yZones)] for x in range(cls.xZones)]
        ux,uy = cls.get_zone(ufo, screenX, screenY)
        grid[ux][uy] = cls.UFO_INDICATOR
        for a in asteroids:
            ax,ay = cls.get_zone(a, screenX, screenY)
            if grid[ax][ay] == cls.UFO_INDICATOR:
                grid[ax][ay] = cls.ASTEROID_INDICATOR + cls.UFO_INDICATOR
            else:
                grid[ax][ay] = cls.ASTEROID_INDICATOR
        flattened = list(chain.from_iterable(grid))
        projectiles = copy(asteroids)
        projectiles.append(ufo)
        #for projectile in projectiles:
        #    if projectile.getVelX() > 1:
        #        flattened.append(1)
        #    elif projectile.getVelX < 1:
        #        flattened.append(-1)
        #    else:
        #        flattened.append(0)
        #    if projectile.getVelY() > 1:
        #        flattened.append(1)
        #    elif projectile.getVelY < 1:
        #        flattened.append(-1)
        #    else:
        #        flattened.append(0)
        flattened = [str(i) for i in flattened]
        return ','.join(flattened)

    @classmethod
    def get_zone(cls, projectile, screenX, screenY):
        xfactor = screenX/cls.xZones
        yfactor = screenY/cls.yZones
        x_zone = floor(projectile.X() / xfactor)
        y_zone = floor(projectile.Y() / yfactor)
        return x_zone,y_zone

    @classmethod
    def record(cls, ufo, asteroids, screenX, screenY, projectiles, input, isLoss, args):
        if isLoss:
            # oppositestates = cls.states[floor(len(cls.states)/2):]
            # oppositestates = reverse_moves(oppositestates)
            # [cls.write_queue.append(s) for s in oppositestates]
            cls.states = []
            return

        for i in input:
            serialized = cls.get_grid_game_state(ufo, asteroids, screenX, screenY)
            if 'key' in i.__dict__.keys():
                serialized += ',' + str(i.key)
                cls.states.append(serialized)

        if len(cls.states) > 150:
            cls.write_queue.append(cls.states[0])
            if len(cls.write_queue) > 1000:
                print('Writing...')
                data = '\n'.join(cls.write_queue) + '\n'
                cls.write(data, args)
                cls.write_queue = []
            cls.states.remove(cls.states[0])

    @classmethod
    def write(cls, data, args):
        extra_string = ''
        if args.random:
            extra_string = 'random'
        if args.human:
            extra_string = 'human'
        if args.robot:
            extra_string = 'robot'
        with open(cls.fname + extra_string, 'a') as outf:
            outf.write(data)


def splits(l, num):
    for i in range(num):
        it = i + 1
        sq = floor(len(l) / num * i)
        eq = floor(len(l) / num * it)
        yield l[sq:eq], it


class Reader:
    filename = None

    @classmethod
    def get_fname(cls):
        if not Reader.filename:
            files = glob('*2016*txt*')
            files = [f for f in files if not 'pickle' in f]
            files = sorted(files)
            Reader.filename = files[-1]
        return Reader.filename

    @classmethod
    def get_data(cls):
        print('Reading file')
        with open(cls.get_fname(), 'r') as infile:
            lines = infile.readlines()
        print('Using {} lines'.format(len(lines)))
        print(cls.get_fname())
        # print('Filtering lines')
        # lines = [l for l in lines if len(l.split(',')) == 9]
        print('extracting features')
        features = []
        for split, i in splits(lines, 100):
            split = [[float(i) for i in l.split(',')[:-1]] for l in split]
            #split = [numpy.array(s).reshape(1,-1) for s in split]
            features += split
            print('Finished split {}'.format(i))
        # features = [numpy.array(f).reshape(1, -1) for f in features]
        print('extracting actions')
        actions = [int(l.split(',')[-1]) for l in lines]
        print('Returning from get_data')
        return features, actions
