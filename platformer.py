from settings import *
from level_data import *
from game_clock import *
from pygame import *

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = int(WIN_WIDTH / 5)


def my_print(message):
    if False:
        print message


def main():
    global cameraX, cameraY
    global DISPLAYSURF, BASICFONT
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("PLATFORMER! Producers: Link, Mark")
    timer = pygame.time.Clock()

    start_the_clock()

    DISPLAYSURF = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    player = Player(32, 32)

    for level_number in range(NUM_LEVELS):
        player.finished_level = False
        player.reset_position(32, 32)
        player.last_hurt_time = current_time() - 10.0
        level = levels[level_number]
        level_width = len(level[0]) * 32
        up = down = left = right = running = False
        bg = Surface((32,32))
        bg.convert()
        bg.fill(Color("#000023"))
        entities = pygame.sprite.Group()
        platforms = []
        start_message = 'Level: {}'.format(level_number + 1)
        info_message = level_messages[level_number]
        message_prompt = 'Press any key to start'

        x = y = 0
        cameraX = cameraY = 0
        level_started = False

        # build the level
        for row in level:
            for col in row:
                if col == "P":
                    p = Platform(x, y)
                    platforms.append(p)
                    entities.add(p)
                if col == "D":
                    d = PlatformPit(x, y)
                    platforms.append(d)
                    entities.add(d)
                if col == "H":
                    h = PlatformHurt(x, y)
                    platforms.append(h)
                    entities.add(h)
                if col == "L":
                    l = PlatformLife(x, y)
                    platforms.append(l)
                    entities.add(l)
                if col == "B":
                    b = PlatformBouncy1(x, y)
                    platforms.append(b)
                    entities.add(b)
                if col == "S":
                    s = PlatformSticky(x, y)
                    platforms.append(s)
                    entities.add(s)
                if col == "M":
                    m = Platformmovingcarpetright(x, y)
                    platforms.append(m)
                    entities.add(m)
                if col == "W":
                    w = Platformmovingcarpetleft(x, y)
                    platforms.append(w)
                    entities.add(w)
                if col == "E":
                    e = ExitBlock(x, y)
                    platforms.append(e)
                    entities.add(e)
                x += 32
            y += 32
            x = 0

        entities.add(player)
        # print "Level {}".format(level_number + 1)
        while not player.finished_level:
            timer.tick(60)

            for e in pygame.event.get():
                if e.type == QUIT: raise SystemExit, "QUIT"
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    raise SystemExit, "ESCAPE"
                if e.type == KEYDOWN and e.key == K_UP:
                    up = True
                    level_started = True
                if e.type == KEYDOWN and e.key == K_DOWN:
                    down = True
                    level_started = True
                if e.type == KEYDOWN and e.key == K_LEFT:
                    left = True
                    level_started = True
                if e.type == KEYDOWN and e.key == K_RIGHT:
                    right = True
                    level_started = True
                if e.type == KEYDOWN and e.key == K_SPACE:
                    running = True
                    level_started = True

                if e.type == KEYUP and e.key == K_UP:
                    up = False
                if e.type == KEYUP and e.key == K_DOWN:
                    down = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False
                if e.type == KEYUP and e.key == K_LEFT:
                    left = False
                if e.type == KEYUP and e.key == K_RIGHT:
                    right = False

            # draw background
            for y in range(32):
                for x in range(32):
                    screen.blit(bg, (x * 32, y * 32))

            # update player, draw everything else
            if level_started:
                player.update(up, down, left, right, running, platforms, level_width)

            # camera movement
            for entity in entities:
                if isinstance(entity, Platform):
                    entity.update(cameraX, cameraY)

            # redraw entities
            entities.draw(screen)

            # draw text
            if not level_started:
                draw_big_message(start_message, color=BLUE, pulse_time=1.0)
                draw_small_message(info_message, color=BLUE, pulse_time=1.0)
                draw_prompt_message(message_prompt, color=BLACK, pulse_time=1.5)
                level_start_time = current_time()

            message_time = 'Time = {:3.1f}'.format(elapsed_time(level_start_time))
            message_life = 'lives = {}'.format(player.lives)
            draw_life_message(message_life, color=BLUE, pulse_time=1.5)
            draw_time_message(message_time, color=RED, pulse_time=1.5)

            pygame.display.update()

        # Add the time spent on the just-finished level
        player.all_previous_level_times = player.all_previous_level_times + elapsed_time(level_start_time)
        print "Finished level {}, total playing time = {:3.1f}".format(level_number + 1, player.all_previous_level_times)

        if level_number + 1 == NUM_LEVELS:
            print "win!!!!!!"
            raise SystemExit


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32,32))
        self.image.fill((0, 225, 0))
        self.image.convert()
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.onSticky = False
        self.groundSpeed = 0
        self.rect = Rect(x, y, 32, 32)
        self.last_hurt_time = current_time() - 10.0
        self.lives = 3
        self.finished_level = False
        self.all_previous_level_times = 0

    def reset_position(self, x, y):
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.onSticky = False
        self.groundSpeed = 0
        self.rect = Rect(x, y, 32, 32)
        self.last_hurt_time = current_time() - 10.0
        self.image.fill((0, 225, 0))

    def update(self, up, down, left, right, running, platforms, level_width):
        global cameraX, cameraY
        if up:
            # only jump if on the ground
            if self.onSticky:
                self.yvel = self.yvel - 0.65
            elif self.onGround:
                self.yvel -= 10.2
            # self.onGround = False
            # self.onSticky = False
        if down:
            if self.onSticky:
                self.yvel = self.yvel + 0.65
            self.onSticky = False
        if running:
            self.xvel = 12
        if left:
            if self.xvel > 0.0 and self.onGround:
                self.xvel = 0.0
            self.xvel = self.xvel - 0.65

        if right:
            if self.xvel < 0.0 and self.onGround:
                self.xvel = 0.0
            self.xvel = self.xvel + 0.65

        # if not self.onGround and not self.onSticky:
        if not self.onSticky:
            # only accelerate with gravity if in the air
            self.yvel += 0.55
            # max falling speed
            if self.yvel > 100:
                self.yvel = 100
        if self.onGround and not(left or right):
            self.xvel = 0

        # only move up or down on stickies when you press up or down.
        if self.onSticky and not(up or down):
            self.yvel = 0

        # increment in x direction
        if self.onGround:
            self.rect.left += self.xvel + self.groundSpeed
        else:
            self.rect.left += self.xvel

        # reset things that are set in collision detection
        self.onSticky = False
        self.groundSpeed = 0

        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)

        # limit horizontal speed
        if self.xvel < -8.0 + self.groundSpeed:
            self.xvel = -8.0 + self.groundSpeed
        if self.xvel > 8.0 + self.groundSpeed:
            self.xvel = 8.0 + self.groundSpeed

        # increment/move in y direction
        self.rect.top = self.rect.top + self.yvel

        # assuming we're in the air
        if not self.onSticky:
            self.onGround = False
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

        # Limit Vertical Speed
        if self.onSticky:
            if self.yvel < -5.0:
                self.yvel = -5.0
            if self.yvel > 5.0:
                self.yvel = 5.0

        # calculate new x camera
        old_cameraX = cameraX

        if (cameraX + HALF_WIDTH) - (self.rect.centerx + cameraX) > CAMERA_SLACK:
            cameraX = (self.rect.centerx + cameraX) + CAMERA_SLACK - HALF_WIDTH
        elif (self.rect.centerx + cameraX) - (cameraX + HALF_WIDTH) > CAMERA_SLACK:
            cameraX = (self.rect.centerx + cameraX) - CAMERA_SLACK - HALF_WIDTH

        if cameraX < 0:
            cameraX = 0
        if cameraX > level_width - WIN_WIDTH:
            cameraX = level_width - WIN_WIDTH

        # update player, based on camera movement.
        self.rect.centerx = self.rect.centerx - (cameraX - old_cameraX)

        # making you turn red after hurt
        if elapsed_time(self.last_hurt_time) < BANDAID_TIME:
            self.image.fill((255, 0, 0, 5))
        else:
            self.image.fill((0, 225, 0))

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):

                # Handle collision with an Exit Block
                if isinstance(p, ExitBlock):
                    self.finished_level = True
                    # pygame.event.post(pygame.event.Event(QUIT))

                # Handle collision with an Bouncy Block
                elif isinstance(p, PlatformBouncy1):
                    my_print("Bouncy: ")
                    if xvel > 0:
                        self.rect.right = p.rect.left
                        my_print("collide left")
                        self.xvel = -self.xvel
                    if xvel < 0:
                        self.rect.left = p.rect.right
                        my_print("collide right")
                        self.xvel = -self.xvel
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = -self.yvel
                        my_print("collide bottom bounce off")
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = False
                        self.yvel = -self.yvel
                        my_print ("collide top bounce off")

                elif isinstance(p, PlatformHurt):
                    if elapsed_time(self.last_hurt_time) > BANDAID_TIME:
                        self.lives -= 1
                        self.last_hurt_time = current_time()
                        if self.lives == 0:
                            pygame.event.post(pygame.event.Event(QUIT))
                        print "Hurt: lives left = {}".format(self.lives)
                    if xvel > 0:
                        self.rect.right = p.rect.left
                        my_print("collide left")
                    if xvel < 0:
                        self.rect.left = p.rect.right
                        my_print("collide right")
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        my_print("collide bottom")
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = False
                        self.yvel = -6.0
                        my_print("collide top")

                elif isinstance(p, PlatformPit):
                    self.lives -= 1
                    if self.lives == 0:
                        pygame.event.post(pygame.event.Event(QUIT))
                    print "hit pit: lives left = {}".format(self.lives)
                    self.reset_position(32, 32)

                elif isinstance(p, PlatformLife):
                    print "Healed: lives = {}".format(self.lives)
                    self.last_hurt_time = current_time() - 10.0
                    if xvel > 0:
                        self.rect.right = p.rect.left
                        self.xvel = 0
                        self.lives = self.lives + 1
                        if self.lives > 3:
                            self.lives = 3
                    if xvel < 0:
                        self.rect.left = p.rect.right
                        self.xvel = 0
                        self.lives = self.lives + 1
                        if self.lives > 3:
                            self.lives = 3
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0
                        self.lives = self.lives + 1
                        if self.lives > 3:
                            self.lives = 3
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0
                        self.lives = self.lives + 1
                        if self.lives > 3:
                            self.lives = 3

                elif isinstance(p, Platformmovingcarpetleft):
                    my_print("Left carpet: ")
                    # if xvel > 0:
                    #     self.rect.right = p.rect.left
                    #     my_print "collide left"
                    #     self.xvel = -self.xvel
                    # if xvel < 0:
                    #     self.rect.left = p.rect.right
                    #     my_print "collide right"
                    #     self.xvel = -self.xvel
                    # if yvel < 0:
                    #     self.rect.top = p.rect.bottom
                    #     my_print "collide bottom"
                    if yvel > 0:
                        self.onGround = True
                        self.yvel = 0
                        self.rect.bottom = p.rect.top
                        # self.xvel = self.xvel - 10
                        self.groundSpeed = -10
                        my_print("collide top")

                elif isinstance(p, Platformmovingcarpetright):
                    my_print("Right carpet: ")

                    if yvel > 0:
                        self.onGround = True
                        self.yvel = 0
                        self.rect.bottom = p.rect.top
                        # self.xvel = self.xvel + 10
                        self.groundSpeed = 10
                        my_print("collide top")

                elif isinstance(p, PlatformSticky):
                    my_print("Sticky: ")
                    self.onGround = True
                    self.onSticky = True

                    # See if only collided/overlapped by 1
                    if self.rect.right == p.rect.left + 1 or self.rect.left == p.rect.right - 1  \
                        or self.rect.top == p.rect.bottom - 1 or self.rect.bottom == p.rect.top + 1:

                        pass
                        # Determine if we are on the top or, say, a side. Only allow side movement when checking
                        # collisions based on the yvel (not when checking horizontal)
                        # if self.rect.bottom != p.rect.top + 1 and yvel != 0.0:
                        #     self.yvel = 0.0

                    else:
                        if xvel > 0:
                            self.rect.right = p.rect.left + 1
                            my_print("collide right")
                            self.yvel = 0.0
                            self.xvel = 0.0
                        if xvel < 0:
                            self.rect.left = p.rect.right - 1
                            my_print("collide left")
                            self.yvel = 0.0
                            self.xvel = 0.0
                        if yvel < 0:
                            self.rect.top = p.rect.bottom - 1
                            self.yvel = 0.0
                            my_print("collide bottom")
                        if yvel > 0:
                            self.rect.bottom = p.rect.top + 1
                            self.yvel = 0.0
                            my_print ("collide top")

                else:  # Must be a normal platform
                    my_print("Platform: ")
                    if xvel > 0:
                        self.rect.right = p.rect.left
                        self.xvel = 0
                        my_print("collide right")
                    if xvel < 0:
                        self.rect.left = p.rect.right
                        self.xvel = 0
                        my_print("collide left")
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0
                        my_print("collide top")
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0


