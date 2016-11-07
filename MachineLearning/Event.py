import pygame


class Event(object):
    def __init__(self, type, key):
        self.type = type
        self.key = key

    @staticmethod
    def get_left():
        return Event(pygame.KEYDOWN, pygame.K_LEFT)

    @staticmethod
    def get_right():
        return Event(pygame.KEYDOWN, pygame.K_RIGHT)

    @staticmethod
    def get_up():
        return Event(pygame.KEYDOWN, pygame.K_UP)

    @staticmethod
    def get_down():
        return Event(pygame.KEYDOWN, pygame.K_DOWN)
