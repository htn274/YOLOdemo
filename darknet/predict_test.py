import matplotlib.pyplot as plt 
import matplotlib.image as img 
import numpy as np 
import os
import darknet as dn

# ./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg

if __name__ == "__main__":
    image_file = "dog.jpg"
    dn.set_gpu(0)
    net = dn.load_net("cfg/yolov3.cfg".encode('utf8'), "weights/yolov3.weights".encode('utf8'), 0)
    meta = dn.load_meta("cfg/coco.data".encode('utf8'))
    r = dn.detect(net, meta, "data/dog.jpg".encode('utf8'))
    print(r)
    # os.system("./darknet detect cfg/yolov3.cfg ./weights/yolov3.weights data/" + image_file)    
    # plt.imshow(img.imread('predictions.jpg'))
    # plt.show()
    