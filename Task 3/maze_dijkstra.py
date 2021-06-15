from typing import List
import numpy as np 
from cv2 import cv2
import time

class Node:
    def __init__(self, _x : int= 0, _y:int= 0):
        self.x = _x
        self.y = _y
        self.distance = float('inf')
        self.prev : Node = None
        self.visited = False

visit = [0, 255, 0]
short_path = [0, 0, 255]

maze = cv2.imread("Blue.png")
h,w,z = maze.shape

start = Node(53,144)
end = Node(420,144)

cv2.namedWindow("Maze",cv2.WINDOW_NORMAL)
cv2.imshow("Maze",maze)

print("Finding Shortest Path from ", (start.x,start.y), "---->", (end.x,end.y))
print("Please Wait........")

cv2.namedWindow("Maze Solution",cv2.WINDOW_NORMAL)
cv2.imshow("Maze Solution",maze)

def is_safeNode(maze,node_mat, x, y):
    global h,w
    return (x < w and x >= 0 and y < h and y >= 0 and node_mat[y][x].visited == False and (maze[(y,x)] != [255,255,255]).all())


def neighbour_node(node_mat, Node) -> List: 
    global maze
    arr = []
    j = Node.x
    i = Node.y
    if(is_safeNode(maze,node_mat, j - 1, i)): #Checking Left
        arr.append((node_mat[i][j-1]))

    if(is_safeNode(maze,node_mat, j + 1, i)): #Checking Right
        arr.append((node_mat[i][j+1]))

    if(is_safeNode(maze,node_mat, j, i-1)): #Checking Top
        arr.append((node_mat[i-1][j]))

    if(is_safeNode(maze,node_mat, j, i+1)): #Checking Bottom
        arr.append((node_mat[i+1][j]))

    return arr

def dijkstra(start, end):
    #global maze
    global h,w
    count =0
    count2 =0
    exit = False
    queue = []      # list of element in the surrounding but not checked yet
    queue.append(start)
    start.distance = 0
    node_mat = np.full((h, w),fill_value= None,dtype=Node)

    for i in range(h):
        for j in range(w):
            node_mat[i][j] = Node(j,i)
    
    while len(queue):
        currentNode = queue[0]
        current_index = 0

        #Checking For the node with Least distance in the to be visited queue
        for obj in (queue):
            
            if obj.distance < currentNode.distance:
                currentNode = obj
                current_index = queue.index(obj)
        
        #exit condition
        if (currentNode.y == end.y and currentNode.x == end.x):
            exit = True
            print("Path Found")
            break

        # Visiting the least distance node
        queue.pop(current_index) 
        count += 1
        currentNode.visited = True
        
        #Checking All the neighbor node of the current node
        for nextNode in neighbour_node(node_mat, currentNode):
            if currentNode.distance + 1 < nextNode.distance:
                node_mat[nextNode.y][nextNode.x].distance = currentNode.distance + 1
                nextNode.distance = currentNode.distance + 1
                queue.append(nextNode)

                node_mat[nextNode.y][nextNode.x].prev = currentNode
                maze[(nextNode.y, nextNode.x)] = visit
               

    pathFound = []
    if exit:
        print(count)
        curr_loc = end
        while (curr_loc.x != start.x or curr_loc.y != start.y):
            curr_loc = node_mat[node_mat[curr_loc.y][curr_loc.x].prev.y][node_mat[curr_loc.y][curr_loc.x].prev.x]
            pathFound.append((curr_loc.x, curr_loc.y))
            maze[curr_loc.y,curr_loc.x] = short_path
            count2 +=1
        print (count2)
    else:
        print("Could not Reach the end......check maze again")
    return pathFound

print("Almost There...")
path = dijkstra(start, end) #saved the pathfound array as path but have not used it anywhere in this case

output_plot = np.zeros((h,w), np.uint8)
for i in range(h):
    for j in range(w):
        if  (maze[i,j] ==  short_path).all():
            output_plot[i,j] = 255
kernel = np.ones((5,5), np.uint8)
cv2.namedWindow("Binary Plot",cv2.WINDOW_NORMAL)
cv2.imshow("Binary Plot",cv2.dilate(output_plot,kernel)) #dilated to make the word more legible
cv2.namedWindow("Maze Solution",cv2.WINDOW_NORMAL)
cv2.imshow("Maze Solution",maze)

k = cv2.waitKey(0)
if k == ord('q'):
    cv2.destroyAllWindows()

#As we can see form the Binary Plot Window the PASSORD is : APPLE
#syntax of all() is not understood well