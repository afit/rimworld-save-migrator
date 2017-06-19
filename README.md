# RimWorld save game migrator

This repo contains a number of Python scripts to convert RimWorld
saves between different versions. The logic for these scripts came from [FMKirby](https://www.reddit.com/user/FMKirby)'s
mighty posts on reddit's [/r/RimWorld](https://www.reddit.com/r/RimWorld/).

Pull requests are gratefully received. Depending on how the save format in later
versions pans out, it may make sense to refactor this into a more general
mechanism.

For more on RimWorld, see the [official site](https://rimworldgame.com).

## Getting started

The scripts work on Windows, macOS and Linux and require Python 2.7 and `lxml`.
To install `lxml`, you'll want to run  `easy_install lxml`.
If you already know Python, you'll probably use `pip` and `virtualenv` for this.

If you have mods installed, you'll want to remove them first, and remove the
references to them from your save.

## A16 to A17 (June 2017)

In the `a16_to_a17` folder there's a script which will wholesale convert an A16
game to A17. In order to do this you'll need to create a new game in A17 with
the same seed as your A16 world, as the script will need some data for that. The
script gives some usage instructions, and [FMKirby's original post](https://www.reddit.com/r/RimWorld/comments/6gk9m9/that_time_again_a16_save_a17/)
is helpful, too.

## A15 to A16 (December 2016)

In the `a15_to_a16` folder there is a much simpler script which patches
occupations as part of the migration to A16. Unfortunately, the rest of the
upgrade logic is not in the script and must be done manually. You can find the
instructions for that on [reddit](https://www.reddit.com/r/RimWorld/comments/5jp9at/best_sit_down_updating_an_a15_save_to_a16/).

## Where are my saves?

On macOS, they're probably at:

`/Users/[username]/Library/Application\ Support/RimWorld/Saves`

On Windows, they're probably at:

`C:\Users\[username]\AppData\LocalLow\Ludeon\RimWorld\Saves`

Check [the wiki](http://rimworldwiki.com/wiki/Save_file) for more detail.
