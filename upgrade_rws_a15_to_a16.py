#!/usr/bin/python
import sys, subprocess, os

from os.path import join, dirname, normpath, exists, split
from ast import literal_eval as make_tuple

try:
    from lxml import etree
except:
    print 'Couldn\'t load lxml. Make sure you have this library installed.\nTry running this:\n\tpip install lxml'
    exit(-1)

if len(sys.argv) != 3:
    print '''This script will patch your save to A16, saving it as a new file and adding "a16-" to the name. It won't modify your old saves. It requires two arguments:

    python upgrade_rws_a15_to_a16.py [a15-save-to-upgrade] [a16-save-with-same-seed]

- [a15-save-to-upgrade] should be the full path to your saved game.
- [a16-save-with-same-seed] second should be the full path to a fresh A16 saved game,
  generated with the same seed as your A15 game.

Like this:

    python upgrade_rws_a15_to_a16.py /path/to/my-save.rws /path/to/a16-same-seed.rws

Good luck! Fixes, etc. to https://github.com/afit/rimworld-save-migrator.'''
    exit(-1)

save = sys.argv[1]
a16 = sys.argv[2]
new_save = join( dirname( save ), 'a16-%s' % split( save )[1] )

if not exists(save):
    print 'The specified save file doesn\'t appear to exist.'
    exit(-1)

if not exists(a16):
    print 'The specified A16 file doesn\'t appear to exist.'
    exit(-1)

def insert_after_only(xpath_results_list, new_element):
    if len(xpath_results_list) > 1:
        raise Exception('There\'s more than one %s' % xpath_results_list[0].getroottree().getpath(xpath_results_list[0]) )

    parent = xpath_results_list[0].getparent()
    parent.insert( parent.index(xpath_results_list[0]) + 1, new_element )

def replace_singular(xpath_results_list, new_element):
    if len(xpath_results_list) > 1:
        raise Exception('There\'s more than one %s' % xpath_results_list[0].getroottree().getpath(element[0]) )

    xpath_results_list[0].getparent().replace( xpath_results_list[0], new_element )

def copy_element_to_section( xpath_results_list, section ):
    if len(xpath_results_list) > 1:
        raise Exception('There\'s more than one %s' % xpath_results_list[0].getroottree().getpath(xpath_results_list[0]) )

    section.insert( -1, xpath_results_list[0] )

# It's just a list of valid occupations in RimWorld A16
f = open( join( 'resources', 'occupations_a15_to_a16.txt' ) )

# Read in the occupations, build a dict and strip the number off. We use the original as a key in the replacement.
occs = {}
for line in f:
    line = line.strip()
    key = ''.join([i for i in line if not i.isdigit()])
    occs[key] = line

f.close()

# Let's do all dumb replacements first.
fin = open( save, 'r' )
fout = open( new_save, 'w' )

for line in fin:
    # Iterate through each line of the save file. It's XML, but we're relying on each
    # object being on its own line, which A15 does. Not proper XML parsing, though.
    oline = line
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

        #print 'I need to match %s and I\'ve found %s' % ( test, occs[test] )

        fout.write('<childhood>%s</childhood>\n' % occs[test] )
        continue
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
        #print 'I need to match %s and I\'ve found %s' % ( test, occs[test] )
        fout.write('<adulthood>%s</adulthood>\n' % occs[test] )
        continue

    # 3c
    line = line.replace( 'MalariBlock', 'Penoxycyline' )

    # 8d, 8e
    line = line.replace( '<map>', '<map><li><uniqueID>0</uniqueID>' )
    line = line.replace( '</map>', '</li></map>' )

    # 10
    line = line.replace( 'carrier>', 'carryTracker>' )
    line = line.replace( 'carrier IsNull', 'carryTracker IsNull' )

    # 11
    line = line.replace( 'container>', 'innerContainer>' )

    # 12
    line = line.replace( 'skinWhiteness', 'melanin' )

    # 13
    line = line.replace( '<story>', '<story>\n<bodyType>Male</bodyType>' )

    # 14
    line = line.replace( '</thing>', '<map>0</map>\n</thing>' )

    # 17
    line = line.replace( 'PackMuffalo', 'Muffalo' )
    line = line.replace( 'PackDromedary', 'Dromedary' )

    # 20
    line = line.replace( 'Megatherium', 'Megasloth' )

    # 21
    line = line.replace( 'MakeStoneBlocks', 'MakeStoneBlocksAny' )

    # 22
    line = line.replace( 'temperatureGrid', 'temperatureCache' )

    # 23a
    line = line.replace( 'cameraMap', 'rememberedCameraPos' )
    # 23b
    line = line.replace( 'cameraRootPos', 'rootPos' )
    # 23c
    line = line.replace( 'desiredSize', 'rootSize' )

    # 27a, 27b
    line = line.replace( '<innerThing', '<innerContainer>\n<maxStacks>1</maxStacks>\n<innerList>\n<li' )
    line = line.replace( '</innerThing>', '</li>\n</innerList>\n</innerContainer>' )

    # 28a, 28b
    line = line.replace( '<containedThings>', '<innerContainer>\n<innerList>' )
    line = line.replace( '</containedThings>', '</innerList>\n</innerContainer>' )

    # 29
    # Uhuh.

    # 32
    line = line.replace( '<inventory>', '<inventory>\n<itemsNotForSale />' )

    fout.write( line )

