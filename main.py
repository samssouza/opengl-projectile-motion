import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import pow, radians, sin, cos, pi, sqrt, floor
from random import randint
from time import time, sleep


class World:
    proportion = 10  #1m para 10 pixels
    objects = []

    def add_object(obj):
        World.objects.append(obj)

    #Calcula quantidade de pixel dado tamanho em metros
    def get_size_px(meters):
        return meters * World.proportion

    def get_size_m(px):
        return px / World.proportion

    def get_window_size_m():
        return {"w":World.w / World.proportion, "h": World.h / World.proportion }


class Object:

    def __init__(self, x, y, size):
        self.x = World.get_size_px(x)
        self.y = World.get_size_px(y)
        self.size = World.get_size_px(size)

        self.start_time = time()
        self.time = 0

    def tick(self):
        #caculated time in secs since object creation
        self.time = time() - self.start_time
        self.draw()
        self.physics()

    def draw(self):
        pass

    def physics(self):
        pass

class Circle(Object):

    def __init__(self, x, y, size, angle, velocity):
        Object.__init__(self, x, y, size)
        self.v0 = velocity
        self.O = radians(angle)


    def draw(self):


        tx = World.get_size_px(self.translation_x())
        ty = World.get_size_px(self.translation_y())

        print("tx: " + str(tx) + " ty: " + str(ty))
        glColor3f(0, 1, 0)
        glBegin(GL_POLYGON)
        for i in range(50):
            theta = (2*pi*i)/50
            glVertex2f(self.x + tx + self.size*cos(theta), self.y + ty + self.size*sin(theta))
        glEnd()


    def check_collision(self):

        circle = RenderThread.Circle
        box = RenderThread.Box

        if circle.x < box.x:
            cX = box.x
        elif circle.x > (box.x + box.size):
            cX = box.x + box.size
        else:
            cX = circle.x

        if circle.y < box.y:
            cY = box.y
        elif circle.y > (box.y + box.size):
            cY = box.y + box.size
        else:
            cY = circle.y


        if RenderThread.squared_distance(circle.x, circle.x, cX, cY) < circle.size:
            return True

        return False

    #Circle Utils Functions
    def get_time(self):

        numerador = 2 * self.v0 * sin(self.O)
        denominador = World.gravity

        return (numerador / denominador)


    def squared_distance(x0 , y0, x1, y1):

        distance = pow(x1 - x0, 2) + pow(y1 - y0, 2)
        distance = sqrt(distance)
        return distance


    def translation_x(self):

        t = min((self.time / World.anim_duration), 1) * self.get_time()
        return self.v0 * cos(self.O) * t

    def translation_y(self):
        t = min((self.time / World.anim_duration), 1) * self.get_time()
        return (self.v0 * sin(self.O) * t) - (1/2 * World.gravity * pow(t, 2))



class Box(Object):

    def draw(self):

        glColor3f(1, 0, 0)
        glBegin(GL_QUADS)
        glVertex2f(self.x, 0)
        glVertex2f(self.x, self.size)
        glVertex2f(self.x + self.size, self.size)
        glVertex2f(self.x + self.size, 0)
        glEnd()


class Scale(Object):


    def draw(self):

        glColor3f(1, 1, 1)
        glBegin(GL_LINES)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x, World.h)
        glVertex2f(self.x, self.y)
        glVertex2f(World.w, self.y)

        meters_x = floor(World.get_window_size_m()["w"])
        meters_y = floor(World.get_window_size_m()["h"])

        for i in range(meters_x):
            glVertex2f(World.get_size_px(i), self.y)
            glVertex2f(World.get_size_px(i), self.y + self.size)

        for i in range(meters_y):
            glVertex2f(self.x, World.get_size_px(i))
            glVertex2f(self.x + self.size, World.get_size_px(i))


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


        circle = Circle(1, 1, 1, 45, 2)
        box_size = 4
        box_x = randint(0, World.get_window_size_m()["w"] - box_size)
        box = Box(box_x, 0, box_size)
        scale = Scale(0, 0, World.get_size_m(10))

        World.add_object(circle)
        World.add_object(box)
        World.add_object(scale)

        glutMainLoop()

    def set_view_port():

        glViewport(0, 0, 500, 500)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)

        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def tick():

        RenderThread.set_view_port()

        #Shifts Scale and objects a little so its overlayin view port
        glTranslatef(5, 5, 0);
        for obj in World.objects:
            obj.tick()




        sleep(0.05)
        glutSwapBuffers()




if __name__ == '__main__':
    RenderThread.run()


