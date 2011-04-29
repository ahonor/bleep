## {{{ http://code.activestate.com/recipes/410469/ (r5)
#import cElementTree as ElementTree
from xml.etree.ElementTree import ElementTree, XMLParser

class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        childrenNames = []        
        childrenNames = [child.tag for child in parent_element.getchildren()]

        if parent_element.items(): #attributes
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                #print len(element), element[0].tag, element[1].tag
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                    # treat like list - we assume that if the first two tags
                    # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                    # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))

                if childrenNames.count(element.tag) > 1:
                    try:
                        currentValue = self[element.tag]
                        currentValue.append(aDict)
                        self.update({element.tag: currentValue})
                    except: #the first of its kind, an empty list must be created
                        self.update({element.tag: [aDict]}) #aDict is written in [], i.e. it will be a list

                else:
                    self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})
## end of http://code.activestate.com/recipes/410469/ }}}

if __name__ == "__main__":
    xmlstring = """<?xml version="1.0" encoding="iso-8859-1"?>
<notification status="succeeded" executionId="111" trigger="success">
 <executions count="1">
  <execution status="succeeded" href="http://strongbad:4440/execution/follow/111" id="111">
   <user>admin
   </user>
   <date-started unixtime="1302737583374">2011-04-13T23:33:03Z
   </date-started>
   <date-ended unixtime="1302737583884">2011-04-13T23:33:03Z
   </date-ended>
   <job id="18">
    <name>test tracker notification
    </name>
    <group>bleep fun
    </group>
    <project>examples
    </project>
    <description>test out the notification features
    </description>
   </job>
   <description>echo hi
   </description>
  </execution>
 </executions>
</notification>
"""
    parser = XMLParser()    
    tree = parser.feed(xmlstring)
    root = parser.close()
    xmldict = XmlDictConfig(root)
    print xmldict
