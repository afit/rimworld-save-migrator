#!/usr/bin/python
import sys, subprocess, os

from os.path import join, dirname, normpath, exists, split

try:
    from lxml import etree
except:
    print 'Couldn\'t load lxml. Make sure you have this library installed.\nTry running this:\n\tpip install lxml'
    exit(-1)

if len(sys.argv) != 3:
    print '''This script will patch your save to A17, saving it as a new file and adding "a17-" to the name. It won't modify your old saves. It requires two arguments:

    python upgrade_rws_a16_to_a17.py [a16-save-to-upgrade] [a17-save-with-same-seed]

- [a16-save-to-upgrade] should be the full path to your saved game.
- [a17-save-with-same-seed] second should be the full path to a fresh A17 saved game,
  generated with the same seed as your A16 game.

Like this:

    python upgrade_rws_a16_to_a17.py /path/to/my-save.rws /path/to/a17-same-seed.rws

Good luck! Fixes, etc. to https://github.com/afit/rimworld-save-migrator.'''
    exit(-1)

save = sys.argv[1]
a17 = sys.argv[2]
new_save = join( dirname( save ), 'a17-%s' % split( save )[1] )

if not exists(save):
    print 'The specified save file doesn\'t appear to exist.'
    exit(-1)

if not exists(a17):
    print 'The specified A17 file doesn\'t appear to exist.'
    exit(-1)

def insert_after(element, new_element):
    parent = element.getparent()
    parent.insert( parent.index(element) + 1, new_element )

# Let's ensure we have a vanilla A17 save pre-generated, so
# we can pull bits from it.
tree = etree.parse(a17)
a17_gameConditionManager = tree.xpath('/savegame/game/world/gameConditionManager' )[0]
a17_storyState = tree.xpath('/savegame/game/world/storyState' )[0]
a17_components = tree.xpath('/savegame/game/world/components' )[0]

# Let's do all dumb replacements first.
fin = open( save, 'r' )
fout = open( new_save, 'w' )

for line in fin:
    line = line.replace( 'PersonalShield', 'ShieldBelt' )
    line = line.replace( 'mapConditionManager', 'gameConditionManager' )

    line = line.replace( '<primary>', '<equipment>\n<innerList>\n<li>' )
    line = line.replace( '</primary>', '</li>\n</innerList>\n</equipment>' )
    line = line.replace( '<primary IsNull="True"/>', '<equipment>\n<innerList />\n</equipment>' )
    line = line.replace( '<wornApparel>', '<wornApparel>\n<innerList>' )
    line = line.replace( '</wornApparel>', '</innerList>\n</wornApparel>' )
    line = line.replace( '<wornApparel/>', '<wornApparel>\n<innerList />\n</wornApparel>' )
    line = line.replace( '<layingDown>True</layingDown>', '<layingDown>LayingSurface</layingDown>' )
    line = line.replace( '<layingDown>False</layingDown>', '<layingDown>NotLaying</layingDown>' )
    line = line.replace( '<resourceContainer>', '<resourceContainer Class="Verse.ThingOwner`1[Verse.Thing]">' )
    line = line.replace( 'AssignedDrugsSet' , 'DrugPolicy' )

    fout.write( line )

fin.close()
fout.close()

# Now for the smarter XML stuff
tree = etree.parse( new_save )

# Add new research keys
insert_after(
    tree.xpath('//researchManager/progress/keys/li[text()="ElectricSmelting"]' )[0],
    etree.XML( '<li>PackagedSurvivalMeal</li>' )
)

insert_after(
    tree.xpath('//researchManager/progress/keys/li[text()="Mortars"]' )[0],
    etree.XML( '<li>SmokepopBelt</li>' )
)

insert_after(
    tree.xpath('//researchManager/progress/keys/li[text()="MultiAnalyzer"]' )[0],
    etree.XML( '<li>LongRangeMineralScanner</li>' )
)

insert_after(
    tree.xpath('//researchManager/progress/keys/li[text()="PoweredArmor"]' )[0],
    etree.XML( '<li>ShieldBelt</li>' )
)

# Fill in the values for those keys. Inefficient, but easy to read.
insert_after(
    tree.xpath('//researchManager/progress/values/li' )[47], # 48th
    etree.XML( '<li>0</li>' )
)

insert_after(
    tree.xpath('//researchManager/progress/values/li' )[37], # 38th
    etree.XML( '<li>0</li>' )
)

insert_after(
    tree.xpath('//researchManager/progress/values/li' )[27], # 28th
    etree.XML( '<li>0</li>' )
)

insert_after(
    tree.xpath('//researchManager/progress/values/li' )[20], # 21st
    etree.XML( '<li>0</li>' )
)

# Add two chunks under the tutor close. In reverse order.
insert_after(
    tree.xpath('//tutor' )[0],
    etree.XML( '<components />' )
)

insert_after(
    tree.xpath('//tutor' )[0],
    etree.XML( '<dateNotifier><lastSeason>Spring</lastSeason></dateNotifier>' )
)

