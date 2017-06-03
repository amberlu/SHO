from tkinter import *
from wavefn import WaveFn
import PIL
from PIL import ImageTk, Image
import math



class Window(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._init_ui()

    def _init_ui(self):
        self.title("SHO Application")
        self.geometry("800x800")
        self.symmetry = "even"
        self.wavefn = None

        image = Image.open("quantum.jpg")
        self.img = image
        #self.img = image.resize((400,800), Image.ANTIALIAS)
        self.bg_img = ImageTk.PhotoImage(self.img)
        self.bg_label = Label(self, image=self.bg_img)
        self.bg_label.place(x=400, y=630)


        label = Label(self, text="Simple Harmonic Oscillator Simulation", bg="DarkOliveGreen1", fg="black")
        label.config(font=("Times", 20, "bold"), relief=RAISED)
        label.place(height=80, width=500, x=150, y=80)

        menubutton = Menubutton(text="Symmetry", font=("Times", 14))
        menubutton.place(x=450, y=220)
        menu = Menu(menubutton, tearoff=0)
        menubutton['menu'] = menu
        menu.add_command(label="even", font=("Times", 14), command=self._click_even)
        menu.add_command(label="odd", font=("Times", 14), command=self._click_odd)

        self.k = 0.5
        self.k_min = 0
        self.k_max = 1.0
        self.scale = Scale(self, troughcolor="cornflower blue", activebackground="black", length=200, resolution=0.01, from_=self.k_min, to=self.k_max)
        self.scale.set(self.k)
        self.scale.place(x=100, y=300)
        self.scale.bind("<ButtonRelease-1>", self._update_k_value)
        label1 = Label(self, text=str(self.k_min))
        label1.place(x=150, y=290)
        label2 = Label(self, text=str(self.k_max))
        label2.place(x=150, y=490)

        scale_label = Label(self, text="k-dial", font=("Times", 16))
        scale_label.place(x=120, y=270)

        min_label = Label(text="k_min", font=("Times", 14))
        max_label = Label(text="k_max", font=("Times", 14))
        min_label.place(x=70, y=550)
        max_label.place(x=70, y=573)
        self.min_entry = Entry(width=4, font=("Times", 14))
        self.max_entry = Entry(width=4, font=("Times", 14))
        self.min_entry.place(x=120, y = 550)
        self.max_entry.place(x=120, y=570)

        self.button = Button(text="Enter", command=self.on_button_click)
        self.button.place(x=100, y=600)
        
        self.canvas = Canvas(self, bg="bisque2", width=600, height=400)
        self.canvas.place(x=200, y=250)
        self.canvas.create_line(0, 200, 600, 200)
        self.canvas.create_line(300, 0, 300, 400)

        
    def on_button_click(self):
        tmp_min, tmp_max = float(self.min_entry.get()), float(self.max_entry.get())
        assert tmp_min < tmp_max, "k_min must be smaller than k_max"
        self.k_min, self.k_max = tmp_min, tmp_max
        self.k = (self.k_max - self.k_min)/2 + self.k_min

        label1 = Label(self, text=str(self.k_min))
        label1.place(x=150, y=290)
        label2 = Label(self, text=str(self.k_max))
        label2.place(x=150, y=490)

        self.scale.config(font=("Times", 14), sliderlength=20, from_=self.k_min, to=self.k_max)
        self.scale.set(self.k)

    def _click_even(self):
        self.symmetry = "even"
        print("even")
        self._render()
        

    def _click_odd(self):
        self.symmetry = "odd"
        self._render()
        print("odd")

    def _render(self):
        # erase old contents and redraw the new function
        self.canvas.delete(ALL)
        self.canvas.create_line(0, 200, 600, 200)
        self.canvas.create_line(300, 0, 300, 400)

        # 0.01, 2
        self.wavefn = WaveFn(self.k, 0.008, 2.4, self.symmetry)

        y = self.wavefn.get_data()
        y_min, y_max = min(y), max(y)
        diff = max(abs(y_min), abs(y_max))
        bias = 200/(diff)
        for i in range(len(y)):
            tmp = y[i] * bias
            y[i] = 200 - tmp
            # if y_min > 0:
            #     y[i] = 200 - tmp + y_min*bias
            # if y_max < 0:
            #     y[i] = 200 - tmp - y_max*bias
        x = 0
        for i in range(len(y)-1):
            self.canvas.create_line(x, y[i], x+1, y[i+1])
            x += 1


    def _update_k_value(self, event):
        self.k = self.scale.get()
        self._render()
        print(self.k)
        

if __name__ == "__main__":
    application = Window()
    application.mainloop()