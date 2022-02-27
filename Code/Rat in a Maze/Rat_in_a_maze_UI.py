'''
#Project Name: Rat in a maze
#Last Updated: 27/02/2022 02:17
#Last Updated by: Sarthak S Kumar
#Changelog:
`   27/02/2022 02:17 Sarthak S Kumar
        # Fixed Overlapping Text when user solves the maze
        # Widget Scaling Corrections
        # Fixed Background Images descaling and moving out of frame
    27/02/2022 22:59 Varun Chandrashekar
        # Function to manage maze box sizes and other fixes
        # Fixed obstacle boxes appearing after backtracking solution
    24/02/2022 15:05 Sarthak S Kumar
        # Success and Failure Messages
    24/02/2022 15:10 Varun Chandrashekar
        # Scaling Issues resolved
    23/02/2022 23:12 Sarthak S Kumar
        # Functionality to change the color of squares visited previously
        # Canvas size updation in maze_ui
        # Code Refinement and Comments
    23/02/2022 20:54 Sarthak S Kumar
        # Added Functionality to check whether the user solution is correct or not
        # UI updation when user solves the maze, or gives up
        # Added Timer functionality
        # Code Refinement and Comments
    22/02/2022 21:47 Sarthak S Kumar
        # Added Functionality to let the user solve the maze manually
        # Comments and Decluttering
    21/02/2022 11:40 Sarthak S Kumar
        # Added the new try, prompt window (Exit Screen)
        # Fixed Username not displaying while using main()
    08/02/2022 20:40 Sarthak S Kumar
        # Added Welcome Screen, User Entry Screen, and Maze UI Screen
        # Show the randomly generated maze
        # Show the solution for the randomly generated maze
    
    08/02/2022 9:10 Vishal M Godi
        # Algorithm to solve Rat in a Maze using Backtracking
#Pending:
    --Cleared
'''
# Modules
import numpy as np
import random
import time
import copy
import datetime
from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk

from ctypes import windll  # To Enable High Resolution Scaling in Windows OS
windll.shcore.SetProcessDpiAwareness(1)

global first_puzzle
first_puzzle = True

# Set the size of the box according to the screen resolution and the number of boxes


def manage_box_size(height, width, N):
    squaresize = int((((height*width)/(5))/(N**2))**0.5)
    return squaresize


