__author__ = 'rjwalls'

import argparse
import datetime
import json
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
    parser.add_argument('-t', '--time', default='25m')
    parser.add_argument('comment', nargs="?", default="No Comment")
    parser.add_argument('-v', '--verbose', action='store_const', const=logging.INFO, dest='loglevel',
                        help='increase output verbosity.')
    parser.add_argument('-d', '--debug', action='store_const', const=logging.DEBUG, dest='loglevel',
                        default=logging.WARNING, help='show debug output (even more than -v).')
    parser.add_argument('-s', '--song', default='Bit Rush League of Legends', help='spotify search query.')
    parser.add_argument('-k', '--keepsong', action='store_true', help='Farfignewton')
    parser.add_argument('-l', '--logpath', default=os.path.expanduser('~/Dropbox/tasks.log'))

    args = parser.parse_args()

    start = datetime.datetime.now()

    if ":" in args.comment:
        task_type, comment = args.comment.split(':')
    else:
        comment = args.comment
        task_type = None

    task = {"Type": task_type,
            "Comment": comment,
            "Start": str(start)}



    logging.basicConfig(level=args.loglevel)

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


    planned_end = datetime.datetime.now()
    task["Planned End"] = str(planned_end)

    logging.info('Task end (planned): %s' % planned_end)

    raw_input('Press enter to end...')

    for action in actions:
        action.end()

    actual_end = datetime.datetime.now()
    task["Actual End"] = str(actual_end)

    task["Duration"] = str(actual_end - start)

    logging.info('Task end (actual): %s' % actual_end)

    with open(args.logpath, 'a+') as f:
        json.dump(task, f, indent=4)



if __name__ == '__main__':
    main()