class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#999999"))
        self.rect = Rect(x, y, 32, 32)
        self.x = x
        self.y = y

    def update(self, camera_x, camera_y):
        self.rect.x = self.x - camera_x
        self.rect.y = self.y - camera_y


class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#DD33FF"))
        self.x = x
        self.y = y


class PlatformBouncy1(Platform):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#5533FF"))
        self.rect = Rect(x, y, 32, 32)
        self.x = x
        self.y = y


class PlatformHurt(Platform):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#FF0000"))
        self.rect = Rect(x, y, 32, 32)
        self.x = x
        self.y = y


class PlatformPit(Platform):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color(0, 0, 0))
        self.rect = Rect(x, y, 32, 32)
        self.x = x
        self.y = y


class PlatformLife(Platform):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color(0, 128, 128, 25))
        self.rect = Rect(x, y, 32, 32)
        self.x = x
        self.y = y


class PlatformSticky(Platform):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color(128, 128, 0))
        self.rect = Rect(x, y, 32, 32)
        self.x = x
        self.y = y


class Platformmovingcarpetleft(Platform):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color(128, 0, 0))
        self.rect = Rect(x, y, 32, 32)
        self.x = x
        self.y = y


class Platformmovingcarpetright(Platform):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color(255, 0, 255))
        self.rect = Rect(x, y, 32, 32)
        self.x = x
        self.y = y


