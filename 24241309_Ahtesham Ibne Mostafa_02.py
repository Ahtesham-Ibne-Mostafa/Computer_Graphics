from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random
import time

w_width, w_height = 500, 700
top, bottom = w_height // 2, -w_height // 2
left, right = -w_width // 2, w_width // 2

restart = False
pause = False
over = False

line_width = 2
catcher_speed = 5
diamond_speed = 100
REFRESH_RATE = 60

diamonds = []
score = 0

t0 = time.time()

class Box:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
class Diamond:
    global line_width, delta_time
    def __init__(self):
        self.x = random.randint(left + 10, right - 10)
        self.y = top - 100
        self.color = [random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)]

    def draw(self):
        glPointSize(line_width)
        glBegin(GL_POINTS)
        glColor3f(self.color[0]/255, self.color[1]/255, self.color[2]/255)
        draw_line(self.x, self.y, self.x + 10, self.y - 10)
        draw_line(self.x + 10, self.y - 10, self.x, self.y - 20)
        draw_line(self.x, self.y - 20, self.x - 10, self.y - 10)
        draw_line(self.x - 10, self.y - 10, self.x, self.y)
        glEnd()

    def move(self):
        if not pause:
            self.y -= diamond_speed * delta_time

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0: return 0
        if dx < 0 and dy >= 0: return 3
        if dx < 0 and dy < 0: return 4
        if dx >= 0 and dy < 0: return 7
    else:
        if dx >= 0 and dy >= 0: return 1
        if dx < 0 and dy >= 0: return 2
        if dx < 0 and dy < 0: return 5
        if dx >= 0 and dy < 0: return 6

def convert_zone_to_zero(zone, x, y):
    match zone:
        case 0: return x, y
        case 1: return y, x
        case 2: return y, -x
        case 3: return -x, y
        case 4: return -x, -y
        case 5: return -y, -x
        case 6: return -y, x
        case 7: return x, -y

def convert_zone_from_zero(zone, x, y):
    match zone:
        case 0: return x, y
        case 1: return y, x
        case 2: return -y, x
        case 3: return -x, y
        case 4: return -x, -y
        case 5: return -y, -x
        case 6: return y, -x
        case 7: return x, -y

def draw_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1_0, y1_0 = convert_zone_to_zero(zone, x1, y1)
    x2_0, y2_0 = convert_zone_to_zero(zone, x2, y2)

    dx = x2_0 - x1_0
    dy = y2_0 - y1_0
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)

    x, y = x1_0, y1_0

    while x <= x2_0:
        og_x, og_y = convert_zone_from_zero(zone, x, y)
        glVertex2i(int(og_x), int(og_y))

        if d <= 0:
            d += dE
            x += 1
        else:
            d += dNE
            x += 1
            y += 1

def catcher():
    global line_width

    top_left = catcher_box.x
    top_right = catcher_box.x + catcher_box.width
    bottom_left = catcher_box.x + 25
    bottom_right = catcher_box.x + catcher_box.width - 25

    glColor3f(1, 1, 1)
    if over:
        glColor3f(1, 0, 0)
    glPointSize(line_width)
    glBegin(GL_POINTS)

    draw_line(top_left, catcher_box.y + catcher_box.height, top_right, catcher_box.y + catcher_box.height)
    draw_line(top_left, catcher_box.y + catcher_box.height, bottom_left, catcher_box.y)
    draw_line(top_right, catcher_box.y + catcher_box.height, bottom_right, catcher_box.y)
    draw_line(bottom_left, catcher_box.y, bottom_right, catcher_box.y)

    glEnd()

def collision_detection(catcher, diamond):
    global diamonds, score

    return (catcher.x < diamond.x + diamond.width and
            catcher.x + catcher.width > diamond.x and
            catcher.y < diamond.y + diamond.height and
            catcher.y + catcher.height > diamond.y)

def play_game():
    global over, diamond_speed, score, catcher_speed, catcher_box, t0, delta_time
    
    if not pause:
        current_time = time.time()
        delta_time = current_time - t0
        t0 = time.time()
        
        for diamond in diamonds:
            diamond_box = Box(diamond.x - 10, diamond.y - 20, 20, 20)
            diamond.move()
            caught =  collision_detection(catcher_box, diamond_box)
            if caught:
                diamonds.remove(diamond)
                diamonds.append(Diamond())
                score += 1
                print("Score:", score)
                
                if score % 3 == 0:
                    catcher_speed += 10
                    diamond_speed += 2
                
                if score % 5 == 0:
                    catcher_box.x -= 25
                    catcher_box.width += 25
                
            if diamond.y < bottom:
                diamonds.remove(diamond)
                over = True
                print("Game Over! Score: ", score)
                break
    glutPostRedisplay()

def animate_diamonds(value):
    play_game()
    glutPostRedisplay()
    glutTimerFunc(REFRESH_RATE, animate_diamonds, 0)   

