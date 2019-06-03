from tkinter import *
import PIL
from PIL import Image, ImageDraw
import darknet as dn
import cv2

class UI:
    # image_number = 0
    def create_canvas(self):
        self.cv = Canvas(self.root, width=640, height=480, bg='white')
        self.cv.bind('<1>', self.activate_paint)
        self.cv.pack(expand=YES, fill=BOTH)

    def create_draw(self):
        self.image1 = PIL.Image.new('RGB', (640, 480), 'white')
        self.draw = ImageDraw.Draw(self.image1)

    def create_button(self, frame, name_btn, cmd_btn, side_btn = LEFT):
        btn = Button(frame, text=name_btn, command=cmd_btn)
        btn.pack(side = side_btn)

    def create_frame_button(self):
        self.frame_btn = Frame(self.root)
        self.frame_btn.pack()

        self.btn_save = self.create_button(self.frame_btn, "save", self.save)
        self.btn_clear = self.create_button(self.frame_btn, "clear", self.clear)

    def __init__(self):
        self.root = Tk()

        self.lastx, self.lasty = None, None
        self.create_canvas()
        self.create_draw()
        self.create_frame_button()
        self.root.mainloop()

    def save(self):
        # filename = f'image_{UI.image_number}.png'   # image_number increments by 1 at every save
        filename = f'drawing.jpg'
        self.image1.save(filename)
        # UI.image_number += 1
        r = dn.detect(net, meta, "drawing.jpg".encode('utf8'))
        print(r)


    def activate_paint(self, e):
        self.cv.bind('<B1-Motion>', self.paint)
        self.lastx, self.lasty = e.x, e.y

    def paint(self, e):
        x, y = e.x, e.y
        self.cv.create_line((self.lastx, self.lasty, x, y), width=1.5)
        #  --- PIL
        self.draw.line((self.lastx, self.lasty, x, y), fill='black', width=1)
        self.lastx, self.lasty = x, y

    def clear(self):
        self.cv.delete('all')
        self.create_draw()
        return

# Load model first
dn.set_gpu(0)
net = dn.load_net("quick-draw-model/my-yolov3.cfg".encode('utf8'), "quick-draw-model/my-yolov3.weights".encode('utf8'), 0)
meta = dn.load_meta("quick-draw-model/obj.data".encode('utf8'))

if __name__ == "__main__":
    ui = UI()
