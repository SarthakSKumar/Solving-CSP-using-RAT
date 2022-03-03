"""
Project Name: solve_sudoku
Last Updated: 02/03/2022 18:33
Last Updated by: Sarthak S Kumar
"""
# Modules
import copy
import math
import random
import datetime
from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
from ctypes import windll

# Variables
first_puzzle = True
white = "#ffffff"
black = "#000000"
purple = "#4d1354"
font_face = "HK Grotesk"

# Functions
windll.shcore.SetProcessDpiAwareness(1)  # To Enable High Resolution Scaling in Windows OS


# Sudoku Global Functions
def generate(difficulty, make_small_boxes):

    initial = [
        [9, 5, 7, 6, 1, 3, 2, 8, 4],
        [4, 8, 3, 2, 5, 7, 1, 9, 6],
        [6, 1, 2, 8, 4, 9, 5, 3, 7],
        [1, 7, 8, 3, 6, 4, 9, 5, 2],
        [5, 2, 4, 9, 7, 1, 3, 6, 8],
        [3, 6, 9, 5, 2, 8, 7, 4, 1],
        [8, 4, 5, 7, 9, 2, 6, 1, 3],
        [2, 9, 1, 4, 3, 6, 8, 7, 5],
        [7, 3, 6, 1, 8, 5, 4, 2, 9]
    ]

    shuffles = random.randint(5, 11)

    # shuffling columns and rows
    for i in range(shuffles):

        indexs = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

        for index in indexs:
            indices = random.sample(index, 2)

            for row in initial:
                row[indices[0]], row[indices[1]
                                     ] = row[indices[1]], row[indices[0]]
            initial[indices[0]], initial[indices[1]
                                         ] = initial[indices[1]], initial[indices[0]]

    if(difficulty == 1):
        probability = (0.6, 0.4)
    elif(difficulty == 2):
        probability = (0.5, 0.5)
    elif(difficulty == 3):
        probability = (0.4, 0.6)

    for row in initial:
        for pos in range(0, 9):
            if random.choices([True, False], weights=probability)[0]:
                row[pos] = 0

    if(is_puzzle_valid(initial, make_small_boxes(initial))):
        return initial
    else:
        return None


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


first_puzzle = True


