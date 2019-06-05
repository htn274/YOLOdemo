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
    def __init__(self, *args, **kwargs):
        dn.set_gpu(0)
        self.net = dn.load_net("quick-draw-model/my-yolov3.cfg".encode('utf8'), "quick-draw-model/my-yolov3.weights".encode('utf8'), 0)
        self.meta = dn.load_meta("quick-draw-model/obj.data".encode('utf8'))
    
    def predict(self):
        r = (dn.detect(self.net, self.meta, "drawing.jpg".encode('utf8')))[0]
        # predicted class and accuracy
        return r[0].decode('utf8'), r[1]

class Game:
    def create_canvas(self):
        self.cv = Canvas(self.root, width=640, height=480, bg='white')
        self.cv.bind('<1>', self.activate_paint)
        self.cv.pack(expand=YES, fill=BOTH)

    def create_draw(self):
        self.image1 = PIL.Image.new('RGB', (640, 480), 'white')
        self.draw = ImageDraw.Draw(self.image1)

    def create_button(self, frame, name_btn, cmd_btn, side_btn = LEFT):
        btn = Button(frame, 
        text=name_btn, 
        font = ("Arial", 16),
        command=cmd_btn,
        width = 8,
        bg = "#24252a",
        fg = "#f03434")

        btn.pack(side = side_btn, padx = 5, pady = 5)

    def draw_live(self, frame):
        image = Image.open('Image/live.png')
        img = ImageTk.PhotoImage(image.resize((48, 48))) 
        label = Label(frame, image=img)
        label.pack(side=LEFT)


    def create_frame_button(self):
        self.frame_btn = Frame(self.root)
        self.frame_btn.pack()

        self.draw_live(self.frame_btn)
        self.btn_submit = self.create_button(self.frame_btn, "Submit", self.submit)
        self.btn_clear = self.create_button(self.frame_btn, "Clear", self.clear)

    def create_window(self):
        self.root = Tk()
        self.root.title("Quick-draw")

    def create_obj_name_label(self):
        self.obj_name = Label(
            self.root, 
            text = "Classes",
            font = ("Arial", 18),
            fg = "#013243"
        )
        self.obj_name.pack()

    def random_object(self):
        num_rnd = random.randrange(0, len(Classes), 1)
        self.obj_name.config(text = "Let draw a/an {}!".format(Classes[num_rnd]))

    def drawing_window(self):
        self.lastx, self.lasty = None, None
        self.create_canvas()
        self.create_draw()

    def __init__(self):
        # Create window
        self.create_window()
        self.create_obj_name_label()
        self.random_object()
        self.drawing_window()
        self.create_frame_button()        
        
        # self.detector = DetectDraw()
        self.root.mainloop()

    def submit(self):
        filename = f'drawing.jpg'
        self.image1.save(filename)
        print("CHECKING.....")
        ans, accuracy = self.detector.predict()
        self.check_ans(ans)

    def check_ans(self, ans):
        if ans == self.obj_name.cget("text"):
            messagebox.showinfo("Sucess", "Congrats! You are an artist!")
            self.random_object()
            self.clear()
        else:
            if len(ans) > 0:
                messagebox.showinfo("Failed", "Wrong! You draw a {}. Try again.".format(ans))
            else:
                messagebox.showinfo("Failed!", "I don't know what you drew. Try again")

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

if __name__ == "__main__":
    read_obj_names('quick-draw-model/obj.names')
    game = Game()
    # root = Tk()
    # image = Image.open('Image/live.png')
    # img = ImageTk.PhotoImage(image.resize((48, 48))) 
    # label = Label(root, image=img)
    # label.image = img
    # label.pack()
    # root.mainloop()

