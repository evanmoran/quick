#!/usr/bin/env python

import argparse
import sys
import os
import subprocess
import glob
import webbrowser
from pprint import pprint

# Constants
# =========================================================

VERSION = "v0.0.3\n"

QUICK_DIR = os.environ.get('QUICK_DIR') or os.path.join(os.environ.get('HOME'), ".quick")
QUICK_CACHE_DIR = os.path.join(QUICK_DIR, 'cache')

SHORT_USAGE = """
  quick [options] topic[:subtopic]

    -h, --help                    Output usage information
    -l, --list                    List all quick files with topic
    -e, --edit                    Edit topic or subtopic
    -w, --web                     Open quick file in website
    -u, --update                  Update quick and its topics cache

"""

LONG_USAGE = """
  Usage:

    quick [options] topic
    quick [options] topic:subtopic

  Options:

    -h, --help                    Output usage information
    -l, --list                    List all quick files with topic
    -e, --edit                    Edit topic or subtopic
    -w, --web                     Open quick file in website
    -u, --update                  Update quick and its topics cache
    --color                       Force color printing
    --nocolor                     Force no color printing
    --version                     Output the version number

  Environment: (optional)

    QUICK_OPTIONS                 Options prepended to all commands

  Examples:

    quick git                     View the `git` topic
    quick git:config              View `git:config` subtopic
    quick git:                    List `git` subtopics

    quick --edit git              Edit or create `git` topic
    quick --edit git:config       Edit or create `git:config` subtopic
    quick --list git              List `git` subtopics
    quick --web git               Open `git` topic in a website
    quick --update                Update quick

"""

# git log -n1 --pretty='#H'

# Enumerations
# =========================================================

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

Exit = enum(SUCCESS=0, ERROR=1, ARGUMENT_ERROR=2)

# ColorMode
ColorMode = enum(AUTO=1, ON=2, OFF=2)

# Helpers
# =========================================================

class working_dir:
  def __init__(self, directory):
    self.scoped_dir = directory
  def __enter__(self):
    self.old_dir = os.getcwd()
    os.chdir(self.scoped_dir)
  def __exit__(self, type, value, traceback):
    os.chdir(self.old_dir)

# call: execute command as subprocess with list of arguments
# returns triplet: code, out, err
def call(args):
  proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = proc.communicate()
  code = proc.returncode
  if code != Exit.SUCCESS:
    raise BaseException(err)
  return code, out, err

# Execute git command
def git(directory, args):
  with working_dir(directory):
    return call(['git'] + args)

class Task:
  def __init__(self, task_name, quiet=True):
    self.task_name = task_name
    self.quiet = quiet
  def __enter__(self):
    if not self.quiet:
      sys.stdout.write(self.task_name + '... ')
      sys.stdout.flush()
  def __exit__(self, type, value, traceback):
    if not self.quiet:
      if type == None:
        print 'OK'
      else:
        print 'ERROR (%s)' % value

# parse_topic
# ---------------------------------------------------------
# parse_topic("git:config")
#   => {'list'=False, 'edit'=False, 'topic'='git', 'subtopic'='config'}
# parse_topic("git:")
#   => {'list'=True, 'edit'=False, 'topic'='git', 'subtopic'=None}

def parse_topic(topic):
  out = {'list':False, 'edit':False, 'web':False, 'topic':None, 'subtopic':None}
  if topic == "" or topic == None:
    return out

  # End in ':' lists
  if topic[-1] == ':':
    out['list'] = True

  # End in '+' edits
  elif topic[-1] == '+':
    out['edit'] = True
    topic = topic[:-1]

  # End in '/' opens web
  elif topic[-1] == '/':
    out['web'] = True
    topic = topic[:-1]

  (_topic, _partition, _subtopic) = topic.partition(':')
  if _topic:
    out['topic'] = _topic
  if _subtopic:
    out['subtopic'] = _subtopic
  return out

# Print errors with special formatting and USAGE
def die(message, error_code = Exit.ARGUMENT_ERROR):
  sys.stderr.write('\n  ERROR: %s\n' % message)
  sys.stdout.write(SHORT_USAGE)
  exit(error_code)

# Example: 'git:config'
def cache_name(topic, subtopic=None):
  fname = topic
  if subtopic:
    fname += ':' + subtopic
  return fname

# Example: 'git:config.md'
def cache_file(topic, subtopic=None):
  return cache_name(topic, subtopic) + '.md'

# Example: 'full/path/git:config.md'
def cache_path(topic, subtopic=None):
  fname = cache_file(topic, subtopic)
  return os.path.join(QUICK_CACHE_DIR, fname)

def cache_file_exists(topic, subtopic=None):
  return os.path.exists(cache_path(topic, subtopic))

