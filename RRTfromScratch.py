import cv2
import numpy as np
import random
import math
class treeNode:
    def __init__(self, x, y):
        self.right = None
        self.left = None
        self.parent = None
        self.x = x
        self.y = y
    def addChild(self, x, y):
        node = treeNode(x, y)
        if self.right == None:
            self.right = node
        else:
            self.left = node
        
        
        node.parent = self

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y ##x and y are the top left point of the obstacle kinda origin
        self.height = height
        self.width = width

def generateObstacle(numberOfObstacles, img):
    global obstacles
    min_width = 10
    max_width = 90
    min_height = 10
    max_height = 90
    obstacles = []
    for i in range(0, numberOfObstacles):
        x = random.randint(200, 600)
        y = random.randint(200, 600)
        width = random.randint(min_width, max_width)
        height = random.randint(min_height, max_height)
        obstacle = Obstacle(x, y, width, height)
        obstacles.append(obstacle)
        cv2.rectangle(img, (y,x), (y+height,x+width) , color=(0,0,0), thickness=-1)
    



def traverseNode(point, node):
    global distance
    global nearestNode
    
    if node is None:
        return
    #For Binary Trees
    '''
    if node.left is not None and node.right is not None:
        traverseNode(point, node.right)
        traverseNode(point, node.left)
    elif node.right is not None :
        current_distance = math.sqrt((node.x - point[0])**2 + (node.y - point[1])**2)
        if current_distance<distance :
            distance = current_distance
            nearestNode = node
        traverseNode(point, node.right)
    elif node.left is not None:

        current_distance = math.sqrt((node.x - point[0])**2 + (node.y - point[1])**2)
        if current_distance<distance :
            distance = current_distance
            nearestNode = node
            
        traverseNode(point, node.left)
    else:
        current_distance = math.sqrt((node.x - point[0])**2 + (node.y - point[1])**2)
        if current_distance<distance :
            distance = current_distance
            nearestNode = node
            hello

    '''
    current_distance = math.sqrt((node.x - point[0]) ** 2 + (node.y - point[1]) ** 2)
    if current_distance < distance:
        distance = current_distance
        nearestNode = node

    traverseNode(point, node.right)
    traverseNode(point, node.left)


def findNearestNode(point, start, goal):
    global distance
    global nearestNode
    distance = 1000
    traverseNode(point, start)

def checkCol(x_sampled, y_sampled):
    global obstacles
    global nearestNode
    nearestNode_x = nearestNode.x
    nearestNode_y = nearestNode.y


    

    for obstacle in obstacles:
        if x_sampled == nearestNode_x :
            slope = 100000
        
        else:
            slope =(y_sampled - nearestNode_y)/(x_sampled - nearestNode_x)
            x_check = (obstacle.x + (obstacle.width/2))
            y_check = nearestNode_y + slope*(x_check - nearestNode_x)


        if ((x_sampled >= obstacle.x and x_sampled<= (obstacle.x + obstacle.width)) and (y_sampled >= obstacle.y and y_sampled<= (obstacle.y + obstacle.height)) ):
            return 1
        elif slope > 10000 :
            return 0
        elif ((x_check >= obstacle.x and x_check<= (obstacle.x + obstacle.width)) and (y_check >= obstacle.y and y_check<= (obstacle.y + obstacle.height)) ):
            return 1
        else :
            return 0
    
    
    
def samplePoint(start, goal, img):
    global nearestNode
    global distance
    max_distance = 30
    x_sampled = random.randint(1, 1000)
    y_sampled = random.randint(1, 1000)
    point = (x_sampled, y_sampled)
    
    findNearestNode(point, start, goal)
    col = checkCol(x_sampled, y_sampled)
    if col == 1:
        distance = 1000
        return
    
    
    if distance> max_distance :
        if x_sampled == nearestNode.x:
            x0 = x_sampled
            if y_sampled >nearestNode.y :
                y0 = nearestNode.y + distance
            else :
                y0 = nearestNode.y - distance
        else:
            slope1 = (y_sampled - nearestNode.y)/(x_sampled - nearestNode.x)
            x0 = nearestNode.x + (max_distance*(math.cos(math.atan(slope1))))
            y0 = (slope1*(x0 - nearestNode.x)) + nearestNode.y
            #change this method
            
    
    elif (math.sqrt((x_sampled-goal[0])**2 + (y_sampled-goal[1])**2)) <= 30 :
        x0 = goal[0]
        y0 = goal[1]
        print(x0, y0)
    else:
        x0 = x_sampled
        y0 = y_sampled
    
    distance = 1000
    
   
    


    nearestNode.addChild(x0, y0)
    cv2.circle(img,(int(y0), int(x0)), 3, (0,0,255), -1)
    cv2.line(img,(int(nearestNode.y), int(nearestNode.x)),(int(y0), int(x0)), (255,0,0), 1)
    




        
if __name__ =="__main__":
    global distance 
    distance = 1000
    img = np.ones((1000, 1000, 3), dtype = np.uint8)
    img = 255*img
    startX = int(100)
    startY = int(100)
    goalX = int(720)
    goalY = int(940)
    total_samples = 5000
    start_pt = [startX, startY]
    goal = [goalX, goalY]
    cv2.circle(img,start_pt, 10, (0,0,255), -1)
    cv2.circle(img,goal, 10, (0,255,0), -1)
    cv2.circle(img,goal, 30, (0,255,0), 2)
    start = treeNode(startX, startY)
    start.addChild(150,170)
    

    cv2.circle(img, (int(start.right.y), int(start.right.x)), 5, (0,0,255), -1)
    cv2.line(img, (int(start.y), int(start.x)), (int(start.right.y), int(start.right.x)), (255,0,0), 1)
    generateObstacle(1, img)
    
    for counter in range(0, total_samples):
        samplePoint(start, goal, img)
        cv2.imshow('image', img)
        cv2.waitKey(1)


    
    cv2.imshow('image', img)
    cv2.waitKey(0)
    
    


  



