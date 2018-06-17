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
    xs = tree.xpath( '//maxDrawSizeInTiles' )

    for x in xs:
        x.text = x.text.split( ',' )[0].strip( '(' )

    # Goodwill is now an int: 10.00471
    xs = tree.xpath( '//goodwill' )

    for x in xs:
        x.text = str( int( float( x.text ) ) )

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

    # Format it nicely; takes space but it's easier to debug.
    tree.write( new_save, pretty_print=True, xml_declaration=True, encoding='utf-8' )
