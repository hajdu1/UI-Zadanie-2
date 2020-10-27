# na rekurzivne kompletne prekopirovanie stavu mriezky, aby sa nevkladali do kopie iba referenice
from copy import deepcopy

# pouzite na tvorbu zasobnika, kedze append() a pop() su takto rychlejsie ako pri zozname
from collections import deque

# na zistenie existencie suboru podla nazvu (cesty)
import os.path


# trieda pre pociatocny stav auta
# uklada sa iba jeden objekt, z ktoreho si objekty aut zistuju svoju farbu, orientaciu v mriezke a velkost
# predchadza sa tak zbytocnemu ukladaniu mnozstva nemennych dat do kazdeho noveho objektu auta
class StartState:
    def __init__(self, color, x, y, size, direction):
        self.color = color
        self.x = x
        self.y = y
        self.size = size
        self.direction = direction


# trieda auta obsahujuca poradove cislo auta a jeho suradnice v mriezke
class Car:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y


# trieda pre uzol obsahujuci odkaz na rodica, informaciu o poslednom tahu autom, stav aut a hlbku v strome
class Node:
    def __init__(self, parent, action, car_array, depth):
        self.parent = parent
        self.action = action
        self.car_array = car_array
        self.depth = depth


# funkcia na hashovanie poloh aut na mape, tento hashovany vystup sa pridava do zoznamov navstivenych uzlov podla hlbok
def hash_cars(car_array):
    hashed = []
    for car in car_array:
        if start_array[car.index].direction == 'h':
            hashed.append(car.y)    # pri horizontalnych autach je hodnotou vzdialenost od laveho okraja
        else:
            hashed.append(car.x)    # pri vertikalnych autach je hodnotou vzdialenost od horneho okraja
    return tuple(hashed)


# overenie, ci je mozne autom pohnut doprava
def goes_right(car, car_array):
    new_end = (car.y + start_array[car.index].size - 1) + 1
    # kontroluje hranice mapy a kolizie s ostatnymi autami
    if new_end < columns:
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


# overenie, ci je mozne autom pohnut dolava
def goes_left(car, car_array):
    new_end = car.y - 1
    # kontroluje hranice mapy a kolizie s ostatnymi autami
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


# overenie, ci je mozne autom pohnut dole
def goes_down(car, car_array):
    new_end = (car.x + start_array[car.index].size - 1) + 1
    # kontroluje hranice mapy a kolizie s ostatnymi autami
    if new_end < rows:
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


# overenie, ci je mozne autom pohnut hore
def goes_up(car, car_array):
    new_end = car.x - 1
    # kontroluje hranice mapy a kolizie s ostatnymi autami
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


# funkcia vypise cestu od pociatocneho uzla k uzlu zadanom v parametri, pouziva sa pri vypise riesenia
def print_path(node, path):
    if node.parent is None:
        print('----------\nFound solution (' + str(len(path)) + ' steps)\n----------')
        for move in path:
            print(move)
        print('----------\nRed car in final destination\n----------')
    else:
        path.insert(0, node.action)
        print_path(node.parent, path)


# rozhodne, ci je novy stav uplne novy (unikatny), pripadne je rovnaky ako niektory existujuci, ale v mensej hlbke
def check(new_array, new_depth):
    for depth in range(0, new_depth + 1):
        if new_array in visited[depth]:
            # ak sme nasli v rovnakej alebo mensej hlbke rovnake rozlozenie aut, stav nema zmysel vytvarat
            return False
    # novy stav je bud unikany, alebo sa dostal do uz znameho rozlozenia aut lacnejsie (mensou hlbkou)
    # takyto stav sa vytvori
    return True


# funkcia vracia novy uzol ak je jeho stav aut unikatny alebo je mensia hlbka ako pri rovnakom existujucom stave
def create_node(node, car, step):
    new_array = deepcopy(node.car_array)    # nove rozlozenie aut

    if step == 'R':                         # zmena polohy auta v zavislosti od smeru tahu
        new_array[car.index].y += 1
    elif step == 'L':
        new_array[car.index].y -= 1
    elif step == 'D':
        new_array[car.index].x += 1
    elif step == 'U':
        new_array[car.index].x -= 1

    if node.depth + 1 >= len(visited):      # ak este neexistuje navstiveny vrchol v tejto hlbke, alokuje sa pamat
        visited.append(set())
    if check(hash_cars(new_array), node.depth + 1):
        # ak je novy stav vyhovujuci, vytvori sa a je vrateny
        return Node(node, start_array[car.index].color + ', ' + step, new_array, node.depth + 1)
    return None


