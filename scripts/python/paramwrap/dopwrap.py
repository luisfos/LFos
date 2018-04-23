import hou


def create_null(source, target_container):
    '''
    Creates subnet inside target_container with name of source
    '''

    new_null = target_container.createNode("subnet", source.name())
    new_null.setPosition(source.position())
    new_null.original = source
    for parm in new_null.parms():
        parm.hide(True)
    #new_null.setUserData("original", source)
    return new_null

def copy_parameter_values(source, target, parm_filter=None):
    '''
    Copies parameter values between source and target parameters given they have the same names

    '''

    all_parameters = source.parms()

    if parm_filter != None:
        all_parameters = [parm for parm in all_parameters if parm_filter in parm.name()]

    for parm in all_parameters: 
        parm_name = parm.name()
        tgt = target.parm(parm_name)
        if tgt == None:
            continue
        # if parm has a expression (keyframes) then copy them over
        if len(parm.keyframes()) > 0:
            # clear any of my keyframes
            #print "KEYFRAME COPY"
            tgt.deleteAllKeyframes()
            tgt.setKeyframes(parm.keyframes())
        else:
        # otherwise if they have non keyframe values just copy them over
            #print "STRING COPY"
            val = parm.eval()
            if(type(val)==str):
                val = parm.unexpandedString()
            tgt.set(val)   

def copy_interface(source, target):
    '''
    copies interface from one node to another using hacky parameterTemplateGroup asCode()

    TODO:
    transfer CURRENT values not DEFAULTs
    transfer over "horizontally join to next parameter"
    '''

    # hi-jacks houdini asCode() local variables (hou_node & hou_parm_template_group)   
    hou_node = target
    otlParmTemplateAsCode = source.parmTemplateGroup().asCode()
    
    # creates the parmTemplateGroup object (hou_parm_template_group) for the node's layout    
    exec otlParmTemplateAsCode
   
    #apply the parmTemplateGroup object to the node (they are not live objects - you are modifying a copy and must reset it) 
    target.setParmTemplateGroup(hou_parm_template_group, False)   
    del hou_parm_template_group

    #________________________________
    # HIDE SPARE & STANDARD FOLDER
    #________________________________
   
    group = target.parmTemplateGroup()
    folder= group.findFolder("Standard")
    folder_copy = folder.clone()
    if folder != None:
        folder.hide(True)
   
    group.replace(folder_copy, folder)
   
    folder= group.findFolder("Spare")
    folder_copy = folder.clone()
    if folder != None:
        folder.setFolderType(hou.folderType.ImportBlock)
       
    group.replace(folder_copy, folder)
       
    target.setParmTemplateGroup(group, True) 


def link_parameters(source, target, failsafe=False): 
    '''
    Links the source parameters to the target (SOURCE will have a REFERENCE)

    THIS ASSUMES BOTH SOURCE & TARGET PARAMETER VALUES ARE ALREADY EQUAL

    If failsafe is true: 
        for any parameters that do not have the same evaluated result,
        reset to original parameter value
    parameter values will evaluate differently if they use nested expressions - move to python to avoid

    for H16.5 update to parm.rawValue()

    need to handle multiparms
    '''

    all_parameters = source.parms()
    parms_normal = []
    parms_multi = []

    for parm in all_parameters:
        if not parm.isMultiParmInstance():
            if len(parm.multiParmInstances())>0:
                parms_multi.append(parm)
            else:
                parms_normal.append(parm)

    for s_parm in parms_multi:
        link_multiparm(s_parm, target.parm(s_parm.name()) )
    
    for s_parm in parms_normal: 
        #print "iterating node {}, parameter {}".format(source.name(), s_parm.name())
        orig_val = None
        if failsafe:
            orig_val = s_parm.eval()    
            orig_string = s_parm.eval()
            print 'evaluated normally'
            if(type(orig_string)==str):
                print 'type is string, unexpanding string'
                orig_string = s_parm.unexpandedString()       


        print 'begin linking'
        source_name = s_parm.name()
        t_parm = target.parm(source_name)       
        s_parm.set(t_parm)
        print 'end linking'

        ''' compare end results to see if parameters don't match up '''
        if failsafe==True: 
            end_val = s_parm.eval()        
            if (orig_val != end_val):
                print "node {}, parameter {} results not matching".format(source.name(), s_parm.name())                
                if(type(t_parm.eval())==str):
                    # parameter accepts string expressions                    
                    s_parm.deleteAllKeyframes()
                    s_parm.set(orig_string)
                else:
                    # parameter only accepts keyframes
                    s_parm.setKeyframes(t_parm.keyframes())

def collapseSingleNodeIntoSubnet(node, subnet_name=None):
    subnet = node.parent().collapseIntoSubnet((node,), subnet_name=subnet_name)
    inputs = subnet.indirectInputs()

def createSubnet(node, subnet_name=None):
    original_name = node.name()

    # make nodes
    subnet = node.parent().collapseIntoSubnet((node,), subnet_name=subnet_name)    
    dopnet = subnet.node("./{}".format(original_name))
    mirror = subnet.createNode("subnet", "mirror")

    # store data for recreating from other functions later
    data = {"isWrapper": "1", "dopnet": dopnet.name(), "mirror": mirror.name()}
    for key, val in data.iteritems():
        subnet.setUserData(key, val)

    output = subnet.createNode("output")
    output.setInput(0, dopnet)
    output.setDisplayFlag(True)

    # tidy layout
    inputs = subnet.indirectInputs()
    inputs[1].setPosition(inputs[0].position()+hou.Vector2(2,0) )
    inputs[2].setPosition(inputs[0].position()+hou.Vector2(4,0) )
    inputs[3].setPosition(inputs[0].position()+hou.Vector2(6,0) )

    mirror.setPosition(inputs[0].position()+hou.Vector2(0,-2) )
    output.setPosition(inputs[0].position()+hou.Vector2(0,-4) )
    dopnet.setPosition(inputs[0].position()+hou.Vector2(-3,-2) )

    mirror.setColor(hou.Color(1, 0.725, 0))
    mirror.setCurrent(1)

    # connect inputs
    for idx, nInput in enumerate(dopnet.inputConnections()):
        if nInput != None:
            to_connect = nInput.inputItem()
            mirror.setInput(idx, to_connect)

    return [subnet, dopnet, mirror]

