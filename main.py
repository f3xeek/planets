import pygame
from pygame.locals import *
import ast
import numpy as np

#constants
G=6.6743e-11
screen_size=1000
timespan_in_seconds=3600
initial_scale=1_000_000_000

class Symulator:
    def __init__(self,surface:pygame.Surface,scale:int=initial_scale, background:tuple[int,int,int]=(0,0,0)) -> None:
        self.elements=[]
        self.background=background
        self.surface=surface
        self.scale=scale

# dictates what happenes each frame during the simulation, calculates position of elements
    def frame(self,screen_size) -> None:
        for element in self.elements:
            pos=element.position/self.scale+screen_size/2
            if initial_scale/self.scale*element.size>=1:
                pygame.draw.circle(self.surface, element.color, [pos[0],screen_size-pos[1]], element.size*initial_scale/self.scale,0)
            else:
                pygame.draw.circle(self.surface, element.color, [pos[0],screen_size-pos[1]], 1,0)

class Planet:
    def __init__(self,name:str, mass:float, velocity:np.array, position:np.array,color:tuple[int,int,int]=(0,0,255), size:int=3) -> None:
        self.name=name
        self.mass=mass
        self.color=color
        self.size=size
        self.velocity=velocity
        self.position=position
# calculates changes in speed and position based on timespan given 
    def change_over_time(self,time_in_seconds:int,elements:list)->None:
        self.position+=self.velocity*time_in_seconds
        self.accelerate(elements, time_in_seconds)
        
# calculates acceleration towards other elements based on their mass and distance
    def accelerate(self, elements, time) ->None:
        self.acceleration=np.array([0.0,0.0])
        for element in elements:
            distance_vector=element.position-self.position
            distance = np.linalg.norm(distance_vector)
            if distance!=0:
                force=self.mass*element.mass*G*distance_vector/distance**3
                self.acceleration+=force/self.mass
        self.velocity+=self.acceleration*time

    @staticmethod
    def load_from_file(file)-> list:
        output=[]
        with open(file) as file:
            for line in file.readlines():
                name,mass,velocity,position,color,size=line.split()
                output.append(Planet(name,float(mass),np.array(ast.literal_eval(velocity)),np.array(ast.literal_eval(position)),ast.literal_eval(color),int(size)))
        return output
    
def main(file) ->None:
    #Initial start up
    pygame.init()
    screen = pygame.display.set_mode((screen_size, screen_size))
    symulator=Symulator(screen)
    symulator.elements=Planet.load_from_file(file)
    #pygame's window utility, scrolling and keypress
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_r:
                    symulator.elements=Planet.load_from_file(file)
            if event.type == pygame.MOUSEWHEEL:
                if symulator.scale >initial_scale/10 or -event.y==1:
                    symulator.scale+=initial_scale/10*-event.y
        #simulating, drawing on screen
        screen.fill(symulator.background)
        for element in symulator.elements:     
            element.change_over_time(timespan_in_seconds, symulator.elements)
        symulator.frame(screen_size)
        pygame.display.update()

if __name__=="__main__":
    main("data22_03_24.txt")