def cache_list(topic, subtopic=None, deep=True):
  if topic:
    glob_name = cache_file(topic, '*')
  else:
    glob_name = cache_file('*')

  files = glob.glob(os.path.join(QUICK_CACHE_DIR, glob_name))

  # Filter out subtopics, ':', when listing everything
  if not topic and not deep:
    files = [f for f in files if f.find(':') == -1]

  # Remove extension and path
  ext = '.md'
  return [os.path.basename(f)[0:-len(ext)] for f in files]

def _update_quick(quiet=True):
  with Task('Updating quick', quiet):
    code, out, err = git(QUICK_DIR, ['pull', '-q'])

def _update_topics(quiet=True):
  with Task('Updating topics', quiet):
    code, out, err = git(QUICK_CACHE_DIR, ['pull', '-q'])

def quick_update(quiet=True):
  try:
    _update_quick(quiet)
    _update_topics(quiet)
  except:
    pass  # Absorb error

def cache_update(quiet=True):
  try:
    _update_topics(quiet)
  except:
    pass  # Absorb error

# Commands
# =========================================================

def command_version():
  print 'command_version'
  sys.stdout.write(VERSION)
  return Exit.SUCCESS

def command_usage():
  sys.stdout.write(SHORT_USAGE)
  return Exit.SUCCESS

def command_help():
  print 'command_help'
  parser.print_help()
  return Exit.SUCCESS

def command_update():
  quick_update(quiet=False)
  return Exit.SUCCESS

def command_list(topic=None):
  files = cache_list(topic, deep=False)
  for f in files:
    print f
  return Exit.SUCCESS

def command_web(topic, subtopic=None, edit=False):
  topic_name = cache_name(topic, subtopic)

  wiki_url = 'https://github.com/evanmoran/quick/wiki/%s' % topic_name
  edit_url = 'https://github.com/evanmoran/quick/wiki/%s/_edit' % topic_name
  new_url = 'https://github.com/evanmoran/quick/wiki/_new?wiki[name]=%s' % topic_name

  if edit:
    cache_update(quiet=False)

  # Check to see if file exists in cache
  if cache_file_exists(topic, subtopic):
    if edit:
      webbrowser.open(edit_url)
    else:
      webbrowser.open(wiki_url)
  else:
    if edit:
      webbrowser.open(new_url)
    else:
      name = 'Topic'
      if subtopic != None:
        name = 'Subtopic'
      print '%s not found.' % name

  return Exit.SUCCESS

def command_edit(topic, subtopic=None):
  return command_web(topic, subtopic, edit=True)

def command_view(topic, subtopic=None):
  file_path = os.path.join(QUICK_CACHE_DIR, topic)
  if subtopic != None:
    file_path = os.path.join(file_path, subtopic)
  file_path = file_path + '.md'

  try:
    with open(file_path) as f:
      print(f.read())
  except:
    name = 'Topic'
    if subtopic != None:
      name = 'Subtopic'
    print '%s not found.' % name
  return Exit.SUCCESS

# Parse Arguments
# =========================================================

class ArgParser(argparse.ArgumentParser):
  def error(self, message):
    die(message, Exit.ARGUMENT_ERROR)

  def print_help(self):
    sys.stdout.write(LONG_USAGE)

parser = ArgParser(add_help=False)
group = parser.add_mutually_exclusive_group()
group.add_argument('-e', '--edit', action='store_true', default=False)
group.add_argument('-l', '--list', action='store_true', default=False)
group.add_argument('-w', '--web', action='store_true', default=False)
group.add_argument('-u', '--update', action='store_true', default=False)
group.add_argument('-h', '--help', action='store_true', default=False)
group.add_argument('--version', action='store_true', default=False)
parser.add_argument('--verbose', action='store_true', default=False)
parser.add_argument('--color', action='store_true', default=False)
parser.add_argument('--nocolor', action='store_true', default=False)

parser.add_argument('topic', nargs='?', default=None)

args = parser.parse_args()

# Fix color to be ColorMode type
args.color_mode = ColorMode.AUTO
if args.color:
  args.color_mode = ColorMode.ON
elif args.nocolor:
  args.color_mode = ColorMode.OFF

# pprint(args)

# Call Commands
# ----------------------------------------------------------

# Parse the topic:subtopic if it exists
parsed_topic = parse_topic(args.topic)

# Version
if args.version == True:
  exit(command_version())

# Help
elif args.help:
  exit(command_help())

# Update
elif args.update:
  exit(command_update())

# List
elif args.list or parsed_topic['list']:
  exit(command_list(topic=parsed_topic['topic']))

# None
elif args.topic == None:
  exit(command_usage())

# Web
if args.web or parsed_topic['web']:
  exit(command_web(topic=parsed_topic['topic'], subtopic=parsed_topic['subtopic']))

# Edit
elif args.edit or parsed_topic['edit']:
  exit(command_edit(topic=parsed_topic['topic'], subtopic=parsed_topic['subtopic']))

# View
else:
  exit(command_view(topic=parsed_topic['topic'], subtopic=parsed_topic['subtopic']))
