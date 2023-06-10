import pygame
from time import sleep
from math import sin,cos,radians
from numpy import matmul
from random import randint

#              -x-- -y-- -z--
point_set_1 =[(-200,-200,-200),
              (-200,-200, 200),
              (-200, 200,-200),
              (-200, 200, 200),
              ( 200,-200,-200),
              ( 200,-200, 200),
              ( 200, 200,-200),
              ( 200, 200, 200)]

edge_set_1 = [(0, 1), (0, 2), (0, 4),   #0
              (1, 3), (1, 5),           #1
              (2, 3), (2, 6),           #2
              (3, 7),                   #3
              (4, 5), (4, 6),           #4
              (5, 7),                   #5
              (6, 7),                   #6
              (7, 5)]                   #7

def get_cube_edges(points):
    for index1,point1 in enumerate(points):
        for index2,point2 in enumerate(points):
            if point1[0] != point2[0] and point1[1] == point2[1] and point1[2] == point2[2]:
                edges.append((index1,index2))
            elif point1[0] == point2[0] and point1[1] != point2[1] and point1[2] == point2[2]:
                edges.append((index1,index2))
            elif point1[0] == point2[0] and point1[1] == point2[1] and point1[2] != point2[2]:
                edges.append((index1,index2))
    return edges

# These have to be the same or it gets broken
focal_length = 300
z_test = 300

class obj:
    def __init__(self, points, edges):
        if list(points) != points or any([True for point in points if tuple(point) != point or len(point) != 3]):
            raise ValueError("Argument 'points' must be a list of tuples, each with length of 3 for the x, y, and z coordinates.")
        if list(edges) != edges or any([True for edge in edges if tuple(edge) != edge or len(edge) != 2]):
            raise ValueError("Argument 'edges' must be a list of tuples, each with length of 2 for the 2 points it links.")
        self.points = points
        self.edges = edges
    
    def move(self,x,y,z):
        self.points = [( (point[0] + x), (point[1] + y), (point[2] + z) ) for point in self.points]

    def rotate(self,angle,plane):
        angle = radians(angle)
        rot_mat = [[cos(angle),-sin(angle)],
                   [sin(angle),cos(angle)]]
        for index,point in enumerate(self.points):
            x = point[0]
            y = point[1]
            z = point[2]
            match plane:
                case 'xy':
                    xr,yr = matmul([x,y],rot_mat)
                    zr = z
                case 'yz':
                    yr,zr = matmul([y,z],rot_mat)
                    xr = x
                case 'xz':
                    xr,zr = matmul([x,z],rot_mat)
                    yr = y
                case _:
                    raise ValueError("Parameter 'plane' must be 'xy', 'yz', or 'xz'")
            self.points[index] = (xr,yr,zr)

    def project(self,surface,colour,width,height):
        proj_points = [(((focal_length * point[0]) / (focal_length + point[2] + z_test))+(width/2),((focal_length * point[1]) / (focal_length + point[2] + z_test))+(height/2)) for point in self.points]
        for edge in self.edges:
            pygame.draw.line(surface, colour, proj_points[edge[0]], proj_points[edge[1]], 1)

def main():
    pygame.init()
    while True:
        try:
            width = int(input("Please enter the prefered width of the screen: "))
            break
        except:
            print("\nPlease enter a number.\n")
    
    while True:
        try:
            height = int(input("Please enter the prefered height of the screen: "))
            break
        except:
            print("\nPlease enter a number.\n")

    try:
        logo = pygame.image.load("cube_wireframe_icon.png")
    except:
        print('Logo failed to load - no file.')
    pygame.display.set_icon(logo)
    pygame.display.set_caption("wireframe test")
    screen = pygame.display.set_mode((width,height))
    cube1 = obj(point_set_1,edge_set_1)
    while True:
        screen.fill((0,0,0))
        
        plane = 'xz' #('xy','yz','xz')[randint(0,2)]
        
        cube1.project(screen,(255,255,200),width,height)
        
        cube1.rotate(0.1,plane)

        cube1.move(0,0,1)
        
        pygame.display.flip()
        sleep(0)
        if pygame.QUIT in pygame.event.get():
            break

if __name__ == "__main__":
    main()
