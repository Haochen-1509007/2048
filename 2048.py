# AUTHOR: HAOCHEN GOU



import random as rnd
import os
import sys

class Grid():
    def __init__(self, row=4, col=4, initial=2):
        self.row = row                              # number of rows in grid
        self.col = col                              # number of columns in grid
        self.initial = initial                      # number of initial cells filled
        self.score = 0

        self._grid = self.createGrid(row, col)   # creates the grid specified above

        self.emptiesSet = list(range(row * col))    # list of empty cells

        for _ in range(self.initial):               # assignation to two random cells
            self.assignRandCell(init=True)


    def createGrid(self,row, col):
        #creat grid
        grid = []
        for row_line in range(row):
            grid.append([])
        
        #add 0 into the grid
        for row_line in grid:
            for col_line in range(col):
                row_line.append(0)
        return grid       
   
    
    def setCell(self, cell, val):
        # cell//self.row get the row number and cell%self.col get the col number
        self._grid[cell//self.row][cell%self.col] = val


    def getCell(self, cell):
        # cell//self.row get the row number and cell%self.col get the col number
        return self._grid[cell//self.row][cell%self.col]


    def assignRandCell(self, init=False):

        """
        This function assigns a random empty cell of the grid
        a value of 2 or 4.

        In __init__() it only assigns cells the value of 2.

        The distribution is set so that 75% of the time the random cell is
        assigned a value of 2 and 25% of the time a random cell is assigned
        a value of 4
        """

        if len(self.emptiesSet):
            cell = rnd.sample(self.emptiesSet, 1)[0]
            if init:
                self.setCell(cell, 2)
            else:
                cdf = rnd.random()
                if cdf > 0.75:
                    self.setCell(cell, 4)
                else:
                    self.setCell(cell, 2)
            self.emptiesSet.remove(cell)


    def drawGrid(self):

        """
        This function draws the grid representing the state of the game
        grid
        """

        for row_index in range(self.row):
            line = '\t|'
            for col_index in range(self.col):
                if not self.getCell((row_index * self.col) + col_index):
                    line += ' '.center(5) + '|'
                else:
                    line += str(self.getCell((row_index * self.col) + col_index)).center(5) + '|'
            print(line)
        print()


    def updateEmptiesSet(self):
        self.emptiesSet = []
        for row in range(self.row):
            for col in range(self.col) :
                if self._grid[row][col] == 0:
                    empty_cell = self.row*row + col #get the position of the empty cell
                    self.emptiesSet.append(empty_cell) 


    def collapsible(self):
        #check if  0 in the grid
        for row in self._grid:
            if 0 in row:
                return True
        
        #creat new list for cols
        cols = []
        for row in self._grid:
            cols.append([])  
            
        #append number to each col
        col_num = 0
        for col in cols:
            for row in range(self.row):
                col.append(self._grid[row][col_num])
            col_num += 1        
        
        # creat new_list that have every col and row
        new_list = cols
        for row in self._grid:
            new_list.append(row)
            
        #check if any row or col have same number near others
        for line in new_list:
            for num in line:
                num_position = line.index(num)
                line.remove(num)
                if line.count(num) > 0 and line.index(num) == num_position :
                    return True
                
                
    def collapseRow(self, lst):
        collapsible = False
        new_list = []
        new_list += lst
        former_position = 0
            
        # if possible,remove 0 in lst like merged the empty position
        for time in range(lst.count(0)):
            lst.remove(0)
                      
        # check if any number in lst has other same number can be merged
        for num in lst[former_position:]:
            if lst[former_position:].count(num) > 1:
                first_num_position = lst.index(num,former_position) #get the first number
                second_num_position = lst.index(num,first_num_position+1) #get the same number
                # merge any number in row have same on if near each other
                if second_num_position == first_num_position + 1:
                    collapsible = True
                    lst[first_num_position]= num*2
                    lst[second_num_position] = 0
                    self.score += num*2
            former_position += 1
        #  merge 0 
        for time in range(lst.count(0)):
            lst.remove(0)
        
        #add 0 reach to the former len
        while len(lst) < len(new_list):
            lst.append(0)   
        
        if lst != new_list: # check if the lst collapse
            collapsible  = True
            
        return lst,collapsible


    def collapseLeft(self):
        moved = False
        for row in self._grid:
            newlist,moved = self.collapseRow(row)
        return moved
       
   
    def collapseRight(self):
        moved = False        
        for row in self._grid:
            row.reverse()
            newlist,moved = self.collapseRow(row)
            row.reverse()
        return moved      
        



    def collapseUp(self):
        # creat new list for columns
        new_cols = []
        new_col = []
        moved= False         
        for col in range(self.col):
            for row in range(self.row):
                new_col.append(self._grid[row][col])
            new_cols.append(new_col)
            new_col = []
        #collapse the columns
        for col in new_cols:
            newlist,moved = self.collapseRow(col)
        #change back 
        for col in range(self.col):
            for row in range(self.row):
                self._grid[row][col] = new_cols[col][row]        
        
        return moved      
        
         

    def getScore(self):
        return self.score


    def collapseDown(self):
        # creat new list for columns
        new_cols = []
        new_col = []
        moved = False          
        for col in range(self.col):
            for row in range(self.row):
                new_col.append(self._grid[row][col])
            new_cols.append(new_col)
            new_col = []
        #collapse the columns
        for col in new_cols:
            col.reverse()
            newlist,moved = self.collapseRow(col)
            col.reverse()
        #change back 
        for col in range(self.col):
            for row in range(self.row):
                self._grid[row][col] = new_cols[col][row]
                
        return moved              

class Game():
    def __init__(self, row=4, col=4, initial=2):

        """
        Creates a game grid and begins the game
        """

        self.game = Grid(row, col, initial)
        self.play()


    def printPrompt(self):

        """
        Prints the instructions and the game grid with a move prompt
        """
        print('Press "w", "a", "s", or "d" to move Up, Left, Down or Right respectively.')
        print('Enter "p" to quit.\n')
        self.game.drawGrid()
        print('\nScore: ' + str(self.game.getScore()))


    def play(self):

        moves = {'w' : 'Up',
                 'a' : 'Left',
                 's' : 'Down',
                 'd' : 'Right'}

        stop = False
        collapsible = True

        while not stop and collapsible:
            self.printPrompt()
            key = input('\nEnter a move: ')

            while not key in list(moves.keys()) + ['p']:
                self.printPrompt()
                key = input('\nEnter a move: ')

            if key == 'p':
                stop = True
            else:
                move = getattr(self.game, 'collapse' + moves[key])
                collapsed = move()

                if collapsed:
                    self.game.updateEmptiesSet()
                    self.game.assignRandCell()

                collapsible = self.game.collapsible()

        if not collapsible:
            print()
            self.game.drawGrid()
            print('\nScore: ' + str(self.game.getScore()))
            print('No more legal moves.')


def main():
    game = Game()
main()
