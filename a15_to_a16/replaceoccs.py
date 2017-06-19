#!/usr/bin/python
import sys, subprocess, os

# Full instructions are here: https://www.reddit.com/r/RimWorld/comments/5jp9at/best_sit_down_updating_an_a15_save_to_a16/
# ...and there's a pastebin guide here: http://pastebin.com/HNFFsMBC
# You did read that, right?

# It's just a list of valid occupations in RimWorld A16
f = open( 'occupations.txt' )

# Read in the occupations, build a dict and strip the number off. We use the original as a key in the replacement.
occs = {}
for line in f:
    line = line.strip()
    key = ''.join([i for i in line if not i.isdigit()])
    occs[key] = line

# The input and output save files
original = open( 'input.rws' )
newfile = open( 'newsave.rws', 'wb' )

# Iterate through each line of the save file. It's XML, but we're relying on each
# object being on its own line, which A15 does. Not proper XML parsing, though.
for oline in original:
    test = oline

    # Iterate through the childhood lines, and replace them with the numbered
    # version from the text file.
    if test.strip().startswith('<childhood>'):
        test = test.strip()[11:-12]
        test = ''.join([i for i in test if not i.isdigit()])

        if test[-1] == '-':
            test = test[:-1]

        # There's no match with the text file, so let's just default.
        if not test in occs:
            print 'I cannot find %s, using VideoGamer94 instead' % test
            test = 'VideoGamer'

        print 'I need to match %s and I\'ve found %s' % ( test, occs[test] )

        newfile.write('<childhood>%s</childhood>\n' % occs[test] )
    elif test.strip().startswith('<adulthood>'):
        test = test.strip()[11:-12]
        test = ''.join([i for i in test if not i.isdigit()])

        if test[-1] == '-':
            test = test[:-1]

        # Iterate through the adulthood lines, and replace them with the numbered
        # version from the text file.
        if not test in occs:
            print 'I cannot find %s, using IntelligenceAgent4 instead' % test
            test = 'IntelligenceAgent'

        # There's no match with the text file, so let's just default.
        print 'I need to match %s and I\'ve found %s' % ( test, occs[test] )
        newfile.write('<adulthood>%s</adulthood>\n' % occs[test] )
    else:
        newfile.write(test)

original.close()
newfile.close()