def riam_main():  # Program execution begins from here.
    """Tkinter Window Initialisation"""
    master = Tk()
    master.title("Rat in a Maze")
    # master.attributes('-fullscreen', True) #To enable fullscreen mode

    # Get the resolution of working monitor
    height = master.winfo_screenheight()
    width = master.winfo_screenwidth()
    resolution = str(width) + "x" + str(height)

    master.geometry(resolution)
    master.configure(bg="#ffffff")

    if first_puzzle:

        """ Welcome Screen """
        intro = Frame(master)
        intro.place(anchor="nw")

        bg = PhotoImage(file=r"Code\Rat in a Maze\Assets\intro.png")  # ./Assets/intro.png (Mac)
        canvas1 = Canvas(intro, height=height, width=width)
        canvas1.pack()
        canvas1.create_image(0, 0, image=bg, anchor="nw")

        intro.after(3000, intro.destroy)
        intro.wait_window(intro)

    """User Entry Screen"""
    user_entry = Frame(master, background="#ffffff")
    user_entry.pack()

    bg = PhotoImage(file=r"Code\Rat in a Maze\Assets\user_entry.png")  # ./Assets/user_entry.png (Mac)
    canvas1 = Canvas(user_entry, height=height, width=width)
    canvas1.pack()
    canvas1.create_image(0, 0, image=bg, anchor="nw")

    Label(user_entry, text="Welcome", font=(r"HK Grotesk", 50), fg="#000000", bg="#ffffff").place(anchor='c', x=(960/1920)*width + (2*width)/10, y=(275/1080)*height)

    Label(user_entry, text="Your Name: ", font=(r"HK Grotesk", 25), fg="#000000", bg="#ffffff").place(anchor='e', x=(800/1920)*width + (2*width)/10, y=(450/1080)*height)

    sizebox = Entry(user_entry, font=(r"HK Grotesk", 20), fg="#000000", bg="#ffffff")
    sizebox.place(anchor='w', x=(960/1920)*width + (2*width)/10, y=(450/1080)*height)

    Label(user_entry, text="Maze Size: ", font=(r"HK Grotesk", 25), fg="#000000", bg="#ffffff").place(anchor='e', x=(800/1920)*width + (2*width)/10, y=(540/1080)*height)

    clicked = StringVar()
    clicked.set("Select one")

    gridsizes = ["5 x 5", "8 x 8", "10 x 10", "15 x 15", "20 x 20", "25 x 25"]
    drop = OptionMenu(user_entry, clicked, *gridsizes)
    drop.place(anchor='w', x=(960/1920)*width + (2*width)/10, y=(540/1080)*height)
    drop.config(font=(r'HK Grotesk', (20)), bg='#ffffff', fg="#000000")

    def movenext():
        global N, username, x
        username = sizebox.get()  # Maze Size Variable
        x = clicked.get().split()
        N = int(x[0])
        user_entry.after(1000, user_entry.destroy)

    submit = Button(user_entry, text="Submit", command=movenext, bg="#4d1354", font=(r'HK Grotesk', (25)), fg="white").place(anchor='c', x=(960/1920)*width + (2*width)/10, y=(800/1920)*width)

    user_entry.wait_window(user_entry)

    """ Maze Initialisation and Solution Generation (Backtracking)"""
    sol_maze = []
    while True:
        global maze
        maze = np.random.randint(2, size=(N, N))

        def MAZE(maze):
            global sol
            sol = copy.deepcopy(maze)

            if BACKTRACKING_ALGORITHM(maze, 0, 0, sol) == False:
                return False

            return True

        def BACKTRACKING_ALGORITHM(maze, x, y, sol):

            if x == N - 1 and y == N - 1:
                sol[x][y] = 5
                return True

            if check(maze, x, y) == True:
                sol[x][y] = 5

                if BACKTRACKING_ALGORITHM(maze, x + 1, y, sol) == True:
                    return True

                if BACKTRACKING_ALGORITHM(maze, x, y + 1, sol) == True:
                    return True

                sol[x][y] = 1
                return False

        def check(maze, x, y):
            if x >= 0 and x < N and y >= 0 and y < N and maze[x][y] == 1:
                return True

        if MAZE(maze) == False or maze[N - 1][N - 1] == 0 or maze[0][0] == 0:
            continue
        break

    """Maze UI"""
    squaresize = manage_box_size(height, width, N)  # Dynamically changes with the maze size
    tile_color = " "
    rectbox_coordinates = [0, 0, squaresize, squaresize]
    forbidden = []  # To store co-ordinates of obstacle boxes in maze grid

    maze_UI = Frame(master, background="#fffceb")
    maze_UI.pack()

    bg2 = PhotoImage(file=r"Code\Rat in a Maze\Assets\maze_ui.png")  # ./Assets/maze_ui.png (Mac)
    canvas2 = Canvas(maze_UI, height=height, width=width)
    canvas2.pack()
    canvas2.create_image(0, 0, image=bg2, anchor="nw")

    headline = Label(maze_UI, text=f"Hello {username}\n Your {tile_color.join(x)} maze is here. Solve it", font=(r"HK Grotesk", 30), fg="#000000", bg="#ffffff")
    headline.place(anchor='center', x=(1390/1920)*width, y=(375/1080)*height)

    # Canvas to display Maze to be solved
    question_canvas = Canvas(maze_UI, height=(N * squaresize)-squaresize/10, width=(N * squaresize)-squaresize/10, bg='#ffffff')
    question_canvas.place(anchor='center', x=(500/1920)*width, y=(512/1080)*height)

    # Drawing the maze to be solved in the question canvas
    for i in maze:
        for j in i:
            if j == 1:
                color = "white"
            else:
                color = "black"
                forbidden.append((rectbox_coordinates[0], rectbox_coordinates[1], rectbox_coordinates[2], rectbox_coordinates[3]))

            square = question_canvas.create_rectangle(rectbox_coordinates[0], rectbox_coordinates[1], rectbox_coordinates[2], rectbox_coordinates[3], fill=color, width=0)
            rectbox_coordinates[0] += squaresize
            rectbox_coordinates[2] += squaresize

        rectbox_coordinates[0], rectbox_coordinates[2] = 0, squaresize
        rectbox_coordinates[1] += squaresize
        rectbox_coordinates[3] += squaresize

    # Rat Object to Traverse through the maze
    rat = question_canvas.create_oval(0, 0, squaresize, squaresize, fill="green", width=0)

    endpoint = question_canvas.create_rectangle(squaresize*(N-1), squaresize*(N-1), squaresize*N, squaresize * N, fill="#660033", outline="#660033")

    use = Label(maze_UI, text="Use", font=(r"HK Grotesk", 20), fg="#000000", bg="#ffffff")
    use.place(anchor='e', x=((height+width)/2 - (width/7)), y=(540/1080)*height)

    img = Image.open(r"Code\Rat in a Maze\Assets\arrowkeys.png")  # ./Assets/arrowkeys.png (Mac)
    img = img.resize((int((height*width)/(4*(height+width))), int((height*width)/(4*(height+width)))), Image.ANTIALIAS)
    photoImg = ImageTk.PhotoImage(img)

    arrow = Canvas(maze_UI, width=(height*width)/(4*(height+width)), height=(height*width)/(4*(height+width)), bg="white", bd=0, highlightthickness=0, relief='ridge')
    arrow.place(x=(height+width)/2 - (width/22), y=(540/1080)*height, anchor='e')
    arrow.create_image(0, 0, image=photoImg, anchor='nw')

    labe = Label(maze_UI, text="to move the rat", font=(r"HK Grotesk", 20), fg="#000000", bg="#ffffff")
    labe.place(anchor='w', x=(height+width)/2 - (width/25), y=(540/1080)*height)

    visited_squares = []  # List to stores the squares in which the rat has been before

    def pathsquare(coord):  # To change color of the path traversed accordingly
        if [coord[0], coord[1], coord[2], coord[3]] not in visited_squares:
            visited_squares.append([coord[0], coord[1], coord[2], coord[3]])
            question_canvas.create_rectangle(coord[0], coord[1], coord[2], coord[3], fill="purple", width=0)
            question_canvas.tag_raise(rat)
        else:
            question_canvas.create_rectangle(coord[0], coord[1], coord[2], coord[3], fill="orange", width=0)
            question_canvas.tag_raise(rat)

    def nextstep():  # When Next button is clicked
        Next = Tk()
        Next.geometry(str(int(1500/1920*width)) + "x" + str(int(300/1080*height)))
        Next.title("Solving the Maze")
        Next.configure(bg="#ffffff", border=1)
        message = Label(Next, text=f"Wanna solve another maze?", font=(
            r"HK Grotesk", 30), fg="#000000", bg="#ffffff")
        message.place(anchor='center', x=(750/1080)*height, y=(100/1080)*height)

        def restart():  # Restart the program
            global first_puzzle
            Next.destroy()
            master.destroy()
            first_puzzle = False
            riam_main()

        yes = Button(Next, text="Yeah", command=restart, bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
        yes.place(anchor='center', x=(550/1080)*height, y=(200/1080)*height)
        no = Button(Next, text="Nah", command=exit, bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
        no.place(anchor='center', x=(950/1080)*height, y=(200/1080)*height)

    def user_solved():  # When user manages to solve the maze

        use.destroy()
        arrow.destroy()
        labe.destroy()
        headline.destroy()
        comp_solve.destroy()

        # To check the number of seconds elapsed after game started
        endtime = datetime.datetime.now()
        td = endtime - starttime
        elapsed = td.total_seconds()
        successmessages = ["Yay! You made it!", "Good one fella!", "That was quite easy!", "Wonderful!", "You aced it!"]
        Label(maze_UI, text="🎉 Congratulations 🎉", font=(r"HK Grotesk", 40), fg="#000000", bg="#ffffff").place(anchor='center', x=(1390/1920)*width, y=(375/1080)*height)
        Label(maze_UI, text=random.choice(successmessages), font=(r"HK Grotesk", 30), fg="#000000", bg="#ffffff").place(anchor='center', x=(1390/1920)*width, y=(455/1080)*height)
        Label(maze_UI, text=f"You solved the maze in {round(elapsed, 2)} seconds", font=(r"HK Grotesk", 20), fg="#000000", bg="#ffffff").place(anchor='center', x=(1390/1920)*width, y=(520/1080)*height)

        # Displays Confirmation Window on clicking next
        nextb = Button(maze_UI, text="Next", command=nextstep, bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
        nextb.place(anchor='center', x=(1390/1920)*width, y=(600/1080)*height)

    # Keybind Events
    def left(event):
        rat_xy = question_canvas.coords(rat)
        if rat_xy[0] > 0:
            x = -squaresize
            y = 0
            if (rat_xy[0] + x, rat_xy[1], rat_xy[2] + x, rat_xy[3]) not in forbidden:
                question_canvas.move(rat, x, y)
                pathsquare(rat_xy)
        if question_canvas.coords(rat) == [squaresize*(N-1), squaresize*(N-1), squaresize*N, squaresize * N]:
            user_solved()

    def right(event):
        rat_xy = question_canvas.coords(rat)
        if rat_xy[2] <= N * squaresize - 1:
            x = squaresize
            y = 0
            if (rat_xy[0] + x, rat_xy[1], rat_xy[2] + x, rat_xy[3]) not in forbidden:
                question_canvas.move(rat, x, y)
                pathsquare(rat_xy)
        if question_canvas.coords(rat) == [squaresize*(N-1), squaresize*(N-1), squaresize*N, squaresize * N]:
            user_solved()

    def up(event):
        rat_xy = question_canvas.coords(rat)
        if rat_xy[1] > 0:
            x = 0
            y = -squaresize
            if (rat_xy[0], rat_xy[1] + y, rat_xy[2], rat_xy[3] + y) not in forbidden:
                question_canvas.move(rat, x, y)
                pathsquare(rat_xy)
        if question_canvas.coords(rat) == [squaresize*(N-1), squaresize*(N-1), squaresize*N, squaresize * N]:
            user_solved()

    def down(event):
        rat_xy = question_canvas.coords(rat)
        if rat_xy[3] <= N * squaresize - 1:
            x = 0
            y = squaresize
            if (rat_xy[0], rat_xy[1] + y, rat_xy[2], rat_xy[3] + y) not in forbidden:
                question_canvas.move(rat, x, y)
                pathsquare(rat_xy)
        if question_canvas.coords(rat) == [squaresize*(N-1), squaresize*(N-1), squaresize*N, squaresize * N]:
            user_solved()

    master.bind("<Left>", left)
    master.bind("<Right>", right)
    master.bind("<Up>", up)
    master.bind("<Down>", down)

    global starttime, endtime
    starttime = datetime.datetime.now()

    # When user gives up on solving the maze
    def solve():
        question_canvas.destroy()

        # To display the maze solution
        solution_canvas = Canvas(maze_UI, height=(N * squaresize)-squaresize/10, width=(N * squaresize)-squaresize/10, bg='#ffffff')
        solution_canvas.place(anchor='center', x=(500/1920)*width, y=(512/1080)*height)

        rectbox_coordinates = [0, 0, squaresize, squaresize]
        for i in sol:
            for j in i:
                if j == 5:
                    color = "green"
                elif j == 1:
                    color = "white"
                else:
                    color = "black"
                square = solution_canvas.create_rectangle(rectbox_coordinates[0], rectbox_coordinates[1], rectbox_coordinates[2], rectbox_coordinates[3], fill=color, width=0)
                rectbox_coordinates[0] += squaresize
                rectbox_coordinates[2] += squaresize

            rectbox_coordinates[0], rectbox_coordinates[2] = 0, squaresize
            rectbox_coordinates[1] += squaresize
            rectbox_coordinates[3] += squaresize

        use.destroy()
        arrow.destroy()
        labe.destroy()
        headline.destroy()
        comp_solve.destroy()

        failmessages = [r"❌ You gave up so quick!", r"🧠 Was it really tough?", r"😂 Help yourself!", "👎 You couldn't make it!"]
        Label(maze_UI, text=random.choice(failmessages), font=(r"HK Grotesk", 40), fg="#000000", bg="#ffffff").place(anchor='center', x=(1390/1920)*width, y=(375/1080)*height)
        Label(maze_UI, text=f"Better luck next time!", font=(r"HK Grotesk", 20), fg="#000000", bg="#ffffff").place(anchor='center', x=(1390/1920)*width, y=(475/1080)*height)

        # Displays Confirmation Window on clicking next
        nextb = Button(maze_UI, text="Next", command=nextstep,
                       bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
        nextb.place(anchor='center', x=(1390/1920)*width, y=(600/1080)*height)

    # Button to let computer display the solution
    comp_solve = Button(maze_UI, text="Give Up!", command=solve,
                        bg="#4d1354", font=(r'HK Grotesk', (20)), fg="white")
    comp_solve.place(anchor='center', x=(1390/1920)*width, y=(800/1080)*height)

    mainloop()


if __name__ == "__main__":
    riam_main()
