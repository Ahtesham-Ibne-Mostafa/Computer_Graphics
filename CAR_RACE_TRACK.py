from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time


class Car:
    global car_y, car_state
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.choice([30, 40, 50, 60])

    def draw_obs(self):
        obstacles(self.x, self.y, self.size)

    def update_car(self):
        global car_state, game_state
        if not game_state["pause"] and not game_state["game_over"]:
            self.y -= car_state["speed"]

def car_func():
    c_x = random.choice([75, 225, 375])
    c_y = 420
    cars.append(Car(c_x, c_y))

def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def pause_button():
    glColor3f(1.0, 1.0, 0.0)
    mpl(210, 450, 210, 490, 2)
    mpl(240, 450, 240, 490, 2)

def play_button():
    glColor3f(1.0, 1.0, 0.0)
    mpl(210, 450, 210, 490, 2)
    mpl(210, 450, 240, 469, 2)
    mpl(210, 491, 240, 471, 2)

def cancel_button():
    glColor3f(1.0, 0.0, 0.0)
    mpl(400, 450, 435, 490, 2)
    mpl(400, 490, 435, 450, 2)

def restart_button():
    glColor3f(0.0, 0.75, 0.8)
    mpl(15, 470, 50, 470, 2)
    mpl(15, 470, 32.5, 490, 2)
    mpl(15, 470, 32.5, 450, 2)

def draw_lane():
    glColor3f(1.0, 1.0, 1.0)

    mpl(lane_x, lane_y, lane_x, lane_y - 50, 10)
    mpl(lane_x + 150, lane_y, lane_x + 150, lane_y - 50, 10)

    mpl(lane_x, lane_y - 125, lane_x, lane_y - 175, 10)
    mpl(lane_x + 150, lane_y - 125, lane_x + 150, lane_y - 175, 10)

    mpl(lane_x, lane_y - 250, lane_x, lane_y - 300, 10)
    mpl(lane_x + 150, lane_y - 250, lane_x + 150, lane_y - 300, 10)

    mpl(lane_x, lane_y - 375, lane_x, lane_y - 425, 10)
    mpl(lane_x + 150, lane_y - 375, lane_x + 150, lane_y - 425, 10)



def draw_circle_points(cx, cy, x, y):

    draw_points(cx + x, cy + y, 5)  # Octant 1
    draw_points(cx - x, cy + y, 5)  # Octant 2
    draw_points(cx + x, cy - y, 5)  # Octant 7
    draw_points(cx - x, cy - y, 5)  # Octant 8
    draw_points(cx + y, cy + x, 5)  # Octant 3
    draw_points(cx - y, cy + x, 5)  # Octant 4
    draw_points(cx + y, cy - x, 5)  # Octant 5
    draw_points(cx - y, cy - x, 5)  # Octant 6



def draw_circle(cx, cy, radius):

    glBegin(GL_POLYGON)
    num_segments = 100 
    for i in range(num_segments):
        theta = 2.0 * math.pi * i / num_segments
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        glVertex2f(cx + x, cy + y)
    glEnd()
    
    
    
def draw_car():
    global car_x, car_y

    # Car body
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_POLYGON)
    glVertex2f(car_x - 50, car_y - 25)
    glVertex2f(car_x + 50, car_y - 25)
    glVertex2f(car_x + 50, car_y + 25)
    glVertex2f(car_x - 50, car_y + 25)
    glEnd()

    # Car roof
    glColor3f(0.8, 0.0, 0.0) 
    glBegin(GL_POLYGON)
    glVertex2f(car_x - 30, car_y + 25)
    glVertex2f(car_x + 30, car_y + 25)
    glVertex2f(car_x + 20, car_y + 50)
    glVertex2f(car_x - 20, car_y + 50)
    glEnd()

    # Rear wheel
    glColor3f(0.0, 0.0, 0.0) 
    draw_circle(car_x - 35, car_y - 30, 15)
    glColor3f(1.0, 1.0, 1.0) 
    draw_circle(car_x - 35, car_y - 30, 10)

    # Front wheel
    glColor3f(0.0, 0.0, 0.0)  
    draw_circle(car_x + 35, car_y - 30, 15)
    glColor3f(1.0, 1.0, 1.0)  
    draw_circle(car_x + 35, car_y - 30, 10)


def random_color():
    return random.random(), random.random(), random.random()


