# Modules

from tkinter import *

from ctypes import windll  # To Enable High Resolution Scaling in Windows OS
windll.shcore.SetProcessDpiAwareness(1)

master = Tk()
master.title("Rounded Button")
master.geometry("1900x1000")

intro = Frame(master)
intro.place(anchor="nw")

bg = PhotoImage(file=r"Code\Assets\intro.png")
canvas1 = Canvas(intro, height=1080, width=1920)
canvas1.pack()
canvas1.create_image(0, -40, image=bg, anchor="nw")

intro.after(3000, intro.destroy)
intro.wait_window(intro)

choose = Frame(master)
choose.place(anchor="nw")

bg = PhotoImage(file=r"Code\Assets\choose.png")  # ./Assets/intro.png (Mac)
canvas2 = Canvas(choose, height=1080, width=1920)
canvas2.pack()
canvas2.create_image(0, -40, image=bg, anchor="nw")

click_sudoku = PhotoImage(file=r'Code\Assets\sudoku_img.png')
click_riam = PhotoImage(file=r'Code\Assets\riam_img.png')

img_label = Label(image=click_sudoku, bg="#ffffff")
img_label = Label(image=click_riam, bg="#ffffff")

Button(choose, image=click_sudoku, command=None, borderwidth=0, bg="#ffffff", highlightcolor="#ffffff").place(x=600, y=540, anchor='center')
Button(choose, image=click_riam, command=None, borderwidth=0, bg="#ffffff", highlightcolor="#ffffff").place(x=1350, y=540, anchor='center')

mainloop()
