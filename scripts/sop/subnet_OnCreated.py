
n = kwargs['node']

input1 = n.indirectInputs()[0]

n_in = n.createNode("null", "IN")
n_out = n.createNode("output", "OUT")


n_in.setInput(0, input1)
n_in.setPosition( input1.position() + hou.Vector2(0,-1) )
#n_in.moveToGoodPosition()
n_out.setInput(0, n_in)
n_out.setPosition( n_in.position() + hou.Vector2(0,-8) )

#print "subnet oncreated run "