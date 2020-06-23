import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import pow, radians, sin, cos, pi, sqrt, floor
from random import randint
from time import time, sleep


class World:
    anim_duration = 10
    w = 500
    h = 500
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

class TrajectoryFunc:
    gravity = 10
    v0 = 10
    O = radians(45)

    #Circle Utils Functions
    def get_time():

        numerador = 2 * TrajectoryFunc.v0 * sin(TrajectoryFunc.O)
        denominador = TrajectoryFunc.gravity

        return (numerador / denominador)

    def translation_x(t):

        return TrajectoryFunc.v0 * cos(TrajectoryFunc.O) * t

    def translation_y(t):

        return (TrajectoryFunc.v0 * sin(TrajectoryFunc.O) * t) \
               - (1/2 * TrajectoryFunc.gravity * pow(t, 2))


class Object:

    def __init__(self, x, y, size, color):
        self.x = World.get_size_px(x)
        self.y = World.get_size_px(y)
        self.size = World.get_size_px(size)
        self.color = color

        self.start_time = time()
        self.time = 0
        self.collision_other = None

    def tick(self):
        #caculated time in secs since object creation
        self.time = time() - self.start_time
        self.shading()
        self.draw()
        self.physics()

    def shading(self):
        glColor3f(self.color[0], self.color[1], self.color[2])

    def draw(self):
        pass

    def physics(self):
        pass

class Circle(Object):

    def __init__(self, x, y, size, color):
        Object.__init__(self, x, y, size, color)

        self.tx = 0
        self.ty = 0

    def calculate_translation(self):

        # if collided won't count motions
        if not self.collision_other:

            t = min((self.time / World.anim_duration), 1) * TrajectoryFunc.get_time()
            self.tx = World.get_size_px(TrajectoryFunc.translation_x(t))
            self.ty = World.get_size_px(TrajectoryFunc.translation_y(t))

        else:
            print("Collided!")
            self.tx = 0
            self.ty = 0

    def draw(self):

        self.calculate_translation()

        glBegin(GL_POLYGON)
        for i in range(50):
            theta = (2*pi*i)/50
            glVertex2f(self.x + self.tx + self.size*cos(theta), self.y + self.ty + self.size*sin(theta))
        glEnd()

    def physics(self):

        # no need to check for collisions
        # since we already detected it
        if self.collision_other:
            return

        #Box is the second object in the world
        box = World.objects[1]

        #center taking translation into consideration
        center_x = self.x + self.tx
        center_y = self.y + self.ty

        if center_x < box.x:
            px = box.x
        elif center_x > (box.x + box.size):
            px = box.x + box.size
        else:
            px = center_x

        if center_y < box.y:
            py = box.y
        elif center_y > (box.y + box.size):
            py = box.y + box.size
        else:
            py = center_y

        square_dist = pow(px - center_x, 2) + pow(py - center_y, 2)
        square_dist = sqrt(square_dist)

        #Objects have overlaped
        if square_dist < self.size:

            #freezes position
            self.x = center_x
            self.y = center_y
            box.color = (0,1,0)
            self.collision_other = box



class Box(Object):

    def draw(self):

        glBegin(GL_QUADS)
        glVertex2f(self.x, 0)
        glVertex2f(self.x, self.size)
        glVertex2f(self.x + self.size, self.size)
        glVertex2f(self.x + self.size, 0)
        glEnd()


class Scale(Object):


    def draw(self):

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

class Trajectory(Object):


    def draw(self):

        glBegin(GL_POINTS)

        graduation = TrajectoryFunc.get_time() / self.size

        times = [i * graduation for i in range(self.size)]

        for t in times:
            x = self.x + World.get_size_px(TrajectoryFunc.translation_x(t))
            y = self.y + World.get_size_px(TrajectoryFunc.translation_y(t))
            print("x " + str(x) +" y "+ str(y))
            glVertex2f(x, y)

        glEnd()



class RenderThread:


    def run():

        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(500, 500)
        glutInitWindowPosition(0, 0)
        wind = glutCreateWindow("OpenGL Coding Practice")

        glutDisplayFunc(RenderThread.tick)
        glutIdleFunc(RenderThread.tick)
        glutKeyboardFunc(RenderThread.keyPressed)
        glutSpecialFunc(RenderThread.keyPressed)

        scale = Scale(0, 0, World.get_size_m(10), (1, 1, 1))

        box_size = 10
        box_x = randint(0, World.get_window_size_m()["w"] - box_size)
        box = Box(box_x, 0, box_size, (0, 0, 1))
        circle = Circle(3, 3, 3, (0, 1, 0))

        trajectory = Trajectory(3, 3, 10, (1, 1, 1))

        World.add_object(scale)
        World.add_object(box)
        World.add_object(circle)
        World.add_object(trajectory)

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

    def keyPressed(key, x, y):

        if key == GLUT_KEY_UP:
            World.objects[1].size += 1
        if key == GLUT_KEY_DOWN:
            World.objects[1].size -= 1

        if key == b'r' or key == b'R' :
            print("Yes!!")


if __name__ == '__main__':
    RenderThread.run()


