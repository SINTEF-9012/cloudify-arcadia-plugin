#mostly copied from https://stackoverflow.com/questions/24492895/comparing-two-xml-files-in-python

import xml.etree.ElementTree as ET


class XmlTree(object):

    @staticmethod
    def convert_string_to_tree(xmlString):
        return ET.fromstring(xmlString)

    def xml_isomorphic(self, x1, x2):

        if x1.tag != x2.tag:
            #print 'Tags do not match: %s and %s' % (x1.tag, x2.tag)
            return False
        for name, value in x1.attrib.items():
            if x2.attrib.get(name) != value:
                #print  'Attributes do not match: %s=%r, %s=%r' % (name, value, name, x2.attrib.get(name))
                return False
        for name in x2.attrib.keys():
            if name not in x1.attrib:
                #print  'x2 has an attribute x1 is missing: %s' % name
                return False
        if not self.text_compare(x1.text, x2.text):
            print 'text: %r != %r' % (x1.text, x2.text)
            return False
        if not self.text_compare(x1.tail, x2.tail):
            #print 'tail: %r != %r' % (x1.tail, x2.tail)
            return False
        cl1 = x1.getchildren()
        cl2 = x2.getchildren()
        if len(cl1) != len(cl2):
            print 'children length differs, %i != %i' % (len(cl1), len(cl2))
            return False
        
        equal_pairs = []
        children_tested = []
        for c1 in cl1:
            for c2 in cl2:
                if c2 not in children_tested:
                    result = self.xml_isomorphic(c1, c2)
                    if result:
                        equal_pairs.append((c1, c2))
                        children_tested.append(c2)
                        continue

        if len(equal_pairs) != len(cl1):
            print 'children are not isomorphic'
            return False

        return True

    def text_compare(self, t1, t2):
        """
        Compare two text strings
        :param t1: text one
        :param t2: text two
        :return:
            True if a match
        """
        if not t1 and not t2:
            return True
        if t1 == '*' or t2 == '*':
            return True
        return (t1 or '').strip() == (t2 or '').strip()