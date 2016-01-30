__author__ = 'rjwalls'

import argparse
import datetime
import json
import logging
import os
import re
import time
import io


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logpath', default=os.path.expanduser('~/Dropbox/tasks.log'))
    args = parser.parse_args()

    #Read in log file
    with open(args.logpath, 'r+') as f:
        tasks = json.load(f)

    today = str(datetime.datetime.now()).split(" ")[0]

    tasks = [t for t in tasks
             if (t["Start"].split(" "))[0] == today]

    projects = {"Unknown": []}

    for task in tasks:
        #Only summarize today's tasks
        if task["Start"].split(" ")[0] != today:
            continue

        if "Project" in task:
            project = task["Project"]

            if project not in projects:
                projects[project] = []
            projects[project].append(task)
        else:
            task["Unknown"].append(task)

#    for project in projects:
#        if "Type" in task:
#            ttype = task["Type"]

#            if ttype

    print "Total Tasks: %d" % len(tasks)

    print "Number of Projects: %d" % len([p for p in projects.keys() if p != "Unknown"])



    for project in projects:
        if len(projects[project]) == 0:
            continue

        print ""
        print "Project: ", project

        for task in projects[project]:
            ttype = "??"

            if "Type" in task:
                ttype = task["Type"]

            print "\t%s: %s" % (ttype, task["Comment"])

    pass



    #Grab all of the tasks for the day

    #Summarize per day, per project, task type
    #We don't want to be case sensitive



if __name__ == '__main__':
    main()