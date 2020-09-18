'''
Ensures JOB variable standard

Notes:
hou.putenv DOESNT WORK
http://forums.odforce.net/topic/27174-job-variables-problem-with-setenv/
use hou.hscript(setenv VAR = VALUE) instead
'''


# check 456 script run with hython in command line tools
#print 'IN 456 SCRIPT'

def atHome():
    import sys
    import os
    #sys.platform != "win32": # check windows
    #    return False
    if os.environ['USERPROFILE'] != "C:\Users\Luis":
        return False
    return True




def main():
    ''' wrap this script in main to allow us to return to exit script early '''
    import os
    import hou
    import sys
    
    # abort when not at home computers
    # atHome = 'LF_HOME' in os.environ
    # if atHome == False:#os.path.exists(DEFAULT)==False:
    #   return
        #print 'not at home, aborting 456.py'
        # exit() / quit() does not work as expected here, see main()
        

    JOB = hou.getenv("JOB")
    HIP = hou.getenv("HIP")
    PROJ = "D:/projects/" #hou.getenv("PROJ") #find how to set variable without houdini.env
    DEFAULT = "C:/Users/Luis"
    

    if JOB == DEFAULT:
        if HIP != DEFAULT: # from a saved scene
            above = os.path.dirname(HIP) # get folder above 
            split = above.split("/houdini")
            if len(split) > 1: # houdini folder found       
                JOB = split[0]+"/houdini"
                #print 'JOB variable modified'
                #print 'from %s -> %s' % (hou.getenv("JOB"), JOB)

        else: # we are in an untitled scene or bad path         
            JOB = PROJ+"video/rnd/houdini"           
        hou.allowEnvironmentToOverwriteVariable("JOB", True)       
        hou.hscript("setenv JOB = %s" % JOB)
        hou.allowEnvironmentToOverwriteVariable("JOB", False)



        

    # def normpath(path):
    #   path = os.path.normpath(path)
    #   path = path.replace("\\", "/")
    #   return path

    # def isCorrect(variable):  
    #   if os.path.isdir(JOB) == False:
    #       return False
    #   if JOB == DEFAULT:
    #       print 'JOB is default'
    #       return False
    #   find = ["/","\\"]
    #   if any(item in variable[-1] for item in find):
    #       print 'JOB ends in slash'
    #       return False
    #   if JOB != normpath(JOB):
    #       print 'JOB is not equal to normpath(JOB)'
    #       return False
    #   return True


    #print(JOB, HIP, PROJ)

    # # only check HIPs that are in Project folder
    # if PROJ in HIP:
    #   #print 'yes proj in hip'
    #   if isCorrect(JOB) == False: 
    #       if HIP != DEFAULT:      
    #           #folders = HIP.split("/")
    #           find = "/houdini"
    #           idx = HIP.rfind(find)
    #           if idx > -1:            
    #               JOB = HIP[0:idx+len(find)]
    #               JOB = normpath(JOB)
    #           else:
    #               # go up one level           
    #               JOB = os.path.dirname(HIP)
    #               JOB = normpath(JOB)
    #               print JOB

    #           print 'JOB variable modified'
    #           print 'from %s -> %s' % (hou.getenv("JOB"), JOB)
    #           hou.hscript("setenv JOB = %s" % JOB)
    

''' execute in main function so we can use return to end script early. 
    quit()/exit() is overwritten by HOM and will cause houdini to exit '''
if __name__ == '__main__':
    if atHome():
        main()

