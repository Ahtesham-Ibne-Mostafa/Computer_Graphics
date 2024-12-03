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