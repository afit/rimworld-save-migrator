from lxml import etree

from util.xml import insert_after, insert_after_only, replace_singular, copy_element_to_section

import pytest


class TestXml(object):
    ''' Tests for the XML utils. '''

    def test_insert_after(self):
        tree = etree.XML( '''<savegame><game><world/></game></savegame>''' )

        n = tree.xpath('//world' )[0]
        x = etree.XML( '<after/>' )
        insert_after( n, x )

        assert etree.tostring(tree) == '<savegame><game><world/><after/></game></savegame>'

    def test_insert_after_only(self):
        tree = etree.XML( '''<savegame><game><world/></game></savegame>''' )

        n = tree.xpath('//world' )
        x = etree.XML( '<after/>' )
        insert_after_only( n, x )

        assert etree.tostring(tree) == '<savegame><game><world/><after/></game></savegame>'

        tree = etree.XML( '''<savegame><game><world/><world/></game></savegame>''' )

        n = tree.xpath('//world' )
        x = etree.XML( '<after/>' )

        with pytest.raises(Exception) as e_info:
            insert_after_only( n, x )

    def replace_singular(self):
        tree = etree.XML( '''<savegame><game><world/></game></savegame>''' )

        n = tree.xpath('//world' )
        x = etree.XML( '<after/>' )
        replace_singular( n, x )

        assert etree.tostring(tree) == '<savegame><game><after/></game></savegame>'

        tree = etree.XML( '''<savegame><game><world/><world/></game></savegame>''' )

        n = tree.xpath('//world' )
        x = etree.XML( '<after/>' )

        with pytest.raises(Exception) as e_info:
            replace_singular( n, x )

    def copy_element_to_section(self):
        tree = etree.XML( '''<savegame><game><world/></game></savegame>''' )

        n = tree.xpath('//world' )
        x = etree.XML( '<after/>' )
        copy_element_to_section( x, n )

        assert etree.tostring(tree) == '<savegame><game><world><after/></world></game></savegame>'

        tree = etree.XML( '''<savegame><game><world/><world/></game></savegame>''' )

        n = tree.xpath('//world' )
        x = etree.XML( '<after/>' )

        with pytest.raises(Exception) as e_info:
            copy_element_to_section( x, n )
