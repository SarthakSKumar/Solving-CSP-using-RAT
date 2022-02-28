'''
#Project Name: solve_sudoku
#Last Updated: 27/02/2022 15:29
#Last Updated by: Sarthak S Kumar

#Changelog:
    28/02/2022 20:29 Sarthak S Kumar
        #Fixed Error while trying to execute from main.py
        
    27/02/2022 15:29 Sarthak S Kumar
        # Fixed 'Nah' Button Not working in next_UI
        # Fixed Numbers overlaying above existing numbers in Sudoku_UI
        # Added play info in sudoku_UI screen
        # Added chances available functionality

    26/02/2022 20:25 Sarthak S Kumar
        # Success and Failure Messages
        # Solved text overlapping during user entry in question_canvas
        # Added key bindings
        # Resolved 'Nah' Button not working in next_UI
        # Code Refinement and Comments

    26/02/2022 13:17 Varun Chandrashekar
        # Resolved Copy bug, while trying to store and access puzzle question

    25/02/2022 21:19 Sarthak S Kumar
        # Added the new try, prompt window (Exit Screen)
        # Resolved Username not displaying while using main()
        # Added Functionality to let the user solve the puzzle manually
        # UI updation when user solves the puzzle, or gives up
        # Canvas size updation in sudoku_ui

    24/02/2022 22:59 Sarthak S Kumar
        # Added Welcome Screen, User Entry Screen, and Sudoku UI Screen
        # Show the randomly generated sudoku puzzle
        # Added Navigator/Selector functionality
    
    24/02/2022 18:47 Varun Chandrashekar
        # Algorithm to solve sudoku puzzles using Backtracking
        # Command line running of the program with output
#Pending:
    # Scaling Issues
'''
# Modules
import copy
import math
from generate_random import generate
import random
import datetime
from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)


""""Sudoku Global Functions"""


def make_small_boxes(current_board):

    small_boxes = {"11": [], "12": [], "13": [], "21": [], "22": [], "23": [], "31": [], "32": [], "33": []}

    for row in range(1, 10):
        arg1 = math.ceil(row/3)

        for column in range(1, 10):

            arg2 = math.ceil(column/3)
            args = str(arg1) + str(arg2)
            small_boxes[args].append(current_board[row-1][column-1])

    return small_boxes


def empty(board):  # Get empty position in the puzzle
    for row in range(len(board)):
        for column in range(len(board[row])):
            if(board[row][column] == 0):
                return(row, column)

    return None


def is_position_valid(board, small_boxes, number, position):  # Check whether board is valid if number is inserted in given position

    for i in range(9):
        if((i != position[1]) and (number == board[position[0]][i])):  # Check in the same row
            return "r"
        elif((i != position[0]) and (number == board[i][position[1]])):  # Check in the same column
            return "c"

    args = str(math.floor(position[0]/3)+1)+str(math.floor(position[1]/3)+1)

    if(number in small_boxes[args]):  # Check in the small 3x3 boxes
        return "b"

    return ""


def csolve(puzzle, small_boxes):  # Solving the puzzle

    empty_position = empty(puzzle)

    if not empty_position:
        return True  # Return if there is no empty position
    else:
        row, column = empty_position

    for i in range(1, 10):

        if(not is_position_valid(puzzle, small_boxes, i, (row, column))):  # If a valid number is found put it in the puzzle
            puzzle[row][column] = i
            small_boxes = make_small_boxes(puzzle)

            if csolve(puzzle, small_boxes):
                return True

            puzzle[row][column] = 0  # Backtrack

    return False


global first_puzzle
first_puzzle = True


