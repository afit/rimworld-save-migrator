from lxml import etree
from os.path import join, dirname, normpath, exists, split

from util.xml import insert_after


def migrate( save, a17, new_save ):
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

        line = line.replace( 'MapCondition_Eclipse', 'GameCondition_Eclipse' )

        line = line.replace( '<primary>', '<equipment>\n<innerList>\n<li>' )
        line = line.replace( '</primary>', '</li>\n</innerList>\n</equipment>' )
        line = line.replace( '<primary IsNull="True"/>', '<equipment>\n<innerList />\n</equipment>' )
        line = line.replace( '<primary IsNull="True" />', '<equipment>\n<innerList />\n</equipment>' )

        line = line.replace( '<wornApparel>', '<wornApparel>\n<innerList>' )
        line = line.replace( '</wornApparel>', '</innerList>\n</wornApparel>' )
        line = line.replace( '<wornApparel/>', '<wornApparel>\n<innerList />\n</wornApparel>' )
        line = line.replace( '<wornApparel />', '<wornApparel>\n<innerList />\n</wornApparel>' )

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

    # Let's fix stuff happening with bodies.
    import a16tables as a16
    import a17tables as a17

    for hediffset in tree.xpath('//hediffSet/hediffs'):

        if hediffset.getparent().getparent().getparent().xpath('name')[0].xpath('nick'):
            # Human
            name = hediffset.getparent().getparent().getparent().xpath('name')[0].xpath('nick')[0].text
            kind = hediffset.getparent().getparent().getparent().xpath('def')[0].text
        elif len( hediffset.getparent().getparent().getparent().xpath('name')[0].getchildren() ) == 0:
            # No name yet
            name = hediffset.getparent().getparent().getparent().xpath('id')[0].text
            kind = hediffset.getparent().getparent().getparent().xpath('kindDef')[0].text
        else:
            # If it's an animal it won't have a nick
            name = hediffset.getparent().getparent().getparent().xpath('name')[0].xpath('name')[0].text
            kind = hediffset.getparent().getparent().getparent().xpath('kindDef')[0].text

        #print 'Name: %s' % name, kind

        for li in hediffset.iterchildren():
            if li.attrib.has_key('Class'): # and li.attrib['Class'] in ['Hediff_AddedPart', 'Hediff_Implant']:
                if li.xpath('partIndex'):

                    # Look up this kind's body
                    if kind in a16.type_bodies.keys():
                        a16_body = a16.type_bodies[kind]

                    if kind in a17.type_bodies.keys():
                        a17_body = a17.type_bodies[kind]

                    a16_parts = a16.body_parts[a16_body]
                    a17_parts = a17.body_parts[a17_body]

                    parts = li.xpath('partIndex')

                    if len(parts) == 1:
                        old_part_index = int( parts[0].text )
                        part = a16_parts[ old_part_index ]

                        try:
                            new_part_index = str( a17_parts.index( part ) )
                        except ValueError:
                            if part == 'Jaw':
                                part = 'AnimalJaw'
                                new_part_index = str( a17_parts.index( part ) )
                            else:
                                raise

                        #print '\t%s\'s part is: %s, changing from %s to %s' % ( name, part, old_part_index, new_part_index )

                        parts[0].text = new_part_index

    tree.write( new_save, pretty_print=True, xml_declaration=True, encoding='utf-8' )
