# Taskr

Taskr is a simple command line utility for keeping track of time spent on
tasks. For example:

```bash
#Set a task timer for 3 minutes
taskr start 3m
```

After 3 minutes has elasped, Taskr will dim your screen and play a song
(configurable). 


Taskr requires you to install the [brightness][br] and [shpotify][spot]
utilities. That is, `brightness` and `spotify` should be executable from the
command line.

[br]: https://github.com/nriley/brightness
[spot]: https://github.com/hnarayanan/shpotify


# Proposed Additions

Rename "Task end" to "break start" with the eventual goal of logging time spent
on each task. Make the task log default to `~/.taskr/logs/YYYYMM/YYYYMMDD.log`.
Each line of log  should have the task's start, planned end, actual end, and
description.


# Developing

```bash
#run from repository root directory.
virtualenv venv
source venv/bin/activate
python setup.py develop
```
Add voice lines to your home directory: 

```bash
ln -s .taskr ~/path/to/gitrepo/say_args.txt`
```