fin.close()
fout.close()

# Let's ensure we have a template save from the newer version pre-generated, so
# we can pull bits from it.
new_template = etree.parse(a16)

# Now for the smarter XML stuff
tree = etree.parse( new_save )

# 1. Add visibleMapIndex
tree.xpath('//game' )[0].insert( 0, etree.XML( '<visibleMapIndex>0</visibleMapIndex>' ) )

# 2. Replace playSettings
replace_singular( tree.xpath( '//playSettings' ), etree.XML( '''<playSettings>
<showLearningHelper>True</showLearningHelper>
<showZones>True</showZones>
<showColonistBar>True</showColonistBar>
<autoHomeArea>True</autoHomeArea>
<lockNorthUp>True</lockNorthUp>
<usePlanetDayNightSystem>True</usePlanetDayNightSystem>
<expandingIcons>True</expandingIcons>
</playSettings>''' ) )

# 3a, 3b
tree.xpath('//researchManager/progress/keys' )[0].insert( 0, etree.XML( '<li>Refining</li>' ) )
tree.xpath('//researchManager/progress/keys' )[0].insert( 0, etree.XML( '<li>TransportPod</li>' ) )
tree.xpath('//researchManager/progress/values' )[0].insert( 0, etree.XML( '<li>0</li>' ) )
tree.xpath('//researchManager/progress/values' )[0].insert( 0, etree.XML( '<li>0</li>' ) )

# 4a
copy_element_to_section( new_template.xpath( '//world/info/planetCoverage' ), tree.xpath('//world/info')[0] )
copy_element_to_section( new_template.xpath( '//world/info/overallRainfall' ), tree.xpath('//world/info')[0] )
copy_element_to_section( new_template.xpath( '//world/info/overallTemperature' ), tree.xpath('//world/info')[0] )

# 4d
for map_size in tree.xpath( '//world/info/size' ):
    map_size.getparent().remove( map_size )
copy_element_to_section( new_template.xpath( '//world/info/initialMapSize' ), tree.xpath('//world/info')[0] )

# 5
copy_element_to_section( new_template.xpath( '//world/uniqueIDsManager/nextWorldObjectID' ), tree.xpath('//world/uniqueIDsManager')[0] )
copy_element_to_section( new_template.xpath( '//world/uniqueIDsManager/nextMapID' ), tree.xpath('//world/uniqueIDsManager')[0] )
copy_element_to_section( new_template.xpath( '//world/uniqueIDsManager/nextAreaID' ), tree.xpath('//world/uniqueIDsManager')[0] )
copy_element_to_section( new_template.xpath( '//world/uniqueIDsManager/nextAncientCryptosleepCasketGroupID' ), tree.xpath('//world/uniqueIDsManager')[0] )

# 6a
faction_colours = []
for faction_colour in new_template.xpath('//factionManager/allFactions/li/colorFromSpectrum'):
    faction_colours.append( faction_colour )

i = 0
for faction in tree.xpath('//factionManager/allFactions/li'):
    faction.insert( 0, faction_colours[i] )
    i += 1

# 6b
for avoidGridBasic in tree.xpath('//factionManager/allFactions/li/avoidGridBasic'):
    replace_singular( [avoidGridBasic,], etree.XML( '''<avoidGridsBasic>
<keys />
<values />
</avoidGridsBasic>''' ) )

for avoidGridSmart in tree.xpath('//factionManager/allFactions/li/avoidGridSmart'):
    replace_singular( [avoidGridSmart,], etree.XML( '''<avoidGridsSmart>
<keys />
<values />
</avoidGridsSmart>''' ) )

# 6c
for homeSquare in tree.xpath('//world/factionManager/allFactions/li/homeSquare'):
    homeSquare.getparent().remove( homeSquare )

# 7
insert_after_only(
    tree.xpath('//worldPawns' ),
    new_template.xpath('//worldObjects' )[0] )

# 8a
for maps in tree.xpath('/savegame/game/map'):
    maps.tag = 'maps'

# 8b
copy_element_to_section( new_template.xpath( '/savegame/game/maps/li/mapInfo/tile' ), tree.xpath('/savegame/game/maps/li/mapInfo')[0] )
copy_element_to_section( new_template.xpath( '/savegame/game/maps/li/mapInfo/parent' ), tree.xpath('/savegame/game/maps/li/mapInfo')[0] )

