# RimWorld save game migrator

This repo contains a number of Python scripts to convert RimWorld
saves between different versions. The logic for these scripts came from [FMKirby](https://www.reddit.com/user/FMKirby)'s
mighty posts on reddit's [/r/RimWorld](https://www.reddit.com/r/RimWorld/).
For more on RimWorld, see the [official site](https://rimworldgame.com).

| Migrate to  | Migrate from | Supported | Name | More info |
| ----------- | ------------ | --------- | -----| --------- |
| A17         | A16          | ✅ Fully automated | [`upgrade_rws_a16_to_a17.py`](https://github.com/afit/rimworld-save-migrator/blob/master/a16_to_a17/upgrade_rws_a16_to_a17.py) | [reddit](https://www.reddit.com/r/RimWorld/comments/6gk9m9/that_time_again_a16_save_a17/) |
| A16         | A15          | Partly automated | [`replaceoccs.py`](https://github.com/afit/rimworld-save-migrator/blob/master/a15_to_a16/replaceoccs.py) | [Pastebin](http://pastebin.com/HNFFsMBC) |

Pull requests are gratefully received. Depending on how the save format in later
versions pans out, it may make sense to refactor this into a more general
mechanism.

### A16 to A17 (June 2017)

In the `a16_to_a17` folder there's a script which will wholesale convert an A16
game to A17. In order to do this you'll need to create a new game in A17 with
the same seed as your A16 world, as the script will need some data for that.

### A15 to A16 (December 2016)

In the `a15_to_a16` folder there is a much simpler script which patches
occupations as part of the migration to A16. Unfortunately, the rest of the
upgrade logic is not in the script and must be done manually. You can find the
instructions for that on [reddit](https://www.reddit.com/r/RimWorld/comments/5jp9at/best_sit_down_updating_an_a15_save_to_a16/).

## Getting started

The scripts work on Windows, macOS and Linux and require Python 2.7 and `lxml`.
To install `lxml`, you'll want to run  `easy_install lxml`.
If you already know Python, you'll probably use `pip` and `virtualenv` for this.

If you run the script without `lxml` installed, it'll tell you what to do:

```bash
$ python upgrade_rws_a16_to_a17.py
Couldn't load lxml. Make sure you have this library installed.
Try running this:
	easy_install lxml
```

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

## Where are my saves?

On macOS, they're probably at:

`~/Library/Application Support/RimWorld/Saves`

On Windows, they're probably at:

`C:\Users\%username%\AppData\LocalLow\Ludeon Studios\RimWorld by Ludeon Studios\Saves`

On Linux, they're probably at:

`~/.config/unity3d/Ludeon Studios/RimWorld by Ludeon Studios/Saves`

Check [the wiki](http://rimworldwiki.com/wiki/Save_file) for more detail.
