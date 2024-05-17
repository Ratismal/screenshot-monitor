#!/usr/bin/env python

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests as r
import re
import json

WEBHOOK = ""
FORUM_WEBHOOK = ""
FORUM_THREADS = {}

with open('config.json') as f:
  config = json.load(f)
  WEBHOOK = config["globalWebhook"]
  FORUM_WEBHOOK = config["forumWebhook"]

try:
  with open('threads.json') as f:
    FORUM_THREADS = json.load(f)
except:
  with open('threads.json', 'w') as f:
    f.write("{ }")

GAME_LIST = {}
REVERSE_GAME_LIST = {}

def cache_games():
  response = r.get('http://api.steampowered.com/ISteamApps/GetAppList/v2')

  l = json.loads(response.text)
  for app in l['applist']['apps']:
    GAME_LIST[str(app['appid'])] = app['name']
    REVERSE_GAME_LIST[app['name']] = str(app['appid'])
  
  with open('games.json', 'w') as f:
    json.dump(GAME_LIST, f, indent = 2)

  print("Finished loading game list.")

cache_games()

def get_game(id):
  global GAME_LIST

  if id not in GAME_LIST:
    cache_games()

  return GAME_LIST.get(id, 'Unknown')

print("Loaded the following threads:")
for key, value in FORUM_THREADS.items():
  print(get_game(key) + ": " + value)

def get_game_from_name(name):
  global REVERSE_GAME_LIST

  if name not in REVERSE_GAME_LIST:
    cache_games()

  return REVERSE_GAME_LIST.get(name, 'Unknown')

class ScreenshotHandler(FileSystemEventHandler):
  def __init__(self):
    self.files_to_process = set()
  
  def on_created(self, event):
    self.files_to_process.add(event.src_path)

  def on_closed(self, event):
    if not (event.src_path in self.files_to_process):
      return

    self.files_to_process.remove(event.src_path)
    global WEBHOOK
    global FORUM_WEBHOOK
    global FORUM_THREADS
    global GAME_LIST

    path = event.src_path

    search = re.search(r".+/(\d+)_(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})", path)
    
    game_id = search.group(1)
    year = search.group(2)
    month = search.group(3)
    day = search.group(4)
    hour = search.group(5)
    minute = search.group(6)
    second = search.group(7)

    game_name = get_game(game_id)

    routed_channel= None


    with open('lastgame', 'w') as f:
      f.write(game_id)

    if game_id in FORUM_THREADS:
      files = {'file': open(path, 'rb')}
      routed_channel = FORUM_THREADS[game_id]
      webhook_url = FORUM_WEBHOOK + '?thread_id={}'.format(routed_channel)
      r.post(webhook_url, files=files)

    message = "{} ({}) - {}/{}/{} {}:{}:{}".format(game_name, game_id, year, month, day, hour, minute, second)

    if routed_channel != None:
      message += "\nRouted screenshot to <#{}>".format(routed_channel)

    print("Uploading screenshot for: " + message)
    data = {
      'content': message,
    }
    files = {'file': open(path, 'rb')}

    r.post(WEBHOOK, data, files=files)

class VideoHandler(FileSystemEventHandler):
  def __init__(self):
    self.files_to_process = set()
  
  def on_created(self, event):
    self.files_to_process.add(event.src_path)

  def on_closed(self, event):
    if not (event.src_path in self.files_to_process):
      return

    self.files_to_process.remove(event.src_path)
    print(event.src_path)
    global WEBHOOK
    global FORUM_WEBHOOK
    global FORUM_THREADS
    global GAME_LIST

    path = event.src_path

    search = re.search(r".+/(.+)-\d+\.\d+s-(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})", path)
    
    game_name = search.group(1)
    year = search.group(2)
    month = search.group(3)
    day = search.group(4)
    hour = search.group(5)
    minute = search.group(6)
    second = search.group(7)

    game_id = get_game_from_name(game_name)

    routed_channel = None


    with open('lastgame', 'w') as f:
      f.write(game_id)

    if game_id in FORUM_THREADS:
      routed_channel = FORUM_THREADS[game_id]
      webhook_url = FORUM_WEBHOOK + '?thread_id={}'.format(routed_channel)
      with open(path, 'rb') as file:
        files = {'file': file}
        r.post(webhook_url, {}, files=files)

    message = "{} ({}) - {}/{}/{} {}:{}:{}".format(game_name, game_id, year, month, day, hour, minute, second)

    if routed_channel != None:
      message += "\nRouted screenshot to <#{}>".format(routed_channel)

    print("Uploading screenshot for: " + message)
    data = {
      'content': message,
    }
    with open(path, 'rb') as file:
      files = {'file': file}
      r.post(WEBHOOK, data, files=files)

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s - %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S')
  path = "/home/deck/Pictures/DCIM"
  video_path = "/home/deck/Videos"

  observer = Observer()
  observer.schedule(ScreenshotHandler(), path, recursive=True)
  observer.schedule(VideoHandler(), video_path, recursive=True)
  observer.start()
  print("Ready!")

  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()
