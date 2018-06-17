# Handy utilities for munging XML, innit?

# Used by A17 only
def insert_after(element, new_element):
    parent = element.getparent()
    parent.insert( parent.index(element) + 1, new_element )

# Below used by A16 only
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
