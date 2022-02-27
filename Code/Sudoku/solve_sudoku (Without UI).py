import math
from generate_random import generate

# Split the 9x9 puzzle into the 3x3 squares


def make_small_boxes(current_board):

    small_boxes = {
        "11": [],
        "12": [],
        "13": [],
        "21": [],
        "22": [],
        "23": [],
        "31": [],
        "32": [],
        "33": [],
    }

    for row in range(1, 10):
        arg1 = math.ceil(row/3)

        for column in range(1, 10):

            arg2 = math.ceil(column/3)
            args = str(arg1) + str(arg2)
            small_boxes[args].append(current_board[row-1][column-1])

    return small_boxes

# Get empty position in the puzzle


def empty(board):
    for row in range(len(board)):
        for column in range(len(board[row])):
            if(board[row][column] == 0):
                return(row, column)

    return None

# Check whether board is valid if number is inserted in given position


def is_position_valid(board, small_boxes, number, position):

    for i in range(9):
        if((i != position[1]) and (number == board[position[0]][i])):  # Check in the same row
            return "r"
        elif((i != position[0]) and (number == board[i][position[1]])):  # Check in the same column
            return "c"

    args = str(math.floor(position[0]/3)+1)+str(math.floor(position[1]/3)+1)

    if(number in small_boxes[args]):  # Check in the small 3x3 boxes
        return "b"

    return ""

# Solving the


def solve(puzzle, small_boxes):

    print("/"*100)
    display_board(puzzle)
    empty_position = empty(puzzle)

    if not empty_position:
        return True  # Return if there is no empty position
    else:
        row, column = empty_position

    for i in range(1, 10):

        if(not is_position_valid(puzzle, small_boxes, i, (row, column))):  # If a valid number is found put it in the puzzle
            puzzle[row][column] = i
            small_boxes = make_small_boxes(puzzle)

            if solve(puzzle, small_boxes):
                return True

            puzzle[row][column] = 0  # Backtrack

    return False


def start(puzzle, original):

    display_board(puzzle)
    print("\n\nPress 'y' to solve the puzzle, or try to solve it yourself!\n\nPress any key to start solving\n")


def display_board(board):
    for row in board:
        print("—"*38)
        for element in row:
            if element == 0:
                element = "◼"
            print(" | " + str(element), end="")
        print(" |")


if __name__ == '__main__':

    problem = generate(1, make_small_boxes)
    print(problem)
    '''solve(problem, make_small_boxes(problem))
    display_board(problem)'''
