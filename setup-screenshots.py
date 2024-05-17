#!/usr/bin/env python
import os
import re
import vdf
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

    data = vdf.loads(contents, mapper=vdf.VDFDict)
    print(data['UserLocalConfigStore']['System'])

    print("Setting 'InGameOverlayScreenshotSaveUncompressedPath' node to '/home/deck/Pictures/DCIM'")
    data['UserLocalConfigStore']['System']['InGameOverlayScreenshotSaveUncompressedPath'] = "/home/deck/Pictures/DCIM"
    print("Setting 'InGameOverlayScreenshotSaveUncompressed' node to '1'")
    data['UserLocalConfigStore']['System']['InGameOverlayScreenshotSaveUncompressed'] = "1"

    print("Writing...")
    with open(config_path, "w") as f:
      dumped = vdf.dumps(data, pretty=True)
      f.write(dumped)

print("Done")