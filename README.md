# RimWorld save game migrator

This repo contains a number of Python scripts to convert RimWorld
saves between different versions.
For more on RimWorld, see the [official site](https://rimworldgame.com) or [/r/RimWorld](https://www.reddit.com/r/RimWorld/).

| Migration   | Supported          | Era |
| ----------- | ------------------ | --- |
| [A16 to A17](https://github.com/afit/rimworld-save-migrator/blob/master/upgrade_rws_a16_to_a17.py) | ✅ Fully automated | June 2017 |
| [A15 to A16](https://github.com/afit/rimworld-save-migrator/blob/master/upgrade_rws_a15_to_a16.py)  | ✅ Fully automated | December 2016 |
| A14 to A15  | [Manual guide](https://www.reddit.com/r/RimWorld/comments/4zrotj/guide_how_to_update_an_a14_save_to_a15/) | August 2016 |

In order to run these migrations, you'll first need to create a new saved game using the version you want to migrate to, with the same seed as the save you want to upgrade.

### Caveats

If you are upgrading multiple versions, load and save the migrated game at each stage.

* A16 to A17:
  * Implants will be reset. There is a [manual workaround](https://www.reddit.com/r/RimWorld/comments/6gk9m9/that_time_again_a16_save_a17/).
  * Some character backstories have been removed; they will be assigned random ones.
  * Some material stacks will be trimmed to 75.
* A15 to A16:
  * Body types will all be set to male: [more details](http://pastebin.com/HNFFsMBC).
  * You will be asked to name your settlement again.

## Requirements

The scripts work on Windows, macOS and Linux, and require Python 2.7.
Python is pre-installed on macOS and Linux. On Windows, it is available as a [free download](https://www.python.org/downloads/).
Make sure you get the 2.7 version, not the 3.x.

There's a single dependancy that the scripts require: `lxml`.
To install `lxml`, you'll want to run  `pip install lxml` in your Command Prompt or Terminal.
If you already know Python, you'll probably use `virtualenv` for this.

If you have mods installed, you'll want to remove them first, and remove the
references to them from your save.

## Analysing saves

These scripts include `analyse_saves.py`, a handy utility for extracting seeds and playtime from maps. If you run it, it looks like this:

```bash
$ python analyse_saves.py
Your saves should be at /Users/Guest/Library/Application Support/RimWorld/Saves...
a14_bogdan
 Version:       0.14.1249 rev944
 Seed:          bogdan (200, 150)
 Real playtime: 0:00:24
 Mods:          Core
a15_bogdan
 Version:       0.15.1284 rev141
 Seed:          bogdan (200, 150)
 Real playtime: 0:00:23
 Mods:          Core
a16_bogdan
 Version:       0.16.1393 rev538
 Seed:          bogdan (250, 1, 250)
 Real playtime: 0:00:26
 Mods:          Core
a17_bogdan
 Version:       0.17.1557 rev1154
 Seed:          bodgan (250, 1, 250)
 Real playtime: 0:00:12
 Mods:          Core
```

## Migrating saves

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

The `analyse_saves.py` script tells you this when you run it, but [the wiki](http://rimworldwiki.com/wiki/Save_file) has more detail.

On macOS, they're probably at:

`~/Library/Application Support/RimWorld/Saves`

On Windows, they're probably at:

`C:\Users\%username%\AppData\LocalLow\Ludeon Studios\RimWorld by Ludeon Studios\Saves`

On Linux, they're probably at:

`~/.config/unity3d/Ludeon Studios/RimWorld by Ludeon Studios/Saves`