# Add a chunk after the outer worldObjects.
insert_after(
    # Note there's another worldObjects nested in this one.
    # The insert comes after the outer one.
    tree.xpath('/savegame/game/world/worldObjects' )[0],
    etree.XML ( '''<settings>
<defaultCareForHumanlikeColonists>Best</defaultCareForHumanlikeColonists>
<defaultCareForAnimalColonists>HerbalOrWorse</defaultCareForAnimalColonists>
<defaultCareForHumanlikeColonistPrisoners>HerbalOrWorse</defaultCareForHumanlikeColonistPrisoners>
<defaultCareForHumanlikeNeutrals>HerbalOrWorse</defaultCareForHumanlikeNeutrals>
<defaultCareForAnimalNeutrals>HerbalOrWorse</defaultCareForAnimalNeutrals>
<defaultCareForHumanlikeEnemies>HerbalOrWorse</defaultCareForHumanlikeEnemies>
</settings>''' ) )

# Let's insert the three parts from the A17 save.
insert_after(
    tree.xpath('/savegame/game/world/settings' )[0],
    a17_storyState
)

insert_after(
    tree.xpath('/savegame/game/world/storyState' )[0],
    a17_gameConditionManager
)

insert_after(
    tree.xpath('/savegame/game/world/gameConditionManager' )[0],
    a17_components
)

# And onwards.
insert_after(
    tree.xpath('//savegame/game/maps/li/mineStrikeManager' )[0],
    etree.XML ( '''<storyState>
<lastThreatBigTick>-1</lastThreatBigTick>
<lastFireTicks>
<keys />
<values />
</lastFireTicks>
</storyState>''' ) )

# Add RoadInfo before the components close.
components = tree.xpath('//savegame/game/maps/li/components' )[0]
components.append( etree.XML( '''<li Class="RoadInfo">
<roadEdgeTiles />
</li>''' ) )

# It gets a little bit more fiddly now. We're working with Things.
things = tree.xpath( '''
//li[@Class="Building_Sarcophagus"]/innerContainer | //thing[@Class="Building_Sarcophagus"]/innerContainer |
//li[@Class="Building_Grave"]/innerContainer | //thing[@Class="Building_Grave"]/innerContainer |
//li[@Class="MinifiedThing"]/innerContainer | //thing[@Class="MinifiedThing"]/innerContainer |
//li[@Class="Building_AncientCryptosleepCasket"]/innerContainer | //thing[@Class="Building_AncientCryptosleepCasket"]/innerContainer |
//thing[@Class="ActiveDropPod"]/contents/innerContainer |
//thing[@Class="DropPodIncoming"]/contents/innerContainer |
//li[@Class="CryptosleepCasket"]/innerContainer | //thing[@Class="CryptosleepCasket"]/innerContainer |
//li[@Class="TransportPod"]/innerContainer | //thing[@Class="TransportPod"]/innerContainer''')

for thing in things:
    thing.attrib['Class'] = 'Verse.ThingOwner`1[Verse.Thing]'

# Here's Traders
traders = tree.xpath('//worldObjects/worldObjects/li[@Class="FactionBase"]/trader' )

for trader in traders:
    trader.attrib['Class'] = 'FactionBase_TraderTracker'
    trader.addprevious( etree.XML( '''<rewards Class="Verse.ThingOwner`1[Verse.Thing]">
<maxStacks>1</maxStacks>
<innerList />
</rewards>''' ) )
    trader.addprevious( etree.XML( '<expiration>-1</expiration>' ) )
    trader.addprevious( etree.XML( '<previouslyGeneratedInhabitants />' ) )

# Finally, let's update the version string!
tree.xpath('/savegame/meta/gameVersion')[0].text = '0.17.1557 rev1154'

# Not in FMKirby's docs, but it's important.
for guest in tree.xpath('//guest'):
    insert_after( guest, etree.XML( '<guilt IsNull="True"/>' ) )

# Let's fix body parts. For now, we'll restore the missing ones, and bind the
# add-ons and implants.
for hediffset in tree.xpath('//hediffSet/hediffs'):
    for li in hediffset.iterchildren():
        if li.attrib.has_key('Class'):
            #print li.attrib['Class'], li.xpath('partIndex')[0].text, li.xpath('def')[0].text
            if li.attrib['Class'] in ['Hediff_AddedPart', 'Hediff_Implant']:
                part = li.xpath('partIndex')[0]

                part_mapping = {
                    '28': '26', # Brain
                    '29': '27', # Eye
                    '30': '28', # Eye
                    '35': '35', # Arm
                    # Other A17 defs
                    # 36 is left humerus
                    # 38 is left hand
                    # 39 is left pinky
                    # 40 is left ring finger
                    '39': '37', # Left radius
                    '45': '46', # Arm
                    '55': '56', # Leg
                    '64': '65', # Leg
                }

                if part.text in part_mapping.keys():
                    part.text = part_mapping[part.text]
            # Restore all missing parts
            elif li.attrib['Class'] in ['Hediff_MissingPart', 'HediffWithComps', 'Hediff_Injury']:
                li.getparent().remove( li )

tree.write( new_save, pretty_print=True, xml_declaration=True, encoding='utf-8' )