########################
# Helper Functions
########################

def draw_big_message(message, color=BLUE, pulse_time=8.0):
    use_color = get_pulse_color([color, GREEN], pulse_time=pulse_time)

    if message is not None:
        font = pygame.font.Font('freesansbold.ttf', 50)
        surf = font.render(message, True, use_color)
        rect = surf.get_rect()
        rect.midtop = (HALF_WIDTH, HALF_HEIGHT)
        DISPLAYSURF.blit(surf, rect)

def draw_life_message(message_life, color=RED, pulse_time=8.0):
    use_color = get_pulse_color([color, DARKRED], pulse_time=pulse_time)

    if message_life is not None:
        font = pygame.font.Font('freesansbold.ttf', 15)
        surf = font.render(message_life, True, use_color)
        rect = surf.get_rect()
        rect.midtop = (WIN_WIDTH - WIN_WIDTH + 50, WIN_HEIGHT - WIN_HEIGHT + 10)
        DISPLAYSURF.blit(surf, rect)

def draw_time_message(message_time, color=RED, pulse_time=8.0):
    use_color = get_pulse_color([color, DARKRED], pulse_time=pulse_time)

    if message_time is not None:
        font = pygame.font.Font('freesansbold.ttf', 15)
        surf = font.render(message_time, True, use_color)
        rect = surf.get_rect()
        rect.midtop = (WIN_WIDTH - 50, WIN_HEIGHT - WIN_HEIGHT + 10)
        DISPLAYSURF.blit(surf, rect)

