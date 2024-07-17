from controller import Robot, Compass
import heapq

robot = Robot()

MAX_SPEED = 6.28
WHEEL_RAD = 0.0205
AXLE_LENGTH = 0.052

TIME_STEP = int(robot.getBasicTimeStep())

comp = robot.getDevice('compass')
comp.enable(TIME_STEP)


# Добавляем класс Node для A* алгоритма
class Node:
    def __init__(self, position, g=0, h=0, parent=None):
        self.position = position
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

# Функция эвристики для A*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Реализация A* алгоритма
def astar(start, goal, grid):
    start_node = Node(start)
    goal_node = Node(goal)
    
    open_list = []
    closed_set = set()
    
    heapq.heappush(open_list, (start_node.f, start_node))
    
    while open_list:
        current_node = heapq.heappop(open_list)[1]
        
        if current_node.position == goal:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]
        
        closed_set.add(current_node.position)
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current_node.position[0] + dx, current_node.position[1] + dy)
            
            if neighbor in closed_set or grid[neighbor[0]][neighbor[1]] == 1:
                continue
            
            neighbor_node = Node(neighbor, current_node.g + 1, heuristic(neighbor, goal), current_node)
            
            if neighbor_node not in open_list:
                heapq.heappush(open_list, (neighbor_node.f, neighbor_node))
            else:
                idx = open_list.index(neighbor_node)
                if open_list[idx].g > neighbor_node.g:
                    open_list[idx] = neighbor_node
                    heapq.heapify(open_list)
    
    return None

# Функция для выполнения пути
def execute_path(path):
    for i in range(1, len(path)):
        current = path[i-1]
        next_pos = path[i]
        
        dx = next_pos[0] - current[0]
        dy = next_pos[1] - current[1]
        
        if dx == 1:
            orientizeToTheHeading(HEADINGS.get("EAST"))
        elif dx == -1:
            orientizeToTheHeading(HEADINGS.get("WEST"))
        elif dy == 1:
            orientizeToTheHeading(HEADINGS.get("NORTH"))
        elif dy == -1:
            orientizeToTheHeading(HEADINGS.get("SOUTH"))
        
        move_straight(0.3, 100)  # Предполагаем, что каждый шаг - это 0.3 метра

# Пример использования
grid = [
    [0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 4)

path = astar(start, goal, grid)
if path:
    execute_path(path)
else:
    print("Path not found")

# Оригинальный код движения
orientizeToTheHeading(HEADINGS.get("NORTH"))
move_straight(0.3, 100)
orientizeToTheHeading(HEADINGS.get("WEST"))
move_straight(0.3, 100)
orientizeToTheHeading(HEADINGS.get("EAST"))
move_straight(0.6, 100)
orientizeToTheHeading(HEADINGS.get("SOUTH"))
move_straight(0.3, 100)
orientizeToTheHeading(HEADINGS.get("WEST"))
move_straight(0.3, 100)
orientizeToTheHeading(HEADINGS.get("NORTH"))