# depth limited search - DFS s nastavenym limitom hlbky
def dls(limit):
    global stack
    while len(stack) > 0:
        node = stack.pop()                                      # vyberie uzol na spracovanie/prehladanie

        if node.depth < limit:
            for car in node.car_array:                          # skusa pohnut kazdym autom
                if start_array[car.index].direction == 'h':     # pre horizontalne auta skusa pohyb dolava a doprava

                    # pohyb vpravo
                    if goes_right(car, node.car_array):
                        new_node = create_node(node, car, 'R')
                        if new_node is not None:
                            if new_node.car_array[0].y + start_array[0].size == columns:
                                return new_node     # nasiel sa cielovy stav
                            # rozlozenie aut sa uklada do zoznamu navstivenych stavov na porovnavanie
                            visited[new_node.depth].add(hash_cars(new_node.car_array))
                            stack.append(new_node)  # pridava sa do zasobnika na spracovanie/prehladanie

                    # pohyb vlavo
                    if goes_left(car, node.car_array):
                        new_node = create_node(node, car, 'L')
                        if new_node is not None:
                            if new_node.car_array[0].y + start_array[0].size == columns:
                                return new_node     # nasiel sa cielovy stav
                            # rozlozenie aut sa uklada do zoznamu navstivenych stavov na porovnavanie
                            visited[new_node.depth].add(hash_cars(new_node.car_array))
                            stack.append(new_node)  # pridava sa do zasobnika na spracovanie/prehladanie

                elif start_array[car.index].direction == 'v':   # pre vertikalne auta skusa pohyb dole a hore

                    # pohyb dole
                    if goes_down(car, node.car_array):
                        new_node = create_node(node, car, 'D')
                        if new_node is not None:
                            if new_node.car_array[0].y + start_array[0].size == columns:
                                return new_node     # nasiel sa cielovy stav
                            # rozlozenie aut sa uklada do zoznamu navstivenych stavov na porovnavanie
                            visited[new_node.depth].add(hash_cars(new_node.car_array))
                            stack.append(new_node)  # pridava sa do zasobnika na spracovanie/prehladanie

                    # pohyb hore
                    if goes_up(car, node.car_array):
                        new_node = create_node(node, car, 'U')
                        if new_node is not None:
                            if new_node.car_array[0].y + start_array[0].size == columns:
                                return new_node     # nasiel sa cielovy stav
                            # rozlozenie aut sa uklada do zoznamu navstivenych stavov na porovnavanie
                            visited[new_node.depth].add(hash_cars(new_node.car_array))
                            stack.append(new_node)  # pridava sa do zasobnika na spracovanie/prehladanie

    return None     # nenaslo sa riesenie


# cyklicky spusta dfs s postupne vyssou hodnotou limitu kym nenajde riesenie alebo nedosiahne pouzivatelom zadany limit
def iddfs(max_limit):
    global visited
    for limit in range(0, max_limit + 1):   # cyklus sa opakuje s limitom vzdy o 1 vacsim ako v predoslom behu
        stack.clear()
        stack.append(root)
        visited.clear()
        visited = [{hash_cars(root.car_array)}]
        solution = dls(limit)               # zavolanie dfs s limitom pre hlbku, ak najde riesenie, vrati cielovy uzol
        if solution is not None:
            print_path(solution, [])
            break
        # ciel nebol najdeny do stanoveneho maximalneho limitu:
        if limit == max_limit:
            print('----------\nTarget unreachable within maximum limit\n----------')


# funkcia nacita z externeho suboru vstupny stav krizovatky
def load_data(file):
    global rows
    global columns
    input_file = open('inputs\\' + file + '.txt', 'r')
    line = input_file.readline()
    rows = int(line.split()[0])
    columns = int(line.split()[1])
    num = 0
    line = input_file.readline()
    while line:
        data = line.split()
        start_array.append(StartState(data[0], int(data[1]), int(data[2]), int(data[3]), data[4]))
        root_array.append(Car(num, int(data[1]), int(data[2])))
        num += 1
        line = input_file.readline()
    input_file.close()


# menu pre pracu s aplikaciou
while 1:
    print('Nacitat subor: 1\nUkoncit program: 0')
    answer = input()

    if answer == '1':

        print('Zadajte meno suboru s krizovatkou')
        answer = input()

        if os.path.isfile('inputs\\' + answer + '.txt'):

            rows = 0                                   # reset struktur
            columns = 0
            start_array = []
            root_array = []
            stack = deque()
            visited = []

            load_data(answer)                           # nacita zo suboru pociatocny stav
            root = Node(None, None, root_array, 0)      # vytvori prvy uzol s povodnym stavom mapy

            print('Zadajte maximalnu hlbku na hladanie riesenia')
            iddfs(int(input()))                         # spusti sa prehladavanie
        else:
            print('Zadany subor sa nenasiel\n')
            continue

    elif answer == '0':
        exit()
