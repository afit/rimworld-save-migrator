#!/usr/bin/python

# Look at the story mappings from rimworld.log
# cat rimworld.log | grep backstory | sort -u > stories.txt
# RimWorld handles the mappings, but pollutes its log when it does so.

f = open( 'stories.txt' )

print 'mappings = {'

for l in f.readlines():
    x = l.strip().split(' ')

    if 'Giving random' in l:
        continue
    elif 'or any close match' in l:
        print '\t\'%s\': \'VideoGamer91\',' % ( x[6] )
    else:
        print '\t\'%s\': \'%s\',' % ( x[6], x[11], )

print '}'