def obstacles(x, y, s):
    color = random_color() 
    is_circle = random.choice([True, False])
    
    glColor3f(*color)
    draw_circle(x, y, s // 2) 


def mpl(x0, y0, x1, y1, s):
    zone = find_zone(x0, y0, x1, y1)
    x0, y0 = convert_zone0(zone, x0, y0)
    x1, y1 = convert_zone0(zone, x1, y1)
    dx = x1 - x0
    dy = y1 - y0
    dne = 2 * dy - 2 * dx
    de = 2 * dy
    dinit = 2 * dy - dx

    while x0 <= x1:
        if dinit >= 0:
            dinit += dne
            x0 += 1
            y0 += 1
        else:
            dinit += de
            x0 += 1
        a, b = convert_zoneM(zone, x0, y0)
        draw_points(a, b, s)

def find_zone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        else:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        else:
            zone = 6
    return zone

def convert_zone0(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

def convert_zoneM(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def KeyListener(key, x, y):
    global car_x, car_y
    if game_state['game_over'] == False and game_state['pause'] == False:
            if key == GLUT_KEY_LEFT:
                if (car_x - 150 >= 0):
                    car_x -= 150
            elif key == GLUT_KEY_RIGHT:
                if (car_x + 150 <= 450):
                    car_x += 150
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global game_state, car_state, car_x, car_y, start_time
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 210 <= x <= 240 and 10 <= y <= 50:
            if game_state["game_over"] == False:
                if game_state["pause"] == False:
                    game_state["pause"] = True
                    if game_state["score"] == 0:
                        print('Paused\n')
                    else:
                        print('\nPaused\n')
                else:
                    game_state["pause"] = False
        elif 15 <= x <= 50 and 10 <= y <= 50:
            if game_state["game_over"] == True:
                game_state["game_over"] = False
            if game_state["score"] == 0:
                print('Starting Over\n')
            else:
                print('\nStarting Over\n')
            cars.clear()
            start_time = time.time()
            game_state["score"] = 0
            car_state["speed"] = .5
            car_x, car_y = 225, 40

        elif 400 <= x <= 435 and 10 <= y <= 50:
            game_state["game_over"] = True
            print('Well Played!', 'Final Score:', game_state["score"])
            glutLeaveMainLoop()
    glutPostRedisplay()

def animate():
    global game_state, car_state, lane_y, vehicles, start_time, score, cars, car_x, car_y, r, g, b
    if game_state["game_over"] == False and game_state['pause'] == False:
        if cars == []:
            car_func()
        else:
            for veh in cars:
                veh.update_car()
        elapsed_time = time.time() - start_time
        if elapsed_time >= 2:
            car_func()
            start_time = time.time()
        lane_y -= car_state["speed"]
        if (lane_y - 375) <= 0:
            lane_y += 125
    glutPostRedisplay()

def play_game():
    global cars, score, game_state, car_state, car_x, car_y, r, g, b
    if game_state["game_over"] == False and game_state["pause"] == False:
        for car in cars:
            if car.y <= 0:
                game_state["score"] += 1
                print(f"Score: {game_state['score']}")
                cars.remove(car)
                if game_state["score"] > 0 and game_state["score"] % 5 == 0:
                    car_state["speed"] += 0.2
                    r = random.uniform(0.0, 1.0)
                    g = random.uniform(0.0, 1.0)
                    b = random.uniform(0.0, 1.0)

                    print("Car Colour Changed. Difficulty increased!")
                break

            if car.x == car_x and (car.y - (car.size / 2)) <= car_y + 30:
                game_state["game_over"] = True
                if game_state["score"] > 0:
                    print("\nCrashed!\nFinal Score:", game_state["score"])
                else:
                    print("Crashed!\nFinal Score:", game_state["score"])
                break

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glClearColor(0.0, 0.0, 0.2, 1.0)  

    iterate()
    animate()
    glColor3f(0.0, 0.0, 0.0)

    if game_state["pause"] == False:
        pause_button()
    else:
        play_button()

    cancel_button()
    restart_button()

    draw_lane()
    draw_car()

    for c in cars:
        c.draw_obs()
    play_game()
    glutSwapBuffers()


car_x = 250
car_y = 250
car_speed = 5

start_time = time.time()
score = 0
r, g, b = 0, 0.3, 0
game_state = {"game_over": False, "pause": False, "score": 0}
car_state = {"speed": 0.5}
lane_x , lane_y = 150, 430
car_x, car_y = 225, 40
cars = []

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(450, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Car Race Track")
glutDisplayFunc(showScreen)
glutSpecialFunc(KeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()
