import time
import numpy as np

from modules.chip import ChipEight
from modules.additional import Graphics, Sound, Keyboard


def initChipEight(rom_name):
    chip_eight = ChipEight()
    with open(f'./roms/{rom_name}', 'rb') as f:
        chip_eight.load_rom(rom_name, np.fromfile(f, dtype=np.uint8))
    return chip_eight


def main(rom_name):
    print('# CHIP-EIGHT EMULATOR #')

    # Init additional
    graphics = Graphics()
    keyboard = Keyboard()
    sound = Sound()

    # Init Chip-8
    chip_eight = initChipEight(rom_name)

    # Emulation loop
    while True:
        chip_eight.emulate_cycle()

        if chip_eight.draw:
            graphics.draw(chip_eight.gfx)
            chip_eight.draw = False

        if chip_eight.clear:
            graphics.clear()
            chip_eight.clear = False

        if chip_eight.sound_timer != 0:
            sound.play()

        key, value = keyboard.check_keys()
        if key != None:
            chip_eight.handle_key(key, value)

        time.sleep(1/60)


main('PONG')