def draw_prompt_message(message_prompt, color=BLACK, pulse_time=8.0):
    use_color = get_pulse_color([color, DARKGREEN], pulse_time=pulse_time)

    if message_prompt is not None:
        font = pygame.font.Font('freesansbold.ttf', 15)
        surf = font.render(message_prompt, True, use_color)
        rect = surf.get_rect()
        rect.midtop = (HALF_WIDTH, WIN_HEIGHT - 25)
        DISPLAYSURF.blit(surf, rect)


def draw_small_message(message_list, color=BLUE, pulse_time=8.0):
    use_color = get_pulse_color([color, GREEN], pulse_time=pulse_time)

    for m, message in enumerate(message_list):
        if message is not None:
            font = pygame.font.Font('freesansbold.ttf', 25)
            surf = font.render(message, True, use_color)
            rect = surf.get_rect()
            rect.midtop = (HALF_WIDTH, HALF_HEIGHT + 50 + (m * 25))
            DISPLAYSURF.blit(surf, rect)


def get_pulse_color(colors, pulse_time=2.0, pulse_start_time=0.0):
    num_colors = len(colors)
    one_color_time = pulse_time/num_colors

    mod_time = ((current_time() - pulse_start_time) % pulse_time)
    norm_time = mod_time/one_color_time
    ix1 = int(norm_time)
    ix2 = (ix1+1) % num_colors
    fraction = norm_time - ix1

    use_color = list(colors[0])
    for ii in range(3):
        use_color[ii] = int((1.0-fraction) * float(colors[ix1][ii]) + fraction * float(colors[ix2][ii]))

    use_color = tuple(use_color)
    return use_color


if __name__ == "__main__":
    main()
