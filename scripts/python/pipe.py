




def ensureDirectory(path):
    '''
    ensures path is a valid directory for use in pipe tools
    '''
    find = ["/","\\"]
    if any(item in path[-1] for item in find):
        return path[:-1]
    else:
        return path

def resetJOB():
    JOB = hou.getenv("JOB")
    HIP = hou.getenv("HIP")
    DEFAULT = "C:/Users/Luis"
    if HIP != DEFAULT:              
        find = "/houdini"
        idx = HIP.rfind(find)
        if idx > -1:            
            JOB = HIP[0:idx+len(find)]
            JOB = normpath(JOB)     
        else:
            # go up one level           
            JOB = os.path.dirname(HIP)
            JOB = normpath(JOB)
            print JOB
            #hou.putenv("JOB", JOB)

        print 'JOB variable modified'
        hou.hscript("setenv JOB = %s" % JOB)


def toDigit(word):
    return int(filter(lambda x: x.isdigit(), word))

###
'''
Parameter callback helpers
'''




def listVersions(node):
    directory = os.path.normpath( node.parm("directory").eval() )
    component = os.path.normpath( node.parm("component").eval() )

    names = os.listdir( os.path.join(directory, component) )
    numbers = list( map( to_digit , names) )
    return dict(zip(names, numbers))

    




###


def normpath(path):
    path = os.path.normpath(path)
    path = path.replace("\\", "/")
    return path

class Cache:
    def __init__(self):
        self.directory = None
        self.component = None       
        self.version = None 

    def listComponents(self):
        return os.listdir(directory)

    def listVersions(self):
        return os.listdir(os.path.join(self.directory, self.component))

    def listWedges(self):
        folder = os.path.join(self.directory, self.component, self.version)
        files = os.listdir(folder)
        files = map( lambda x: x.split('.')[0].split('_')[-1], files)
        files = set(files)
        return files

    def versionLast(self):
        ver = self.listVersions()       
        def to_digit(word):
            return int(filter(lambda x: x.isdigit(), word))
        
        return max(list(map( to_digit , ver)))
        
        


'''
cache.component
cache.components()
cache.components()[0].versions()

dir.components()
components(dir)?
components.versions

all i need is to store strings / lists . 
can still use userdata but this lib has to be ambig
'''
