#!/usr/bin/env python

import json
import sys

if (len(sys.argv) == 1):
  print("Please specify the ID of the forum thread.")
  sys.exit(1)

FORUM_THREADS = {}
with open('threads.json') as threads:
  FORUM_THREADS = json.load(threads)

try:
  with open('lastgame') as f:
    game_id = f.read()

    FORUM_THREADS[game_id] = sys.argv[1]

    with open('threads.json', 'w') as threads:
      json.dump(FORUM_THREADS, threads)
    
    print("Added " + game_id + " with thread " + sys.argv[1])
except:
  print("Could not read last game. Take a screenshot and try again.")