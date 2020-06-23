import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import pow, radians, sin, cos, pi
from random import randint
from time import time, sleep
   

class World:
    pass
    
class Object:
    
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
    
        self.start_time = time()        
        self.time = 0
    
    def tick(self):

        #caculated time in secs since object creation
        self.time = time() - self.start_time
        self.push_transforms()
        self.draw()
        self.pop_transforms()

    def push_transforms(self):
        pass

    def pop_transforms(self):
        pass

    def draw(self):
        pass

class Circle(Object):
    
    def __init__(self, x, y, size, angle, velocity):
        Object.__init__(self, x, y, size)
        self.v0 = velocity
        self.O = radians(angle)

    
    def push_transforms(self):    

        glPushMatrix()
        alfa = min((self.time / World.anim_duration), 1) * self.get_time()
        tx = self.translation_x(0 , alfa)
        ty = self.translation_y(0, alfa)
        glTranslatef( tx * 100, ty * 100, 0)
        
    def pop_transforms(self):
        glPopMatrix()

    def draw(self):    
 
        glColor3f(0, 1, 0)
        glBegin(GL_POLYGON)
        for i in range(50):
            theta = (2*pi*i)/50
            glVertex2f(self.x + self.size*cos(theta), self.y + self.size*sin(theta))
        glEnd()
        
     
    def get_time(self):
        
        numerador = 2 * self.v0 * sin(self.O)
        denominador = World.gravity
        
        return (numerador / denominador)


    def translation_x(self, x0, t):
       
       return x0 + (self.v0 * cos(self.O) * t)

    def translation_y(self, y0, t):
        return (y0 + (self.v0 * sin(self.O) * t)) - (1/2 * World.gravity * pow(t, 2))

    def lerp(x0, x1, alfa):            
        delta =  (x1 - x0) * alfa
        return x0 + delta


class Box(Object):
    
    def draw(self):
        
        glColor3f(1, 0, 0)
        glBegin(GL_QUADS) 
        glVertex2f(self.x, 0) 
        glVertex2f(self.x, self.size) 
        glVertex2f(self.x + self.size, self.size) 
        glVertex2f(self.x + self.size, 0) 
        glEnd()

    


class RenderThread:
    
    World.gravity = 10
    World.anim_duration = 10
    World.w = 500
    World.h = 500
   

    def run():

        glutInit()
        glutInitDisplayMode(GLUT_RGBA)  
        glutInitWindowSize(500, 500)    
        glutInitWindowPosition(0, 0)  
        wind = glutCreateWindow("OpenGL Coding Practice") 
        glutDisplayFunc(RenderThread.tick)
        glutIdleFunc(RenderThread.tick) 
        
        RenderThread.Circle = Circle(25, 25, 25, 45, 2)
        
        box_size = 25
        box_x = randint(0, World.w - box_size)
        RenderThread.Box = Box(box_x, 0, box_size)
        
        glutMainLoop()  
    
        
    def tick():
        
        RenderThread.set_view_port()    
        RenderThread.Circle.tick()
        RenderThread.Box.tick()
        
        
        sleep(0.05)
        glutSwapBuffers()

    def set_view_port():
    
        glViewport(0, 0, 500, 500)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
        
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()
          
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      




if __name__ == '__main__':
    RenderThread.run()


