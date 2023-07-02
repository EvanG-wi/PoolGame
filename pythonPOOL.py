#pygame

import pygame
from math import (acos,atan,cos,sin,sqrt,pi)
import sys
pygame.init()

WIDTH, HEIGHT = 1600,900
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("pool")



WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (20,100,50)
BROWN = (55,60,20)
FPS = 90

balls = []
class Ball:
    def __init__(self):
        self.angle=(.9999*pi)
        self.x=1200
        self.y=400
        self.velocity=0
        self.radius = 35
        self.color = WHITE
    def frictionInstance(self):
        self.velocity/=1.3 #slow when hit wall
    
 
holes=[]
class Hole:
    def __init__(self, x, y,radius =40):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = BLACK
        holes.append(self)

h1 = Hole(200,100)             #1   2    3
h2 = Hole(800,85,35)           
h3 = Hole(1400,100)            #4   5    6
h4 = Hole(200,800)
h5 = Hole(800,815,35)
h6 = Hole(1400,800)


       
#########Balls 


cue=Ball()
cue.x = 1300
cue.y = 450
balls.append(cue)


eight=Ball()
eight.color=BLACK
eight.x=490
eight.y=450
balls.append(eight)

red=Ball() #front ball
red.x = 610
red.y = 450
red.color = (100,0,0)
balls.append(red)

blue=Ball()
blue.x = 552
blue.y = 500
blue.color=(0,0,100)
balls.append(blue)

green = Ball()
green.x = 552
green.y = 400
green.color=(0,170,0)
balls.append(green)

orange = Ball()
orange.x = 490
orange.y = 540
orange.color = (255,165,0)
balls.append(orange)

pink = Ball()
pink.x = 490
pink.y = 360
pink.color = (255,80,125)
balls.append(pink)

purple = Ball()
purple.x = 420
purple.y = 500
purple.color = (128,0,128)
balls.append(purple)

yellow = Ball()
yellow.x = 420
yellow.y = 410
yellow.color = (255,255,0)
balls.append(yellow)

cyan = Ball()
cyan.x = 420
cyan.y = 590
cyan.color = (0,255,255)
balls.append(cyan)

gray = Ball()
gray.x = 420
gray.y = 320
gray.color = (105,105,105)
balls.append(gray)


def distance(x1,y1,x2,y2): #pythagorrean
    return sqrt( (x2-x1)**2 + (y2-y1)**2)

def totalVelocity(): #sum balls velocity
    totalV = 0
    for ball in balls:
        totalV += ball.velocity
    return str(round(totalV,2))

def friction(ball):
    if ball.velocity > 0: 
        ball.velocity = ball.velocity/1.003-.005 
    if ball.velocity <0:
        ball.velocity = 0
            
        
def draw_balls():
    font = pygame.font.SysFont("comicsans",30)
    vText = font.render(totalVelocity(),1,WHITE)
    
    WIN.blit(vText,(150,150))
    
    for ball in balls:
        pygame.draw.circle(WIN,ball.color,(ball.x,ball.y),ball.radius)
        
        
def draw_holes():
    for hole in holes:
        pygame.draw.circle(WIN,hole.color,(hole.x,hole.y),hole.radius)

def r2d(radians):
    return radians*180/pi

def cleanAngle(ball): #set angle between 0 and 2pi
    ball.angle = ball.angle % (2*pi)
    if ball.angle<0:
        ball.angle= 2*pi-ball.angle
    return ball.angle
    

def ball_collision(b0,deltaX,deltaY):
    cleanAngle(b0)    
    
    collision = False
    for ball in balls:                                      #b0 is hitter, ball is being hit
        if ball is b0: #dont check collision with self
            pass
        elif ball.velocity>b0.velocity: #b0 should be faster
            pass
        #elif b0 is cue:
        else:
            dist = sqrt((ball.x-(b0.x+deltaX))**2 + (ball.y-(b0.y+deltaY))**2)
            if dist < (ball.radius+b0.radius): #collision
                collision =True
                
                cleanAngle(ball)
                
                #ball angle
                quad14 = 1
                angleFlip = -1 #flip angle change
                if b0.x<ball.x: #quadrants 2,3
                    quad14=0
                    angleFlip = 1
                    
                ball.angle = (atan( (b0.y-ball.y) / (b0.x-ball.x )) +quad14*pi)%(2*pi)
                
                #find if ball is "over or under" trajectory
                angleDif = (abs(ball.angle - b0.angle))
                if angleDif>pi:
                    angleDif = 2*pi - angleDif
                    
                
                if (((ball.angle>b0.angle) or (b0.angle-pi>ball.angle)) and not ((ball.angle-pi)>b0.angle)): #if lesser angle, correct for the seam at 0 to 359
                    if quad14:
                        hit = "over"
                    else:
                        hit = "under"
                else:
                    if quad14:
                        hit = "under"
                    else:
                        hit = "over"
                
                if hit =="over":    
                    b0.angle = (ball.angle+pi/2 * angleFlip)
                    
                else: #under
                    b0.angle = (ball.angle-pi/2 * angleFlip)
                    
                    
                    
            #velocity transfer
                transfEnergyPerc = 100 - r2d(angleDif)*1.111 
                
                if transfEnergyPerc > 93:
                    transfEnergyPerc = 93
                elif transfEnergyPerc < 15:
                    transfEnergyPerc = 15
                transfEnergy = b0.velocity*transfEnergyPerc/100 
                 
                b0.velocity -= transfEnergy
                ball.velocity += transfEnergy
                  
                               
    return collision
                
                