def sudoku_main():
    """Tkinter Window Initialisation"""
    master = Toplevel()  # master = Tk() if main window
    master.title("Rat in a Maze")
    # master.attributes('-fullscreen', True) #To enable fullscreen mode
    master.geometry("1920x1080")
    master.configure(bg="#4d1354")

    if first_puzzle:
        """ Welcome Screen """
        intro = Frame(master)
        intro.place(anchor="nw")

        bg = PhotoImage(file=r"Code\Sudoku\Assets\intro.png")
        canvas1 = Canvas(intro, height=1080, width=2000)
        canvas1.pack()
        canvas1.create_image(0, 0, image=bg, anchor="nw")

        intro.after(3000, intro.destroy)
        intro.wait_window(intro)

    """User Entry Screen"""
    user_entry = Frame(master, background="#4d1354")
    user_entry.pack()

    bg = PhotoImage(file=r"Code\Sudoku\Assets\user_entry.png")
    canvas1 = Canvas(user_entry, height=1080, width=2000)
    canvas1.pack()
    canvas1.create_image(0, 0, image=bg, anchor="nw")

    Label(user_entry, text="Welcome", font=(r"HK Grotesk", 50), fg="#ffffff", bg="#4d1354").place(anchor='c', x=960, y=275)

    Label(user_entry, text="Your Name: ", font=(r"HK Grotesk", 25), fg="#ffffff", bg="#4d1354").place(anchor='e', x=800, y=450)

    sizebox = Entry(user_entry, font=(r"HK Grotesk", 20), fg="#ffffff", bg="#4d1354")
    sizebox.place(anchor='w', x=960, y=450)

    def movenext():
        global username
        username = sizebox.get()
        user_entry.after(1000, user_entry.destroy)

    submit = Button(user_entry, text="Submit", command=movenext, bg="#ffffff", font=(r'HK Grotesk', (25)), fg="#4d1354").place(anchor='c', x=960, y=800)
    user_entry.wait_window(user_entry)

    """Sudoku UI"""
    sudoku_UI = Frame(master, background="#4d1354")
    sudoku_UI.pack()

    bg2 = PhotoImage(file=r"Code\Sudoku\Assets\sudoku_UI.png")
    canvas2 = Canvas(sudoku_UI, height=1080, width=2000)
    canvas2.pack()
    canvas2.create_image(0, 0, image=bg2, anchor="nw")

    headline = Label(sudoku_UI, text=f"Hello {username}\n Your sudoku is here. Go ahead, Solve it", font=(r"HK Grotesk", 30), fg="#ffffff", bg="#4d1354")
    headline.place(anchor='center', x=1390, y=375)

    use = Label(sudoku_UI, text="Use" + " "*16 + "to enter numbers", font=(r"HK Grotesk", 20), fg="#ffffff", bg="#4d1354")
    use.place(anchor='center', x=1395, y=540)

    img = Image.open(r"Code\Sudoku\Assets\numpad.png")  # ./Assets/arrowkeys.png (Mac)
    img = img.resize((100, 100), Image.ANTIALIAS)
    photoImg = ImageTk.PhotoImage(img)

    numpad = Canvas(sudoku_UI, width=100, height=100, bg="#4d1354", bd=0, highlightthickness=0, relief='ridge')
    numpad.place(x=1295, y=540, anchor='center')
    numpad.create_image(0, 0, image=photoImg, anchor='nw')

    use2 = Label(sudoku_UI, text="and" + " "*16 + "to move the selector", font=(r"HK Grotesk", 20), fg="#ffffff", bg="#4d1354")
    use2.place(anchor='center', x=1390, y=640)

    img2 = Image.open(r"Code\Sudoku\Assets\arrowkeys.png")  # ./Assets/arrowkeys.png (Mac)
    img2 = img2.resize((100, 100), Image.ANTIALIAS)
    photoImg2 = ImageTk.PhotoImage(img2)

    arrow = Canvas(sudoku_UI, width=100, height=100, bg="#4d1354", bd=0, highlightthickness=0, relief='ridge')
    arrow.place(x=1270, y=640, anchor='center')
    arrow.create_image(0, 0, image=photoImg2, anchor='nw')

    # Canvas to display sudoku puzzle
    question_canvas = Canvas(sudoku_UI, height=720, width=720, bg='#4d1354', bd=0, highlightthickness=0, relief='ridge')
    question_canvas.place(anchor='center', x=500, y=512)

    for i in (0, 3, 6, 9):  # To draw lines
        question_canvas.create_line(0, 80*i, 730, 80*i, width=5, fill="#ffffff")
        question_canvas.create_line(80*i, 0, 80*i, 730, width=5, fill="#ffffff")

    for i in range(11):
        question_canvas.create_line(80*i, 0, 80*i, 730, width=2, fill="#ffffff")
        question_canvas.create_line(0, 80*i, 730, 80*i, width=2, fill="#ffffff")

    problem = generate(1, make_small_boxes)  # Generates random valid sudoku puzzle
    y_coord, x_coord, p, q = 40, 40, 0, 0
    allowed_squares = []
    for i in problem:  # adding numbers from question puzzle
        for j in i:
            if j == 0:
                j = ""
                allowed_squares.append((x_coord-40, y_coord-40, x_coord+40, y_coord+40))
            question_canvas.create_text(x_coord, y_coord, font=(r"HK Grotesk", 30), fill="#ffffff", text=j)
            x_coord += 80
            p += 1
        p = 0
        x_coord = 40
        y_coord += 80
        q += 1

    pos = allowed_squares[1]
    selector = question_canvas.create_rectangle(pos[0], pos[1], pos[2], pos[3], fill="#4d1354", width=3, outline="#35668f")

    # KeyBind Events
    def left(event):
        selector_xy = question_canvas.coords(selector)
        if selector_xy[0] > 0:
            x = -80
            y = 0
            question_canvas.move(selector, x, y)
            if (selector_xy[0] + x, selector_xy[1], selector_xy[2] + x, selector_xy[3]) in allowed_squares:
                question_canvas.tag_raise(selector)
            else:
                question_canvas.tag_lower(selector)

    def right(event):
        selector_xy = question_canvas.coords(selector)
        if selector_xy[2] <= 719:
            x = 80
            y = 0
            question_canvas.move(selector, x, y)
            if (selector_xy[0] + x, selector_xy[1], selector_xy[2] + x, selector_xy[3]) in allowed_squares:
                question_canvas.tag_raise(selector)
            else:
                question_canvas.tag_lower(selector)

    def up(event):
        selector_xy = question_canvas.coords(selector)
        if selector_xy[1] > 0:
            x = 0
            y = -80
            question_canvas.move(selector, x, y)
            if (selector_xy[0], selector_xy[1] + y, selector_xy[2], selector_xy[3] + y) in allowed_squares:
                question_canvas.tag_raise(selector)
            else:
                question_canvas.tag_lower(selector)

    def down(event):
        selector_xy = question_canvas.coords(selector)
        if selector_xy[3] <= 719:
            x = 0
            y = 80
            question_canvas.move(selector, x, y)
            if (selector_xy[0], selector_xy[1] + y, selector_xy[2], selector_xy[3] + y) in allowed_squares:
                question_canvas.tag_raise(selector)
            else:
                question_canvas.tag_lower(selector)

    usersol = copy.deepcopy(problem)  # To store a copy of the question puzzle

    csolve(problem, make_small_boxes(problem))  # Solves the sudoku puzzle
    sudoku_sol = problem

    def addnum(event):  # To add numbers entered by user in the puzzle
        selector_xy = question_canvas.coords(selector)
        if tuple(selector_xy) in allowed_squares:
            y = question_canvas.create_rectangle(selector_xy[0], selector_xy[1], selector_xy[2], selector_xy[3], fill="#4d1354", outline="#ffffff", width=2)
            x = question_canvas.create_text(selector_xy[0]+40, selector_xy[1]+40, font=(r"HK Grotesk", 30), fill="#f2ea52", text=event)
            usersol[int((selector_xy[3]/80))-1][int((selector_xy[2]/80))-1] = int(event)

    # Keybindings
    master.bind("<Left>", left)
    master.bind("<Right>", right)
    master.bind("<Up>", up)
    master.bind("<Down>", down)

    master.bind("1", lambda event: addnum("1"))
    master.bind("2", lambda event: addnum("2"))
    master.bind("3", lambda event: addnum("3"))
    master.bind("4", lambda event: addnum("4"))
    master.bind("5", lambda event: addnum("5"))
    master.bind("6", lambda event: addnum("6"))
    master.bind("7", lambda event: addnum("7"))
    master.bind("8", lambda event: addnum("8"))
    master.bind("9", lambda event: addnum("9"))

    global starttime, endtime  # To start the timer
    starttime = datetime.datetime.now()

    def nextstep():  # When Next button is clicked
        Next = Tk()
        Next.geometry("1500x300")
        Next.title("Solving Sudoku")
        Next.configure(bg="#4d1354", border=1)
        message = Label(Next, text=f"Wanna solve another maze?", font=(r"HK Grotesk", 30), fg="#ffffff", bg="#4d1354")
        message.place(anchor='center', x=750, y=100)

        def restart():  # Restart the program
            Next.destroy()
            master.destroy()
            sudoku_main()

        yes = Button(Next, text="Yeah", command=restart, bg="#ffffff", font=(r'HK Grotesk', (20)), fg="#4d1354")
        yes.place(anchor='center', x=550, y=200)
        no = Button(Next, text="Nah", command=exit, bg="#ffffff", font=(r'HK Grotesk', (20)), fg="#4d1354")
        no.place(anchor='center', x=950, y=200)

    def user_solved():  # When user manages to solve the maze
        comp_solve.destroy()
        check_sol.destroy()
        arrow.destroy()
        numpad.destroy()
        use.destroy()
        use2.destroy()

        # To check the number of seconds elapsed after game started
        endtime = datetime.datetime.now()
        td = endtime - starttime
        elapsed = td.total_seconds()

        successmessages = ["Yay! You made it!", "Good one fella!", "That was quite easy!", "Wonderful!", "You aced it!"]
        headline.configure(text=r"🎉 Congratulations 🎉")
        Label(sudoku_UI, text=random.choice(successmessages), font=(r"HK Grotesk", 20), fg="#ffffff", bg="#4d1354").place(anchor='center', x=1390, y=445)
        Label(sudoku_UI, text=f"You solved the maze in {round(elapsed, 2)} seconds", font=(r"HK Grotesk", 15), fg="#ffffff", bg="#4d1354").place(anchor='center', x=1390, y=525)

        nextb = Button(sudoku_UI, text="Next", command=nextstep, bg="#ffffff", font=(r'HK Grotesk', (20)), fg="#4d1354")
        nextb.place(anchor='center', x=1390, y=600)

    def solve():  # When user gives up on solving the puzzle
        question_canvas.destroy()
        check_sol.destroy()
        arrow.destroy()
        numpad.destroy()
        use.destroy()
        use2.destroy()
        # To display the maze solution
        solution_canvas = Canvas(sudoku_UI, height=720, width=720, bg='#4d1354', bd=0, highlightthickness=0, relief='ridge')
        solution_canvas.place(anchor='center', x=500, y=512)

        for i in (0, 3, 6, 9):  # To draw lines
            solution_canvas.create_line(0, 80*i, 730, 80*i, width=5, fill="#ffffff")
            solution_canvas.create_line(80*i, 0, 80*i, 730, width=5, fill="#ffffff")

        for i in range(11):
            solution_canvas.create_line(80*i, 0, 80*i, 730, width=2, fill="#ffffff")
            solution_canvas.create_line(0, 80*i, 730, 80*i, width=2, fill="#ffffff")

        y_coord, x_coord = 40, 40
        for i in sudoku_sol:  # Displays the puzzle answer
            for j in i:
                solution_canvas.create_text(x_coord, y_coord, font=(r"HK Grotesk", 30), fill="#ffffff", text=j)
                x_coord += 80
            x_coord = 40
            y_coord += 80

        comp_solve.destroy()

        failmessages = [r"❌ You gave up so quick!", r"🧠 Was it really tough?", r"😂 Help yourself!", "👎 You couldn't make it!"]
        headline.configure(text=random.choice(failmessages))
        Label(sudoku_UI, text="Better luck next time", font=(r"HK Grotesk", 20), fg="#ffffff", bg="#4d1354").place(anchor='center', x=1390, y=445)
        Label(sudoku_UI, text=f"With Experience comes Expertise!", font=(r"HK Grotesk", 15), fg="#ffffff", bg="#4d1354").place(anchor='center', x=1390, y=525)

        # Displays Confirmation Window on clicking next
        nextb = Button(sudoku_UI, text="Next", command=nextstep, bg="#ffffff", font=(r'HK Grotesk', (20)), fg="#4d1354")
        nextb.place(anchor='center', x=1390, y=600)

    chances = 0

    def check():  # Runs when user checks the solution entered
        nonlocal chances
        if usersol == sudoku_sol:
            user_solved()
        else:
            if chances == 0:
                use2.destroy()
                arrow.destroy()
                use.destroy()
                numpad.destroy()
            # Error Messages to display on not getting the right solution
            if chances < 9:
                chances += 1
                error_messages = ["You didn't get that right!", "No, something isn't right!", "Nah, its not finished yet!", "No relief mate!"]
                headline.configure(text=random.choice(error_messages))
                Label(sudoku_UI, text="Check it again!", font=(r"HK Grotesk", 20), fg="#ffffff", bg="#4d1354").place(anchor='center', x=1390, y=445)
                Label(sudoku_UI, text=f"Chances Remaining: {10-chances}", font=(r"HK Grotesk", 15), fg="#ffffff", bg="#4d1354").place(anchor='center', x=1390, y=525)
            else:
                solve()

    # Button to let computer solve the puzzle
    comp_solve = Button(sudoku_UI, text="Solve Sudoku", command=solve,
                        bg="#ffffff", font=(r'HK Grotesk', (20)), fg="#4d1354")
    comp_solve.place(anchor='center', x=1640, y=800)

    # Button to check the user solution
    check_sol = Button(sudoku_UI, text="Check Solution", command=check, bg="#ffffff", font=(r'HK Grotesk', (20)), fg="#4d1354")
    check_sol.place(anchor='center', x=1140, y=800)

    mainloop()


# For Standalone
"""if __name__ == "__main__":
    sudoku_main()
"""
