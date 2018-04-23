import hou
import toolutils
import os
import sys

import subprocess
import shlex
import logging

# INPUTS
NAME = "myEffect"


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


#viewer = toolutils.sceneViewer()
#settings = viewer.flipbookSettings().stash()


def isJobSet():
    job = hou.getenv('JOB')

    logger.info("Job is set to %s" % job)

    default_job = 'C:/Users/Luis'
    if job == default_job:
        logger.error("Job is using default path - please configure JOB variable")
        # log job path is using default value - please set up project
        return False

    if os.path.exists(job) == False:
        logger.error("Job path %s does not exist" % job)
        # log job path does not exist
        return False

    path = os.path.dirname(job)
    dir = path.split("/")[-1]
    if dir != 'houdini':
        logger.error("Job path %s does not follow protocol structure" % job)
        return False

    logger.info("Job is set correctly")
    return True



def find_output(name='myEffect'):
    job = hou.getenv('JOB')
    job = os.path.dirname(job)

    dirFlip = job + '/flip'
    dirName = dirFlip + '/' + name
    # skip version for now

    if not os.path.exists(dirName):
        os.makedirs(dirName)

    seqName = '{0}_v01.$F4.jpg'.format(name)

    output = '{dirName}/{seqName}'.format(dirName=dirName, seqName=seqName)

    logger.info("output path set: %s" % output)
    return output



def seqToMp4(path, settings):

    frameS = 1
    frameE = 100
    resolution = settings.resolution()
    x = int(resolution[0])
    x = x - (x%2)

    #y = int(resolution[1])
    #y = y - (y % 2)

    output = path.split("/")[-1]
    output = output.split('.$F4')[0]
    output = output + '.mp4'
    output = "/".join(path.split("/")[:-1]) + "/" + output

    path = path.replace('$F4', '%04d')

    cmd = 'ffmpeg -i {seq} -start_number {frameS} -vframes {nF} -vf scale={x}:-2 {output} -y'
    cmd = cmd.format(seq=path, frameS=frameS, nF=frameE-frameS, x=x, output=output )

    print cmd
    subprocess.Popen(shlex.split(cmd))
    # ffmpeg -i "./myEffect_v01.%04d.jpg" -start_number 1 -vframes 240 -vf scale=720:-2 -y test.mp4



def main():

    if isJobSet() == False:
        return

    # check user inputs are good

    viewer = toolutils.sceneViewer()
    settings = viewer.flipbookSettings().stash()

    output = find_output()

    #settings.outputToMplay(True)
    settings.output(output)

    viewer.flipbook(settings=settings)
    logger.info("flipbook complete")

    seqToMp4(output, settings)
    # after flipbook










def viewName(viewer):
    '''
    Returns the Scene viewer name in a hscript compatible format
    '''
    name = {
        'desktop': viewer.pane().desktop(),
        'pane': viewer.name(),
        'type': 'world',
        'viewport': viewer.curViewport().name()
    }
    # special case for floating windows - they don't belong to desktops
    if name['desktop'] == None:
        name['desktop'] = '*'
    else:
        name['desktop'] = name['desktop'].name()

    return '{desktop}.{pane}.{type}'.format(**name)


# viewer = toolutils.sceneViewer()
# hscriptViewer = viewName(viewer)
# cmd = "viewerstow -t open -b open -l open -x open -m open -c open -d open %s" % hscriptViewer
# hou.hscript(cmd)