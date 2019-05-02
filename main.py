import numpy as np

from modules.chip import ChipEight
from modules.additional import Engine, Graphics, Sound


def initChipEight(rom_name):
    chip_eight = ChipEight()
    with open(f'./roms/{rom_name}', 'rb') as f:
        chip_eight.load_rom(rom_name, np.fromfile(f, dtype=np.uint8))
    return chip_eight


def main(rom_name):
    print('# CHIP-EIGHT EMULATOR #')

    # Init additional
    engine = Engine()
    graphics = Graphics()
    sound = Sound()

    # Init Chip-8
    chip_eight = initChipEight(rom_name)

    # Emulation loop
    while True:
        engine.handle_time()
        chip_eight.handle_opcode()

        if chip_eight.draw:
            graphics.draw(chip_eight.gfx)
            chip_eight.draw = False
        elif chip_eight.clear:
            graphics.clear()
            chip_eight.clear = False

        if chip_eight.sound_timer != 0:
            sound.play()

        engine.check_events(chip_eight)
        chip_eight.handle_timers()


main('BRIX')
