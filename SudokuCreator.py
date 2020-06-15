import numpy as np
import pprint
import sys
import numpy.ma as ma
sys.setrecursionlimit(29000)

matrix = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,7,0,2],[0,0,3,0,0,0,6,0,0],
            [0,0,0,5,0,0,0,0,0],[0,0,1,6,0,0,3,0,0],[0,5,6,4,0,0,0,0,0],
            [0,0,0,0,1,0,0,9,0],[0,0,0,0,2,0,0,7,0],[0,0,0,0,3,0,0,0,4]]
try:
    grid = matrix
except:
    grid = np.zeros([9,9], dtype=int)

global matrix_DoF
matrix_DoF = [[9 for _ in range(9)] for _ in range(9)]
global allowed_pos 
allowed_pos = [i for i in range(9)]
global options 
options = [(-1,-2),(-1,2),(-2,1),(-2,-1),(1,2),(1,-2),(2,1),(2,-1)] #x,y possibilities

def print_sudoku(board):
    print("+" + "---+"*9)
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |"*3).format(*[x if x != 0 else " " for x in row]))
        if i % 3 == 2:
            print("+" + "---+"*9)
        else:
            print("+" + "   +"*9)

def normal_sudoku_rules_apply(y,x,n):
    global grid
    if grid[y][x] != 0: return False #there is a number 
    for i in range(9):
        if grid[y][i] == n: #number in the colummn
            return False
    for  i in range(9):
        if grid[i][x] == n: #number in the row
            return False
    x0, y0 = (x//3)*3,(y//3)*3
    for i in range(3):
        for j in range(3):
            if grid[y0+i][x0+j] == n: #number in the box
                return False
    return True

def knights_move_constraint(y,x,n):
    global grid
    global allowed_pos
    global options
    for op in options:
        if x+op[0]  in allowed_pos and y+op[1]  in allowed_pos: #if it doesn't passes the grid dimensions
            if grid[y+op[1]][x+op[0]] == n:
                return False
    return True

def possible(y,x,n):
    normal = normal_sudoku_rules_apply(y,x,n)
    knights = knights_move_constraint(y,x,n)
    if normal and knights: #it is possible by both constraints
        return True
    else: 
        return False

def less_degrees_of_freedom():
    global grid
    global matrix_DoF
    matrix_DoF = [[9 for _ in range(9)] for _ in range(9)]
    grid_numpy = np.matrix(grid)
    for x in range(9):
        for y in range(9):
            x0, y0 = (x//3)*3,(y//3)*3
            box_numbers = []
            row_numbers= []
            columm_numbers = []
            knight_numbers = []
            for i in range(3):
                for j in range(3):
                    if grid_numpy[y0+i, x0+j] !=0 : #number in the box
                        box_numbers.append(grid_numpy[y0+i, x0+j])
            for op in options:
                if x+op[0]  in allowed_pos and y+op[1]  in allowed_pos: #if it doesn't passes the grid dimensions
                    if grid_numpy[y+op[1], x+op[0]] != 0:
                        knight_numbers.append(grid_numpy[y+op[1], x+op[0]])
            if grid_numpy[y, x] != 0 :
                matrix_DoF[y][x] = 0
            else: #there's a empty space
                for i in range(9): row_numbers.append(grid_numpy[y,i])
                for j in range(9): columm_numbers.append(grid_numpy[j,x])
                numbers = np.unique(np.array(row_numbers + columm_numbers + box_numbers))
                numbers = numbers[numbers != 0]
                matrix_DoF[y][x] -= (len(numbers))
    return matrix_DoF

def solve():
    global grid
    matrix_DoF = less_degrees_of_freedom()
    numpy_DoF = np.array(matrix_DoF)
    minvalpos = np.argmin(ma.masked_where(numpy_DoF==0, numpy_DoF))
    minvalposy, minvalposx = minvalpos//9, minvalpos%9
    # Get the indices of minimum element in numpy array 
    #That means the element with lest degrees of freedom
    y, x = minvalposy, minvalposx
    if grid[y][x] == 0: #blanck space
        for n in range(1,10):
            if possible(y,x,n):
                grid[y][x] = n #if the number fits there, we try it!
                solve() #and we try to solve it...
                grid[y][x] = 0 #if we came back here it didn't work....
        return
    print_sudoku(grid)
    input("More solutions?")


print_sudoku(grid)
trying = input("Wanna see the solution? y/n ")
if trying == 'y':
    solve()
else: print("Fuck you, then!")


    