from os.path import splitext, basename
from lxml import etree

from util.exceptions import MisformedSaveError


class Save(object):

    def __init__( self, path ):
        self.name = splitext( basename( path ) )[0]
        self.path = path
        try:
            self.tree = etree.parse( path )
        except etree.XMLSyntaxError, e:
            raise MisformedSaveError( e.message )

    @property
    def version(self):
        return self.tree.xpath('/savegame/meta/gameVersion' )[0].text

    @property
    def versions(self):
        return [int(i) for i in self.version.split( ' ' )[0].split( '.' )]

    @property
    def seed(self):
        return self.tree.xpath('/savegame/game/world/info/seedString' )[0].text

    @property
    def playtime(self):
        playtime = self.tree.xpath('/savegame/game/info/realPlayTimeInteracting' )[0].text
        m, s = divmod( float(playtime), 60)
        h, m = divmod(m, 60)
        return '%d:%02d:%02d' % (h, m, s)

    @property
    def size(self):
        majorVersion = int( self.version.split('.')[0] )
        minorVersion = int( self.version.split('.')[1] )

        if majorVersion == 1:
            return self.tree.xpath('/savegame/game/world/info/initialMapSize' )[0].text
        elif minorVersion >= 16:
            return self.tree.xpath('/savegame/game/maps/li/mapInfo/size' )[0].text
        return self.tree.xpath('/savegame/game/world/info/size' )[0].text

    @property
    def mods(self): # Build a dict representing mods.
        modIds = self.tree.xpath('/savegame/meta/modIds/li' )
        modNames = self.tree.xpath('/savegame/meta/modNames/li' )
        i, mods = 0, {}

        for name in modNames:
            id = modIds[i].text
            if id == name.text: id = None
            mods[ name.text ] = id
            i += 1

        return mods
