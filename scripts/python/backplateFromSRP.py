"""
Sets a camera's backplate from a shotgun submission

Logic:
    User inputs shotreview version, tags, & camera
    Query shotreview version & find image sequence
    If jpg:
        set camera backplate to image sequence path
    else:
        make new plate directory in /images/
        rvio exr to jpg in new directory
        set camera backplate to new jpg sequence


To run put the following in a houdini shelf tool:
    import sys
    import os

    isAlreadyImported = 'backplateFromSRP' in sys.modules
    path = '/net/homes/lfos/myStuff/myHoudini/python/'
    if path not in sys.path: sys.path.insert(0, path)
    import backplateFromSRP
    if isAlreadyImported: reload(backplateFromSRP)
            
"""

print '\n NEW RUN ______________ \n'

# __ imports __

from plassetapi.session import Session
from plassetapi.session.search import (VersionFilter, RelationshipFilter, 
                                       AncestryFilter)

from productionInfo import ProductionInfo
from shotReview import ShotReview

import hou
import os
import subprocess
import glob
import toolutils
                                       
# __ VARIABLES __

# Defaults
SHOW = os.environ["PL_SHOW"]
DIVISION = os.environ["PL_DIVISION"]
SEQUENCE = os.environ["PL_SEQ"]
SHOT = os.environ["PL_SHOT"]
VERSION = str(1)

try:
    CAMERA = hou.selectedNodes()[0]
except IndexError:
    CAMERA = hou.node("/obj/cam1/")
    
print "cam = {}".format(CAMERA)

fasset_cam_path = "/Camera01/rig_group/rig/reference_GRP/rig_GRP/control_GRP/render_GRP/render_:cameraLeft"


input = hou.ui.readMultiInput(message="Input shotreview details",
                              buttons=("Ok", "Cancel"),
                              input_labels=("Show", "Division", "Sequence", "Shot", "Version"),
                              initial_contents=(SHOW, DIVISION, SEQUENCE, SHOT, VERSION),
                              default_choice=0, close_choice=1)
                  


if input[0]==1:
    quit()

SHOW = input[1][0]
DIVISION = input[1][1]
SEQUENCE = input[1][2]
SHOT = input[1][3]
VERSION = input[1][4]
#CAMERA = input[1][5]

#input = hou.ui.selectNode()


'''
# DEBUG
SHOW = "cr"
DIVISION = "film"
SEQUENCE = "brb999"
SHOT = "brb999_1910"
VERSION = 482
'''

# __ functions __

def select_camera(node):
    pass

def check_is_camera(node):
    '''
    Checks the given node is a valid camera
    '''
    cam_type = hou.nodeType(hou.objNodeTypeCategory(), "cam")
    if node.type() == cam_type:
        return True
    else:
        raise Exception("Camera invalid")
        
        
def output_path(version):
    '''
    Generates the expected output path if we need to re-export the shotreview image sequence
    '''
    images_path = getImagesDirectory()
    naming = "Plate_v{0}".format(str(version))
    plate_path = "{0}{1}".format(images_path, naming)               
    plate_out_seq = "{0}/{1}.#.jpg".format(plate_path, naming)    
    print "Default path:\n%s \n" % plate_out_seq
    return plate_out_seq

    
def check_already_exists(path):
    '''
    Checks if files exist at the given path
    '''
    path = path.replace(".#.", ".*.")
    matches = glob.glob(path)
    if len(matches)>0:
        print 'Plate already exists \n'
        return True
        
    return False 
    
    def check_is_valid_sequence(sequence_path):
    '''
    Checks the given image sequence is valid for use as a houdini camera background
    '''
    if sequence_path.split(".")[-1] not in ['exr', 'tiff', 'mov']:
        # check if aspect ratio is standard 1:1
        res, ratio = get_real_resolution(sequence_path)
        if int(ratio)!=1:
            return False
        else:
            return True
    else:
        print 'Sequence not valid'
        return False
        
        
def getImagesDirectory():
    '''
    Returns the image directory inside the houdini folder
    Based on {SHOT}/work/{USER}/houdini/images
    '''    
    shot = os.environ.get("PL_SHOT_PATH", "")
    user = os.environ.get("USER",'unknown')
    exportPath = '%s/work/%s/houdini/images/' % (shot, user)
    return exportPath
    

def get_real_resolution(img_path):
    '''
    Uses rvls to find the true resolution of the image (if pixelAspectRatio was 1.0)
    This is needed to convert an EXR with a non 1.0 ratio to jpeg which doesn't support non 1.0 ratios
    '''
    command = "rvls -x {0}".format(img_path)

    output = ""
    try:
        output = subprocess.check_output(["rvls", "-x", img_path])
    except subprocess.CalledProcessError, e:
        output = "rvls stdout output:\n", e.output

    # string parsing
    res = []
    ratio = 1
    for line in output.splitlines():
        if 'Resolution' in line:
            words=line.replace(",","").split()
            x = words[1]
            y = words[3]
            res = [x,y]            
        if ('EXR/pixelAspectRatio' in line) or ('JPEG/PixelAspect' in line):
            words = line.split()
            ratio = words[-1]           

    return (res, ratio)


