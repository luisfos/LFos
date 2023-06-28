import hou

stage = hou.node('/stage')
match = "prism::LOP_Import"

imports = [n for n in stage.children() if n.type().name().startswith(match)]

for node in imports:
    fp = node.parm('filepath')    
    s = fp.unexpandedString()
    match = "03_Production"
    rep = "$PRISM_JOB/"    
    split = s.split(match)
    split[0] = rep
    s = match.join(split)    
    fp.set(s)
    