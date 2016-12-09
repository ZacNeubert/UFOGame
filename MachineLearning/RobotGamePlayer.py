import pickle
from datetime import datetime
from glob import glob

import numpy
import pygame
from keras import models
from keras.layers import Activation, Dense
from keras.models import Sequential
from keras.optimizers import SGD
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.kernel_approximation import RBFSampler
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier

from MachineLearning.Event import Event
from MachineLearning.TruthHandler import Reader


class RobotGamePlayer():
    @staticmethod
    def get(gamestate, classifier_class=None, args=None):
        gamestate = [float(i) for i in gamestate.split(',')]
        # gamestate = numpy.array(gamestate).reshape(1,-1)
        if not classifier_class:
            prediction = Pickled.get_prediction(gamestate)
        #print(prediction)
        return [Event(pygame.KEYDOWN, p) for p in prediction]


class Pickled():
    fname = ''
    classifier = None

    @classmethod
    def get_file_name(cls):
        if not cls.fname:
            #files = glob('*pickle')
            #files = sorted(files)
            #cls.fname = files[-1]
            cls.fname = input('Enter the pickle: ')
        return cls.fname

    @classmethod
    def get_classifier(cls):
        if not cls.classifier:
            cls.classifier = joblib.load(cls.get_file_name())
        return cls.classifier

    @classmethod
    def get_prediction(cls, game_state):
        chooser = cls.get_classifier()
        game_state = numpy.array(game_state).reshape(1,-1)
        return chooser.predict(game_state)

class KerasLoaded():
    fname = ''

    @classmethod
    def get_fname(cls):
        if not cls.fname:
            files = sorted(glob('*keras'))
            cls.fname = files[-1]
        return cls.fname

    @classmethod
    def get_classifier(cls):
        if not cls.classifier:
            cls.classifier = models.load_model(cls.get_fname())
        return cls.classifier

    @classmethod
    def get_prediction(cls, game_state):
        chooser = cls.get_classifier()
        classes = chooser.predict_classes(game_state, batch_size=32)
        return classes[0] # probably

class KerasNN():
    classifier = None
    features = None
    actions = None

    @classmethod
    def get_classifier(cls):
        if not cls.classifier:
            cls.features, cls.actions = Reader.get_data()
            input_dim = len(cls.features[0])
            model = Sequential()
            model.add(Dense(12, input_dim=input_dim))
            model.add(Activation('sigmoid'))
            model.add(Dense(12, input_dim=input_dim))
            model.add(Activation('sigmoid'))
            model.add(Dense(output_dim=5))

            sgd = SGD(lr=0.1)
            model.compile(loss='mse', optimizer=sgd)

            model.fit(cls.features, cls.actions, show_accuracy=True, batch_size=100, nb_epoch=500)
            cls.classifier = model
            fname = str(datetime.now()) + '.keras'
            model.save(fname)
        return cls.classifier

    @classmethod
    def get_prediction(cls, game_state):
        chooser = cls.get_classifier()
        game_state = numpy.array(game_state).reshape(1,-1)
        classes = chooser.predict_classes(game_state, batch_size=32)
        return classes[0] # probably

class Classifier():
    classifier = None
    features = None
    actions = None

    @classmethod
    def get_classifier(cls):
        if not cls.classifier:
            print('Training Model')
            cls.features, cls.actions = Reader.get_data()
            cls.classifier = SGDClassifier(loss='hinge', penalty="l2", fit_intercept=273)
            cls.classifier.fit(cls.features, cls.actions)
            fname = str(datetime.now())
            with open(fname+'.pickle', 'wb') as f:
                pickle.dump(cls.classifier, file=f)
        return cls.classifier

    @classmethod
    def get_prediction(cls, game_state):
        chooser = cls.get_classifier()
        return chooser.predict(game_state)


class SVC():
    classifier = None
    features = None
    actions = None

    @classmethod
    def get_classifier(cls):
        if not cls.classifier:
            cls.features, cls.actions = Reader.get_data()
            num = 10000
            cls.features = cls.features[:num]
            cls.actions = cls.actions[:num]
            cls.classifier = svm.SVC()
            cls.classifier.fit(cls.features, cls.actions)
        return cls.classifier

    @classmethod
    def get_prediction(cls, game_state):
        chooser = cls.get_classifier()
        return chooser.predict(game_state)


class Kernelizer():
    classifier = None
    features = None
    actions = None

    @classmethod
    def get_classifier(cls):
        if not cls.classifier:
            cls.features, cls.actions = Reader.get_data()
            print('Got data...')
            cls.rbf_feature = RBFSampler(gamma=1, random_state=1)
            print('Created Sampler...')
            X_features = cls.rbf_feature.fit_transform(cls.features)
            print('Created X_Features...')
            cls.classifier = SGDClassifier(loss='hinge', penalty='l2', fit_intercept=273)
            print('Created classifier...')
            cls.classifier.fit(X_features, cls.actions)
            print('Fit Classifier...')
            print(cls.classifier.score(X_features, cls.actions))
            print('Returning classifier...')
            with open(Reader.get_fname()+'.pickle', 'wb') as f:
                pickle.dump(cls.classifier, file=f)
        return cls.classifier

    @classmethod
    def get_prediction(cls, game_state):
        chooser = cls.get_classifier()
        X_features = cls.rbf_feature.fit_transform(game_state)
        return chooser.predict(X_features)

class DecisionTreeWrapper():
    classifier = None
    features = None
    actions = None

    @classmethod
    def get_classifier(cls):
        if not cls.classifier:
            cls.features, cls.actions = Reader.get_data()
            cls.classifier = DecisionTreeClassifier()
            cls.classifier.fit(cls.features, cls.actions)
            with open(Reader.get_fname()+'.pickle', 'wb') as f:
                pickle.dump(cls.classifier, file=f)
        return cls.classifier

    @classmethod
    def get_prediction(cls, game_state):
        chooser = cls.get_classifier()
        probs = chooser.predict_proba(game_state)
        return chooser.predict(game_state)

class RandomForestWrapper():
    classifier = None
    features = None
    actions = None

    @classmethod
    def get_classifier(cls):
        if not cls.classifier:
            print('Getting data')
            cls.features, cls.actions = Reader.get_data()
            print('Initializing classifier')
            cls.classifier = RandomForestClassifier()
            print('Training classifier')
            cls.classifier.fit(cls.features, cls.actions)
            with open(Reader.get_fname()+'.pickle', 'wb') as f:
                pickle.dump(cls.classifier, file=f)
        return cls.classifier

    @classmethod
    def get_prediction(cls, game_state):
        chooser = cls.get_classifier()
        probs = chooser.predict_proba(game_state)
        # if none is most probable, use that
        # else get top three keys
            #Pick the middle key from that
        picked = []
        for i,p in enumerate(probs[0:1][0]):
            if p > .35:
                picked.append(chooser.classes_[i])
        if not picked or len(picked) == 1:
            return [chooser.predict(game_state)]
        return picked
