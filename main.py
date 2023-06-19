from random_automata import random_automata
from OBS import OBS
from opacity_verification import opacity_verification
from KripkeStructure import KripkeStructure
from mKripkeStructure import mKripkeStructure
from transform import transform
from rFSA import rFSA
from initial_state_opacity_verification import initial_state_opacity_verification
from infinite_step_opacity_verification import infinite_step_opacity_verification
from TwinPlant import TwinPlant
from cycle_detection import TarjansAlgorithm, is_self_loop
from diagnosability_verification import diagnosability_verification
from detectability_verification import detectability_verification
from predictability_verification import predictability_verification
from I_detectability_verification import I_detectability_verification
from rTwinPlant import rTwinPlant
from weak_detectability_verification import weak_detectability_verification
from TwoWayVerifier import TwoWayVerifier
from delayed_detectability_verification import delayed_detectability_verification

import time

des = random_automata(10, 7, 3, min_trans_per_state=3, max_trans_per_state=3, num_init=2, num_uo=2, num_secret=2, num_faultevent=1)

#for edge in des.edges:
#    print(edge, ' ', des.edges[edge]['event'], ' ', des.edges[edge]['obs'])

#for state in des.nodes:
#    print(state, des.nodes[state]['fault'])

#for edge in des.edges:
#    print(edge, des.edges[edge]['event'])

KS = KripkeStructure(des)
mKS = mKripkeStructure(KS)
transform(mKS)
print("Kripke Structure constructed!")


t7=time.process_time()
TP=TwinPlant(des)
if diagnosability_verification(TP, des):
    print("diagnosable")
else:
    print("NOT diagnosable")
t8=time.process_time()
print("cputime:", t8-t7)


t11=time.process_time()
TP=TwinPlant(des)
if predictability_verification(TP, des):
    print("predictable")
else:
    print("NOT predictable")
t12=time.process_time()
print("cputime:", t12-t11)


t13=time.process_time()
rTP=rTwinPlant(des)
if I_detectability_verification(rTP, des):
    print("I-detectable")
else:
    print("NOT I-detectable")
t14=time.process_time()
print("cputime:", t14-t13)


t9=time.process_time()
TP=TwinPlant(des)
if detectability_verification(TP, des):
    print("strongly detectable")
else:
    print("NOT strongly detectable")
t10=time.process_time()
print("cputime:", t10-t9)



t17=time.process_time()
TW=TwoWayVerifier(des)
if delayed_detectability_verification(TW, des):
    print("delayed-detectable")
else:
    print("NOT delayed-detectable")
t18=time.process_time()
print("cputime:", t18-t17)



t15=time.process_time()
observer=OBS(des)
if weak_detectability_verification(observer, des):
    print("weakly detectable")
else:
    print("NOT weakly detectable")
t16=time.process_time()
print("cputime:", t16-t15)




#opacity_verification

t3=time.process_time()
des_reverse = rFSA(des)
observer_reverse = OBS(des_reverse)

if initial_state_opacity_verification(observer_reverse, des):
    print("initial-state opaque")
else:
    print("NOT initial-state opaque")
t4=time.process_time()
print("cputime:", t4-t3)


t1=time.process_time()
observer=OBS(des)

if opacity_verification(observer, des):
    print("current-state opaque")
else:
    print("NOT current-state opaque")

t2=time.process_time()
print("cputime:", t2-t1)


t5=time.process_time()
observer=OBS(des)
des_reverse = rFSA(des)
observer_reverse = OBS(des_reverse)
if infinite_step_opacity_verification(observer_reverse, observer, des):
    print("infinite-step opaque")
else:
    print("NOT infinite-step opaque")
t6=time.process_time()
print("cputime:", t6-t5)






















