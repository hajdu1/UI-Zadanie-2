from copy import deepcopy

MAP_X = 6
MAP_Y = 6


class StartState:
    def __init__(self, color, x, y, size, direction):
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        self.direction = direction


class Car:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y


# class v stave. V globalnom poli array aut s farbou, velkostou a orientaciou
class Node:
    def __init__(self, parent, action, car_array, depth):
        self.parent = parent
        self.action = action
        self.car_array = car_array
        self.depth = depth


start_array = [StartState('red', 2, 1, 2, 'h'), StartState('orange', 0, 0, 2, 'h'), StartState('yellow', 1, 0, 3, 'v'),
               StartState('pink', 4, 0, 2, 'v'), StartState('cyan', 5, 2, 3, 'h'), StartState('grey', 4, 4, 2, 'h'),
               StartState('green', 1, 3, 3, 'v'), StartState('blue', 0, 5, 3, 'v')]


def goes_right(car, car_array):
    new_end = (car.y + start_array[car.index].size - 1) + 1

    if new_end < MAP_Y:
        for obstacle in car_array:
            if start_array[obstacle.index].direction == 'h':
                if new_end == obstacle.y and car.x == obstacle.x:
                    return False
            elif start_array[obstacle.index].direction == 'v':
                for i in range(0, start_array[obstacle.index].size):
                    if new_end == obstacle.y and car.x == obstacle.x + i:
                        return False
        return True
    else:
        return False


def goes_left(car, car_array):
    new_end = car.y - 1

    if new_end >= 0:
        for obstacle in car_array:
            if start_array[obstacle.index].direction == 'h':
                if new_end == (obstacle.y + start_array[obstacle.index].size - 1) and car.x == obstacle.x:
                    return False
            elif start_array[obstacle.index].direction == 'v':
                for i in range(0, start_array[obstacle.index].size):
                    if new_end == obstacle.y and car.x == obstacle.x + i:
                        return False
        return True
    else:
        return False


def goes_down(car, car_array):
    new_end = (car.x + start_array[car.index].size - 1) + 1

    if new_end < MAP_X:
        for obstacle in car_array:
            if start_array[obstacle.index].direction == 'v':
                if new_end == obstacle.x and car.y == obstacle.y:
                    return False
            elif start_array[obstacle.index].direction == 'h':
                for i in range(0, start_array[obstacle.index].size):
                    if new_end == obstacle.x and car.y == obstacle.y + i:
                        return False
        return True
    else:
        return False


def goes_up(car, car_array):
    new_end = car.x - 1

    if new_end >= 0:
        for obstacle in car_array:
            if start_array[obstacle.index].direction == 'v':
                if new_end == (obstacle.x + start_array[obstacle.index].size - 1) and car.y == obstacle.y:
                    return False
            elif start_array[obstacle.index].direction == 'h':
                for i in range(0, start_array[obstacle.index].size):
                    if new_end == obstacle.x and car.y == obstacle.y + i:
                        return False
        return True
    else:
        return False


def print_map(car_array):
    line = ''
    for x in range(0, MAP_X):
        for y in range(0, MAP_Y):
            flag = 0
            for car in car_array:
                if x == car.x and y == car.y:
                    line += start_array[car.index].color[0] + ' '
                    flag = 1
            if flag == 0:
                line += '- '
        print(line)
        line = ''


def print_solution(node):
    if node.parent is None:
        print('root\n\n')
    else:
        print(node.action)
        print_solution(node.parent)


def check(new_array, new_depth):
    for node in visited:
        if node.depth <= new_depth:
            flag = 0
            for i in range(0, len(new_array)):
                if node.car_array[i].x != new_array[i].x or node.car_array[i].y != new_array[i].y:
                    flag = 1
            if flag == 0:
                return False
    return True


def check_parents(node, new_array):
    if node.parent is not None:
        flag = 0
        for i in range(0, len(new_array)):
            if node.car_array[i].x != new_array[i].x or node.car_array[i].y != new_array[i].y:
                flag = 1
        if flag == 0:
            return False
        check_parents(node.parent, new_array)
    return True


def dfs(node):
    if node.car_array[0].y + start_array[0].size == MAP_Y:
        # if node.action == 'red R' or node.action == 'red L':
        print_solution(node)
        return
    if node.depth >= MAX_LEVEL:
        return
    for car in node.car_array:
        if start_array[car.index].direction == 'h':
            if goes_right(car, node.car_array) is True:
                new_array = deepcopy(node.car_array)
                new_array[car.index].y += 1
                # if check_parents(node, new_array) is True:
                if check(new_array, node.depth + 1):
                    new_node = Node(node, start_array[car.index].color + ' R', new_array, node.depth + 1)
                    visited.append(new_node)
                    # print(start_array[car.index].color + '\n')
                    # print_map(new_node.car_array)
                    # print('\n')
                    dfs(new_node)
            if goes_left(car, node.car_array) is True:
                new_array = deepcopy(node.car_array)
                new_array[car.index].y -= 1
                # if check_parents(node, new_array) is True:
                if check(new_array, node.depth + 1):
                    new_node = Node(node, start_array[car.index].color + ' L', new_array, node.depth + 1)
                    visited.append(new_node)
                    # print(start_array[car.index].color + '\n')
                    # print_map(new_node.car_array)
                    # print('\n')
                    dfs(new_node)
        elif start_array[car.index].direction == 'v':
            if goes_down(car, node.car_array) is True:
                new_array = deepcopy(node.car_array)
                new_array[car.index].x += 1
                # if check_parents(node, new_array) is True:
                if check(new_array, node.depth + 1):
                    new_node = Node(node, start_array[car.index].color + ' D', new_array, node.depth + 1)
                    visited.append(new_node)
                    # print(start_array[car.index].color + '\n')
                    # print_map(new_node.car_array)
                    # print('\n')
                    dfs(new_node)
            if goes_up(car, node.car_array) is True:
                new_array = deepcopy(node.car_array)
                new_array[car.index].x -= 1
                # if check_parents(node, new_array) is True:
                if check(new_array, node.depth + 1):
                    new_node = Node(node, start_array[car.index].color + ' U', new_array, node.depth + 1)
                    visited.append(new_node)
                    # print(start_array[car.index].color + '\n')
                    # print_map(new_node.car_array)
                    # print('\n')
                    dfs(new_node)


root_array = []
for index in range(0, len(start_array)):
    root_array.append(Car(index, start_array[index].x, start_array[index].y))

root = Node(None, None, root_array, 0)
visited = [root]
MAX_LEVEL = 16
dfs(root)
