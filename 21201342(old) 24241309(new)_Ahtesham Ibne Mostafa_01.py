# TASK 1


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Define screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600

class Raindrops:
    def __init__(self, count):
        self.drops = [[random.uniform(-1, 1), random.uniform(0, 7)] for _ in range(count)]
        self.wind_force = 0.0

    def render(self):
        glColor3f(0.0, 0.0, 1.0)
        glBegin(GL_LINES)
        for x, y in self.drops:
            glVertex2f(x, y)
            glVertex2f(x + self.wind_force * 0.02, y - 0.1)
        glEnd()

    def update(self):
        for drop in self.drops:
            drop[1] -= 0.01
            drop[0] += self.wind_force * 0.001
            if -0.5 <= drop[0] <= 0.5 and -0.2 <= drop[1] <= 0.2 or drop[1] < -1:
                drop[1] = 1
                drop[0] = random.uniform(-1, 1)

    def adjust_wind(self, direction):
        if direction == "left":
            self.wind_force -= 0.08
        elif direction == "right":
            self.wind_force += 0.08
        elif direction == "reset":
            self.wind_force = 0.0

class SceneBackground:
    def __init__(self):
        self.rgb = [0.9, 0.9, 0.9]
        self.change_step = 0.10

    def brighten(self):
        self.rgb = [min(1.0, color + self.change_step) for color in self.rgb]

    def darken(self):
        self.rgb = [max(0.0, color - self.change_step) for color in self.rgb]

    def apply(self):
        glClearColor(*self.rgb, 1.0)

def build_house():
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 1.0, 0.0)
    for vertices in [(-0.4, -0.2), (0.4, -0.2), (-0.4, -0.8), (-0.4, -0.8), (0.4, -0.2), (0.4, -0.8)]:
        glVertex2f(*vertices)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.5, 1.0)
    for vertices in [(-0.5, -0.2), (0.0, 0.2), (0.5, -0.2)]:
        glVertex2f(*vertices)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(0.3, 0.2, 0.1)
    for vertices in [(0.1, -0.8), (0.3, -0.8), (0.1, -0.5), (0.1, -0.5), (0.3, -0.8), (0.3, -0.5)]:
        glVertex2f(*vertices)
    glEnd()

    glPointSize(5)
    glBegin(GL_POINTS)
    glColor3f(0.0, 0.0, 0.0)
    glVertex2f(0.26, -0.65)
    glEnd()

    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0)
    for vertices in [
        (-0.3, -0.3), (-0.1, -0.3), (-0.1, -0.3), (-0.1, -0.5),
        (-0.1, -0.5), (-0.3, -0.5), (-0.3, -0.5), (-0.3, -0.3),
        (-0.3, -0.4), (-0.1, -0.4), (-0.2, -0.3), (-0.2, -0.5)
    ]:
        glVertex2f(*vertices)
    glEnd()

def configure_viewport():
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def render_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    configure_viewport()
    background.apply()
    build_house()
    rain.render()
    glutSwapBuffers()

def handle_keys(key, x, y):
    if key == b'n':
        background.darken()
    elif key == b'm':
        background.brighten()
    elif key == b'r':
        rain.adjust_wind("reset")

def handle_special_keys(key, x, y):
    if key == GLUT_KEY_LEFT:
        rain.adjust_wind("left")
    elif key == GLUT_KEY_RIGHT:
        rain.adjust_wind("right")

def animation_step():
    rain.update()
    glutPostRedisplay()

def timer_update(value):
    animation_step()
    glutTimerFunc(16, timer_update, 0)

# Initialize objects
rain = Raindrops(200)
background = SceneBackground()

# GLUT setup
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Rainy Day Scene")
glClearColor(0.9, 0.9, 0.9, 1.0)
glutDisplayFunc(render_scene)
glutKeyboardFunc(handle_keys)
glutSpecialFunc(handle_special_keys)
glutTimerFunc(16, timer_update, 0)
glutMainLoop()




# TASK 2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import random

# Screen dimensions
SCREEN_W, SCREEN_H = 800, 600
particles = []
bg_color = [0.0, 0.0, 0.0]
paused = False

def initialize():
    glClearColor(*bg_color, 1.0)
    glPointSize(7)

def render_scene():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_POINTS)
    for p in particles:
        if p[7]:  # Check if the point should blink
            color = bg_color if p[8] else (p[4], p[5], p[6])
        else:
            color = (p[4], p[5], p[6])
        glColor3f(*color)
        glVertex2f(p[0], p[1])
    glEnd()
    glutSwapBuffers()

def animate_particles():
    if paused:
        glutTimerFunc(16, animate_particles, 0)
        return
    for p in particles:
        p[0] += p[2]
        p[1] += p[3]
        if p[0] <= -1.0 or p[0] >= 1.0:
            p[2] *= -1  # Bounce horizontally
        if p[1] <= -1.0 or p[1] >= 1.0:
            p[3] *= -1  # Bounce vertically
    glutPostRedisplay()
    glutTimerFunc(16, animate_particles, 0)

def screen_to_gl_coords(x, y):
    gl_x = (x / SCREEN_W) * 2 - 1
    gl_y = -((y / SCREEN_H) * 2 - 1)
    return gl_x, gl_y

def toggle_blinking(count):
    if paused:
        return
    for p in particles:
        if p[7]:
            if count > 0:
                p[8] = not p[8]  # Toggle blinking
            else:
                p[7] = p[8] = False
    glutPostRedisplay()
    if count > 0:
        glutTimerFunc(100, toggle_blinking, count - 1)

def handle_mouse(button, state, x, y):
    if paused:
        return
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        gl_x, gl_y = screen_to_gl_coords(x, y)
        print(f"Right-click at: ({x}, {y})")
        particles.append([gl_x, gl_y, random.choice([-0.01, 0.01]), random.choice([-0.01, 0.01]),
                          random.random(), random.random(), random.random(), False, False])

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        for p in particles:
            p[7] = True
            p[8] = False
        print(f"Left-click at: ({x}, {y}) - Starting blink")
        glutTimerFunc(100, toggle_blinking, 10)

def adjust_viewport(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def handle_special_keys(key, x, y):
    if paused:
        return
    if key == GLUT_KEY_UP:
        for p in particles:
            p[2] *= 1.2
            p[3] *= 1.2
        print("Speed increased")
    elif key == GLUT_KEY_DOWN:
        for p in particles:
            p[2] *= 0.8
            p[3] *= 0.8
        print("Speed decreased")

def handle_keyboard(key, x, y):
    global paused
    if key == b' ':
        paused = not paused
        print("Paused!" if paused else "Resumed!")
        glutPostRedisplay()

# GLUT setup and main loop
glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(SCREEN_W, SCREEN_H)
glutCreateWindow(b"Particle Box")
initialize()
glutDisplayFunc(render_scene)
glutReshapeFunc(adjust_viewport)
glutMouseFunc(handle_mouse)
glutSpecialFunc(handle_special_keys)
glutKeyboardFunc(handle_keyboard)
glutTimerFunc(16, animate_particles, 0)
glutMainLoop()
