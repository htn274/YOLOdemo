# Stupid python path shit.
# Instead just add darknet.py to somewhere in your python path
# OK actually that might not be a great idea, idk, work in progress
# Use at your own risk. or don't, i don't care

import sys, os
sys.path.append(os.path.join(os.getcwd(),'python/'))

import darknet as dn
import pdb

dn.set_gpu(0)
net = dn.load_net("cfg/yolo-thor.cfg".encode('utf8'), "/home/pjreddie/backup/yolo-thor_final.weights".encode('utf8'), 0)
meta = dn.load_meta("cfg/thor.data".encode('utf8'))
r = dn.detect(net, meta, "data/bedroom.jpg".encode('utf8'))
print(r)

# And then down here you could detect a lot more images like:
r = dn.detect(net, meta, "data/eagle.jpg")
print(r)
r = dn.detect(net, meta, "data/giraffe.jpg")
print(r)
r = dn.detect(net, meta, "data/horses.jpg")
print(r)
r = dn.detect(net, meta, "data/person.jpg")
print(r)

