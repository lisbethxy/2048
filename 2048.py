import random
import copy
import os

def looks(grid):
    """
    Formatterer utskriften av spill-tilstanden.
    Det lengste tallet i kolonnen setter føringer for formatteringen.
    """
    new_grid = transpose(grid)
    longest = [1, 1, 1, 1]
    i = 0
    for row in new_grid:
        for num in row:
            if len(str(num)) > longest[i]:
                longest[i] = len(str(num))
        i += 1

    grid = transpose(new_grid)
    for row in grid:
        formatted_row = []
        i = 0
        for num in row:
            format = str(num).rjust(longest[i]+1)
            formatted_row.append(format)
            i += 1
        print(f"{formatted_row[0]} {formatted_row[1]} {formatted_row[2]} {formatted_row[3]}")

def grid():
    """
    Start-grid med to 2-ere på randomiserte posisjoner.
    """
    numbers = []
    for i in range(16):
        numbers.append(0)

    for i in range(2):
        x = random.randrange(0, 16)
        while numbers[x] != 0:
            x = random.randrange(0, 16)
        numbers[x] = 2
    
    grid = [[], [], [], []]
    i = 0
    for element in numbers:
        if len(grid[i]) < 4:
            grid[i].append(element)
        else:
            i += 1
            grid[i].append(element)
    return grid

def new_number(grid):
    """
    Erstatter en tilfeldig 0 i spill-tilstanden med enten en 2-er (90 %) eller 4-er (10 %).
    """
    numbers = []
    for row in grid:
        for element in row:
            numbers.append(element)
    
    if 0 not in numbers:
        return grid

    x = random.randrange(0, 16)
    while numbers[x] != 0:
        x = random.randrange(0, 16)
    
    new = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
    numbers[x] = new[random.randrange(0, 10)]
    
    grid = [[], [], [], []]
    i = 0
    for element in numbers:
        if len(grid[i]) < 4:
            grid[i].append(element)
        else:
            i += 1
            grid[i].append(element)
    return grid

def remove_zeros(grid):
    """
    Fjerner alle 0-er.
    Kun et mellomsteg i forflytningen av tallene.
    """
    for row in grid:
        while 0 in row:
            row.remove(0)
    return grid

def transpose(grid):
    """
    Flipper matrisen, slik at kolonnene blir rader og vice versa.
    """
    grid_column = [[], [], [], []]
    for row in grid:
        for i in range(4):
            grid_column[i].append(row[i])
    return grid_column

def check_lose(grid):
    """
    Sjekker om det fremdeles eksisterer lovlige trekk, ergo om man har tapt.
    """
    new_grid = copy.deepcopy(grid)
    if move_w(new_grid) == move_a(new_grid) == move_s(new_grid) == move_d(new_grid) == grid:
        return True
    return False

def move_left(grid):
    for row in grid:
        if len(row) > 1:
            for i in range(len(row)-1):
                if row[i] == row[i+1]:
                    row[i] *= 2
                    row.pop(i+1)
                    row.append(0)
        while len(row) < 4:
            row.append(0)
    return grid

def move_right(grid):
    for row in grid:
        if len(row) > 1:
            for i in range(len(row)-1, 0, -1):
                if row[i] == row[i-1]:
                    row[i] *= 2
                    row.pop(i-1)
                    row.insert(0, 0)
        while len(row) < 4:
            row.insert(0, 0)
    return grid

def move_w(grid):
    new_grid = copy.deepcopy(grid)
    new_grid = transpose(new_grid)
    new_grid = remove_zeros(new_grid)
    new_grid = move_left(new_grid)
    new_grid = transpose(new_grid)
    if new_grid == grid:
        return grid
    new_grid = new_number(new_grid)
    return new_grid

def move_a(grid):
    new_grid = copy.deepcopy(grid)
    new_grid = remove_zeros(new_grid)
    new_grid = move_left(new_grid)
    if new_grid == grid:
        return grid
    new_grid = new_number(new_grid)
    return new_grid

def move_s(grid):
    new_grid = copy.deepcopy(grid)
    new_grid = transpose(new_grid)
    new_grid = remove_zeros(new_grid)
    new_grid = move_right(new_grid)
    new_grid = transpose(new_grid)
    if new_grid == grid:
        return grid
    new_grid = new_number(new_grid)
    return new_grid

def move_d(grid):
    new_grid = copy.deepcopy(grid)
    new_grid = remove_zeros(new_grid)
    new_grid = move_right(new_grid)
    if new_grid == grid:
        return grid
    new_grid = new_number(new_grid)
    return new_grid

def spill():
    moves = {"w": move_w, "a": move_a, "s": move_s, "d": move_d}
    state = grid()

    looks(state)

    move = input("Use WASD to move\n(W = up, A = left, S = down, D = right, 0 = quit the game)\n> ")
    os.system('clear')
    while move != "0" and check_lose(state) == False:
        if move in moves:
            state = moves[move](state)
            looks(state)
            check_lose(state)
            if check_lose(state) == False:
                move = input("Use WASD to move\n(W = up, A = left, S = down, D = right, 0 = quit the game)\n> ")
                os.system('clear')
        else:
            looks(state)
            print("Invalid input.")
            move = input("Use WASD to move\n(W = up, A = left, S = down, D = right, 0 = quit the game)\n> ")
            os.system('clear')
    
    numbers = []
    for row in state:
        for number in row:
            numbers.append(number)
    print("\nGAME OVER")
    print(f"Score: {sum(numbers)}")

spill()