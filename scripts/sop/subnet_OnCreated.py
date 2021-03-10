#print "subnet oncreated run "
n = kwargs['node']

input1 = n.indirectInputs()[0]
n_in = n.createNode("null", "IN")
#n_out = n.node("output0")
# output node is now generate after this script so we cant access it - will need to discuss with sesi how to

# print n.children()

n_in.setInput(0, input1)
n_in.setPosition( input1.position() + hou.Vector2(0.1,-1) )
# print "done"
#print n_out
# n_out.setInput(0, n_in)
# n_out.setPosition( n_in.position() + hou.Vector2(0,-8) )