# 8c
worldCoords = tree.xpath( '/savegame/game/maps/li/mapInfo/worldCoords' )[0]
worldCoords.getparent().remove( worldCoords )

# 9
insert_after_only(
    tree.xpath('/savegame/game/maps' ),
    etree.XML ( '''<cameraMap>
<camRootPos>(175.9, 21.6, 163.3)</camRootPos>
<desiredSize>17.45855</desiredSize>
</cameraMap>''' ) )

# 15
for pawn_dead in tree.xpath('//pawnsDead/li'):
    pawn_dead.insert( 0, etree.XML( '<map>-2</map>' ) )

# 16
for corpse in tree.xpath('//corpse'):
    corpse.getparent().remove( corpse )

# 18
for seed in tree.xpath('//thing[@Class="Seed"]'):
    seed.getparent().remove( seed )

# 19
for trait in tree.xpath('//story/traits/allTraits/li/def'):
    if trait.text == 'TemperaturePreference':
        trait.text = 'Kind'
        trait.getparent().remove( trait.getnext() )

# 24
insert_after_only(
    tree.xpath('//rememberedCameraPos' ),
    etree.XML ( '''<mineStrikeManager>
<strikeRecords />
</mineStrikeManager>''' ) )

# 25
for corpse in tree.xpath('//thing[@Class="Corpse"]/innerPawn'):
    name = corpse.text
    corpse.getparent().insert( 0, etree.XML( '''<innerContainer>
<maxStacks>1</maxStacks>
<contentsLookMode>Reference</contentsLookMode>
<innerList>
<li>%s</li>
</innerList>
</innerContainer>''' % name ) )
    corpse.getparent().remove( corpse )

# 26a, 26b
area_index = 0
areas_seen = {}

# We diverge slightly from the instructions here to make it work properly.
for area in tree.xpath('//areaManager/areas/li[starts-with(@Class, "Area_")]'):
    # Give all uniquely classed (not named!) areas a number
    if area.attrib['Class'] not in areas_seen.keys():
        areas_seen[ area.attrib['Class'] ] = area_index
        area.insert( 0, etree.XML( '<ID>%s</ID>' % area_index ) )
        area_index += 1

# Find all references to those areas, and change the name to reflect the number
# That's what the instructions say. But real world it always seems to be -1,
# so we'll do that instead.
for area_reference in tree.xpath('//areaAllowed[starts-with(text(), "Area_")]' ):
    # ie. So 'Area_Named_People_outside' becomes 'Area_-1_Named_People_outside'
    if area_reference.text.startswith('Area_Named_'):
        area_reference.text = area_reference.text.replace( 'Area_', 'Area_-1_' )
    else:
        area_reference.text = area_reference.text.replace( 'Area_', 'Area_%s_' % areas_seen[ area_reference.text ] )

# 26c
map_size_tuple = new_template.xpath( '//mapInfo/size' )[0] # Looks like '(250, 1, 250)'
map_size_tuple = make_tuple( map_size_tuple.text )

for innerGrid in tree.xpath('//innerGrid'):
    innerGrid.append( etree.XML( '<mapSizeX>%s</mapSizeX>' % map_size_tuple[0] ) )
    innerGrid.append( etree.XML( '<mapSizeZ>%s</mapSizeZ>' % map_size_tuple[2] ) )

# 30
for drafter in tree.xpath('//savegame/game/maps/li/things/thing/drafter/drafter'):
    # Remove the inner drafter element
    old_parent = drafter.getparent()
    drafter.getparent().getparent().append( drafter )
    old_parent.getparent().remove( old_parent )

# 31
for def_ate in tree.xpath('//li/def[text()="AteInImpressiveDiningRoom"]'):
    for sibling in def_ate.itersiblings():
        if sibling.tag == 'age':
            def_ate.getparent().insert( 1, etree.XML( '<otherPawn>null</otherPawn>' ) )
            def_ate.getparent().remove( sibling )
            break

# 34
insert_after_only(
    tree.xpath('//deepResourceGrid' ),
    etree.XML ( '''<weatherDecider>
<curWeatherDuration>124018</curWeatherDuration>
</weatherDecider>''' ) )

insert_after_only(
    tree.xpath('//deepResourceGrid' ),
    etree.XML ( '''<damageWatcher>
<everDamage>378</everDamage>
</damageWatcher>''' ) )

# Not in FMKirby's docs, but it's important.
for nullJobQueue in tree.xpath('//jobs/jobQueue[@IsNull="True"]'):
    del nullJobQueue.attrib['IsNull']
    nullJobQueue.insert( 0, etree.XML( '<jobs/>' ) )

# Finally, let's update the version string!
tree.xpath('/savegame/meta/gameVersion')[0].text = '0.16.1393 rev538'

tree.write( new_save, pretty_print=True, xml_declaration=True, encoding='utf-8' )
