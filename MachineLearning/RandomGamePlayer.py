from random import choice
from MachineLearning.Event import Event


class RandomGamePlayer():
    choices = [Event.get_down(), Event.get_left(), Event.get_right(), Event.get_up()]

    @staticmethod
    def get(gamestate):
        return [choice(RandomGamePlayer.choices)]
