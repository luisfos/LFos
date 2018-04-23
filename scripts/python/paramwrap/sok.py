==================================
#sok

import hou
target = hou.node("/obj/geo1/null2")
sourceNodes = [hou.node("/obj/geo1/null1")]

def newFolder(currEntry, currNodeName):
    ''' Creates a new empty folder temp with a new name
    '''
    return hou.FolderParmTemplate(currNodeName + "_" + currEntry.name(), label = currEntry.label())

def expandFolders(currEntry, currNodeName):
    ''' Expands the folders and renames everything thats inside
    '''
    # make a new folder to start adding shit inside
    newFolderName = newFolder(currEntry, currNodeName)
    # Loop through all the indexes inside the folder
    for currEntryParm in currEntry.parmTemplates():
        if currEntryParm.type() == hou.parmTemplateType.Folder:
           #Inception 
           newFolderName.addParmTemplate( expandFolders(currEntryParm, currNodeName) )
        else:
            # Rename and add to teh folder
            currEntryParm.setName(currNodeName + "_" + currEntryParm.name())
            newFolderName.addParmTemplate(currEntryParm)
            
    return  newFolderName

def copyPasteTemplate(sourceNodes, target):
    ''' Copy the templates of the source nodes to the target node
    '''
    # Create a new empty templateGroup
    parmTempGroup = hou.ParmTemplateGroup()
    for currNode in sourceNodes:
        # Get template group from whole node
        currParmTemplGroup = currNode.parmTemplateGroup()
        currNodeName = currNode.name()
        # Create a tab with current nodes name and stick template there 
        folderName = currNodeName + "_Folder"
        currfolder = hou.FolderParmTemplate(currNodeName+"Fold", folderName)
        parmTempGroup.append(currfolder)
        # loop through all the the entries of the current nodes parmTemplate
        for currEntry in currParmTemplGroup.entries() :
            # if its a folder we need to recreate it. If not simply rename parameter
            if currEntry.type() == hou.parmTemplateType.Folder:
                currEntry = expandFolders(currEntry, currNodeName)
            else :
                currEntry.setName(currNodeName + "_" + currEntry.name())
            # Add to our empty new templateGroup the renamed entries
            parmTempGroup.appendToFolder(folderName, currEntry)
    target.setParmTemplateGroup(parmTempGroup, rename_conflicting_parms = True)

copyPasteTemplate(sourceNodes, target)

## TESTING FOR SESI BUG

import hou
pathOfTarget = "/obj/geo1/subnet1/null1"

hou.hscript( 'opmultiparm '+pathOfTarget+' "parm#pos" "../parm#pos" "parm#value" "../parm#value" "parm#interp" "../parm#interp"')
a = hou.node('/obj/geo1/subnet1').parm("parm")
hou.node(pathOfTarget).parm("parm").set(a)

import hou
inside = hou.node('/obj/geo1/subnet1/add1')
s = "opmultiparm"+inside.path()+" 'usept#' '../usept#' 'pt#x' '../pt#x' 'pt#y' '../pt#y' 'pt#z' '../pt#z' 'weight#' '../weight#'"
outside = hou.node('/obj/geo1/subnet1')
inside.parm('points').set(outside.parm('points'))


import hou
inside = hou.node('/obj/geo1/subnet1/add1')
s = "opmultiparm "+inside.path()+" 'usept#' '../usept#' 'pt#x' '../pt#x' 'pt#y' '../pt#y' 'pt#z' '../pt#z' 'weight#' '../weight#'"
print hou.hscript(s)
outside = hou.node('/obj/geo1/subnet1')
inside.parm('points').set(outside.parm('points'))