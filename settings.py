import pygame
from pygame.locals import *

FPS = 8
BANDAID_TIME = 1.567  # seconds
UP_JUMP_TIME = 0.2    # seconds
FLY_TIME = 5.0    # seconds

GRAVITY = 0.55

NUM_LIVES = 3
NUM_HP = 3

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
DARKRED   = (255,  50,   0)
DARKERRED = (195,  40,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
BLUE2     = ( 10,   0, 215)
LIGHTBLUE = (180, 180, 255)
DARKGREEN = (  0, 155,   0)
LIMEGREEN = ( 50, 205,  50)
DARKGRAY  = ( 40,  40,  40)
LIGHTGRAY = ( 80,  80,  80)
PURPLE    = (127,   0, 255)
YELLOW    = (255, 255,   0)
BYELLOW   = (255, 255, 150)
GOLD      = (255, 215,   0)
LIFECOLOR = (255, 255,   0)


SOUND_LIFE_FILE = 'sounds/angelic.wav'
SOUND_JUMP_FILE = 'sounds/jump1.wav'
SOUND_PORTAL_FILE = 'sounds/portal1.wav'
SOUND_STICKY_ON_FILE = 'sounds/sticky_on.wav'
SOUND_STICKY_OFF_FILE = 'sounds/sticky_off.wav'
SOUND_STICKY_MOVE_FILE = 'sounds/sticky_move.wav'
SOUND_HURT_FILE1 = 'sounds/hurt1.wav'
SOUND_HURT_FILE2 = 'sounds/hurt2.wav'
SOUND_BOUNCE_LARGE_FILE = 'sounds/boing_large.wav'
SOUND_BOUNCE_MEDIUM_FILE = 'sounds/boing_med.wav'
SOUND_BOUNCE_SMALL_FILE = 'sounds/boing_little.wav'
SOUND_DIE_FILE = 'sounds/deaded.wav'
SOUND_PIT_DIE_FILE = 'sounds/deaded_pit.wav'
