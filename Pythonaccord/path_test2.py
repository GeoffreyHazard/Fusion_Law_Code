#!/usr/bin/python

from parser2 import key
from parser2 import parsevalue
from parser2 import mdtoexphash
from parser2 import expand
from parser2 import render


def key_test():

    k = key(["Person.", "Name.", "Greek." , "First"])
    assert(k == "Person.Name.Greek.First")
    assert(k.path == ["Person.", "Name.", "Greek." , "First"])
    h = {"Person.Name.Greek.First": "Basilki"}
    assert(k in h)

    j = k.newvar("Last")
    assert(j == "Person.Name.Greek.Last")
    assert(j.path == ["Person.", "Name.", "Greek." , "Last"])
    assert(j not in h)
    h["Person.Name.Greek.Last"]= "Zarias"
    assert(j in h)

    z = j.prefix(" (Maternal)")
    assert(z == "Person.Name.Greek.Last (Maternal)")
    assert(z.path == ["Person.", "Name.", "Greek." , "Last", " (Maternal)"])
    assert(z not in h)
    h["Person.Name.Greek.Last (Maternal)"]= "Tsitsana"
    assert(z in h)

    assert(k.path == ["Person.", "Name.", "Greek.", "First"])
    i = k.deprefix()
    assert(k.path == ["Person.", "Name.", "Greek.", "First"])

    assert(k in h)
    assert(k == "Person.Name.Greek.First")
    assert(k.path == ["Person.", "Name.", "Greek.", "First"])

    assert(not i in h)
    assert(i == "Person.Name.First")
    assert(i.path == ["Person.", "Name.", "First"])
    h["Person.Name.First"]= "Alazar"
    assert(i in h)


    print "   - Key test passed!"

def parsevalue_test():
    val = "The {Defendant} has to resign on {Date}"
    ky = key(["Case1.", "Litigation.", "Resignation"])
    s = parsevalue(val, ky)
    assert(s == ["The ","Case1.Litigation.Defendant", " has to resign on ", "Case1.Litigation.Date",""])
    assert(s[1].path == ["Case1.", "Litigation.", "Defendant"])
    assert(s[3].path == ["Case1.", "Litigation.", "Date"])

    val = "Defendant"
    t = parsevalue(val)
    assert(t == ["Defendant"])
    assert(type(t[0]) == key)
    assert(t[0].path == ["Defendant"])

    print "   - parsevalue test passed!"

def mdtoexphash_test():
    h = mdtoexphash("root")
    assert(h == {"Person.Name.First":"Bob", "Name.MI":"B"})
    assert(h.refs == [["","keyterms"],["","form"]])
    assert(h.refs[0][0].path == ["", ""])
    assert(h.refs[1][0].path == ["", ""])

    h = mdtoexphash("root", key(["Case1.", "Doc2.", "Clause3."]))
    assert(h == {"Case1.Doc2.Clause3.Person.Name.First":"Bob", "Case1.Doc2.Clause3.Name.MI":"B"})
    assert(h.refs == [["Case1.Doc2.Clause3.","keyterms"],["Case1.Doc2.Clause3.","form"]])
    assert(h.refs[0][0].path == ["Case1.", "Doc2.", "Clause3.", ""])
    assert(h.refs[1][0].path == ["Case1.", "Doc2.", "Clause3.", ""])

    print "   - mdtoexphash test passed!"

def expand_test():

    h = mdtoexphash("root")
    h = expand(h, h.refs[0], 0)
    assert(h == {"Person.Name.First":"Bob", "Name.MI":"B", "Amount":"5$", "Provider":"Cactus Co."})

    h = mdtoexphash("keyterms")
    h = expand(h, h.refs[0], 0)
    assert(h == {"Amount":"5$", "Provider":"Cactus Co." ,"Person.Name.Full" : "{Name.First} {Name.MI}. {Name.Last}", "Person.Name.First":"Robert","Person.Name.Last":"Jackson"})
    assert(h.refs[0]== ["Person.City.", "Alabanza"])

    h = expand(h, h.refs[0], 0)
    assert(h == {"Person.City.Country":"Spain","Amount":"5$", "Provider":"Cactus Co." ,"Person.Name.Full" : "{Name.First} {Name.MI}. {Name.Last}", "Person.Name.First":"Robert","Person.Name.Last":"Jackson"})
    assert(not h.refs)

    print "   - expand test passed!"

def render_test():
    print "** "+render("doc", "root")+" **"


def get_tests():
    return [key_test, parsevalue_test, mdtoexphash_test, expand_test, render_test]

# DO NOT EDIT BELOW THIS LINE ==================================================

# The mainline runs all of the test functions in the list returned by get_tests
if __name__ == '__main__' :
    print '------------- Running tests -------------'
    for test in get_tests():
        test()
    print '------------- All tests passed! -------------'
