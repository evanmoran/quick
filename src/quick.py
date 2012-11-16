#!/usr/bin/env python

import argparse
import sys

# Constants
# =========================================================

# Version
VERSION = "v0.0.1\n"

# Short Usage
SHORT_USAGE = """
  quick [options] topic[:subtopic]

    -h, --help                    Output usage information
    -l, --list                    List all quick files with topic
    -e, --edit                    Edit topic or subtopic
    -w, --web                     Open quick file in website\n
"""

# Long Usage
LONG_USAGE = """
  Usage:

    quick [options] topic
    quick [options] topic:subtopic

  Options:

    -h, --help                    Output usage information
    -l, --list                    List all quick files with topic
    -e, --edit                    Edit topic or subtopic
    -w, --web                     Open quick file in website
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
    quick --web git               Open `git` topic in a website\n
"""

NO_TOPIC = "__NO_TOPIC__"
NO_SUBTOPIC = "__NO_SUBTOPIC__"

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

# parse_topic
# ---------------------------------------------------------
# parse_topic("git:config")
#   => {'list'=False, 'edit'=False, 'topic'='git', 'subtopic'='config'}
# parse_topic("git:")
#   => {'list'=True, 'edit'=False, 'topic'='git', 'subtopic'=NO_SUBTOPIC}

def parse_topic(topic):
  out = {'list':False, 'edit':False, 'topic':NO_TOPIC, 'subtopic':NO_SUBTOPIC}
  if topic == "" or topic == NO_TOPIC:
    return out
  if topic[-1] == ':':
    out['list'] = True
  elif topic[-1] == '+':
    out['edit'] = True
  (_topic, _partition, _subtopic) = topic.partition(':')
  if _topic:
    out['topic'] = _topic
  if _subtopic:
    out['subtopic'] = _subtopic
  return out

def update():
  pass


# Commands
# =========================================================

def command_none():
  sys.stdout.write(SHORT_USAGE)
  return Exit.SUCCESS

def command_version():
  sys.stdout.write(VERSION)
  return Exit.SUCCESS

def command_help():
  parser.print_help()
  return Exit.SUCCESS

def command_update():
  print 'command_update'
  update()
  return Exit.SUCCESS

def command_list(topic=NO_TOPIC, subtopic=NO_SUBTOPIC):
  print 'command_list %(topic)s, %(subtopic)s' % locals()
  return Exit.SUCCESS

def command_edit(topic=NO_TOPIC, subtopic=NO_SUBTOPIC):
  print 'command_edit %(topic)s, %(subtopic)s' % locals()
  return Exit.SUCCESS

def command_view(topic=NO_TOPIC, subtopic=NO_SUBTOPIC):
  print 'command_view %(topic)s, %(subtopic)s' % locals()
  return Exit.SUCCESS

# Parse Arguments
# =========================================================

class ArgParser(argparse.ArgumentParser):
  def error(self, message):
    sys.stderr.write('\n  ERROR: %s\n' % message)
    sys.stdout.write(SHORT_USAGE)
    sys.exit(Exit.ARGUMENT_ERROR)

  def print_help(self):
    sys.stdout.write(LONG_USAGE)

parser = ArgParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('-e', '--edit', action='store_true', default=False)
group.add_argument('-l', '--list', action='store_true', default=False)
group.add_argument('-w', '--web', action='store_true', default=False)
group.add_argument('--version', action='store_true', default=False)
parser.add_argument('--verbose', action='store_true', default=False)
parser.add_argument('--color', action='store_true', default=False)
parser.add_argument('--nocolor', action='store_true', default=False)

parser.add_argument('topic', nargs='?', default=NO_TOPIC)

args = parser.parse_args()

# Fix color to be ColorMode type
args.color_mode = ColorMode.AUTO
if args.color:
  args.color_mode = ColorMode.ON
elif args.nocolor:
  args.color_mode = ColorMode.OFF

from pprint import pprint
# pprint(args)

# Call Commands
# ----------------------------------------------------------

# Version
if args.version == True:
  exit(command_version())

# Help
elif args.topic == NO_TOPIC:
  exit(command_none())

elif args.help:
  exit(command_help())

# All the rest have topics so lets parse that
parsed_topic = parse_topic(args.topic)

if args.edit or parsed_topic['edit']:
  exit(command_edit(topic=parsed_topic['topic'], subtopic=parsed_topic['subtopic']))

elif args.list or parsed_topic['list']:
  exit(command_list(topic=parsed_topic['topic'], subtopic=parsed_topic['subtopic']))

else:
  exit(command_view(topic=parsed_topic['topic'], subtopic=parsed_topic['subtopic']))
