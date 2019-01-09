import sys
import pygame

WIDTH = 64
HEIGHT = 32
SCALE = 10
COLOR_OFF = pygame.Color(0, 0, 0, 255)
COLOR_ON = pygame.Color(255, 255, 255, 255)


class Graphics:
    def __init__(self, width=WIDTH*SCALE, height=HEIGHT*SCALE):
        print('Graphics initiation')
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('CHIP-EIGHT EMULATOR')
        self.clear()

    def update(self):
        pygame.display.flip()

    def clear(self):
        # print('Clearing...')
        self.screen.fill(COLOR_OFF)
        self.update()

    def draw(self, sprite=[]):
        # print('Drawing...')
        col, row = 0, 0
        for i in range(len(sprite)):
            col = (i % WIDTH) * SCALE
            row = int(i / WIDTH) * SCALE
            if sprite[i] == 1:
                if self.screen.get_at((col, row)) == COLOR_OFF:
                    pygame.draw.rect(self.screen, COLOR_ON, (col, row, SCALE, SCALE))
                else:
                    pygame.draw.rect(self.screen, COLOR_OFF, (col, row, SCALE, SCALE))
        self.update()


class Sound:
    def __init__(self):
        print('Sound initiation')

    def play(self):
        print('@##$%^* SOUND @#$%^&')


class Keyboard:
    def __init__(self):
        print('Keyboard initiation')

    def check_keys(self):
        # print('Checking keys...')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return event.key, 1
            if event.type == pygame.KEYUP:
                return event.key, 0
        return None, None
