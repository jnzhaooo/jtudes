from networkx.classes.digraph import DiGraph
from FSA import FSA
from OBS import OBS
from opacity_verification import opacity_verification
from observable_transition import obsnext_from_state
from KripkeStructure import KripkeStructure
from mKripkeStructure import mKripkeStructure
from transform import transform
from rFSA import rFSA
from initial_state_opacity_verification import initial_state_opacity_verification
from infinite_step_opacity_verification import infinite_step_opacity_verification
from FSA_run import FSA_run
from TwinPlant import TwinPlant
from cycle_detection import TarjansAlgorithm, is_self_loop, JohnsonsAlgorithm
from diagnosability_verification import diagnosability_verification
from detectability_verification import detectability_verification
from delayed_detectability_verification import delayed_detectability_verification
from weak_detectability_verification import weak_detectability_verification
from predictability_verification import predictability_verification
from TwoWayVerifier import TwoWayVerifier
from rTwinPlant import rTwinPlant
from I_detectability_verification import I_detectability_verification
from Subgraph import Subgraph
import time

#diagnosability
#state_fsa = [ ('0','s','nf'), ('1','ns','nf'), ('2','ns','f'), ('3','s','nf'), ('4','ns','nf'), ('5', 'ns', 'nf') ]
#edge_fsa = [ ('0','1','a','o1'), ('0','3','u1','epsilon'), ('1','2','f','epsilon'), ('2','2','d','o2'), ('3','4','b','o1'), ('4','1','u2','epsilon'), ('4','5','u1','epsilon'), ('5','5','c','o3') ]
#init_fsa = [ '0' ]

#opacity
#state_fsa = [ ('0','s','nf'), ('1','ns','nf'), ('2','ns','nf'), ('3','ns','nf'), ('4','s','nf'), ('5', 'ns', 'nf') ]
#edge_fsa = [ ('0','1','a','o1'), ('1','2','c','o2'), ('2','2','d','o3'), ('3','4','b','o1'), ('4','2','c','o2'), ('4','5','e','o4'), ('5','5','d','o3')]
#init_fsa = [ '0', '3' ]

#detectability
state_fsa = [ ('0','ns','nf'), ('1','ns','nf'), ('2','ns','nf'), ('3','ns','nf'), ('4','ns','nf'), ('5', 'ns', 'nf') ]
edge_fsa = [ ('0','1','a','o1'), ('0','4','b','o1'), ('1','2','c','o2'), ('2','2','d','o3'), ('3','4','e','o3'), ('4','2','c','o2'), ('4','5','a','o1'), ('5','5','b','o1') ]
init_fsa = [ '0', '3' ]


des=FSA(state_fsa, init_fsa, edge_fsa)


KS = KripkeStructure(des)
mKS = mKripkeStructure(KS)
transform(KS)

TP=TwinPlant(des)
rTP=rTwinPlant(des)
print(predictability_verification(TP, des))

t15=time.process_time()
observer=OBS(des)
if weak_detectability_verification(observer, des):
    print("weakly detectable")
else:
    print("NOT weakly detectable")
t16=time.process_time()
print("cputime:", t16-t15)
