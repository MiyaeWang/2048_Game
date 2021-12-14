'''
    CS5001
    Final Project, 12/10/2021
    Fall 2021
    Mingyue Wang
    
    This game is played on a 4×4 grid board, with numbered tiles that
    slide when a player moves them using the four arrow keys.Every turn,
    a new tile randomly appears in an empty spot on the board with
    a value of either 2 or 4. Tiles slide as far as possible in the chosen
    direction until they are stopped by either another tile or the edge of the
    grid. If two tiles of the same number collide while moving, they will merge
    into a tile with the total value of the two tiles that collided.
'''


import random
import copy


# Creates the size of the board. In this game, it is 4.
boardSize = 4


# Prints the current board.
def display(currentBoard):
    # Finds out the largest spaces the number needed.
    largest = currentBoard[0][0]
    for row in currentBoard:
        for element in row:
            if element > largest:
                largest = element
    largestSpaces = len(str(largest))

    # Prints each row.
    for row in currentBoard:
        currentRow = "|"
        for element in row:
            if element == 0:
                currentRow += " " * largestSpaces + "|"
            else:
                currentRow += " " * (largestSpaces - len(str(element))) + \
                              str(element) + "|"
        print(currentRow)
    print()


# Merges one row left.
def merge_one_row_left(row):
    # Move each element to the left as possible.
    for i in range(boardSize - 1):
        for j in range(boardSize - 1, 0 , -1):
            if row[j - 1] == 0:
                row[j - 1] = row[j]
                row[j] = 0

    # Merge the two identical elements.
    for i in range(boardSize - 1):
        if row[i] == row[i + 1]:
            row[i] = 2 * row[i]
            row[i + 1] = 0

    # Move each element to the left again.
    for i in range(boardSize - 1, 0, -1):
        if row[i - 1] == 0:
            row[i - 1] = row[i]
            row[i] = 0
    return row


# Merges all rows left.
def merge_left(currentBoard):
    for i in range(boardSize):
        currentBoard[i] = merge_one_row_left(currentBoard[i])
    return currentBoard


# Reverses the order of one row.
def reverse(row):
    reverse_row = []
    for i in range(boardSize - 1, -1 , -1):
        reverse_row.append(row[i])
    return reverse_row


# Merges all rows right.
def merge_right(currentBoard):
    for i in range(boardSize):
        currentBoard[i] = reverse(currentBoard[i])
        currentBoard[i] = merge_one_row_left(currentBoard[i])
        currentBoard[i] = reverse(currentBoard[i])
    return currentBoard


# Transposes the whole board.
def transpose(currentBoard):
    for i in range(boardSize):
        for j in range(i, boardSize):
            if not i == j:
                temp = currentBoard[i][j]
                currentBoard[i][j] = currentBoard[j][i]
                currentBoard[j][i] = temp
    return currentBoard


# Merges all rows up.
def merge_up(currentBoard):
    for i in range(boardSize):
        currentBoard = transpose(currentBoard)
        currentBoard = merge_left(currentBoard)
        currentBoard = transpose(currentBoard)
    return currentBoard


# Merges all rows down.
def merge_down(currentBoard):
    for i in range(boardSize):
        currentBoard = transpose(currentBoard)
        currentBoard = merge_right(currentBoard)
        currentBoard = transpose(currentBoard)
    return currentBoard


# Picks a new value for the board.
def pick_new_value():
    if random.randint(0,3) == 0:
        return 4
    else:
        return 2


# Adds a new value to the board.
def add_new_value(currentBoard):
    rowNum = random.randint(0, boardSize - 1)
    colNum = random.randint(0, boardSize - 1)

    while not currentBoard[rowNum][colNum] == 0:
        rowNum = random.randint(0, boardSize - 1)
        colNum = random.randint(0, boardSize - 1)

    currentBoard[rowNum][colNum] = pick_new_value()


# Tests if the user has won.
def win(currentBoard):
    for row in currentBoard:
        if 2048 in row:
            return True
    return False    


# Tests if the user has lost.
def lose(currentBoard):
    tempBoard1 = copy.deepcopy(currentBoard)
    tempBoard2 = copy.deepcopy(currentBoard)

    # Tests if there is no move in any direction.
    tempBoard1 = merge_left(tempBoard1)
    if tempBoard1 == tempBoard2:
        tempBoard1 = merge_right(tempBoard1)
        if tempBoard1 == tempBoard2:
            tempBoard1 = merge_up(tempBoard1)
            if tempBoard1 == tempBoard2:
                tempBoard1 = merge_down(tempBoard1)
                if tempBoard1 == tempBoard2:
                    return True
    return False


def main():
    # Creates a blank board.
    board = []
    for i in range(boardSize):
        row = []
        for j in range(boardSize):
            row.append(0)
        board.append(row)
        
    # Fills two positions with random values.
    numNeeded = 2
    while numNeeded > 0:
        rowNum = random.randint(0, boardSize - 1)
        colNum = random.randint(0, boardSize - 1)

        if board[rowNum][colNum] == 0:
            board[rowNum][colNum] = pick_new_value()
            numNeeded -= 1

    # Prints the game instructions.
    print("Welcome to 2048! "
          "Your goal is to merge values in different directions to get 2048.\n"
          " l ---- merge left\n"
          " r ---- merge right\n"
          " u ---- merge up\n"
          " d ---- merge down\n"
          " q ---- quit the game\n")
    
    display(board)
    
    gameOver = False

    # Repeats asking for new move while the game isn't over.
    while not gameOver:
        move = input("Choose a direction to merge: ")
        validInput = True

        # Creates a copy of the board.
        tempBoard = copy.deepcopy(board)

        if move == "l":
            merge_left(board)
        elif move == "r":
            merge_right(board)
        elif move == "u":
            merge_up(board)
        elif move == "d":
            merge_down(board)
        elif move == "q":
            gameOver = True
        else:
            validInput = False

        if not validInput:
            print("Your input is invalid. Please try again.")
        elif gameOver:
            print("Goodbye!")
        else:
            if board == tempBoard:
                print("Try a different direction.")
            else:
                if win(board):
                    display(board)
                    print("You win!")
                    gameOver = True
                else:
                    add_new_value(board)
                    display(board)
                    if lose(board):
                        gameOver = True
                        print("Game Over!")


if __name__ == "__main__":
    main()










