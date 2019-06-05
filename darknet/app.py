from tkinter import *
from tkinter import messagebox
import PIL
from PIL import Image, ImageDraw, ImageTk
import darknet as dn
import cv2
import random

Classes = []

def read_obj_names(file):
    with open(file, 'r') as f:
        for line in f:
            Classes.append(line.strip())

class DetectDraw:
    def __init__(self):
        dn.set_gpu(0)
        self.net = dn.load_net("quick-draw-model/my-yolov3.cfg".encode('utf8'), "quick-draw-model/my-yolov3.weights".encode('utf8'), 0)
        self.meta = dn.load_meta("quick-draw-model/obj.data".encode('utf8'))
    
    def predict(self):
        r = (dn.detect(self.net, self.meta, "drawing.jpg".encode('utf8')))
        print(r)
        if len(r) == 0:
            return None
        r = r[0]
        # predicted class and accuracy
        return r[0].decode('utf8'), r[1]

# Main area contains drawing area and question area
class MainArea:
    def activate_paint(self, e):
        self.cv.bind('<B1-Motion>', self.paint)
        self.lastx, self.lasty = e.x, e.y

    def paint(self, e):
        x, y = e.x, e.y
        self.cv.create_line((self.lastx, self.lasty, x, y), width=1.5)
        #  --- PIL
        self.draw.line((self.lastx, self.lasty, x, y), fill='black', width=1)
        self.lastx, self.lasty = x, y

    def create_canvas(self, _frame):
        self.cv = Canvas(_frame, width=640, height=480, bg='white')
        self.cv.bind('<1>', self.activate_paint)
        self.cv.pack(expand=YES, fill=BOTH)

    def create_draw(self):
        self.image1 = PIL.Image.new('RGB', (640, 480), 'white')
        self.draw = ImageDraw.Draw(self.image1)
    
    def drawing_window(self, _frame):
        self.lastx, self.lasty = None, None
        self.create_canvas(_frame)
        self.create_draw()

    def create_frame(self):
        self.top_frame = Frame(self.root)
        self.top_frame.pack()
        self.drawing_frame = Frame(self.root)
        self.drawing_frame.pack()

    def create_obj_name_label(self, _frame):
        self.obj_name = Label(
            _frame, 
            text = "Classes",
            font = ("Arial", 18),
            fg = "#013243"
        )
        self.obj_name.pack()

    def __init__(self, _root):
        self.root = Frame(_root, width=640, height=480, relief='sunken', borderwidth=2)
        self.root.pack(expand=True, fill='both', side='left', anchor='nw')
        self.create_frame()
        self.drawing_window(self.drawing_frame)
        self.create_obj_name_label(self.top_frame)

    def get_canvas(self):
        return self.cv

    def get_drawing(self):
        return self.draw
    
    def get_image(self):
        return self.image1

    def set_text_label_obj_name(self, _text):
        self.obj_name.config(text=_text)

class Game:
    def create_button(self, frame, name_btn, cmd_btn):
        btn = Button(frame, 
        text=name_btn, 
        font = ("Arial", 16),
        command=cmd_btn,
        width = 8,
        bg = "#24252a",
        fg = "#f03434")
        btn.pack(padx = 5, pady = 5)

    def draw_live(self, frame):
        image = Image.open('Image/live.png')
        img = ImageTk.PhotoImage(image.resize((48, 48))) 
        label = Label(frame, image=img)
        label.pack(side=LEFT)

    def random_obj_name(self):
        num = random.randrange(0, len(Classes), 1)
        self.obj_name = Classes[num]
        self.mainarea.set_text_label_obj_name(self.obj_name)

    def __init__(self):
        self.root = Tk()
        self.mainarea = MainArea(self.root)
        self.sidebar = Frame(self.root, width=200, height=480, relief='sunken', borderwidth=2)
        self.sidebar.pack(expand=True, fill='both', side='right', anchor='nw')
        self.btn_submit = self.create_button(self.sidebar, "Submit", self.submit)
        self.btn_clear = self.create_button(self.sidebar, "Clear", self.clear)
        self.random_obj_name()
        self.detector = DetectDraw()
        self.root.mainloop()

    def submit(self):
        filename = f'drawing.jpg'
        self.mainarea.get_image().save(filename)
        print("CHECKING.....")
        result = self.detector.predict()
        self.check_ans(result)

    def check_ans(self, res):
        if res == None:
            messagebox.showinfo("Failed!", "I don't know what you drew. Try again")
            return 

        ans = res[0]
        if ans == self.obj_name:
            messagebox.showinfo("Sucess", "Congrats! You are an artist!")
            self.random_obj_name()
            self.clear()
        else:
            messagebox.showinfo("Failed", "Wrong! You draw a {}. Try again.".format(ans))
                

    def clear(self):
        self.mainarea.get_canvas().delete('all')
        self.mainarea.create_draw()

if __name__ == "__main__":
    read_obj_names('quick-draw-model/obj.names')
    game = Game()
