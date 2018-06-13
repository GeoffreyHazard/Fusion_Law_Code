#!/usr/bin/python
import parser
from parser import key
from parser import parsevalue
from mdtoexphash import exphash

def key_class_test():
    """print tests for the key class"""


    k = key("First",["Person.","Name."])
    print "key looks like: " + k
    print "its prefixes are: " + str(k.prefixes)

    nk = key("Last", k.prefixes)
    print "passing on key's prefs to new key"
    print "new key looks like: " + nk
    print "its prefixes are: " + str(nk.prefixes)

    nk = nk.deprefix()
    print "now deprefixing to look like: " + nk
    print "new list of prefixes is: "  + str(nk.prefixes)

    h = exphash({"Person.Name.First":"Iakob"})
    assert(k in h)

def parsevalue_test():
    """ a very simple print test for parsevalue method"""

    k = key("Restrict", ["Company.","Leadership.","CTO."])
    v = "{Name} is liable to restriction in {State}"

    print "a key : " + k
    print "has a value : " + v
    s = parsevalue(k,v)
    print "parsed value is: " + str(s)

    print "prefixes of 2nd element are: " + str(s[1].prefixes)

def expand_test():
    """ another simple print test for expand method"""
    exphash({"Island.Cap.Name":"Micro Parisi","Island.":"Kea"})


if __name__ == '__main__' :
    print "TESTING..."
    print
    key_class_test()
