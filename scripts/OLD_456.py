'''
Runs on scene open
Wrapped in try except to prevent houdini hanging on launch
Disabled because rvfx 456.py more important. how do we have multiple 456?
'''
try:    
    from pathlib import Path
    from LF import utils

    utils.setCacheVar()
except Exception as error:
    # handle the exception
    print("An exception occurred in LF 456.py:", error)