def sudoku_main():  # Program execution begins from here.
    """Tkinter Window Initialisation"""

    master = Toplevel()  # master = Tk() if main window
    master.title("Solve Sudoku")
    # master.attributes('-fullscreen', True) #To enable fullscreen mode

    master.geometry("1920x1080")
    master.configure(bg=purple)

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
    user_entry = Frame(master, background=purple)
    user_entry.pack()

    bg = PhotoImage(file=r"Code\Sudoku\Assets\user_entry.png")
    canvas1 = Canvas(user_entry, height=1080, width=2000)
    canvas1.pack()
    canvas1.create_image(0, 0, image=bg, anchor="nw")

    Label(user_entry, text="Welcome", font=(font_face, 50), fg=white, bg=purple).place(anchor='center', x=960, y=275)

    Label(user_entry, text="Your Name: ", font=(font_face, 25), fg=white, bg=purple).place(anchor='e', x=800, y=450)

    sizebox = Entry(user_entry, font=(font_face, 20), fg=white, bg=purple)
    sizebox.place(anchor='w', x=960, y=450)

    def movenext():
        global username
        username = sizebox.get()
        user_entry.after(1000, user_entry.destroy)

    submit = Button(user_entry, text="Submit", command=movenext, bg=white, font=(font_face, (25)), fg=purple).place(anchor="center", x=960, y=800)
    user_entry.wait_window(user_entry)

    """Sudoku UI"""
    sudoku_UI = Frame(master, background=purple)
    sudoku_UI.pack()

    bg2 = PhotoImage(file=r"Code\Sudoku\Assets\sudoku_UI.png")
    canvas2 = Canvas(sudoku_UI, height=1080, width=2000)
    canvas2.pack()
    canvas2.create_image(0, 0, image=bg2, anchor="nw")

    headline = Label(sudoku_UI, text=f"Hello {username}\n Your sudoku is here. Go ahead, Solve it", font=(font_face, 30), fg=white, bg=purple)
    headline.place(anchor='center', x=1390, y=375)

    use = Label(sudoku_UI, text="Use" + " "*16 + "to enter numbers", font=(font_face, 20), fg=white, bg=purple)
    use.place(anchor='center', x=1395, y=540)

    img = Image.open(r"Code\Sudoku\Assets\numpad.png")  # ./Assets/arrowkeys.png (Mac)
    img = img.resize((100, 100), Image.ANTIALIAS)
    photoImg = ImageTk.PhotoImage(img)

    numpad = Canvas(sudoku_UI, width=100, height=100, bg=purple, bd=0, highlightthickness=0, relief='ridge')
    numpad.place(x=1295, y=540, anchor='center')
    numpad.create_image(0, 0, image=photoImg, anchor='nw')

    use2 = Label(sudoku_UI, text="and" + " "*16 + "to move the selector", font=(font_face, 20), fg=white, bg=purple)
    use2.place(anchor='center', x=1390, y=640)

    img2 = Image.open(r"Code\Sudoku\Assets\arrowkeys.png")  # ./Assets/arrowkeys.png (Mac)
    img2 = img2.resize((100, 100), Image.ANTIALIAS)
    photoImg2 = ImageTk.PhotoImage(img2)

    arrow = Canvas(sudoku_UI, width=100, height=100, bg=purple, bd=0, highlightthickness=0, relief='ridge')
    arrow.place(x=1270, y=640, anchor='center')
    arrow.create_image(0, 0, image=photoImg2, anchor='nw')

    # Canvas to display sudoku puzzle
    question_canvas = Canvas(sudoku_UI, height=720, width=720, bg=purple, bd=0, highlightthickness=0, relief='ridge')
    question_canvas.place(anchor='center', x=500, y=512)

    for i in (0, 3, 6, 9):  # To draw lines
        question_canvas.create_line(0, 80*i, 730, 80*i, width=5, fill=white)
        question_canvas.create_line(80*i, 0, 80*i, 730, width=5, fill=white)

    for i in range(11):
        question_canvas.create_line(80*i, 0, 80*i, 730, width=2, fill=white)
        question_canvas.create_line(0, 80*i, 730, 80*i, width=2, fill=white)

    problem = generate(1, make_small_boxes)  # Generates random valid sudoku puzzle
    y_coord, x_coord, p, q = 40, 40, 0, 0
    allowed_squares = []
    for i in problem:  # adding numbers from question puzzle
        for j in i:
            if j == 0:
                j = ""
                allowed_squares.append((x_coord-40, y_coord-40, x_coord+40, y_coord+40))
            question_canvas.create_text(x_coord, y_coord, font=(font_face, 30), fill=white, text=j)
            x_coord += 80
            p += 1
        p = 0
        x_coord = 40
        y_coord += 80
        q += 1

    pos = allowed_squares[1]
    selector = question_canvas.create_rectangle(pos[0], pos[1], pos[2], pos[3], fill=purple, width=3, outline="#35668f")

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
            y = question_canvas.create_rectangle(selector_xy[0], selector_xy[1], selector_xy[2], selector_xy[3], fill=purple, outline=white, width=2)
            x = question_canvas.create_text(selector_xy[0]+40, selector_xy[1]+40, font=(font_face, 30), fill="#f2ea52", text=event)
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
        Next.configure(bg=purple, border=1)
        message = Label(Next, text=f"Wanna solve another maze?", font=(font_face, 30), fg=white, bg=purple)
        message.place(anchor='center', x=750, y=100)

        def restart():  # Restart the program
            Next.destroy()
            master.destroy()
            sudoku_main()

        yes = Button(Next, text="Yeah", command=restart, bg=white, font=(font_face, (20)), fg=purple)
        yes.place(anchor='center', x=550, y=200)
        no = Button(Next, text="Nah", command=exit, bg=white, font=(font_face, (20)), fg=purple)
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
        Label(sudoku_UI, text=random.choice(successmessages), font=(font_face, 20), fg=white, bg=purple).place(anchor='center', x=1390, y=445)
        Label(sudoku_UI, text=f"You solved the maze in {round(elapsed, 2)} seconds", font=(font_face, 15), fg=white, bg=purple).place(anchor='center', x=1390, y=525)

        nextb = Button(sudoku_UI, text="Next", command=nextstep, bg=white, font=(font_face, (20)), fg=purple)
        nextb.place(anchor='center', x=1390, y=600)

    def solve():  # When user gives up on solving the puzzle
        question_canvas.destroy()
        check_sol.destroy()
        arrow.destroy()
        numpad.destroy()
        use.destroy()
        use2.destroy()
        # To display the maze solution
        solution_canvas = Canvas(sudoku_UI, height=720, width=720, bg=purple, bd=0, highlightthickness=0, relief='ridge')
        solution_canvas.place(anchor='center', x=500, y=512)

        for i in (0, 3, 6, 9):  # To draw lines
            solution_canvas.create_line(0, 80*i, 730, 80*i, width=5, fill=white)
            solution_canvas.create_line(80*i, 0, 80*i, 730, width=5, fill=white)

        for i in range(11):
            solution_canvas.create_line(80*i, 0, 80*i, 730, width=2, fill=white)
            solution_canvas.create_line(0, 80*i, 730, 80*i, width=2, fill=white)

        y_coord, x_coord = 40, 40
        for i in sudoku_sol:  # Displays the puzzle answer
            for j in i:
                solution_canvas.create_text(x_coord, y_coord, font=(font_face, 30), fill=white, text=j)
                x_coord += 80
            x_coord = 40
            y_coord += 80

        comp_solve.destroy()

        failmessages = [r"❌ You gave up so quick!", r"🧠 Was it really tough?", r"😂 Help yourself!", "👎 You couldn't make it!"]
        headline.configure(text=random.choice(failmessages))
        Label(sudoku_UI, text="Better luck next time", font=(font_face, 20), fg=white, bg=purple).place(anchor='center', x=1390, y=445)
        Label(sudoku_UI, text=f"With Experience comes Expertise!", font=(font_face, 15), fg=white, bg=purple).place(anchor='center', x=1390, y=525)

        # Displays Confirmation Window on clicking next
        nextb = Button(sudoku_UI, text="Next", command=nextstep, bg=white, font=(font_face, (20)), fg=purple)
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
                Label(sudoku_UI, text="Check it again!", font=(font_face, 20), fg=white, bg=purple).place(anchor='center', x=1390, y=445)
                Label(sudoku_UI, text=f"Chances Remaining: {10-chances}", font=(font_face, 15), fg=white, bg=purple).place(anchor='center', x=1390, y=525)
            else:
                solve()

    # Button to let computer solve the puzzle
    comp_solve = Button(sudoku_UI, text="Solve Sudoku", command=solve,
                        bg=white, font=(font_face, (20)), fg=purple)
    comp_solve.place(anchor='center', x=1640, y=800)

    # Button to check the user solution
    check_sol = Button(sudoku_UI, text="Check Solution", command=check, bg=white, font=(font_face, (20)), fg=purple)
    check_sol.place(anchor='center', x=1140, y=800)

    mainloop()


# For Standalone
"""if __name__ == "__main__":
    sudoku_main()
"""
