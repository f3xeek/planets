import pygame
from pygame.locals import *
import ast
import math as m

#constants
G=6.6743e-11
screen_size=1000
timespan_in_seconds=3600


class Symulator:
    def __init__(self,surface:pygame.Surface,scale:int=3_000_000_000, background:tuple[int,int,int]=(0,0,0)) -> None:
        self.elements=[]
        self.background=background
        self.surface=surface
        self.scale=scale

# dictates what happenes each frame during the simulation, calculates position of elements
    def frame(self,screen_size) -> None:
        for element in self.elements:
            posx=element.position[0]/self.scale+screen_size/2
            posy=screen_size-(element.position[1]/self.scale+screen_size/2)
            if 1_000_000_000/self.scale*element.size>=1:
                pygame.draw.circle(self.surface, element.color, [posx,posy], element.size*1_000_000_000/self.scale,0)
            else:
                pygame.draw.circle(self.surface, element.color, [posx,posy], 1,0)

class Planet:
    def __init__(self,name:str, mass:float, velocity:list[int,int], position:list[int,int],color:tuple[int,int,int]=(0,0,255), size:int=3) -> None:
        self.name=name
        self.mass=mass
        self.color=color
        self.size=size
        self.velocity=velocity
        self.acceleration=[0,0]
        self.position=position
# calculates changes in speed and position based on timespan given 
    def change_over_time(self,time_in_seconds:int,elements:list)->None:
        self.position[0]+=self.velocity[0]*time_in_seconds
        self.position[1]+=self.velocity[1]*time_in_seconds
        self.calc_acceleration(elements)
        self.velocity[0]+=self.acceleration[0]*time_in_seconds
        self.velocity[1]+=self.acceleration[1]*time_in_seconds
# calculates acceleration towards other elements based on their mass and distance
    def calc_acceleration(self, elements) ->None:
        self.acceleration=[0,0]
        for element in elements:
            distanceX=element.position[0] -self.position[0]
            distanceY=element.position[1] -self.position[1]
            distance= m.sqrt((distanceX)**2+(distanceY)**2)
            if distance!=0:
                forceX=self.mass*element.mass*G*distanceX/distance**3
                forceY=self.mass*element.mass*G*distanceY/distance**3
                self.acceleration=[self.acceleration[0]+forceX/self.mass,self.acceleration[1]+forceY/self.mass]

    @staticmethod
    def load_from_file(file)-> list:
        output=[]
        with open(file) as file:
            for line in file.readlines():
                name,mass,velocity,position,color,size=line.split()
                output.append(Planet(name,float(mass),ast.literal_eval(velocity),ast.literal_eval(position),ast.literal_eval(color),int(size)))
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
                if symulator.scale >100_000_000 or -event.y==1:
                    symulator.scale+=100_000_000*-event.y
        #simulating, drawing on screen
        screen.fill(symulator.background)
        for element in symulator.elements:
            element.change_over_time(timespan_in_seconds, symulator.elements)
        symulator.frame(screen_size)
        pygame.display.update()

if __name__=="__main__":
    main("data22_03_24.txt")
