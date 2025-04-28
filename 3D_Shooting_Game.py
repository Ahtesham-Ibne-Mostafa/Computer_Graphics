from OpenGL.GL import *
from OpenGL.GLUT import *  # Import all GLUT functions
from OpenGL.GLU import *
from math import *
from OpenGL.GLUT import *  # Import all GLUT functions
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18  # Explicitly import GLUT_BITMAP_HELVETICA_18
import random

# ========================
# Camera and View Settings
# ========================
last_camera_coords = None  # Stores the last known camera position
camera_pos = (0, 500, 500)  # Initial camera location (above and behind the player)
first_person_mode = False  # True if first-person view is active
cheat_mode = False         # True if cheats (like unlimited lives) are enabled
gun_follow_mode = False    # True if the gun moves along with the camera

fovY = 120                 # Vertical field of view (in degrees)
GRID_LENGTH = 600          # Size of the grid area
rand_var = 423             # Random variable (placeholder or seed)

# ========================
# Game State and Progress
# ========================
game_over = False          # True when the game ends
life_remaining = 5         # Number of lives left
score = 0                  # Current player score
bullets_missed = 0         # Bullets that did not hit any targets

# ========================
# Player Settings
# ========================
player_pos = (0, 0, 0)     # Player’s position in 3D space
player_angle = 0           # Direction the player is facing
player_fall_angle = 0      # Fall angle when the player collapses
player_rotate_speed = 10   # Rotation speed (degrees per input)
player_speed = 30          # Movement speed
gun_barrel_length = 80     # Visual length of the gun barrel

# ========================
# Bullet Settings
# ========================
bullet_speed = 10          # Bullet movement speed
bullet_height = 100        # Height from which bullets are fired
bullet_pos = player_pos    # Initial bullet position (same as player)
bullet_angle = player_angle  # Initial bullet direction
bullets = []               # List to hold bullets with their properties

# ========================
# Enemy Settings
# ========================
enemies = []               # List to hold enemy positions
enemy_radius = 50          # Collision detection radius for enemies
enemy_speed = 0.15         # Enemy movement speed toward the player

# ========================
# Time and Animation
# ========================
time_elapsed = 0           # Timer to track game duration or effects (like pulsing)


def create_enemy():
    """
    Generate a single enemy at a random spot within the play grid.
    """
    x = random.randint(-GRID_LENGTH + 50, GRID_LENGTH - 50)
    y = random.randint(-GRID_LENGTH + 50, GRID_LENGTH - 50)
    z = 50  # Constant height for all enemies
    enemies.append({'pos': (x, y, z)})

def setup_initial_enemies():
    """
    Populate the game world with 5 enemies if fewer exist.
    """
    global enemies
    existing_enemies = len(enemies)
    for _ in range(5-existing_enemies):
        create_enemy()

def render_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    """
    Render a given text string at the specified screen coordinates.
    """
    glColor3f(1, 1, 1)  # White text color
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    gluOrtho2D(0, 1000, 0, 800)  # Set up a 2D orthographic projection

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(font, ord(character))
    
    # Revert to the previous projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def render_scene():
    """
    Draw all game elements: player, enemies, and bullets.
    """
    draw_player()
    render_enemies()
    render_bullets()

def draw_player():
    """
    Render the player's character with associated parts and animations.
    """
    global player_pos, player_fall_angle, game_over, player_angle

    glPushMatrix()

    x, y, z = player_pos
    glTranslatef(x, y, z)
    glRotatef(180, 0, 0, 1)
    glRotatef(player_angle, 0, 0, 1)

    if game_over:
        glRotatef(player_fall_angle, 0, 1, 0)

    # Draw body
    glColor3f(0, 0.4, 0)  # Dark green
    glTranslatef(0, 0, 100)
    glScalef(0.5, 1, 2)
    glutSolidCube(50)
    glScalef(2, 1, 0.5)
    glTranslatef(0, 0, -100)

    # Draw legs
    glColor3f(0, 0, 1)  # Blue
    for offset in [10, -10]:
        glPushMatrix()
        glTranslatef(0, offset, 50)
        glRotatef(180, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)
        glPopMatrix()

    # Draw head
    glColor3f(0, 0, 0)  # Black
    glTranslatef(0, 0, 165)
    gluSphere(gluNewQuadric(), 15, 10, 10)
    glTranslatef(0, 0, -165)

    # Draw arms
    glColor3f(1, 0.8, 0.6)  # Light peach (skin tone)
    for offset in [30, -30]:
        glPushMatrix()
        glTranslatef(0, offset, 125)
        glRotatef(-90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)
        glPopMatrix()

    # Draw gun
    glColor3f(0.5, 0.5, 0.5)  # Gray color
    glPushMatrix()
    glTranslatef(0, 0, 125)
    glRotatef(-90, 0, 1, 0)
    glScalef(1, 1, 2)
    gluCylinder(gluNewQuadric(), 10, 3, 40, 10, 10)
    glPopMatrix()

    glPopMatrix()