def restart_button():
    global top, bottom, left, right, line_width, restart_box

    glColor3f(65/255, 181/255, 182/255)
    glPointSize(line_width)
    glBegin(GL_POINTS)

    draw_line(restart_box.x, restart_box.y, restart_box.x + restart_box.width, restart_box.y)
    draw_line(restart_box.x, restart_box.y, restart_box.x + restart_box.width//2, restart_box.y + restart_box.height//2)
    draw_line(restart_box.x, restart_box.y, restart_box.x + restart_box.width//2, restart_box.y - restart_box.height//2)

    glEnd()

def restart_game():
    global diamonds, restart, over, score, pause, diamond_speed, catcher_speed, catcher_box
    
    if restart:
        diamonds.clear()
        diamonds.append(Diamond())
        over = False
        pause = False
        restart = False
        catcher_speed = 5
        diamond_speed = 100
        catcher_box.x = -75
        catcher_box.width = 150
        score = 0

def pause_button():
    global top, bottom, left, right, line_width, pause_box

    left_point = pause_box.x - pause_box.width//4
    right_point = pause_box.x + pause_box.width//4

    glColor3f(242/255, 173/255, 12/255)
    glPointSize(line_width)
    glBegin(GL_POINTS)

    draw_line(left_point, pause_box.y, left_point, pause_box.y - pause_box.height)
    draw_line(right_point, pause_box.y, right_point, pause_box.y - pause_box.height)

    glEnd()

def resume_button():
    global top, bottom, left, right, line_width, pause_box
    
    left_point = pause_box.x - pause_box.width//4
    mid_point = pause_box.x + pause_box.width//2

    glColor3f(242/255, 173/255, 12/255)
    glPointSize(line_width)
    glBegin(GL_POINTS)

    draw_line(left_point, pause_box.y, left_point, pause_box.y - pause_box.height)
    draw_line(left_point, pause_box.y, mid_point, pause_box.y - pause_box.height//2)
    draw_line(left_point, pause_box.y - pause_box.height, mid_point, pause_box.y - pause_box.height//2)

    glEnd()

def exit_button():
    global top, bottom, left, right, line_width, exit_box

    glColor3f(242/255, 12/255, 12/255)
    glPointSize(line_width)
    glBegin(GL_POINTS)

    draw_line(exit_box.x, exit_box.y, exit_box.x - exit_box.width, exit_box.y - exit_box.height)
    draw_line(exit_box.x, exit_box.y - exit_box.height, exit_box.x - exit_box.width, exit_box.y)

    glEnd()

def mouse_listener(button, state, x, y):
    global pause, over, restart

    x, y = x - right, top - y

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if restart_box.x <= x <= restart_box.x + restart_box.width and restart_box.y - restart_box.height//2 <= y <= restart_box.y + restart_box.height//2:
            restart = True
            print("Starting Over!")
   
        elif pause_box.x - pause_box.width//2 <= x <= pause_box.x + pause_box.width//2 and pause_box.y - pause_box.height <= y <= pause_box.y:
            pause = not pause
            if pause:
                print("Pausing!")
            else:
                print("Resuming!")
    
        elif exit_box.x - exit_box.width <= x <= exit_box.x and exit_box.y - exit_box.height <= y <= exit_box.y:
            glutLeaveMainLoop()
            print("Goodbye!")
        
    glutPostRedisplay()

def special_key_listener(key, x, y):
    global left, right, catcher_point, catcher_speed, pause
    if not pause and not over:
        if key == GLUT_KEY_LEFT:
            catcher_box.x -= catcher_speed
        elif key == GLUT_KEY_RIGHT:
            catcher_box.x += catcher_speed

        # Clamp catcher within screen borders
        if catcher_box.x < left:
            catcher_box.x = left
        if catcher_box.x + catcher_box.width > right:
            catcher_box.x = right - catcher_box.width

    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    catcher()
    restart_button()
    if not pause:
        pause_button()
    else:
        resume_button()
    exit_button()
    for diamond in diamonds:
        diamond.draw()
    restart_game()
    glutSwapBuffers()

def init():
    global left, right, bottom, top

    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(left, right, bottom, top, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

diamonds.append(Diamond())

restart_box = Box(left + 10, top - 50, 50, 50)
pause_box = Box(0, top - 25, 40, 50)
resume_box = Box(0, top - 25, 40, 50)
exit_box = Box(right - 10, top - 25, 50, 50)
catcher_box = Box(-75, bottom + 10, 150, 20)

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(w_width, w_height)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Catch the Diamonds!")
init()

glutSpecialFunc(special_key_listener)
glutMouseFunc(mouse_listener)
glutDisplayFunc(display)
glutTimerFunc(REFRESH_RATE, animate_diamonds, 0)
glutMainLoop()