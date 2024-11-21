import numpy as np
import random

class BodyNode(): # Initializes a body node of the snake
    def __init__(self, parent, x, y):
        self.parent = parent # Parent node (previous node in the snake body)
        self.x = x           # X coordinate of this node
        self.y = y           # Y coordinate of this node

# Setter for y coordinate
    def setX(self, x):
        self.x = x

# Setter for y coordinate
    def setY(self, y):
        self.y = y

# Setter for parent node
    def setParent(self, parent):
        self.parent = parent

# Getter for the node's position as a tuple (x, y)
    def getPosition(self):
        return (self.x, self.y)

# Getter for the node's position with swapped coordinates for numpy array indexing
    def getIndex(self):
        return (self.y, self.x)


class Snake():
# Initializes the snake with its head at the provided coordinates
    def __init__(self, x, y):
        self.head = BodyNode(None, x, y)
        self.tail = self.head

# Moves all body nodes forward to the position of their parent node
    def moveBodyForwards(self):
        currentNode = self.tail
        while currentNode.parent != None:
            parentPosition = currentNode.parent.getPosition()
            currentNode.setX(parentPosition[0])
            currentNode.setY(parentPosition[1])
            currentNode = currentNode.parent

# Move the snake in a specified direction
    def move(self, direction):
        (oldTailX, oldTailY) = self.tail.getPosition()
        self.moveBodyForwards()
        headPosition = self.head.getPosition()
        if direction == 0:
            self.head.setY(headPosition[1] - 1)
        elif direction == 1:
            self.head.setX(headPosition[0] + 1)
        elif direction == 2:
            self.head.setY(headPosition[1] + 1)
        elif direction == 3:
            self.head.setX(headPosition[0] - 1)
        return (oldTailX, oldTailY, *self.head.getPosition())

# Adds a new head to the snake in the given position
    def newHead(self, newX, newY):
        newHead = BodyNode(None, newX, newY)
        self.head.setParent(newHead)
        self.head = newHead

# Getter for snake's head
    def getHead(self):
        return self.head
    
    def getTail(self):
        return self.tail


class SnakeGame():
# Initializes the snake game with specified board dimensions
    def __init__(self, width, height):
        self.headVal = 2
        self.bodyVal = 1
        self.foodVal = 7
        self.width = width
        self.height = height
        self.board = np.zeros([height, width], dtype=int)

        self.length = 1

        startX = width//2
        startY = height//2

        self.board[startX, startY] = self.headVal
        self.snake = Snake(startX, startY)
        self.spawnFood()
        self.calcState()
#        print(self.board)

# Spawns food at a random empty location on the board
    def spawnFood(self):
        emptyCells = []
        for index, value in np.ndenumerate(self.board):
            if value != self.bodyVal and value != self.headVal:
                emptyCells.append(index)
        self.foodIndex = random.choice(emptyCells)
        self.board[self.foodIndex] = self.foodVal

    def checkValid(self, direction):
        # check if move is blocked by wall
        newX, newY = self.potentialPosition(direction)
        if newX == -1 or newX == self.width:
            return False
        if newY == -1 or newY == self.height:
            return False
        # check if move is blocked by snake body
        if self.board[newY, newX] == self.bodyVal:
            return False
        return True

    def potentialPosition(self, direction):
        (newX, newY) = self.snake.getHead().getPosition()
        if direction == 0:
            newY -= 1
        elif direction == 1:
            newX += 1
        elif direction == 2:
            newY += 1
        elif direction == 3:
            newX -= 1
        return (newX, newY)

    def calcState(self):
        self.state = np.zeros(8, dtype=int)
        for i in range(4):
            self.state[i] = not self.checkValid(i)
        self.state[4:] = self.calcFoodDirection()

    def calcStateNum(self):
        stateNum = 0
        for i in range(8):
            stateNum += 2**i*self.state[i]
        return stateNum

    def calcFoodDirection(self):
        foodDirections = np.zeros(4, dtype=int)
        dist = np.array(self.foodIndex) - np.array(self.snake.getHead().getIndex())
        if dist[0] < 0:
            # down
            foodDirections[0] = 1
        elif dist[0] > 0:
            # up
            foodDirections[2] = 1
        if dist[1] > 0:
            # right
            foodDirections[1] = 1
        elif dist[1] < 0:
            # left
            foodDirections[3] = 1
        return foodDirections

    def plottableBoard(self):
        #returns board formatted for animations
        board = np.zeros([self.width, self.height])
        currentNode = self.snake.tail
        count = 0
        while True:
            count += 1
            board[currentNode.getIndex()] = 0.2 + 0.8*count/self.length
            currentNode = currentNode.parent
            if currentNode == None:
                break
        board[self.foodIndex] = -1
        return board
        
        
    def display(self):
        for i in range(self.width+2):
            print('-', end='')
        for i in range(self.height):
            print('\n|', end='')
            for j in range(self.width):
                if self.board[i, j] == 0:
                    print(' ', end='')
                elif self.board[i, j] == self.headVal:
                    print('O', end='')
                elif self.board[i, j] == self.bodyVal:
                    print('X', end='')
                elif self.board[i, j] == self.foodVal:
                    print('*', end='')
            print('|', end='')
        print()
        for i in range(self.width+2):
            print('-', end='')
        print()
#        print(self.board)

    def makeMove(self, direction):
        gameOver = False
        if self.checkValid(direction):
            # set reward if moving in the right direction
            if self.calcFoodDirection()[direction] == 1:
                reward = 1
            else:
                reward = 0
            (headX, headY) = self.snake.getHead().getPosition()
            # set old head to body val
            self.board[headY, headX] = self.bodyVal

            # check if we got the fruit
            potX, potY = self.potentialPosition(direction)
            if self.board[potY, potX] == self.foodVal:
                # extend the snake
                self.snake.newHead(potX, potY)
                self.board[potY, potX] = self.headVal
                self.spawnFood()
                self.length += 1
                # if you want to give a higher reward for getting the fruit, uncomment below
                reward = 2
            else:
                # move the snake
                (oldTailX, oldTailY, newHeadX, newHeadY) = self.snake.move(direction)
                self.board[oldTailY, oldTailX] = 0
                self.board[newHeadY, newHeadX] = self.headVal
        else:
            reward = -2
            gameOver = True
        self.calcState()
        return (self.calcStateNum(), reward, gameOver, self.length)


if __name__ == "__main__":
    game = SnakeGame(8, 8)
    game.display()
    print("Score: 1")
    while True:
        direction = input("Input Direction (w,a,s,d or q to quit): ")
        if direction == 'w':
            new_state, reward, gameOver, score = game.makeMove(0)
        elif direction == 'a':
            new_state, reward, gameOver, score = game.makeMove(3)
        elif direction == 's':
            new_state, reward, gameOver, score = game.makeMove(2)
        elif direction == 'd':
            new_state, reward, gameOver, score = game.makeMove(1)
        elif direction == 'q':
            break
        if gameOver:
            print("Game Over, Score:", score)
            break
        else:
            game.display()
            print("Reward:", reward, "Score:", score)