def move_balls():
    for ball in balls:
        deltaX = ball.velocity*cos(ball.angle)
        deltaY = ball.velocity*sin(ball.angle)
        #WALLSx = (200,1400)
        #WALLSy = (100,800)
        
        if ball.x+deltaX < (200+ball.radius): #collide left
            if ball.angle>=pi:
                ball.angle=pi-ball.angle
                ball.frictionInstance()
            else:
                ball.angle = 3*pi-ball.angle
                ball.frictionInstance()
                
        elif ball.x+deltaX > (1400-ball.radius): #collide right
            if ball.angle>=0:
                ball.angle=pi-ball.angle
                ball.frictionInstance()
            else:
                ball.angle = 3*pi-ball.angle
                ball.frictionInstance()
        
        elif (ball.y+deltaY > (800-ball.radius)) or (ball.y+deltaY < (100+ball.radius)): #collide top+bottom
            ball.angle = 2*pi - ball.angle
            ball.frictionInstance()
        
        elif ball_collision(ball,deltaX,deltaY): #check if ball hits another ball, if it does dont move it this tick
            pass
            
        else: #move forward if no collision
            ball.x+=deltaX
            ball.y+=deltaY            
               
        friction(ball) #apply friction to the ball
        
def check_holes():
    for hole in holes:
        for ball in balls:
            dist = distance(hole.x,hole.y,ball.x,ball.y)
            if dist < (hole.radius+ball.radius):
                #sink ball
                if ball is cue:
                    ball.x = 1300
                    ball.y = 450
                    ball.velocity = 0
                else:
                    balls.remove(ball)
        
        
def draw_window():
    WIN.fill((84, 8, 14))
    pygame.draw.rect(WIN,BROWN,(150,50,1300,800))    
    pygame.draw.rect(WIN,GREEN,(200,100,1200,700))
    draw_balls()
    draw_holes()

def check_shot(mouseX,mouseY): #returns true if mouse is inside the cue ball
    dist = distance(mouseX,mouseY,cue.x,cue.y)
    if dist < cue.radius:
        return True
    else:
        return False
    
def draw_target_arrow(mouseX,mouseY):
    thickness = round(distance(mouseX,mouseY,cue.x,cue.y)/50)+5
    pygame.draw.line(WIN,BLACK,(mouseX,mouseY),(cue.x,cue.y),thickness)
    
def make_shot(mouseX,mouseY):
    #velocity
    dist = distance(mouseX,mouseY,cue.x,cue.y)
    cue.velocity = dist/10
    #angle
    dX = cue.x - mouseX
    theta = acos(dX/dist)
    if cue.y < mouseY: #quadrant adjust
        theta  = -theta
    cue.angle = theta
    
def main():
    clock = pygame.time.Clock()
    run = True
    mouseHeld = False
    mX=0 ; mY=0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mX,mY = pygame.mouse.get_pos()
                if check_shot(mX,mY):
                    mouseHeld =True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mX,mY = pygame.mouse.get_pos()
                if mouseHeld:
                    mouseHeld = False
                    make_shot(mX,mY)
                    
            if event.type == pygame.QUIT:
                run = False
            
        move_balls()
        check_holes()
        draw_window()
        
        if mouseHeld:
            mX,mY = pygame.mouse.get_pos()
            draw_target_arrow(mX,mY)
            
        pygame.display.update()
        
        
        if len(balls)==1:
            run = False
       
                
    pygame.quit()

if __name__ == "__main__":
    main()
     