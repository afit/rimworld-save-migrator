from lxml import etree
from os.path import join, dirname, normpath, exists, split

from util.xml import insert_after

import b18tables, u1tables


def migrate( save, new_save ):
    # 1.0 unstable already handles a bunch of things, though it'll warn like hell:
    # Couldn't find exact match for backstory Politician92 , using closest match Politician1
    # Could not find think node with key 1694688019
    # etc.

    # Now for the smarter XML stuff
    tree = etree.parse( save )

    # "<maxDrawSizeInTiles>(26.4, 26.4)</maxDrawSizeInTiles>" should be
    # <maxDrawSizeInTiles>26.4</maxDrawSizeInTiles>
    xs = tree.xpath( '//maxDrawSizeInTiles' )
    for x in xs:
        x.text = x.text.split( ',' )[0].strip( '(' )

    # Goodwill is now an int: 10.00471
    xs = tree.xpath( '//goodwill' )
    for x in xs:
        x.text = str( int( float( x.text ) ) )

    # jobgivers can't be looked up. Who knows why? Not me.
    # "Could not find think node with keyX"
    xs = tree.xpath( '//lastJobGiverKey' )
    for x in xs:
        x.getparent().remove( x )

    # On one hand, relying on the order of the XML is horrible. On the other...
    # No, it's always grim. We do it in reverse order, otherwise we'd change the
    # order as we went.

    # Could not load reference to Verse.ResearchProjectDef named IEDIncendiary
    n = tree.xpath('//researchManager/progress/keys/li' )[33] # IEDIncendiary
    n.getparent().remove( n )
    n = tree.xpath('//researchManager/progress/values/li' )[33] # "Beds"
    n.getparent().remove( n )

    # Could not load reference to Verse.ResearchProjectDef named Beds
    n = tree.xpath('//researchManager/progress/keys/li' )[7] # IEDIncendiary
    n.getparent().remove( n )
    n = tree.xpath('//researchManager/progress/values/li' )[7]
    n.getparent().remove( n )

    '''SaveableFromNode exception: System.ArgumentException: Can't load abstract class RimWorld.Verb_MeleeAttack
      at Verse.ScribeExtractor.SaveableFromNode[Verb] (System.Xml.XmlNode subNode, System.Object[] ctorArgs) [0x0015b] in C:\Dev\RimWorld\Assets\Scripts\Verse\SaveLoad\Scribe\Loader\ScribeExtractor.cs:100
    Subnode:
    <li Class="Verb_MeleeAttack"><loadID>Bow_Great450__Poke</loadID></li>'''

    xs = tree.xpath( '//li[@Class="Verb_MeleeAttack"]' )
    for x in xs:
        x.attrib['Class'] = 'Verb_MeleeAttackDamage'
        x.insert( 1, etree.XML( '<li>0</li>' ) )

    # Could not load reference to RimWorld.TraitDef named GreenThumb
    xs = tree.xpath('//def[text()="GreenThumb"]' )
    for x in xs:
        x.getparent().remove( x )

    # GreenThumbHappy issues
    xs = tree.xpath('//def[text()="GreenThumbHappy"]' )
    for x in xs:
        x.getparent().getparent().remove( x.getparent() )

    # Could not find class Need_Space while resolving node li.
    xs = tree.xpath( '//li[@Class="Need_Space"]' )
    for x in xs:
        x.getparent().remove( x )

    # Spawned NeutroamineX with stackCount 393 but stackLimit is 150. Truncating.
    # Big stacks!
    xs = tree.xpath( '//thing/def[text()="Neutroamine"]' )
    for x in xs:
        count = x.getparent().xpath('stackCount')[0]
        if int( count.text ) > 150:
            x.text = '150'

    # Current map is null after loading but there are maps available. Setting current map to [0].
    n = tree.xpath( '/savegame/game' )[0]
    n.insert( 0, etree.XML( '<currentMapIndex>0</currentMapIndex>' ) )

    # Oh my god, some animals now have underscores in their names. But not all.
    # Let's use a map
    kinds = {
        # Old, new
        'WolfTimber': 'Wolf_Timber',
        'WolfArctic': 'Wolf_Arctic',
        'FoxArctic': 'Fox_Arctic',
        'FoxRed': 'Fox_Red',
        'FoxFennec': 'Fox_Fennec',
        'PolarBear': 'Bear_Polar',
        'GrizzlyBear': 'Bear_Grizzly',
        'Mechanoid_Centipede': 'Mech_Centipede',
        'Mechanoid_Scyther': 'Mech_Scyther',
    }

    extra_kinds = {
        'Centipede': 'Mech_Centipede',
        'Scyther': 'Mech_Scyther',
    }

    for kind in kinds.keys():
        xs = tree.xpath( '//def[text()="%s"] | //kindDef[text()="%s"] | //kind[text()="%s"]' % ( kind, kind, kind ) )
        for x in xs:
            x.text = kinds[kind]

    for kind in extra_kinds.keys():
        xs = tree.xpath( '//def[text()="%s"] | //kindDef[text()="%s"] | //kind[text()="%s"]' % ( kind, kind, kind ) )
        for x in xs:
            x.text = extra_kinds[kind]

    # Let's fix stuff happening with bodies.
    for hediffset in tree.xpath('//hediffSet/hediffs'):
        # We need the kind to map it, and the name really helps with debugging this.
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

                    found = False

                    # Let's map that new kind back to the old to look it up
                    if kind in kinds.values():
                        for o, n in kinds.iteritems():
                            if n == kind:
                                found = True
                                old_kind = o
                                break

                    if not found:
                        old_kind = kind

                    # Look up this kind's body
                    if not old_kind in b18tables.type_bodies.keys():
                        raise Exception( 'Kind "%s" not found in old bodies' % old_kind )
                    old_body = b18tables.type_bodies[old_kind]

                    if not kind in u1tables.type_bodies.keys():
                        raise Exception( 'Kind "%s" not found in new bodies' % kind )
                    new_body = u1tables.type_bodies[kind]

                    old_parts = b18tables.body_parts[old_body]
                    new_parts = u1tables.body_parts[new_body]

                    #print kind, old_body, new_body

                    parts = li.xpath('partIndex')

                    if len(parts) == 1:
                        old_part_index = int( parts[0].text )
                        part = old_parts[ old_part_index ]

                        try:
                            new_part_index = str( new_parts.index( part ) )
                        except ValueError:
                            # It seems everything is now ambidextrous.
                            old_part = part

                            if 'Left' in part:
                                part = part.replace( 'Left', '' )
                            if 'Right' in part:
                                part = part.replace( 'Right', '' )
                            if 'Front' in part:
                                part = part.replace( 'Front', '' )
                            if 'Rear' in part:
                                part = part.replace( 'Rear', '' )

                            # Digit contexts
                            if 'HandMechanicalMiddle' in part:
                                part = part.replace( 'HandMechanicalMiddle', 'Mechanical' )
                            if 'HandMiddle' in part:
                                part = part.replace( 'HandMiddle', '' )
                            if 'HandRing' in part:
                                part = part.replace( 'HandRing', '' )
                            if 'HandMechanicalIndex' in part:
                                part = part.replace( 'HandMechanicalIndex', 'Mechanical' )
                            if 'HandIndex' in part:
                                part = part.replace( 'HandIndex', '' )
                            if 'HandMechanicalPinky' in part:
                                part = part.replace( 'HandMechanicalPinky', 'MechanicalFinger' )
                            if 'HandPinky' in part:
                                part = part.replace( 'HandPinky', 'Finger' )
                            if 'HandMechanicalThumb' in part:
                                part = part.replace( 'HandMechanicalThumb', 'MechanicalFinger' )
                            if 'HandThumb' in part:
                                part = part.replace( 'HandThumb', 'Finger' )
                            if 'FootLittle' in part:
                                part = part.replace( 'FootLittle', '' )
                            if 'FootMiddle' in part:
                                part = part.replace( 'FootMiddle', '' )
                            if 'FootFourth' in part:
                                part = part.replace( 'FootFourth', '' )
                            if 'FootSecond' in part:
                                part = part.replace( 'FootSecond', '' )
                            if 'FootBig' in part:
                                part = part.replace( 'FootBig', '' )

                            if part == 'Rib':
                                part = 'Ribcage' # FIXME multiple injured ribs = multiple ribcages!

                            if part == old_part:
                                raise

                            try:
                                new_part_index = str( new_parts.index( part ) )
                            except:
                                #print old_part, part, new_parts
                                raise

                        #print '\t%s\'s part is: %s, changing from %s to %s' % ( name, part, old_part_index, new_part_index )

                        parts[0].text = new_part_index

    # Let's update the version string
    tree.xpath('/savegame/meta/gameVersion')[0].text = '1.0.1936 rev835'

    # Format it nicely; takes space but it's easier to debug.
    tree.write( new_save, pretty_print=True, xml_declaration=True, encoding='utf-8' )
