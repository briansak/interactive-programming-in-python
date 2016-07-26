# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.friction = .025
        self.rotation_speed = .15
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward = [0,1]
        self.clockwise = False
        self.counterclockwise = False
        
    def draw(self,canvas):
        
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        
        # screen wrap
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # turning
        if self.clockwise:
            self.angle += self.rotation_speed
        if self.counterclockwise:
            self.angle -= self.rotation_speed
            
        # position and velocity update
        for i in (0, 1):
            self.forward[i] = angle_to_vector(self.angle)[i]
            self.vel[i] *= (1 - self.friction)
            if self.thrust:
                self.vel[i] += self.forward[i]
                
    def keydown(self, key):
        if key == simplegui.KEY_MAP['left']: # Turn Counterclockwise
            self.counterclockwise = True
        elif key == simplegui.KEY_MAP['right']:# Turn Clockwise
            self.clockwise = True
        elif key == simplegui.KEY_MAP['up']:# Thrust
            self.thrust = True
            ship_thrust_sound.play()
        elif key == simplegui.KEY_MAP['space']:# Fire
            missile_spawner()
            
    def keyup(self, key):
        if key == simplegui.KEY_MAP['left']: # Stop Turning Counterclockwise
            self.counterclockwise = False
        elif key == simplegui.KEY_MAP['right']:# Stop Turning Clockwise"
            self.clockwise = False
        elif key == simplegui.KEY_MAP['up']:# Stop Thrusting
            self.thrust = False
            ship_thrust_sound.pause()

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):    
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        
        #screen wrap
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT  
        
        self.angle += self.angle_vel
    
def draw(canvas):
    global time, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)

    for missile in missiles:
        missile.draw(canvas)
        
    for asteroid in asteroids:
        asteroid.draw(canvas)
        
    
    # update ship and sprites
    my_ship.update()

    for missile in missiles:
        missile.update()
            
    for asteroid in asteroids:
        asteroid.update()
    
    # draw score and lives
    canvas.draw_text("Lives: "+ str(lives), [20, 30], 20, "Yellow")
    canvas.draw_text("Score: " + str(score), [WIDTH - 80, 30], 20, "Yellow")

# triggered missle fire
def missile_spawner():
    global missiles
   
    missile_speed = 5.0
    missile_pos = (my_ship.pos[0] + my_ship.radius * math.cos(my_ship.angle), my_ship.pos[1] + my_ship.radius * math.sin(my_ship.angle))
    missile_vel = (my_ship.vel[0] + my_ship.forward[0] * missile_speed, my_ship.vel[1] + my_ship.forward[1] * missile_speed)
    
    a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
    
    # only draw one right now
    if len(missiles) == 0:
        missiles.append(a_missile)
    else:
        missiles[0] = (a_missile)
        
# timer handler that spawns a rock    
def asteroid_spawner():
    global asteroids
    
    asteroid_pos = [random.randrange(50, WIDTH - 50), random.randrange(50, HEIGHT - 50)]
    asteroid_vel = [random.randrange(-5, 5), random.randrange(-5, 5)]
    asteroid_ang = random.random() * .05 - .05
    asteroid_angle_vel = (random.randrange(-10,10) / 100.0)
    
    # generate new asteroid
    an_asteroid = Sprite(asteroid_pos, asteroid_vel, asteroid_ang, asteroid_angle_vel, asteroid_image, asteroid_info)
    
    # only draw one right now
    if len(asteroids) == 0:
        asteroids.append(an_asteroid)
    else:
        asteroids[0] = (an_asteroid)
    
# initialize frame
frame = simplegui.create_frame("Spaceship", WIDTH, HEIGHT)

# initialize ship and two sprites
missiles = []
asteroids = []
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(1000.0, asteroid_spawner)

# register keyhandlers

frame.set_keydown_handler(my_ship.keydown)
frame.set_keyup_handler(my_ship.keyup)

# get things rolling
timer.start()
frame.start()


###    1 pt - The program draws the ship as an image.
###    1 pt - The ship flies in a straight line when not under thrust.
###    1 pt - The ship rotates at a constant angular velocity in a counter clockwise direction when the left arrow key is held down.
###    1 pt - The ship rotates at a constant angular velocity in the clockwise direction when the right arrow key is held down.
###    1 pt - The ship's orientation is independent of its velocity.
###    1 pt - The program draws the ship with thrusters on when the up arrow is held down.
###    1 pt - The program plays the thrust sound only when the up arrow key is held down.
###    1 pt - The ship accelerates in its forward direction when the thrust key is held down.
###    1 pt - The ship's position wraps to the other side of the screen when it crosses the edge of the screen.
###    1 pt - The ship's velocity slows to zero while the thrust is not being applied.
###    1 pt - The program draws a rock as an image.
###    1 pt - The rock travels in a straight line at a constant velocity.
###    1 pt - The rock is respawned once every second by a timer.
###    1 pt - The rock has a random spawn position, spin direction and velocity.
###    1 pt - The program spawns a missile when the space bar is pressed.
###    1 pt - The missile spawns at the tip of the ship's cannon.
###    1 pt - The missile's velocity is the sum of the ship's velocity and a multiple of its forward vector.
###    1 pt - The program plays the missile firing sound when the missile is spawned.
###    1 pt - The program draws appropriate text for lives on the upper left portion of the canvas.
###    1 pt - The program draws appropriate text for score on the upper right portion of the canvas.


