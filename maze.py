import sys

class Node(): 
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state ==     state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self): 
        if self.empty():
            raise Exception("Empty frontier")
        else: 
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state ==     state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self): 
        if self.empty():
            raise Exception("Empty frontier")
        else: 
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


""" 
Alternative way to the queueFrontier is by extending the stackFrontier

class QueueFrontier(StackFrontier): 
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        else: 
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
"""

class Maze(): 
    def __init__(self, filename):
        #REads file and sets height and width of the maze
        with open(filename) as f:
            contents = f.read()

        #Validate start and goal
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point")
        
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one end point")

        #Determine height and width of Maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)


        #Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        self.goal = (i, j)
                        row.append(False)
                    else: 
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None
        

        def print(self):
            solution = self.solution[1] if self.solution is not None else None
            print()
            for i, row in enumerate(self.walls):
                for j, col in enumerate(row):
                    if col:
                        print("O", end="")
                    elif(i, j) == self.start:
                        print("A", end="")
                    elif(i, j) == self.goal:
                        print("B", end="")
                    elif solution is not None and (i, j) in solution:
                        print("*", end="")
                    else: 
                        print(" ", end="")
                    print()
                print()


        def neighbors(self, state):
            row, col = state
            
            #All possible actions
            candidates = [
                ("up", (row - 1, col)),
                ("down", (row + 1, col)),
                ("left", (row, col - 1)),
                ("right", (row, col + 1))
            ]


            #Ensure actions are valid
            result = []
            for action, (r, c) in candidates:
                try:
                    if not self.walls[r][c]:
                        result.append((action, (r,c)))
                except IndexError:
                    continue
            return result


            def solve(self):
                ##Finds solution to the maze

                self.numExplored = 0 #Keeps track of number of state explored

                #Initialize frontier to the starting position
                start = Node(state=self.start, parent=None, action=None)
                frontier = StackFrontier()
                frontier.add(start)

                #Initialize an empty explored set
                self.explored = set()

                #Keep looping till solution is found
                while True:

                    #If theres nothing left, then there is no solution
                    if frontier.empty():
                        raise Exception("no solution")
                    
                    #choose node from the frontier
                    node = frontier.remove()
                    self.numExplored += 1

                    #If goal is reached
                    if node.state == self.goal:
                        actions = []
                        cells = []

                    #follow parent node to find solution
                    while node.parent is not None:
                        actions.append(node.action)
                        cells.append(node.state)
                        node = node.parent
                    actions.reverse()
                    cells.reverse()
                    self.solution = (actions, cells)
                    return

                    #Mark node as exploreed
                    self.explored.add(node.state)

                    # Add neighbors to frontier
                    for action, state in self.neighbors(node.state):
                        if not frontier.contains_state(state) and state not in self.explored:
                            child = Node(state=state, parent=node, action=action)
                            frontier.add(child)