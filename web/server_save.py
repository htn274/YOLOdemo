from flask import Flask, render_template, request
import os
import sys
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def run_detect(image_dir):
    print("DECTECTING..................")
    print(image_dir)
    # Change directory to darknet file to run darknet
    RUN_DIR = "../darknet"
    os.chdir(RUN_DIR)
    print("Change dir: " + os.getcwd())
    sys.path.append(os.getcwd())
    
    # import darknet as dn
    # dn.set_gpu(0)
    # net = dn.load_net("cfg/yolov3.cfg".encode('utf8'), "weights/yolov3.weights".encode('utf8'), 0)
    # meta = dn.load_meta("cfg/coco.data".encode('utf8'))
    # r = dn.detect(net, meta, image_dir.encode('utf8'))
    # print(r)

    os.system("./darknet detect cfg/yolov3.cfg ./weights/yolov3.weights " + image_dir) 
    # Move the result to /static
    os.system("mv ./predictions.jpg " + APP_ROOT + '/static')
    os.chdir(APP_ROOT)
    print("Back to: ", os.getcwd())
    return

@app.route('/')
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)

    # for upload in request.files.getlist("file"):
    #     print(upload)
    #     filename = upload.filename
    #     destination = "/".join([target, filename])
    #     print("Save it to:", destination)
    #     upload.save(destination)
    # run_detect(destination)
    
    return render_template("complete.html")

if __name__ == "__main__":
    # run_detect(os.path.join(APP_ROOT, 'images/') + 'dog.jpg')
    app.run(debug = True)