from flask import Flask, request, render_template
import cv2
import os
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print('save image to: ', target)

    return render_template('complete.html')

if __name__ == "__main__":
    app.run(port = 4000, debug = True)