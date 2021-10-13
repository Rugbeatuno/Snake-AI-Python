from queue import *
import math

screen_width = 700
screen_height = 700


# cords
scale = 20  # scaling factor ---> 1 node = 20p x 20p
start = [0, 0]  # starting and ending nodes
end = [0, 0]


body_cords = []  # stores coordinates for all walls (x, y)
searching = False
visited_nodes = []  # stores coordinates of visited nodes to prevent backtracking (x, y)
path_cords = 0, 0  # current ending coordinates of path
path_to_food = ""
distance = None


def follow_path(moves):
    x, y = start[0], start[1]  # copies starting position
    for letter in moves:  # runs through current path
        if letter == "L":
            x -= scale
        elif letter == "R":
            x += scale
        elif letter == "U":
            y -= scale
        elif letter == "D":
            y += scale

    return x, y  # returns ending position

def valid(moves):  # moves is passed from BFS() -- path with un-visited edges - moves is passed 4 times with each direction (L, R, U, D) and checks if valid
    global distance
    x, y = follow_path(moves)  # current best path ending point

    for cords in body_cords:  # ensures algorithm doesn't grow 'on' walls
        if x == cords[0] and y == cords[1]:  # compares x, y cords with stored wall cords
            return False

    if not(0 <= x <= screen_width - scale and 0 <= y <= screen_height - scale):  # checks if within screen dimensions
        return False

    if (x, y) in visited_nodes:  # checks if specific cords have been visited already
        return False


    else:
        visited_nodes.append((x, y))  # adds cords to visited
        distance = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        return True

def found_end(moves):
    global path_to_food

    path = follow_path(moves)  # if no keyboard interrupt continues searching algorithm at regular speed

    if path[0] == end[0] and path[1] == end[1]:  # if the algorithm has found the end node
        path_to_food = moves
        #if visited_70():
        reset()
        return True
    return False


def no_end(queue):
    if queue.qsize() == 0:  # checks length of queue
        return True  # if true breaks out of loop -- called in BFS()

def visited_70():
    nodes = (int(screen_width / scale) * int(screen_height / scale)) - len(body_cords)
    percent_visited = float(len(visited_nodes) / nodes)
    print(percent_visited)
    if percent_visited > 0.7:
        return True
    return False


def BFS():
    global visited_nodes, PTF

    queue = Queue()
    visited_nodes = []  # reset() fails to clear previous search ending point
    with queue.mutex:  # clears the queue
        queue.queue.clear()

    queue.put("")
    path = ""  # starts off as empty but builds up moves

    while searching:
        if found_end(path):  # checks if the algorithm has found end node with current best path
            return path_to_food

        path = queue.get()  # gets first element of the queue

        for i in ["L", "R", "U", "D"]:  # cycles through directions
            new = path + i  # adds direction path

            if valid(new):  # checks if valid
                if len(new) < 3:
                    queue.put(new)  # adds to end of queue

                # speeds up run-time
                elif new[-1] == "L" and new[-2] != "R" or new[-1] == "R" and new[-2] != "L" or \
                    new[-1] == "U" and new[-2] != "D" or new[-1] == "D" and new[-2] != "U":
                    queue.put(new)

        if no_end(queue):
            reset()
            return PTF

def reset():
    global visited_nodes, body_cords, searching
    visited_nodes = []
    body_cords = []
    searching = False
    start[0], start[1] = None, None
    end[0], end[1] = None, None

def assign_variables(body, food):
    global searching, distance
    head = len(body) - 1
    start[0], start[1] = body[head].x, body[head].y
    end[0], end[1] = (food)

    for segment in body:
        x = segment.x
        y = segment.y
        body_cords.append((x, y))

    distance = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
    searching = True
    PTF = BFS()
    return PTF



