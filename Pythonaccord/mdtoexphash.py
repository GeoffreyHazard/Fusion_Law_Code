#!/usr/bin/python
from parser import exphash

def mdtoexphash(map, prefixes = [""]):
    """Takes a str corresponding to filename, and a prefix if
    a referenced map and creates an expandable hash from corresponding .md file.
    """
    h = exphash({})
    for line in open(map+".md"):
        line = line[0:line.find("\n")] # removing newline
        if "=" in line and not line.endswith("="):
            keyval = line.split("=")
            k = key(keyval[0], prefixes)
            v = keyval[1]

            if "[" and "]" in v: # add to references
                v = v[v.find("[")+1:v.find("]")] # removing brackets
                h.refs.append([k,v])
            else: #add to direct values
                if not k in h:
                    h[k]=v
    return h

if __name__ == '__main__' :
    print "testing mdtoexphash..."
    h=mdtoexphash("form")
    print "h: " + str(h)
    print "h.refs: " + str(h.refs)
