'''
Functions used in various locations such as shelf tools or 123 / 456.py
'''
import hou

def setSceneVar():
    '''
    todo for replacing $HIP when in backup / deadline files
    '''
    pass


def setCacheVar(overwrite=False):
    '''
    Sets $CACHE variable as alternative to HIP/SCENE
    '''
    current_cache = hou.getenv("CACHE")
    if current_cache != None and not overwrite:
            return # its already defined
    prismjob = hou.getenv("PRISMJOB")
    if prismjob != None:
        hip = hou.getenv("HIP")
        if hip != None:
            prismjob = Path(prismjob)
            hip = Path(hip)
        if hip.as_posix().startswith(prismjob.as_posix()):            
            end = hip.as_posix()[len(prismjob.parent.as_posix()):]
            CACHE_DIR = Path("S:/hou_cache")            
            CACHE_DIR = Path(CACHE_DIR, end)
            
            #hou.putenv("CACHE", CACHE_DIR.as_posix())
            # set using hscript so that it shows in alias+var window
            hou.hscript( "set -g {} = {}".format("CACHE",CACHE_DIR.as_posix()) )