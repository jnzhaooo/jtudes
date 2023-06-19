from networkx.classes.digraph import DiGraph
from ureach import ureach_from_state
from ureach import ureach_from_set

def obsnext(FSA, x_set, obs):
    nodes = FSA.nodes()
    edges = FSA.edges()
    obsnext_set = set()
    for x in x_set:
        for y in nodes:
            #print((x,y))
            if (x,y) in edges and FSA.edges[(x,y)]['obs'] == obs:
                obsnext_set.add(y)
                ur=ureach_from_set(FSA, obsnext_set)
                obsnext_set = obsnext_set | ur
    return obsnext_set
                
def obsnext_from_state(FSA, x, obs):
    nodes = FSA.nodes()
    edges = FSA.edges()
    obsnext_set = set()

    for y in ureach_from_state(FSA, x):
        for z in nodes:
            if (y,z) in edges and FSA.edges[(y,z)]['obs'] == obs:
                obsnext_set.add(z)
                ur=ureach_from_set(FSA, obsnext_set)
                obsnext_set = obsnext_set | ur
    return obsnext_set
