import sys
import pygame

# ENGINE
TIMER = pygame.USEREVENT + 1
DELAY = 17

# GRAPHICS
CAPTION = 'CHIP-EIGHT EMULATOR'
WIDTH = 64
HEIGHT = 32
SCALE = 10
COLOR_OFF = pygame.Color(0, 0, 0, 255)
COLOR_ON = pygame.Color(255, 255, 255, 255)


class Engine:
    def __init__(self):
        print('Engine initiation')
        pygame.init()
        pygame.time.set_timer(TIMER, DELAY)

    def handle_time(self, delay=1):
        pygame.time.wait(delay)

    def check_events(self, chip_eight):
        for event in pygame.event.get():
            if event.type == TIMER:
                chip_eight.handle_timers()
            if event.type == pygame.KEYDOWN:
                chip_eight.handle_key(event.key, 1)
            if event.type == pygame.KEYUP:
                chip_eight.handle_key(event.key, 0)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


class Graphics:
    def __init__(self, width=WIDTH*SCALE, height=HEIGHT*SCALE):
        print('Graphics initiation')
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(CAPTION)
        self.clear()

    def update(self):
        pygame.display.flip()

    def clear(self):
        self.screen.fill(COLOR_OFF)
        self.update()

    def draw(self, sprite):
        col, row = 0, 0
        for i in range(len(sprite)):
            col = (i % WIDTH) * SCALE
            row = int(i / WIDTH) * SCALE
            if sprite[i] == 1:
                pygame.draw.rect(self.screen, COLOR_ON, (col, row, SCALE, SCALE))
            else:
                pygame.draw.rect(self.screen, COLOR_OFF, (col, row, SCALE, SCALE))
        self.update()


class Sound:
    def __init__(self):
        print('Sound initiation')

    def play(self):
        print('@##$%^* SOUND @#$%^&')
