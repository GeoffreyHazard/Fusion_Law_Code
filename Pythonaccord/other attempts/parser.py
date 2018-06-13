#!/usr/bin/python
import re

def render(val, map):
    """In: a string for a key or series of keys to expand (really a value),
    and another string being the name of the root map (without the .md extention
    for example)
    Out: a string representing the fully rendered document (though eventually
    should be an annotated string with tags to where each part came from)
    Purpose: to render a full document from a graph of maps
    """
    s = parsevalue(val)
    h = mdtoexphash(map)
    print ">>> H AT START LOOKS LIKE: " + str(h)
    print ">>> WITH REFS: " + str(h.refs)
    print " $$$$$$$$ SHOULD MATCH " + str(h.refs[0][0].path)
    doc = []

    print "s is : " + str(s)
    while s:
        print
        print "MAP NOW LOOKS LIKE " + str(h)
        e = s.pop(0)
        if type(e) is key:
            print e + " is a key!"
            if e in h:
                print e + " is in hashmap!"
                s[0:0]= parsevalue(h[e], e.path) #push to top of stack
            else:
                print "looking at references"
                for i in range(len(h.refs)):
                    if e.startswith(h.refs[i][0]):
                        print "EXPANDING REF " + str(h.refs[i])
                        print "$$$$$$$$$$$ REF key has path " + str(h.refs[i][0].path)
                        h = expand(h, h.refs[i], i)
                        s.insert(0,e) #push back onto stack
                        break
                if i is len(h.refs) and not len(e.path) is 1:
                        s.insert(0,e.deprefix())
        else:
            doc.append(e)

    return "".join(doc)

def expand(map, ref , p):
    """ In: the root dict and a list of two strings representing the
    prefix of the reference and the reference itself, along with p,
    a priority representing the position of the reference in the map's
    list of references
    Out: an dict with all the info from reference
    """
    print "CALLING EXPAND"
    ref[0].path.append("")
    print "ref [0]'s path is now: " + str(ref[0].path)

    newMap = mdtoexphash(ref[1], ref[0].path)
    print "EXPANDED MAP LOOKS LIKE: " + str(newMap)
    print "with refs: " +str(newMap.refs)
    newMap.update(map)
    #all references of newMap placed where reference to this map used to be
    map.refs[p:p+1] = newMap.refs
    newMap.refs = map.refs

    return map

def parsevalue( v,  k = key("") ):
    """In: the value to be parsed and the entire prefixes of key (including the base keyname
    itself)
    Out: a list alternating text and keys to be expanded
    """
    #splitting value @ curly braces
    l = re.compile("[\\{\\}]").split(v)

    if len(l) is 1: # make a key of this only element in list
        l[0] = k.newvar([l[0]])
        return l
    else:
        for n in range(len(l)):
            if n%2 !=0:
                l[n] = k.newvar([l[n]])
    return l

class key(str):
    """Keys are strings that also have a path attribute. They take in this list
    to be instantiated
    """
    def __new__(cls, path):
        """ We need to override __new__ to take in list since str is immutable class
        In: a list of strings
        """
        pathedKey = str.__new__(cls, "".join(path))
        pathedKey.path = path
        return pathedKey

    def newvar(self, var):
        """In: a string representing a varirable (found in a value)
        Out: a new key with the last element of current key's path changed to
        the variable
        """
        return key(self.path[0:-1]+[var])

    def prefix(self, k):
        """In: a string representing an unpathed key (abstracted from a path an
        unparsed map)
        Out: a key with the unpathed key added to the end of current key's full path
        """
        return key(self.path+[k])


    def deprefix(self):
        """Out: a new key with the second to last element in path removed
        TODO: perhaps improve efficiency of list splice
        """
        return key(self.path[0:-2]+[self.path[-1]])


class exphash(dict):
    """A subclass of the dict class, the expandable hash
    class also has an attribute that is a list called
    refs of references. Each reference is a list
    of two stings, the first being the prefix and the
    second the map name.
    """
    def __init__(self,data):
        dict.__init__(self,data)
        self.refs = []



def mdtoexphash(map, path = [""]):
    """Takes a str corresponding to filename, and a prefix if
    a referenced map and creates an expandable hash from corresponding .md file.
    """
    h = exphash({})
    for line in open(map+".md"):
        line = line[0:line.find("\n")] # removing newline

        if "=" in line and not line.endswith("="):

            keyval = line.split("=")
            print "----- in mdtoexphash -------"

            path[-1] = keyval[0]
            print "reading line: " + str(keyval)
            print "path for new key is: " + str(path)

            k = key(path)
            v = keyval[1]

            if "[" and "]" in v: # add to references
                v = v[v.find("[")+1:v.find("]")] # removing brackets
                h.refs.append([k,v])
            else: #add to direct values
                if not k in h:
                    h[k]=v
    return h

if __name__ == '__main__' :
    print "testing parser..."
    print

    print "*" + render("doc","root") +"*"

    print
    print "finished!"
