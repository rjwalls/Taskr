# Taskr

Relies on the [brightness][br] utility.

[br]: https://github.com/nriley/brightness

Add voice lines to your home directory: 

```bash
ln -s .taskr ~/path/to/gitrepo/say_args.txt`
```


# Proposed Additions

Rename "Task end" to "break start" with the eventual goal of logging time spent
on each task.

Related: Add task label.

Make the task log by default to `~/.taskr/logs/YYYYMM/YYYYMMDD.log`.
Each line of log  should have the task's start, planned end, actual end, and
description.

# Developing

```bash
#run from repository root directory.
virtualenv venv
source venv/bin/activate
python setup.py develop
```
