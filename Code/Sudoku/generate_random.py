import random


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


def is_puzzle_valid(board, small_boxes):

    if(len(board) != 9):
        return False

    # Check if repeated digits are present in the 3x3 boxes
    for box in small_boxes.values():
        for element in box:
            if(element == 0):
                continue
            for other_element in range(len(box)):
                if((element == box[other_element]) and (other_element != box.index(element))):
                    return False

    # Check if same digits are present in the same row or column
    for row in range(len(board)):

        if(len(board[row]) != 9):
            return False

        for element in range(len(board[row])):
            chosen_number = board[row][element]

            if(chosen_number == 0):
                continue

            for number in range(len(board[row])):

                if(number == element):
                    continue

                if((board[row][element] == board[row][number]) and ((board[row][element] != 0) and (board[row][number] != 0))):
                    return False
                if((board[element][row] == board[number][row]) and ((board[element][row] != 0) and (board[number][row] != 0))):
                    return False
    return True