def resolveParameters(node, parm_filter=None):
    '''
    Resolves a channel reference to its value

    '''

    all_parameters = node.parms()

    if parm_filter != None:
        all_parameters = [parm for parm in all_parameters if parm_filter in parm.name()]

    for parm in all_parameters:    
        # can check if has expression with keyframes (or expression but then you have to catch errors)
        if len(parm.keyframes()) > 0:
            expression = parm.expression()
            #print "previous expression %s" % expression
            # find path by finding strings starting with "
            expression_split = expression.split('"')
            
            path = expression_split[1]
            print path
            link_parm = node.parm(path)

            # only resolve parm if is another expression
            if len(link_parm.keyframes())>0:        
                new_expression = link_parm.expression()
                print new_expression        
                parm.deleteAllKeyframes()        
                parm.setExpression(new_expression)
            else:
                new_value = link_parm.eval()
                parm.deleteAllKeyframes()        
                parm.set(new_value)


def expand_tuple_template(template):    
    scheme = template.namingScheme()
    num = int(template.numComponents())
    
    if num==1:
        return [template.name()]
    else:
        suffix = []
        out = []
        if scheme == hou.parmNamingScheme.Base1:
            suffix = list(scheme.name())
        else:
            chars = scheme.name()
            suffix = re.sub( r"([A-Z])", r" \1", chars).lower().split()
        
        letter = ""        
        for idx in range(0, num):
            #print "idx = %i" % idx
            letter = suffix[idx]
            out.append(template.name()+letter)
            
        return out


def link_multiparm(src, tgt):
    '''
    special linking of multiparm
    '''
    instances_src = src.multiParmInstances()
    if (len(instances_src)==0 or len(tgt.multiParmInstances())==0):
        raise hou.OperationFailed("Cannot link parameters as they are not multi parm instances")

    path_tgt = tgt.path()
    name_src = src.name()
    to_path = src.node().relativePathTo(tgt.node())    
    unique = []

    if src.parmTemplate().type() == hou.parmTemplateType.Ramp:
        for instance in src.multiParmInstances():
            name = instance.name()
            name = name.lstrip(name_src)
            #remove leading digits 
            name = name.lstrip('0123456789_')              
            if name not in unique:
                unique.append(name)
        unique = [name_src+'#'+name for name in unique]
    else:
        for template in src.parmTemplate().parmTemplates():
            unique += expand_tuple_template(template)
    
    command_toLink = ''
    for param_name in unique:        
        other_param_name = to_path + '/' + param_name
        command_toLink += ' "{}" "{}"'.format(param_name, other_param_name)

    command = 'opmultiparm {}{}'.format(src.node().path(), command_toLink)
    err = hou.hscript(command)
    if err[0]=='' and err[1]=='':
        src.set(tgt)    
        # ramp has a bug where first one isnt linked.. manually fixing this
        if src.parmTemplate().type() == hou.parmTemplateType.Ramp:
            for param_name in unique:
                name = param_name.replace('#', '1')
                src.node().parm(name).set(tgt.node().parm(name))
    else:
        raise hou.OperationFailed(err[0], err[1])


def main():
    # list of pairs [original, mirror]
	sel_orig = hou.selectedNodes()[0]

	if sel_orig.childTypeCategory() != hou.nodeTypeCategories()['Dop']:
	    raise hou.OperationFailed("Selected node is not DOP type")
	    quit()


    pairs = []
    n_dopnet = None
    lookup = sel_orig.name()

    #n_wrapper = collapseSingleNodeIntoSubnet(sel_orig, sel_orig.name()+'_WRAP')

    # create network
    nodes = createSubnet(sel_orig, sel_orig.name()+'_WRAP')
    n_wrapper = nodes[0]
    n_dopnet = nodes[1]
    n_mirror = nodes[2]


    copy_interface(n_dopnet, n_mirror)
    copy_parameter_values(n_dopnet, n_mirror)
    link_parameters(n_dopnet, n_mirror, failsafe=False)

    '''
    CREATE NODES
    '''
     
    # first create nodes with parameters
    for node in n_dopnet.children():
        
        # temp node
        #node = hou.node('/obj/geo1/dop_container/popnet/popobject')

        new = create_null(node, n_mirror)    
        pairs.append([node, new])
       
        copy_interface(node, new) 
        copy_parameter_values(node, new) 
       
        # link parameters of node to new
        link_parameters(node, new, failsafe=False)
       
        
    #link_parameters(n_dopnet, n_mirror)



    '''
    CONNECT NODES
    '''
     
     
    # now connect up nodes
    for pair in pairs:
        orig= pair[0]
        new = pair[1]
        print "\nCurrent node: %s" % new.name()
        print "Original: %s" % orig.path()
        orig_inputs = orig.inputs()
        print "Original Inputs:", orig_inputs
       
        for idx, input in enumerate(orig.inputs()):
            if input != None:
                print "Index: %i" % idx
                print "Input: ", input
                to_connect = new.node("../{}".format(input.name()))
                new.setInput(idx, to_connect)



