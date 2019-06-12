from flask import Flask
import os
import sys
import darknet as dn
import matplotlib.pyplot as plt 
import matplotlib.image as img 
import cv2
from io import BytesIO
import base64

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

options = {
        'model': 'cfg/yolov3.cfg',
        'load': 'weights/yolov3.weights',
        'data' : 'cfg/coco.data',
        'threshold': 0.4,
}

class YOLO:
    def __init__(self):
        RUN_DIR = "../darknet"
        os.chdir(RUN_DIR)
        dn.set_gpu(0)
        self.net = dn.load_net(options['model'].encode('utf8'), options['load'].encode('utf8'), 0)
        self.meta = dn.load_meta(options['data'].encode('utf8'))
        self.threshold = options['threshold']
        os.chdir(APP_ROOT)
        print("INIT DONE ========================")
        print("Back to: ", os.getcwd())

    def run_detect(self, image_dir):
        print("DECTECTING..................")
        img = cv2.imread(image_dir, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = dn.detect(self.net, self.meta, image_dir.encode('utf8'), self.threshold)
        return res, img

def drawPred(class_pred, conf, left, top, right, bottom, img):
    # Draw a bounding box.
    cv2.rectangle(img, (left, top), (right, bottom), (255, 178, 50), 3)

    # label = '%.2f' % conf
    label = '%s:%s' % (class_pred, conf)

    #Display the label at the top of the bounding box
    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    img = cv2.rectangle(img, (left, top - round(1.5*labelSize[1])), (left + round(1.5*labelSize[0]), top + baseLine), (255, 178, 50), cv2.FILLED)
    img = cv2.putText(img, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 2)
    plt.imshow(img)

def draw_bouding_box(pred, img):
    detected_obj = set()
    for ele in pred:
        label = ele[0].decode('utf-8')
        detected_obj.add(label)

        score = '%.2f' % (ele[1]*100)
        center_x=int(ele[2][0])
        center_y=int(ele[2][1])
        width = int(ele[2][2])
        height = int(ele[2][3])

        UL_x = int(center_x - width/2) 
        UL_y = int(center_y + height/2) 
        LR_x = int(center_x + width/2)
        LR_y = int(center_y - height/2)

        drawPred(label, score, UL_x, UL_y, LR_x, LR_y, img)
    return detected_obj

app = Flask(__name__)
yolo = None  

@app.route('/')
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)

    for upload in request.files.getlist("file"):
        print(upload)
        filename = upload.filename
        destination = "/".join([target, filename])
        print("Save it to:", destination)
        upload.save(destination)
    
    pred, img = yolo.run_detect(destination)
    print('RESULT\n', pred)

    detected_obj_name = draw_bouding_box(pred, img)

    # Save image to static/
    plt.savefig('static/predictions.png')
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = figdata_png
    
    return render_template("complete.html", pred= detected_obj_name)

if __name__ == "__main__":
    yolo = YOLO()
    app.run(port = 5000)