import random
import heapq
import sys

class Node:
    def __init__(self,x,y,blocked):
        self.x = x
        self.y = y
        self.blocked = blocked
        self.parent = None
        self.g = sys.maxsize
        self.f = sys.maxsize

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.f < other.f
    
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.x == other.x and self.y == other.y
        return False
    
    def __hash__(self):
        return hash((self.x,self.y))
    
    def get_position(self):
        return "["+str(self.x)+", "+str(self.y)+"]"
class World:
    def __init__(self, width, height, block_percentage):
        self.width = width
        self.height = height
        self.block_percentage = block_percentage
        self.nodes = [[Node(x,y,random.random() < block_percentage) 
                       for y in range(height)] for x in range(width)]
    
    def get_node(self,x,y):
        if x < 0 or x >= self.width:
            return None
        if y < 0 or y >= self.height:
            return None
        return self.nodes[x][y]
    
    def get_neighbors(self,node):
        x = node.x
        y = node.y
        neighbors = []
        for dx,dy in [(0,-1),(0,1),(-1,0),(1,0)]:
            neighbor = self.get_node(x+dx,y+dy)
            if neighbor and not neighbor.blocked:
                neighbors.append(neighbor)
        return neighbors
    
def manhattan_distance(node1,node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)
    
def a_star(world, start_node, goal_node):
    start_node.g = 0
    start_node.f = manhattan_distance(start_node,goal_node)
    open_list = [start_node]
    closed_list = set()
    while open_list:
        current = heapq.heappop(open_list)
        if current == goal_node:
            path = []
            while current != start_node:
                path.append([current.x,current.y])
                current = current.parent
            path.append([start_node.x,start_node.y])
            path.reverse()
            return path
        closed_list.add(current)
        for neighbor in world.get_neighbors(current):
            if neighbor in closed_list:
                continue
            test_g = current.g + manhattan_distance(current,neighbor)
            if test_g < neighbor.g:
                neighbor.parent = current
                neighbor.g = test_g
                neighbor.f = neighbor.g + manhattan_distance(neighbor,goal_node)
                if neighbor not in open_list:
                    heapq.heappush(open_list, neighbor)
    return None
    
def print_world(world,start_node=None,goal_node=None,path=None):
    for y in range(world.height):
        for x in range(world.width):
            node = world.nodes[x][y]
            if start_node and node == start_node:
                print("\u001b[33mS\u001b[0m", end=" ")
            elif goal_node and node == goal_node:
                print("\u001b[33mG\u001b[0m", end=" ")
            elif path and node in path:
                print("\u001b[32mO\u001b[0m", end=" ")
            elif node.blocked:
                print("\u001b[31mX\u001b[0m", end=" ")
            else:
                print("·", end=" ")
        print()

# Main
# World (15x15 with 10% )
world = World(15,15,0.1)
while True:
    print_world(world)
    start_node_x = int(input("Enter Starting Node X (0-14): "))
    start_node_y = int(input("Enter Starting Node Y (0-14): "))
    if world.get_node(start_node_x,start_node_y).blocked:
        print("\u001b[0mInvalid Starting Node Position\u001b[0m")
    else:
        start_node = world.get_node(start_node_x,start_node_y)
        break

while True:
    goal_node_x = int(input("Enter Goal Node X (0-14): "))
    goal_node_y = int(input("Enter Goal Node Y (0-14): "))
    if world.get_node(goal_node_x,goal_node_y).blocked:
        print("\u001b[0mInvalid Goal Node Position\u001b[0m")
    else:
        goal_node = world.get_node(goal_node_x,goal_node_y)
        break

print("\n\u001b[33mStart Node:",start_node.get_position()+"\nGoal Node:",goal_node.get_position()+"\u001b[0m")
path = a_star(world,start_node,goal_node)
if path:
    print_world(world,start_node,goal_node,[world.get_node(*path) for path in path])
    print("\u001b[32mPath found!\u001b[0m\n"+str(path))
else:
    print_world(world, start_node, goal_node)
    print("\u001b[31mPath not found!\u001b[0m\n")
