from modules.sets import chip_fontset, chip_keys
from random import randint


class ChipEight:
    def __init__(self):
        print('Chip-8 initiation')
        # 35 operation codes
        self.opcode = 0
        # 4096B memory size
        self.memory = [0]*4096
        # 15 registers of 8b + 1 to 'carry flag'
        self.V = [0]*16
        # Index register
        self.I = 0
        # Program counter (starts at 512)
        self.pc = 0x200
        # Graphics (64 * 32 pixels)
        self.gfx = [0]*64*32
        # Timers
        self.delay_timer = 0
        self.sound_timer = 0
        # Stack (16 levels)
        self.stack = [0]*16
        # Stack pointer
        self.sp = 0
        # Keyboard state (HEX = 16b)
        self.keyboard = [0]*16
        # Draw flag
        self.draw = False
        # Clear flag
        self.clear = False
        # Load fontset
        for i in range(80):
            self.memory[i] = chip_fontset[i]

    def load_rom(self, name, data):
        for i in range(len(data)):
            self.memory[i+512] = data[i]
        print(f'Loaded ROM: {name}')

    def emulate_cycle(self):
        # Fetch opcode
        self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc+1]
        opcode_msb = self.opcode & 0xF000
        hex_opcode = '{:04x}'.format(self.opcode).upper()
        print(f'Fetched opcode: {hex_opcode}', end=' | ')

        # Decode and execute opcode
        if opcode_msb == 0x0:
            if self.opcode == 0xE0:
                self.gfx = [0]*64*32
                self.clear = True
                self.pc += 2
                print('00E0')
            elif self.opcode == 0xEE:
                self.sp -= 1
                self.pc = self.stack[self.sp]
                self.pc += 2
                print('00EE')
            else:
                # not used, ignored
                print('0NNN')
        elif opcode_msb == 0x1000:
            self.pc = self.opcode & 0x0FFF
            print('1NNN')
        elif opcode_msb == 0x2000:
            self.stack[self.sp] = self.pc
            self.sp += 1
            self.pc = self.opcode & 0x0FFF
            print('2NNN')
        elif opcode_msb == 0x3000:
            if self.V[(self.opcode & 0x0F00) >> 8] == (self.opcode & 0x00FF):
                self.pc += 2
            self.pc += 2
            print('3XNN')
        elif opcode_msb == 0x4000:
            if self.V[(self.opcode & 0x0F00) >> 8] != (self.opcode & 0x00FF):
                self.pc += 2
            self.pc += 2
            print('4XNN')
        elif opcode_msb == 0x5000:
            if self.V[(self.opcode & 0x0F00) >> 8] == self.V[(self.opcode & 0x00F0) >> 4]:
                self.pc += 2
            self.pc += 2
            print('5XY0')
        elif opcode_msb == 0x6000:
            self.V[(self.opcode & 0x0F00) >> 8] = self.opcode & 0x00FF
            self.pc += 2
            print('6XNN')
        elif opcode_msb == 0x7000:
            self.V[(self.opcode & 0x0F00) >> 8] += self.opcode & 0x00FF
            self.pc += 2
            print('7XNN')
        elif opcode_msb == 0x8000:
            opcode_lsb = self.opcode & 0x000F
            if opcode_lsb == 0x00:
                self.V[(self.opcode & 0x0F00) >> 8] = self.V[(self.opcode & 0x00F0) >> 4]
                self.pc += 2
                print('8XY0')
            elif opcode_lsb == 0x01:
                self.V[(self.opcode & 0x0F00) >> 8] |= self.V[(self.opcode & 0x00F0) >> 4]
                self.pc += 2
                print('8XY1')
            elif opcode_lsb == 0x02:
                self.V[(self.opcode & 0x0F00) >> 8] &= self.V[(self.opcode & 0x00F0) >> 4]
                self.pc += 2
                print('8XY2')
            elif opcode_lsb == 0x03:
                self.V[(self.opcode & 0x0F00) >> 8] ^= self.V[(self.opcode & 0x00F0) >> 4]
                self.pc += 2
                print('8XY3')
            elif opcode_lsb == 0x04:
                if self.V[(self.opcode & 0x00F0) >> 4] + self.V[(self.opcode & 0x0F00) >> 8] > 0xFF:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0
                self.V[(self.opcode & 0x0F00) >> 8] += self.V[(self.opcode & 0x00F0) >> 4]
                self.pc += 2
                print('8XY4')
            elif opcode_lsb == 0x05:
                if self.V[(self.opcode & 0x00F0) >> 4] > self.V[(self.opcode & 0x0F00) >> 8]:
                    self.V[0xF] = 0
                else:
                    self.V[0xF] = 1
                self.V[(self.opcode & 0x0F00) >> 8] -= self.V[(self.opcode & 0x00F0) >> 4]
                self.pc += 2
                print('8XY5')
            elif opcode_lsb == 0x06:
                self.V[0xF] = self.V[(self.opcode & 0x0F00) >> 8] & 0x1
                self.V[(self.opcode & 0x0F00) >> 8] >>= 1
                self.pc += 2
                print('8XY6')
            elif opcode_lsb == 0x07:
                if self.V[(self.opcode & 0x0F00) >> 8] > self.V[(self.opcode & 0x00F0) >> 4]:
                    self.V[0xF] = 0
                else:
                    self.V[0xF] = 1
                self.V[(self.opcode & 0x0F00) >> 8] = self.V[(self.opcode & 0x00F0) >> 4] - self.V[(self.opcode & 0x0F00) >> 8]
                self.pc += 2
                print('8XY7')
            elif opcode_lsb == 0x0E:
                self.V[0xF] = self.V[(self.opcode & 0x0F00) >> 8] >> 7
                self.V[(self.opcode & 0x0F00) >> 8] <<= 1
                self.pc += 2
                print('8XYE')
            else:
                print('Unknown!')
        elif opcode_msb == 0x9000:
            if self.V[(self.opcode & 0x0F00) >> 8] != self.V[(self.opcode & 0x00F0) >> 4]:
                self.pc += 2
            self.pc += 2
            print('9XY0')
        elif opcode_msb == 0xA000:
            self.I = self.opcode & 0x0FFF
            self.pc += 2
            print('ANNN')
        elif opcode_msb == 0xB000:
            self.pc = (self.opcode & 0x0FFF) + self.V[0]
            print('BNNN')
        elif opcode_msb == 0xC000:
            self.V[(self.opcode & 0x0F00) >> 8] = self.opcode & 0x00FF & randint(0, 255)
            self.pc += 2
            print('CXNN')
        elif opcode_msb == 0xD000:
            x = self.V[(self.opcode & 0x0F00) >> 8]
            y = self.V[(self.opcode & 0x00F0) >> 4]
            self.V[0xF] = 0
            for row in range(self.opcode & 0x000F):
                for col in range(8):
                    if (self.memory[self.I + row] & (0x80 >> col)) != 0:
                        i = x + col + ((y + row) * 64)
                        if len(self.gfx) > i:
                            if self.gfx[i] == 1:
                                self.V[0xF] = 1
                            self.gfx[i] ^= 1
            self.draw = True
            self.pc += 2
            print('DXYN')
        elif opcode_msb == 0xE000:
            opcode_2lsb = self.opcode & 0x00FF
            if opcode_2lsb == 0x9E:
                if self.keyboard[self.V[(self.opcode & 0x0F00) >> 8]] != 0:
                    self.pc += 2
                self.pc += 2
                print('EX9E')
            elif opcode_2lsb == 0xA1:
                if self.keyboard[self.V[(self.opcode & 0x0F00) >> 8]] == 0:
                    self.pc += 2
                self.pc += 2
                print('EXA1')
            else:
                print('Unknown!')
        elif opcode_msb == 0xF000:
            opcode_2lsb = self.opcode & 0x00FF
            if opcode_2lsb == 0x07:
                self.V[(self.opcode & 0x0F00) >> 8] = self.delay_timer
                self.pc += 2
                print('FX07')
            elif opcode_2lsb == 0x0A:
                key_pressed = False
                for i in range(len(self.keyboard)):
                    if self.keyboard[i] != 0:
                        self.V[(self.opcode & 0x0F00) >> 8] = i
                        key_pressed = True
                if key_pressed:
                    self.pc += 2
                print('FX0A')
            elif opcode_2lsb == 0x15:
                self.delay_timer = self.V[(self.opcode & 0x0F00) >> 8]
                self.pc += 2
                print('FX15')
            elif opcode_2lsb == 0x18:
                self.sound_timer = self.V[(self.opcode & 0x0F00) >> 8]
                self.pc += 2
                print('FX18')
            elif opcode_2lsb == 0x1E:
                if self.I + self.V[(self.opcode & 0x0F00) >> 8] > 0xFFF:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0
                self.I += self.V[(self.opcode & 0x0F00) >> 8]
                self.pc += 2
                print('FX1E')
            elif opcode_2lsb == 0x29:
                self.I = self.V[(self.opcode & 0x0F00) >> 8] * 0x5
                self.pc += 2
                print('FX29')
            elif opcode_2lsb == 0x33:
                self.memory[self.I] = int(self.V[(self.opcode & 0x0F00) >> 8] / 100)
                self.memory[self.I+1] = int(self.V[(self.opcode & 0x0F00) >> 8] / 10) % 10
                self.memory[self.I+2] = (self.V[(self.opcode & 0x0F00) >> 8] % 100) % 10
                self.pc += 2
                print('FX33')
            elif opcode_2lsb == 0x55:
                for i in range(((self.opcode & 0x0F00) >> 8) + 1):
                    self.memory[self.I + i] = self.V[i]
                self.pc += 2
                print('FX55')
            elif opcode_2lsb == 0x65:
                for i in range(((self.opcode & 0x0F00) >> 8) + 1):
                    self.V[i] = self.memory[self.I + i]
                self.pc += 2
                print('FX65')
            else:
                print('Unknown!')
        else:
            print('Unknown!')

        # Update timers
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1

    def handle_key(self, key, value):
        if key in chip_keys:
            self.keyboard[chip_keys.index(key)] = value
