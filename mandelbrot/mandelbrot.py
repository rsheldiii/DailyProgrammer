import sys, pygame, time, os
import numpy as N
import pygame.surfarray as surfarray

pygame.init()

size = width, height = 1024,768

xlength,xoffset = 3.5, -2.5
ylength,yoffset = 2,-1
LEFT,CENTER,RIGHT = 1,2,3

screen = pygame.display.set_mode(size)


def save_image():
    string = os.path.join(os.getcwd() , "mandelbrot_"+str(width)+"x"+str(height)+"_at_"+str(zoom)+"xZoom_at_offset_"+str(xoffset)+"x"+str(yoffset)+"_time_"+str(time.time())+".png" )
    pygame.image.save(screen,string)
    print("image saved at " + string)

def mandelbrot(width,height,zoom,xoffset,yoffset,max_iterations=100,color = (255,255,255)):
    mandelbrotset = [None]*width
    for x in range(0,width):
        #print x
        mandelbrotset[x] = []
        for y in range(0,height):

            iterations,i,j = 0,0,0
            
            xscaled = (x/width) * xlength/zoom + xoffset
            yscaled = (y/height) * ylength/zoom + yoffset
            
            
            while ( i*i + j*j < 2*2  and  iterations < max_iterations ):
                xtemp = i*i - j*j + xscaled
                j = 2*i*j + yscaled
                i = xtemp
                iterations +=1
                
            weight = iterations / max_iterations
            mandelbrotset[x].append((int(weight*color[0]),int(weight*color[1]),int(weight*color[2])))#i can't even use deepcopy. I have to use append.and append is fucking linear
    return mandelbrotset
        
prevzoom,zoom = 1,1 
    
mandelbrotset = N.array(mandelbrot(width,height,zoom,xoffset,yoffset,50))

lastmandelbrot = mandelbrotset
prevxoffset = xoffset
prevyoffset = yoffset

pressed = True
moved = False

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            mousex, mousey = event.pos
            #print "you moved"
            moved = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                mousex, mousey = event.pos
                pressed = True
                print("You pressed the left mouse button at (%d, %d)" % event.pos)
                prevxoffset,prevyoffset = xoffset,yoffset
                lastmandelbrot = mandelbrotset
                
                xoffset += (mousex/width) * xlength/zoom - xlength/zoom/4
                yoffset += (mousey/height) * ylength/zoom - ylength/zoom/4
                prevzoom = zoom
                zoom *=2
                mandelbrotset = N.array(mandelbrot(width,height,zoom,xoffset,yoffset,50))
                
            elif event.button == CENTER:
                pygame.surfarray.blit_array(screen, mandelbrotset)#to get the 
                pygame.display.flip()
                save_image()
                
            elif event.button == RIGHT:
                pressed = True
                mandelbrotset = lastmandelbrot
                xoffset = prevxoffset
                yoffset = prevyoffset
                if zoom != prevzoom:
                    zoom = prevzoom
                
            
    
            
    if pressed:  #if we changed   
        pygame.surfarray.blit_array(screen, mandelbrotset)
        pygame.display.flip()
        
    if moved:
        pygame.surfarray.blit_array(screen, mandelbrotset)
        
        leftx = mousex - int(width/4)
        rightx = mousex + int(width/4)
        topy = mousey - int(height/4)
        bottomy = mousey + int(height/4)
        
        pygame.draw.line(screen, (255, 0, 0), (leftx, topy), (rightx, topy))
        pygame.draw.line(screen, (255, 0, 0), (leftx, bottomy), (rightx, bottomy))
        pygame.draw.line(screen, (255, 0, 0), (rightx, topy), (rightx, bottomy))
        pygame.draw.line(screen, (255, 0, 0), (leftx, topy), (leftx, bottomy))
        
        pygame.display.flip()
    pressed = False
    moved = False
