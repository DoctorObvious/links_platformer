from settings import *

import pygame
from pygame import *

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 300   # not sure what this is for


def main():
    global cameraX, cameraY
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("PLATFORMER! coproducers: Link, mark")
    timer = pygame.time.Clock()

    up = down = left = right = running = False
    bg = Surface((32,32))
    bg.convert()
    bg.fill(Color("#000023"))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []

    x = y = 0
    level = [
        "PPPPPPPPPPPPPPPPPSPPPPPPP",
        "P               P P     P",
        "P               P      EP",
        "P            SSSS PPPPPPP",
        "P                       P",
        "P         P             P",
        "P         P      B      P",
        "P      B  B B           P",
        "P      B  B E           P",
        "PP     B  B E           P",
        "P      B  B E           P",
        "P  P   B  B E           P",
        "P      B  B B           P",
        "P      B  B             P",
        "P      B  B             P",
        "P         BBB           P",
        "P  B                    P",
        "P                       P",
        "P                       P",
        "PPWWWWPMMMMMMMMMMPPPPPPPP", ]
    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
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

    while 1:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT: raise SystemExit, "QUIT"
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit, "ESCAPE"
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                running = True

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
        player.update(up, down, left, right, running, platforms)
        entities.draw(screen)

        pygame.display.update()

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32,32))
        self.image.fill((0, 225, 0))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self, up, down, left, right, running, platforms):
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 10
        if down:
            pass
        if running:
            self.xvel = 12
        if left:
            self.xvel = self.xvel - 0.65

        if right:
            self.xvel = self.xvel + 0.65

        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.55
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if self.onGround and not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)

        #limit horizontal speed
        if self.xvel < -8.0:
            self.xvel = -8.0
        if self.xvel > 8.0:
            self.xvel = 8.0

        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):

                # Handle collision with an Exit Block
                if isinstance(p, ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))

                # Handle collision with an Bouncy Block
                elif isinstance(p, PlatformBouncy1):
                    if xvel > 0:
                        self.rect.right = p.rect.left
                        print "collide left bounce"
                        self.xvel = -self.xvel
                    if xvel < 0:
                        self.rect.left = p.rect.right
                        print "collide right bounce"
                        self.xvel = -self.xvel
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = -self.yvel
                        print "collide bottom bounce off"
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = False
                        self.yvel = -self.yvel
                        print "collide top bounce off"

                elif isinstance(p, Platformmovingcarpetleft):
                    if xvel > 0:
                        self.rect.right = p.rect.left
                        print "collide left mcarpet"
                        self.xvel = -self.xvel
                    if xvel < 0:
                        self.rect.left = p.rect.right
                        print "collide right mcarpet"
                        self.xvel = -self.xvel
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.xvel = self.xvel + 10
                        print "collide bottom mcarpet"
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.xvel = -self.xvel - 10
                        print "collide top mcarpet"
                    if yvel < 0:
                        self.rect.bottom = p.rect.top
                        self.xvel = -self.xvel - 10
                        print "collide top mcarpet"

                elif isinstance(p, Platformmovingcarpetright):
                    if xvel > 0:
                        self.rect.right = p.rect.left
                        print "collide left mcarpet"
                        self.xvel = -self.xvel
                    if xvel < 0:
                        self.rect.left = p.rect.right
                        print "collide right mcarpet"
                        self.xvel = -self.xvel
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.xvel = self.xvel + 10
                        print "collide bottom mcarpet"
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.xvel = self.xvel + 10
                        print "collide top mcarpet"

                elif isinstance(p, PlatformSticky):
                    self.onGround = True
                    if xvel > 0:
                        self.rect.right = p.rect.left + 1
                        print "collide right stick"
                        self.yvel = 0.0
                        self.xvel = 0.0
                    if xvel < 0:
                        self.rect.left = p.rect.right - 1
                        print "collide left stick"
                        self.yvel = 0.0
                        self.xvel = -0.0
                    if yvel < 0:
                        self.rect.top = p.rect.bottom - 1
                        self.yvel = 0.0
                        print "collide bottom stick"
                    if yvel > 0:
                        self.rect.bottom = p.rect.top + 1
                        self.yvel = 0.0
                        print "collide top stick"

                else:  # Must be a normal platform
                    if xvel > 0:
                        self.rect.right = p.rect.left
                        print "collide right"
                    if xvel < 0:
                        self.rect.left = p.rect.right
                        print "collide left"
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0
                        print "collide top"
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

    def update(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#DD33FF"))

class PlatformBouncy1(Platform):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#5533FF"))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class PlatformSticky(Platform):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#FF0155"))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class Platformmovingcarpetleft(Platform):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#0000FF"))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class Platformmovingcarpetright(Platform):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#0000FF"))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass


if __name__ == "__main__":
    main()

# def main():
#     global FPSCLOCK, DISPLAYSURF, BASICFONT
#
#     pygame.init
#     pygame.mixer.init(frequency=44100, channels=2)
#     s = pygame.mixer.Sound(SOUND_HAPPY)
#     s.play()
#
#     FPSCLOCK = pygame.time.Clock()
#     DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHIEGHT))
#     BASICFONT = pygame.font.Font('freesanbold.ttf', 18)
#     pygame.display.set_caption('Platformer')
#
#     show_splash_screen()
#
#
# def show_splash_screen():
#     title_font = pygame.font.Font('freesanbold.ttf', 100)
#
#     degrees1 = 0
#     degrees2 = 0
#
#     pygame.event.get
#
#     while True:
#         DISPLAYSURF.fill(BGCOLOR)
#
#         use_color = get_pulse_color((BLACK, PURPLE), pulse_time=2.0)
#         title_surf_2 = title_font.render('Platformer', True, use_color)
#
#
# def terminate():
#     pygame.quit()
#     sys.exit