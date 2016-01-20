__author__ = 'rjwalls'

import argparse
import datetime
import logging
import os
import re
import time

from progressbar import ProgressBar, Timer, ETA, Bar, ReverseBar

from actions import Spotify, DimScreen



_description='(default) Start a task timer'



def get_time(raw):
    # Matches seconds, hours, minutes, e.g., 10, 10s, 1m, 1h
    value, unit = re.match(r'(?P<value>[0-9]+)(?P<unit>[smh]?)', raw.lower()).groups()

    return int(value) * {'': 1, 's': 1, 'm': 60, 'h': 3600}[unit]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('time')
    parser.add_argument('comment', nargs="?", default="No Comment")
    parser.add_argument('-v', '--verbose', action='store_const', const=logging.INFO, dest='loglevel',
                        help='increase output verbosity.')
    parser.add_argument('-d', '--debug', action='store_const', const=logging.DEBUG, dest='loglevel',
                        default=logging.WARNING, help='show debug output (even more than -v).')
    parser.add_argument('-s', '--song', default='Bit Rush League of Legends', help='spotify search query.')
    parser.add_argument('-k', '--keepsong', action='store_true', help='Farfignewton')
    parser.add_argument('-l', '--logpath', default=os.path.expanduser('~/Dropbox/tasks.log'))

    args = parser.parse_args()


    logging.basicConfig(level=logging.INFO, filename=args.logpath)

    seconds = get_time(args.time)
    logging.info('Task start: %s' % datetime.datetime.now())
    logging.info('Starting a timer for %s seconds' % seconds)
    logging.info('Task comment: %s' % args.comment)

    widgets = [Bar('>'), ' ', ETA(), ' ', ReverseBar('<')]
    progress = ProgressBar(widgets=widgets)

    for i in progress(xrange(seconds)):
        time.sleep(1)

    #time.sleep(seconds)

    actions = [Spotify(args.song, args.keepsong), DimScreen()]

    for action in actions:
        action.start()


    logging.info('Task end (planned): %s' % datetime.datetime.now())

    raw_input('Press enter to end...')

    for action in actions:
        action.end()

    logging.info('Task end (actual): %s' % datetime.datetime.now())



if __name__ == '__main__':
    main()