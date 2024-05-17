#!/usr/bin/env python
import os
import re
# Config directory: /home/deck/.local/share/Steam/userdata/<userid>/config/localconfig.vdf

USERDATA_PATH = "/home/deck/.local/share/Steam/userdata/"

for name in os.listdir(USERDATA_PATH):
  if name != "0":
    print(name)
    config_path = USERDATA_PATH + name + "/config/localconfig.vdf"
    contents = ""
    with open(config_path) as f:
      contents = f.read()

    backup_path = config_path + ".bak"
    print("Backing up local config file at:")
    print(backup_path)
    with open(backup_path, 'w') as f:
      f.write(contents)

    if "InGameOverlayScreenshotSaveUncompressedPath" in contents:
      print("Found existing 'InGameOverlayScreenshotSaveUncompressedPath' node, overwriting to '/home/deck/Pictures/DCIM'")
      contents = re.sub(r'"InGameOverlayScreenshotSaveUncompressedPath"\t\t".+"', '"InGameOverlayScreenshotSaveUncompressedPath"\t\t"/home/deck/Pictures/DCIM/"', contents)
      print("Setting 'InGameOverlayScreenshotSaveUncompressed' node to '1'")
      contents = re.sub(r'"InGameOverlayScreenshotSaveUncompressed"\t\t"0"', '"InGameOverlayScreenshotSaveUncompressed"\t\t"1"', contents)
    else:
      print("Setting 'InGameOverlayScreenshotSaveUncompressed' node to '1' and")
      print("creating new 'InGameOverlayScreenshotSaveUncompressedPath' node, with value '/home/deck/Pictures/DCIM'")
      contents = re.sub(r'"InGameOverlayScreenshotSaveUncompressed"\t\t".+"', '"InGameOverlayScreenshotSaveUncompressed"\t\t"1"\n\t\t"InGameOverlayScreenshotSaveUncompressedPath"\t\t"/home/deck/Pictures/DCIM/"', contents)

    print("Writing...")
    with open(config_path, "w") as f:
      f.write(contents)

print("Done")