def resolution_by_ratio(res, ratio):
    x = res[0]
    y = res[1]

    doUpres = False
    if doUpres:
        # enlarge to match
        x = int( int(res[0]) * float(ratio) )
        y = int(res[1])
    else:
        # shrink to match
        x = int(res[0])
        y = int ( int(res[1]) * 1.0/float(ratio) )

    return [x,y]    


def make_local_sequence(in_path, out_path):
    '''
    Wrapper for RVIO - converts an image sequence using RV    
    '''
    out_directory = out_path[0:out_path.rfind("/")]
    
    if not os.path.exists(out_directory):
        print "No directory found, making new directory at:\n%s" % out_directory
        os.makedirs(out_directory)
        
    resolution, ratio = get_real_resolution(in_path)
    
    doResize = int(ratio)!=1
    if doResize is True:
        resolution = resolution_by_ratio(resolution, ratio)        

    rvio_command = "rvio {0} -o {1} &".format(in_path, out_path)    
    
    # resizes to account for different aspect ratios that houdini cant deal with
    if doResize is True:
        rvio_command = "rvio [ -pa 1.0 {0} ] -resize {1} {2} -o {3} -outsrgb &".format(
                        in_path, resolution[0], resolution[1], out_path)    

    subprocess.call(rvio_command, shell=True)
    print "rvio executed - converting image sequence now"
    print "command: \n {}".format(rvio_command)
    return out_path
    

def image_sequence_from_sr(show, division, sequence, shot, version):
    '''
    Gets the image sequence by querying the shotgun database
    Uses prodtools API to convert SHOW to JOB NUMBER
    '''
    
    job_number = ProductionInfo.getJobNumber(show)
    
    sr = ShotReview()
    sr.connect()
    submission = sr.get_submission(job_number, division, sequence, shot, version=version)
    out = submission.source
    sr.disconnect()
    return out
    
    def image_sequence_from_pl(shot, version):
    '''
    No longer used
    Finds the image sequence by retrieving the shotreview asset and tracing the dependency relationship
    '''
    session = Session()
    filter_shotreview = VersionFilter("shotreview")
    filter_shotreview.tags.shot = shot   
    filter_shotreview.tags.submission_version = str(version)
    out = session.advanced_search(filter_shotreview)
    
    asset_shotreview = list(out)[0]
    
    asset_imageSeq = 0
    print asset_shotreview
    if asset_shotreview:
        # should iterate OUT and check if result is image sequence instead
        out = session.iterate_sources(asset_shotreview, relationship_type='dependency', depth=1)        
        print out
        #asset_imageSeq = next(out, None)
        for source in out:
            print source
            #print 'type is %s ' % source.asset_type.value
            if source.asset_type.value == "vfx_image_sequence":
                asset_imageSeq = source
                break
    else:
        raise Exception("invalid shotreview version")
    
    if asset_imageSeq:
        return asset_imageSeq.files.file_list[0]['path']
    
def set_camera_background(node, image_sequence):
    '''
    Sets the given cameras background image to the given image sequence
    '''
    parm_bg = node.parm("vm_background")
    img_path = image_sequence.replace(".#.", ".$F4.")
    print 'Setting camera background to: \n%s' % img_path
    parm_bg.set(img_path)
    
    
def getCameras():
    '''
    Returns all non hidden cameras in the scene
    '''
    cam_type = hou.nodeType(hou.objNodeTypeCategory(), "cam")
    cams = cam_type.instances()
    cams = [c for c in cams if not c.isHidden()]

    # add the current camera to first index in list
    current = toolutils.sceneViewer().curViewport().camera()
    cams.insert(0, current)
    return cams
    
    

#__ LOGIC __


if check_is_camera(CAMERA):
    
    default_path = output_path(VERSION)
    
    if check_already_exists(default_path):
        print 'Plate has already been exported locally'
        set_camera_background(CAMERA, default_path)

    else:
        print 'Plate not found locally, looking to shotreview version \n'
        #sequence_path = image_sequence_from_pl(SHOT, VERSION)
        sequence_path = image_sequence_from_sr(SHOW, DIVISION, SEQUENCE, SHOT, VERSION)
        print "sequence path = " + sequence_path
        
        #override = True
        if (check_is_valid_sequence(sequence_path) is False):# or override:
            print 'Version source image sequence incompatible, re-exporting to jpg in images directory \n'
            sequence_path = make_local_sequence(sequence_path, default_path)
            set_camera_background(CAMERA, sequence_path)
        else:
            print "Version source image is compatible, using original \n"
            set_camera_background(CAMERA, sequence_path)

    
   
    
    
