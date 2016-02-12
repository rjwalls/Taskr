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
    parser.add_argument('comment', nargs="?", default="No Comment", help="Project?:Type?:Comment")
    parser.add_argument('-v', '--verbose', action='store_const', const=logging.INFO, dest='loglevel',
                        help='increase output verbosity.')
    parser.add_argument('-d', '--debug', action='store_const', const=logging.DEBUG, dest='loglevel',
                        default=logging.WARNING, help='show debug output (even more than -v).')
    parser.add_argument('-s', '--song', default='Bit Rush League of Legends', help='spotify search query.')
    parser.add_argument('-k', '--keepsong', action='store_true', help='Farfignewton')
    parser.add_argument('-l', '--logpath', default=os.path.expanduser('~/Dropbox/tasks.log'))
    parser.add_argument('-x', '--disable', action='store_true')

    args = parser.parse_args()

    start = datetime.datetime.now()

    parts = args.comment.split(':')

    project = "Unknown"
    task_type = "??"
    comment = args.comment

    if len(parts) == 2:
        project, comment = parts
    elif len(parts) == 3:
        project, task_type, comment = parts

    task = {"Type": task_type,
            "Project": project,
            "Comment": comment,
            "Start": str(start)}

    logging.basicConfig(level=args.loglevel)

    seconds = get_time(args.time)
    task_start = datetime.datetime.now()
    logging.info('Task start: %s' % task_start)
    logging.info('Starting a timer for %s seconds' % seconds)
    logging.info('Task comment: %s' % args.comment)

    print('Press Ctrl+C to end early')

    widgets = [Bar('>'), ' ', ETA(), ' ', ReverseBar('<')]
    progress = ProgressBar(widgets=widgets)

    broken = False

    try:
        for i in progress(xrange(seconds)):
            time.sleep(1)
            #This will make sure we break out properly if the computer goes to sleep while
            #a task is running. Give it a small buffer (10 s) so that we don't always hit this
            #break point
            if (datetime.datetime.now() - task_start).total_seconds() > (seconds + 10):
                break
    except KeyboardInterrupt:
        logging.debug("breaking progress loop (keyboard interrupt)")
        broken = True


    # don't execute the actions if they are disable by the user
    # or we receive a sigint
    if args.disable or broken:
        actions = []
    else:
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

    log_exists = os.path.isfile(args.logpath)

    with open(args.logpath, 'a+') as f:
        if log_exists:
            #The whole point of this code is allow us to
            #append another JSON dictionary (the task) to
            #the end of the list (with reading everything in).

            #Go to the end of the file
            f.seek(-1, os.SEEK_END)
            pos = f.tell()

            #Work backward until the last "]" is found.
            while pos > 0 and f.read(1) != "]":
                pos -= 1
                f.seek(pos, os.SEEK_SET)

            #If we aren't at the start of the file, remove the
            #"]" and everything after.
            if pos > 0:
                f.seek(pos, os.SEEK_SET)
                f.truncate()
            f.write(",")
        else:
            f.write("[")

        json.dump(task, f, indent=4)
        f.write("]")



if __name__ == '__main__':
    main()