def render_enemies():
    """
    Draw all enemies with pulsing effect and details like eyes or other features.
    """
    global enemies, time_elapsed, enemy_radius

    # Apply a pulsing effect with oscillation between 0.8 and 1.2 scale
    pulse_scale = 1 + 0.2 * sin(time_elapsed)

    for enemy in enemies:
        glPushMatrix()

        x, y, z = enemy['pos']  # Get the enemy's position
        glTranslatef(x, y, z)  # Move to the enemy's location
        glScalef(pulse_scale, pulse_scale, pulse_scale)  # Scale the enemy for the pulsing effect
        glColor3f(1, 0, 0)  # Set enemy color to red
        glutSolidSphere(enemy_radius, 10, 10)  # Draw enemy body

        glColor3f(0, 0, 0)  # Set detail color to black (e.g., eyes or inner features)
        glTranslatef(0, 0, 75)  # Move up to draw the enemy's detail
        glutSolidSphere(enemy_radius // 2, 10, 10)  # Draw a smaller sphere for detail (eyes, etc.)
        glTranslatef(0, 0, -75)  # Reset to the original position
        
        glPopMatrix()

def render_bullets():
    """
    Draw each bullet in the game, based on their current position and direction.
    """
    global bullets

    # Iterate over the list of bullets
    for bullet in bullets:
        glPushMatrix()

        # Set bullet's position and orientation
        glTranslatef(bullet['pos'][0], bullet['pos'][1], bullet['pos'][2])
        glRotatef(bullet['angle'], 0, 0, 1)  # Align the bullet with its travel direction
        
        glColor3f(1, 0, 0)  # Color the bullet red
        glutSolidCube(10)  # Render the bullet as a solid cube of size 10
        
        glPopMatrix()


def check_line_of_sight(player_pos, player_angle, enemy_pos, tolerance=1):
    """
    Determines if the enemy is visible within the player's line of sight.
    :param player_pos: Player's position (x, y, z)
    :param player_angle: Orientation angle of the player's gun
    :param enemy_pos: Enemy's position (x, y, z)
    :param tolerance: Allowable angle difference to consider the enemy in line of sight
    :return: True if the enemy is in sight, False otherwise
    """
    # Calculate gun direction vector based on the player's angle
    gun_dx = cos(radians(player_angle))
    gun_dy = sin(radians(player_angle))

    # Vector from player to enemy
    enemy_dx = enemy_pos[0] - player_pos[0]
    enemy_dy = enemy_pos[1] - player_pos[1]

    # Normalize the vector towards the enemy
    distance = sqrt(enemy_dx**2 + enemy_dy**2)
    if distance == 0:
        return False  # Enemy is at the same location as the player, hence not in sight
    enemy_dx /= distance
    enemy_dy /= distance

    # Dot product between the gun direction and the enemy direction
    dot_product = gun_dx * enemy_dx + gun_dy * enemy_dy

    # Calculate the angle between the two vectors
    angle_between = degrees(acos(dot_product))

    # Check if the calculated angle is within the specified tolerance
    return abs(angle_between) <= tolerance

def handle_keyboard_input(key, x, y):
    """
    Handles keyboard events for movement, rotation, cheat mode, and game reset.
    """
    global camera_pos, life_remaining, score, bullets_missed, player_pos, player_angle, player_speed, player_rotate_speed, cheat_mode, gun_follow_mode, game_over, first_person_mode

    # Player moves forward (W key)
    if key == b'w':
        dx = player_speed * cos(radians(player_angle))  # Move in x direction
        dy = player_speed * sin(radians(player_angle))  # Move in y direction
        if -GRID_LENGTH <= player_pos[0] + dx <= GRID_LENGTH and -GRID_LENGTH <= player_pos[1] + dy <= GRID_LENGTH:
            player_pos = (player_pos[0] + dx, player_pos[1] + dy, player_pos[2])

    # Player moves backward (S key)
    if key == b's':
        dx = player_speed * cos(radians(player_angle))
        dy = player_speed * sin(radians(player_angle))
        if -GRID_LENGTH <= player_pos[0] - dx <= GRID_LENGTH and -GRID_LENGTH <= player_pos[1] - dy <= GRID_LENGTH:
            player_pos = (player_pos[0] - dx, player_pos[1] - dy, player_pos[2])

    # Rotate gun left (A key)
    if key == b'a':
        player_angle += player_rotate_speed

    # Rotate gun right (D key)
    if key == b'd':
        player_angle -= player_rotate_speed

    # Toggle cheat mode (C key)
    if key == b'c':
        cheat_mode = not cheat_mode
        if cheat_mode:
            print("Cheat mode enabled!")
        else:
            print("Cheat mode disabled!")

    # Toggle gun-follow mode in cheat mode (V key)
    if key == b'v':
        if cheat_mode and first_person_mode:
            gun_follow_mode = not gun_follow_mode
            if gun_follow_mode:
                print("Gun-follow mode enabled!")
            else:
                print("Gun-follow mode disabled!")

    # Reset the game (R key)
    if key == b'r':
        global game_over, life_remaining, score, bullets_missed

        game_over = False
        cheat_mode = False
        life_remaining = 5
        score = 0
        bullets_missed = 0
        player_pos = (0, 0, 0)
        player_angle = 0
        player_speed = 10
        player_rotate_speed = 10
        bullets.clear()
        enemies.clear()
        setup_initial_enemies()
        print("Game reset!")

        
def handle_special_keys(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos, first_person_mode

    if not first_person_mode:
        x, y, z = camera_pos

        # Move camera up (UP arrow key)
        if key == GLUT_KEY_UP:
            z += 10  # Move camera upwards by 10 units

        # Move camera down (DOWN arrow key)
        if key == GLUT_KEY_DOWN:
            z -= 10  # Move camera downwards by 10 units

        # Rotate camera left (LEFT arrow key)
        if key == GLUT_KEY_LEFT:
            angle = -1  # Rotate camera to the left
            x = x * cos(radians(angle)) - y * sin(radians(angle))
            y = x * sin(radians(angle)) + y * cos(radians(angle))

        # Rotate camera right (RIGHT arrow key)
        if key == GLUT_KEY_RIGHT:
            angle = 1  # Rotate camera to the right
            x = x * cos(radians(angle)) - y * sin(radians(angle))
            y = x * sin(radians(angle)) + y * cos(radians(angle))

        camera_pos = (x, y, z)

def handle_mouse_input(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    global player_pos, player_angle, bullets, bullet_height, bullet_speed, camera_pos, gun_barrel_length, first_person_mode, fovY

    # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Calculate the bullet's initial position at the tip of the gun nozzle
        bullet_x = player_pos[0] + gun_barrel_length * cos(radians(player_angle))
        bullet_y = player_pos[1] + gun_barrel_length * sin(radians(player_angle))
        bullet_z = bullet_height  # Set bullet height to match the gun nozzle height

        # Create a new bullet object with the calculated position and angle
        bullet = {
            'pos': (bullet_x, bullet_y, bullet_z),  # Position at the gun nozzle
            'angle': player_angle  # Bullet direction based on player's angle
        }
        bullets.append(bullet)

    # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person_mode = not first_person_mode  # Toggle between modes
        if first_person_mode:
            fovY = 90  # Set field of view for first-person mode
            print("First-person mode activated")
        else:
            fovY = 120  # Set field of view for third-person mode
            camera_pos = (0, 500, 500)  # Reset camera position for third-person view
            print("Third-person mode activated")


def check_aabb_collision_2d(pos1, size1, pos2, size2):
    """
    Checks for axis-aligned bounding box (AABB) collision between two objects in 2D (ignoring z-axis).
    :param pos1: Position of the first object (x, y, z)
    :param size1: Size (half-width) of the first object
    :param pos2: Position of the second object (x, y, z)
    :param size2: Size (half-width) of the second object
    :return: True if the objects collide in 2D, False otherwise
    """
    return (
        abs(pos1[0] - pos2[0]) <= size1 + size2 and  # Check overlap in x-axis
        abs(pos1[1] - pos2[1]) <= size1 + size2      # Check overlap in y-axis
    )


def update():
    """
    Handles all game logic, such as player movement, bullet updates, enemy movement,
    collision detection, and score updates.
    """
    global bullets, enemies, life_remaining, score, bullets_missed, time_elapsed, player_pos, player_angle
    global player_speed, player_rotate_speed, game_over, first_person_mode, camera_pos, cheat_mode
    global gun_follow_mode, player_fall_angle

    if game_over:
        if player_fall_angle < 90:
            player_fall_angle += 2
        return  # Stop further game updates if game over

    time_elapsed += 0.05  # Increment time elapsed (simulate frame-based game logic)

    # Cheat mode logic (continuous rotation and enemy detection)
    if cheat_mode:
        player_angle += player_rotate_speed * 0.25  # Rotate the gun slowly
        for enemy in enemies:
            if check_line_of_sight(player_pos, player_angle, enemy['pos']):
                fire_bullet_towards_enemy()  # Fire a bullet when an enemy is in line of sight
                break  # Fire only one bullet per frame

    # Update bullets (move forward and check for out-of-bounds)
    for bullet in bullets[:]:
        bullet['pos'] = (
            bullet['pos'][0] + bullet_speed * cos(radians(bullet['angle'])),
            bullet['pos'][1] + bullet_speed * sin(radians(bullet['angle'])),
            bullet['pos'][2]
        )

        if abs(bullet['pos'][0]) > GRID_LENGTH or abs(bullet['pos'][1]) > GRID_LENGTH:
            bullets.remove(bullet)
            bullets_missed += 1
            print(f"Bullet missed! Total missed: {bullets_missed}")

            if bullets_missed >= 10:
                game_over = True
                print("Game Over! You missed too many bullets.")
                return  # Stop further updates

    # Check for collisions between bullets and enemies
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if check_aabb_collision_2d(bullet['pos'], 10, enemy['pos'], enemy_radius):  # Bullet size = 10
                bullets.remove(bullet)  # Remove the bullet
                enemies.remove(enemy)  # Remove the enemy
                score += 1  # Increment score
                break  # Stop checking further once collision is handled

    # Check for collisions between the player and enemies
    for enemy in enemies[:]:
        if check_aabb_collision_2d(player_pos, 25, enemy['pos'], enemy_radius):  # Player size = 25
            print(f"Player collided with enemy at {enemy['pos']}")
            enemies.remove(enemy)  # Remove the enemy
            life_remaining -= 1  # Decrement life
            print(f"Life remaining: {life_remaining}")

            if life_remaining <= 0:
                game_over = True
                print("Game Over! You ran out of lives.")
                return  # Stop further updates

    # Move enemies toward the player
    for enemy in enemies:
        move_enemy_towards_player(enemy)  # Call helper function to handle enemy movement

    setup_initial_enemies()


def fire_bullet_towards_enemy():
    """
    Fires a bullet towards the nearest enemy based on player's angle.
    """
    bullet_x = player_pos[0] + gun_barrel_length * cos(radians(player_angle))
    bullet_y = player_pos[1] + gun_barrel_length * sin(radians(player_angle))
    bullet_z = bullet_height  # Same height as the gun nozzle

    bullet = {
        'pos': (bullet_x, bullet_y, bullet_z),  # Start at the gun nozzle
        'angle': player_angle  # Use the player's angle for the bullet
    }
    bullets.append(bullet)


def move_enemy_towards_player(enemy):
    """
    Moves the enemy towards the player's position.
    """
    ex, ey, ez = enemy['pos']  # Enemy position
    px, py, pz = player_pos  # Player position

    # Calculate direction vector from enemy to player
    dx = px - ex
    dy = py - ey
    dz = pz - ez

    # Normalize the direction vector
    distance = sqrt(dx**2 + dy**2 + dz**2)
    if distance > 0:  # Avoid division by zero
        dx /= distance
        dy /= distance
        dz /= distance

    # Update enemy position
    enemy['pos'] = (
        ex + dx * enemy_speed,
        ey + dy * enemy_speed,
        ez + dz * enemy_speed
    )


def setupCamera():
    """
    Configures the camera's projection and view based on the player's position and orientation.
    Supports both first-person and third-person camera modes.
    """
    global first_person_mode, player_pos, player_angle, gun_follow_mode, camera_pos, last_camera_coords
    glMatrixMode(GL_PROJECTION)  # Set to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    gluPerspective(fovY, 1.25, 0.1, 1500)  # Perspective projection (FOV, aspect ratio, near & far clip)

    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset model-view matrix

    if first_person_mode:
        # First-person mode: Position camera at player's head
        head_offset = 200  # Camera at head height
        shoulder_offset = -25  # Offset to the player's right shoulder
        backward_offset = 75  # Slightly behind the player for better view
        x, y, z = player_pos

        # Calculate camera's right direction based on player's rotation
        right_x = -sin(radians(player_angle)) * shoulder_offset
        right_y = cos(radians(player_angle)) * shoulder_offset

        # Calculate backward offset based on player's angle
        backward_x = -cos(radians(player_angle)) * backward_offset
        backward_y = -sin(radians(player_angle)) * backward_offset

        # Camera position: Adjusted from player's position
        camera_x = x + gun_barrel_length * cos(radians(player_angle)) * 0.25 + right_x + backward_x
        camera_y = y + gun_barrel_length * sin(radians(player_angle)) * 0.25 + right_y + backward_y
        camera_z = z + head_offset
        
        # Freeze camera rotation when the gun follow mode is active
        if gun_follow_mode:
            gluLookAt(last_camera_coords[0], last_camera_coords[1], last_camera_coords[2],  # Camera position
                      last_camera_coords[3], last_camera_coords[4], last_camera_coords[5],  # Look-at target
                      0, 0, 1)  # Up vector (fixed upward direction)
        else:
            # Calculate where the camera should look (based on player's orientation)
            look_at_x = camera_x + cos(radians(player_angle))
            look_at_y = camera_y + sin(radians(player_angle))
            last_camera_coords = (camera_x, camera_y, camera_z, look_at_x, look_at_y, camera_z)
            gluLookAt(camera_x, camera_y, camera_z,  # Camera position
                      look_at_x, look_at_y, camera_z,  # Target to look at
                      0, 0, 1)  # Up vector (fixed upward direction)
    else:
        # Third-person mode: Set up the camera behind the player
        x, y, z = camera_pos
        gluLookAt(x, y, z,  # Camera position
                  0, 0, 0,  # Looking at the origin (center)
                  0, 0, 1)  # Up vector (fixed upward direction)


def idle():
    """
    Idle function that runs continuously to update game state and render the scene.
    """
    update()  # Handle game logic and updates
    glutPostRedisplay()  # Trigger screen redraw for real-time updates


def showScreen():
    """
    Render the game scene by clearing buffers, setting the camera, and drawing objects.
    Displays the environment, player status, and game information.
    """
    global game_over

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen and depth buffer
    glLoadIdentity()  # Reset model-view matrix
    glViewport(0, 0, 1000, 800)  # Set window size

    setupCamera()  # Set up the camera

    # Draw the grid (floor)
    glBegin(GL_QUADS)
    for i in range(-GRID_LENGTH, GRID_LENGTH, 100):
        for j in range(-GRID_LENGTH, GRID_LENGTH, 100):
            if (i + j) % 200 == 0:
                glColor3f(1, 1, 1)  # Light gray color
            else:
                glColor3f(0.7, 0.5, 0.95)  # Darker gray color
            glVertex3f(i, j, 0)
            glVertex3f(i + 100, j, 0)
            glVertex3f(i + 100, j + 100, 0)
            glVertex3f(i, j + 100, 0)
    glEnd()

    # Draw game walls with different colors
    wall_height = 100
    glBegin(GL_QUADS)

    glColor3f(0, 0, 1)  # Blue color / Top Wall
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)

    glColor3f(0, 1, 1)  # Cyan color / Left Wall
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)

    glColor3f(1, 1, 0)  # Yellow color / Bottom Wall
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, wall_height)

    glColor3f(1, 0, 1)  # Magenta color / Right Wall
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, wall_height)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, wall_height)

    glEnd()


    # Display game status information
    render_text(10, 770, f"Player Life Remaining: {life_remaining}")
    render_text(10, 740, f"Game Score: {score}")
    render_text(10, 710, f"Player Bullet Missed: {bullets_missed}")

    # Display game over message if applicable
    if game_over:
        render_text(400, 750, "GAME OVER", font=GLUT_BITMAP_HELVETICA_18)
        render_text(400, 710, "Press R to Restart", font=GLUT_BITMAP_HELVETICA_18)
        drawp_layer()  # Draw the player in a stationary state (if game is over)
    else:
        render_scene()  # Continue drawing the game scene (if active)

    glutSwapBuffers()  # Swap buffers to update the display


# Main function to initialize and run the OpenGL game window

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Enable double buffering, RGB, depth test
glutInitWindowSize(1000, 800)  # Set window dimensions
glutInitWindowPosition(0, 0)  # Set window position
wind = glutCreateWindow(b"3D OpenGL Game")  # Create the OpenGL window

glutDisplayFunc(showScreen)  # Register the display callback function
glutKeyboardFunc(handle_keyboard_input)  # Register keyboard input handler
glutSpecialFunc(handle_special_keys)  # Register special key input handler
glutMouseFunc(handle_mouse_input)  # Register mouse input handler
glutIdleFunc(idle)  # Register idle function to continuously update game state
glutMainLoop()  # Enter the GLUT main loop to run the game

