# RimWorld save game migrator

This repo contains a number of Python scripts to convert RimWorld
saves between different versions.
For more on RimWorld, see the [official site](https://rimworldgame.com) or [/r/RimWorld](https://www.reddit.com/r/RimWorld/).

| Migration   | Supported          | Era | More info |
| ----------- | ------------------ | --------- | -----| --------- |
| [A16 to A17](https://github.com/afit/rimworld-save-migrator/blob/master/a16_to_a17/upgrade_rws_a16_to_a17.py) | ✅ Fully automated | June 2017 | [reddit](https://www.reddit.com/r/RimWorld/comments/6gk9m9/that_time_again_a16_save_a17/) |
| [A15 to A16](https://github.com/afit/rimworld-save-migrator/blob/master/a15_to_a16/replaceoccs.py)  | Partly automated   | December 2016 | [Pastebin](http://pastebin.com/HNFFsMBC) |

In order to run these migrations, you'll first need to create a new saved game using the version you want to migrate to.

### A16 to A17

In the `a16_to_a17` folder there's a script which will wholesale convert an A16
game to A17. In order to do this you'll need to create a new game in A17 with
the same seed as your A16 world, as the script will need some data for that.

### A15 to A16

In the `a15_to_a16` folder there is a much simpler script which patches
occupations as part of the migration to A16. Unfortunately, the rest of the
upgrade logic is not in the script and must be done manually. You can find the
instructions for that on [reddit](https://www.reddit.com/r/RimWorld/comments/5jp9at/best_sit_down_updating_an_a15_save_to_a16/).

## Requirements

The scripts work on Windows, macOS and Linux, and require Python 2.7.
Python is pre-installed on macOS and Linux. On Windows, it is available as a [free download](https://www.python.org/downloads/).
Make sure you get the 2.7 version, not the 3.x.

There's a single dependancy that the scripts require: `lxml`.
To install `lxml`, you'll want to run  `pip lxml` in your Command Prompt or Terminal.
If you already know Python, you'll probably use `virtualenv` for this.

If you have mods installed, you'll want to remove them first, and remove the
references to them from your save.

## Usage

The A16 to A17 script is simple to run. If you run it without any arguments, it'll tell you how:

```bash
$ python upgrade_rws_a16_to_a17.py
This script will patch your save to A17, saving it as a new file and adding "a17-" to the name. It won't modify your old saves. It requires two arguments:

    python upgrade_rws_a16_to_a17.py [a16-save-to-upgrade] [a17-save-with-same-seed]

- [a16-save-to-upgrade] should be the full path to your saved game.
- [a17-save-with-same-seed] second should be the full path to a fresh A17 saved game,
  generated with the same seed as your A16 game.

Like this:

    python upgrade_rws_a16_to_a17.py /path/to/my-save.rws /path/to/a17-same-seed.rws

Good luck! Fixes, etc. to https://github.com/afit/rimworld-save-migrator.
```

## Contributing improvements and reporting problems

Please use the [issues tracker](https://github.com/afit/rimworld-save-migrator/issues) to report any bugs.
Pull requests are gratefully received.

The logic for these scripts came from FMKirby's posts on reddit.

## Where are my saves?

On macOS, they're probably at:

`~/Library/Application Support/RimWorld/Saves`

On Windows, they're probably at:

`C:\Users\%username%\AppData\LocalLow\Ludeon Studios\RimWorld by Ludeon Studios\Saves`

On Linux, they're probably at:

`~/.config/unity3d/Ludeon Studios/RimWorld by Ludeon Studios/Saves`

Check [the wiki](http://rimworldwiki.com/wiki/Save_file) for more detail.
