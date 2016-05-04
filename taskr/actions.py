__author__ = 'rjwalls'

import logging
import numpy
import subprocess
import threading
import time


class Action(object):
    def start(self):
        pass

    def end(self):
        pass


class Spotify(Action):
    def __init__(self, query, keepsong):
        self._query = query
        self._keepsong = keepsong

    def start(self):
        p_spotify = subprocess.Popen(['spotify', 'play', self._query], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.debug(p_spotify.communicate())

    def end(self):
        if self._keepsong:
            return

        p_spotify = subprocess.Popen(['spotify', 'pause'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.debug(p_spotify.communicate())


class DimScreen(threading.Thread, Action):
    """
    Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition.
    """

    def __init__(self):
        super(DimScreen, self).__init__()
        self._stop = threading.Event()

    def end(self):
        self._stop.set()
        self.join()
        #todo: set brightness back to what it was previously
        subprocess.Popen(['brightness', '0.75']).wait()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        for step in numpy.arange(0.75, 0.1, -0.01):
            subprocess.Popen(['brightness', str(step)])

            if self.stopped():
                break

            time.sleep(0.3)