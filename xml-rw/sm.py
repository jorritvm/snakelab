#The SM class will manage all the sites - favorites
from PyQt4.QtCore import *
from PyQt4.QtXml import *

class sm(object):

    def __init__(self):
        
        #upon creation of an sm object we need to load our xml file data into
        #our own internal type
        self.filename = "sm.xml"
        self.sites = self.importxml()
    
    def addsite(self, name, ip, port, login, password):
        x = dict()
        x["name"] = name
        x["ip"] = ip
        x["port"] = port
        x["login"] = login
        x["password"] = password
        self.sites[name] = x
    
    def delsite(self, name):
        try:
            del self.sites[name]
        except (KeyError), e:
            print "This site could not be found: %s!" % str(e)
            
    #importxml reads the sm-xml file and converts all data into a python dictionary format
    def importxml(self):
        sites = dict()
        dom = QDomDocument()
        fh = None #initialize
        try: 
            #try to open xml file, raise exception on error
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError, unicode(fh.errorString())
            #try to parse xml file, raise exception on error
            if not dom.setContent(fh):
                raise ValueError, "Could not parse XML"
        except (IOError, OSError, ValueError), e:
            #if we have stumbled upon an error we let the user know
            print "uh oh! " + unicode(e)
        finally:
            #we make sure our file handle is closed 
            if fh is not None:
                fh.close()
        
        #since we've gotten this far, it's now safe to populate our own dictionaries
        root = dom.documentElement() #ANY XML FILE CAN ONLY HAVE ONE ROOT ELEMENT
        #loop over the site nodes
        node = root.firstChild()
        while not node.isNull():
            if node.toElement().tagName() == "site": #just to make sure
                settings = dict() #create a new list of settings per site
                #loop over site-settings
                childnode = node.firstChild()
                while not childnode.isNull():
                    #put the value in the dictionary, using the same keys as the xml file
                    settings[str(childnode.toElement().tagName())] = str(childnode.toElement().text())
                    childnode = childnode.nextSibling()
            else: 
                print "Some other element that is not a site is present in your %s!" % self.filename
            #we add our settings to the dictionary of sites
            name = settings["name"]
            sites[name] = settings
            node = node.nextSibling()
        return sites
            
    #exportxml writes all data from the dictionary sites into the xml file
    def exportxml(self,sites):
        fh = None
        try:
            #try to open xml file if possible, else throw exception
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError, unicode(fh.errorString())
            #create a textstream that operates on your xml file
            stream = QTextStream(fh) 
            stream.setCodec("UTF-8") #standard
            #now we start writing our settings from our dictionaries to our stream
            stream << "<sites>\n"
            for item in sites.items():
                    stream << "<site>\n"
                    for tup in item[1].items():
                        stream << "<" << tup[0] << ">" << tup[1] << "</" << tup[0] << ">\n"
                    stream << "</site>\n"
            stream << "</sites>\n"
        except (IOError, OSError), e:
            #if we have stumbled upon an error we let the user know
            print "Failed to export: %s" % e
        finally:
            #we make sure our file handle is closed
            if fh is not None:
                fh.close()
    
x = sm()

#x.addsite("azerty","1354.1.21.5","6969","logiiiin","paaaswoord")
#x.exportxml(x.sites)

#x.delsite("laatstesitename222")
#x.exportxml(x.sites)