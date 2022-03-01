'''
#Project Name: Main
#Last Updated: 27/02/2022 20:25
#Last Updated by: Sarthak S Kumar
#Changelog:
    1/02/2022 10:13 Sarthak S Kumar
        # Updated Window Title
        # Updated Background
        # Added Exit Button
        # Comments and refining

    28/02/2022 20:29 Sarthak S Kumar
        # To link buttons with functions
        # Importing RIAM and Sudoku Codes

`   27/02/2022 20:25 Sarthak S Kumar
        # Added Comments
        # Created Intro Frame with Background
        # Added Buttons for Sudoku and Rat in a Maze
        # Added choose screen with buttons
#Pending:
    # Scaling issues
'''

# Modules

from ctypes import windll  # To Enable High Resolution Scaling in Windows OS

from tkinter import *

import sys  # noqa: E402
sys.path.append('Code\Sudoku')  # noqa: E402
sys.path.append('Code\Rat in a Maze')  # noqa: E402

# Importing Rat in a Maze and Sudoku Codes
import Rat_in_a_maze_UI  # noqa: E402
import solve_sudoku_UI  # noqa: E402

windll.shcore.SetProcessDpiAwareness(1)

master = Tk()
master.title("Solving Constraint Satisfaction Problems using RAT")
master.geometry("1920x1080")

# Intro Screen
intro = Frame(master)
intro.place(anchor="nw")

bg = PhotoImage(file=r"Code\Assets\intro.png")
canvas1 = Canvas(intro, height=1080, width=1920)
canvas1.pack()
canvas1.create_image(0, -40, image=bg, anchor="nw")

intro.after(3000, intro.destroy)
intro.wait_window(intro)

# choose screen
choose = Frame(master)
choose.place(anchor="nw")

bg = PhotoImage(file=r"Code\Assets\choose.png")
canvas2 = Canvas(choose, height=1080, width=1920)
canvas2.pack()
canvas2.create_image(0, -40, image=bg, anchor="nw")

# Images for Buttons
click_sudoku = PhotoImage(file=r'Code\Assets\sudoku_img.png')
click_riam = PhotoImage(file=r'Code\Assets\riam_img.png')

img_label = Label(image=click_sudoku, bg="#ffffff")
img_label = Label(image=click_riam, bg="#ffffff")

# Buttons for choosing project
Button(choose, image=click_sudoku, command=solve_sudoku_UI.sudoku_main, borderwidth=0, bg="#ffffff", highlightcolor="#ffffff").place(x=600, y=540, anchor='center')
Button(choose, image=click_riam, command=Rat_in_a_maze_UI.riam_main, borderwidth=0, bg="#ffffff", highlightcolor="#ffffff").place(x=1350, y=540, anchor='center')

Button(choose, text="Exit", command=exit, bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white").place(anchor='c', x=1650, y=950)

mainloop()
