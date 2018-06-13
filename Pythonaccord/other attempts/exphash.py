#!/usr/bin/python


class exphash(dict):
    """A subclass of the dict class, the expandable hash
    class also has an attribute that is a list called
    refs of references. Each reference is a list
    of two stings, the first being the prefix and the
    second the map name.
    """
    def __init__(self,data):
        print "made new exphash! "
        print "data is of type " + str(type(data))
        dict.__init__(self,data)
        self.keys = {}
        self.refs = []
        
    def __getitem__(self, key):
        return dict.__getitem__(self,key)




if __name__ == '__main__' :

    h = exphash({"2":"two"})
    print h["2"]

    data = {"2":"two", "3":"four"}
    print {v:k for k,v in data.items}
