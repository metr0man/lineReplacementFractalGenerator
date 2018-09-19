import pygame
import sys
import math
import time

#params
width = 1600
height = 900

#pygame setup
pygame.init()
screen = pygame.display.set_mode([width,height])
font = pygame.font.SysFont("consolas", 20)
bColor = (255,255,255)
screen.fill(bColor)
color = (0,0,0)
lineWidth = 1
delay = 0 # in ms
erase = 1

#testing
#pygame.draw.line(screen,color,(50,25),(500,500),1)
#pygame.draw.line(screen,bColor,(25,25),(500,500),1)

line = []
fLine = []
nLine = []

mode = "n"
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            screen.fill(bColor)
            line = []
            fLine = []
            nLine = []
            mode = "n"

        if mode == "n":#new
            if event.type == pygame.MOUSEBUTTONDOWN:
                fLine.append(pygame.mouse.get_pos())
                pygame.draw.line(screen,color,fLine[0],fLine[0],lineWidth)
                mode = "d"
        elif mode == "d":#draw
            if event.type == pygame.MOUSEBUTTONDOWN:
                fLine.append(pygame.mouse.get_pos())
                pygame.draw.line(screen,color,fLine[-2],fLine[-1],lineWidth)
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                line = list(fLine)
                deltaX = fLine[-1][0]-fLine[0][0]
                deltaY = fLine[-1][1]-fLine[0][1]
                lineLength = math.sqrt((deltaX)**2+(deltaY)**2)
                if deltaY > 0:
                    lineAngle = math.acos((deltaX)/lineLength)*180/math.pi
                else:
                    lineAngle = 360-math.acos((deltaX)/lineLength)*180/math.pi
                angle = []#angle is from x axis, down is positive
                magnitude = []
                #print(lineLength,lineAngle)
                for x in range(len(fLine)-1):
                    deltaX = fLine[x+1][0] - fLine[x][0]
                    deltaY = fLine[x+1][1] - fLine[x][1]
                    segLength = math.sqrt((deltaX)**2+(deltaY)**2)
                    if deltaY > 0:
                        segAngle = math.acos((deltaX)/segLength)*180/math.pi-lineAngle
                    else:
                        segAngle = 360-math.acos((deltaX)/segLength)*180/math.pi-lineAngle
                    if segAngle < 0:
                        segAngle += 360
                    magnitude.append(segLength/lineLength)
                    angle.append(segAngle)
                #print(magnitude,angle)
                mode = "g"
        
        elif mode == "w":#wait
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                mode = "g"
            
            
    if mode == "g":#generate
        time.sleep(delay/1000)
        if len(line) == 1:
            mode = "w"
            nLine.append(line[0])
            line = list(nLine)
            nLine = []
        else:
            if erase == 1:
                pygame.draw.line(screen,bColor,line[0],line[1],lineWidth)
            movingX = line[0][0]
            movingY = line[0][1]
            deltaX = line[1][0] - line[0][0]
            deltaY = line[1][1] - line[0][1]
            constantLength = math.sqrt((deltaX)**2+(deltaY)**2)
            if constantLength == 0:
                del line[0]
            else:
                if deltaY > 0:
                    constantAngle = math.acos((deltaX)/constantLength)*180/math.pi
                else:
                    constantAngle = 360-math.acos((deltaX)/constantLength)*180/math.pi
                #print(constantLength,constantAngle)
                for x in range(len(fLine)-1):
                    nLine.append((round(movingX),round(movingY)))
                    startX = movingX
                    startY = movingY
                    nextLength = magnitude[x]*constantLength
                    nextAngle = constantAngle + angle[x]
                    
                    if nextAngle < 0:
                        nextAngle += 360

                    changeX = nextLength*math.cos(nextAngle/180*math.pi)
                    changeY = nextLength*math.sin(nextAngle/180*math.pi)

                    #print(nextLength,nextAngle,changeX,changeY)

                    movingX += changeX
                    movingY += changeY
                    
                    pygame.draw.line(screen,color,(round(startX),round(startY)),(round(movingX),round(movingY)),lineWidth)
                del line[0]

            
    pygame.display.update()


pygame.quit()
sys.exit()
