# Steamdeck Screenshot Monitor

This is a small service to monitor screenshots taken on a steamdeck, and upload them to Discord via webhooks.

## Features

- Monitor screenshots taken
- Upload to a Discord webhook
- Optionally forward screenshots of specific games to threads in a forum

The following is not supported, but may be added if there is demand
- Uploading to webhooks per-game

## Screenshots (haha)

![Persona 5](https://owo.whats-th.is/2cnoWBF.png)
![Thread Example](https://owo.whats-th.is/5WKrXwM.png)
![Balatro](https://owo.whats-th.is/6txvSac.png)


## Setup

Clone this repository to your steamdeck.
```
git clone https://github.com/Ratismal/screenshot-monitor
cd screenshot-monitor
```

Before doing anything, make sure to grant execution permission to all scripts.
```
chmod +x *.sh
chmod +x *.py
```

### Screenshot Directory

First, configure Steam to copy screenshots to a consolidated directory.

1. Enter Desktop Mode
2. Open Steam
3. Open Steam Settings
4. Go to the "In-Game" tab
5. Enable "Save an Uncompressed Copy"
6. Set the Screenshot Folder to "/home/deck/Pictures/DCIM"

> **Note:** Steam has made an update to Desktop mode that prevents setting uncompressed screenshots directory. As a workaround, I've created a `setup-screenshots.py` script that will edit the config file directly to enable it. **Use this at your own risk.**
> 
> Run the script.
> ```
> ./setup-screenshots.py
> ```
> You will get confirmation on what's been updated, and backups to the config file will be created first.

### Config File

Next, setup your config file. Copy `config.json.example` to a new file titled `config.json`, and fill out
- "globalWebhook" - this is the webhook that will be triggered for all taken screenshots.
- "forumWebhook" - this is a webhook created on either a forum channel, or a text channel that will use threads for individual games

### Install Service

Finally, set up the systemctl service. This is what will allow the monitor to run in the background, and (hopefully) start automatically.

Run:
```
./install.sh
```

There are also helper scripts for `start.sh`, `stop.sh`, `restart.sh`, and `status.sh`. These are just wrappers around the systemctl commands since it's annoying typing them all the time.


## Usage

Using the screenshot monitor is as easy as taking a screenshot. It also works with [Decky Recorder](https://github.com/safijari/decky-recorder-fork), as long as your videos are stored in `/home/deck/Videos`.

Setting up threads for specific games is a bit more involved. First, create a `threads.json` file (or start the service for the first time). The file should have the following format:
```json
{
  "<APP_ID>": "<THREAD_ID>"
}
```

Maintaining this is annoying, so I've created a helper `add.py` script. 1. Run the screenshot service. 
2. Open the game you want to add to a thread
3. Take a screenshot. This will create a file called `lastgame` that contains the app id of the game you're trying to add.
4. Run: `./app.py <THREAD_ID>`

This will automatically update your threads file with the new game mapping. Remember to `./restart.sh` afterwards.