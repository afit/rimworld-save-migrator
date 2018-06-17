from lxml import etree
from os.path import join, dirname, normpath, exists, split

from util.xml import insert_after


def migrate( save, seed, new_save ):
    # 1.0 unstable already handles a bunch of things, though it'll warn like hell:
    # Could not find class Need_Space while resolving node li. Trying to use RimWorld.Need instead.
    # Couldn't find exact match for backstory Politician92 , using closest match Politician1
    # Could not find think node with key 1694688019
    # etc.

    # Now for the smarter XML stuff
    tree = etree.parse( save )

    # "<maxDrawSizeInTiles>(26.4, 26.4)</maxDrawSizeInTiles>" should be
    # <maxDrawSizeInTiles>26.4</maxDrawSizeInTiles>
    xs = tree.xpath('//maxDrawSizeInTiles' )

    for x in xs:
        x.text = x.text.split( ',' )[0].strip( '(' )

    # Goodwill is now an int: 10.00471
    xs = tree.xpath('//goodwill' )

    for x in xs:
        x.text = str( int( float( x.text ) ) )

    # Could not load reference to Verse.ResearchProjectDef named IEDIncendiary
    # Could not load reference to Verse.ResearchProjectDef named Beds

    '''SaveableFromNode exception: System.ArgumentException: Can't load abstract class RimWorld.Verb_MeleeAttack
      at Verse.ScribeExtractor.SaveableFromNode[Verb] (System.Xml.XmlNode subNode, System.Object[] ctorArgs) [0x0015b] in C:\Dev\RimWorld\Assets\Scripts\Verse\SaveLoad\Scribe\Loader\ScribeExtractor.cs:100
    Subnode:
    <li Class="Verb_MeleeAttack"><loadID>Bow_Great450__Poke</loadID></li>'''

    # Format it nicely; takes space but it's easier to debug.
    tree.write( new_save, pretty_print=True, xml_declaration=True, encoding='utf-8' )
