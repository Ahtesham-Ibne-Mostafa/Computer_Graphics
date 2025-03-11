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





#Task 2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

w_width, w_height = 800, 600
balls = []
blink = False
frozen = False
speed = 5
size = 5

def add_ball(x, y):
    direction = random.choice([(-1, 1), (-1, -1), (1, 1), (1, -1)])
    color = [random.random(), random.random(), random.random()]
    balls.append({'x': x, 'y': y, 'dx': direction[0], 'dy': direction[1], 'color': color, 'visible': True})

def move_balls():
    global balls, frozen
    if frozen:
        return
    for b in balls:
        b['x'] += b['dx'] * speed
        b['y'] += b['dy'] * speed
        
        if b['x'] <= 0 or b['x'] >= w_width:
            b['dx'] = -b['dx']
        if b['y'] <= 0 or b['y'] >= w_height:
            b['dy'] = -b['dy']

def toggle_visibility():
    global balls, blink
    if blink:
        for b in balls:
            b['visible'] = not b['visible']

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glPointSize(size)
    glBegin(GL_POINTS)
    for b in balls:
        if b['visible']:
            glColor3fv(b['color'])
            glVertex2f(b['x'], b['y'])
    glEnd()
    glutSwapBuffers()

def update(value):
    move_balls()
    toggle_visibility()
    glutPostRedisplay()
    glutTimerFunc(20, update, 0)

def mouse(button, state, x, y):
    global blink
    if frozen:
        return
    if state == GLUT_DOWN:
        if button == GLUT_RIGHT_BUTTON:
            add_ball(x, w_height - y)
            print("New ball added")
        elif button == GLUT_LEFT_BUTTON:
            blink = not blink
            print("Blinking" if blink else "Not Blinking")
    glutPostRedisplay()

def keyboard(key, x, y):
    global speed, frozen, size
    if key == b' ':
        frozen = not frozen
    if frozen:
        return
    if key == b'l':
        size = min(20, size + 1)
        print("Ball Size increased")
    if key == b's':
        size = max(5, size - 1)
        print("Ball Size Decreased")
    glutPostRedisplay()

def special_keys(key, x, y):
    global speed
    if frozen:
        return
    if key == GLUT_KEY_UP:
        speed += 0.5
        print("Speed Increased")
    elif key == GLUT_KEY_DOWN:
        speed = max(0.5, speed - 0.5)
        print("Speed Decreased")

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(w_width, w_height)
glutCreateWindow(b"Bouncing Balls")
glClearColor(0, 0, 0, 1)
glPointSize(5)

glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutMouseFunc(mouse)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_keys)
glutTimerFunc(16, update, 0)
glutMainLoop()
