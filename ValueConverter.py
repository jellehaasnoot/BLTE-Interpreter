# A code to transfer values between different
import time
import math


class ValueConverter:
    """This class will be used to convert values in different systems, like binary to decimal."""
    def __init__(self):
        pass

    def hex_to_number(self, hex):
        """This will convert the hex value to decimal values, it will produce it digit by digit. So if the input is
        '1C' it will give the list [1, 12]. Because  C in hex will be 12 in decimal. This will be used to use other
        functions in this class"""
        self.hex_raw = hex
        hex_split = list(self.hex_raw)
        for i in range(len(hex_split)):
            if hex_split[i] == 'A':
                hex_split[i] = 10
            elif hex_split[i] == 'B':
                hex_split[i] = 11
            elif hex_split[i] == 'C':
                hex_split[i] = 12
            elif hex_split[i] == 'D':
                hex_split[i] = 13
            elif hex_split[i] == 'E':
                hex_split[i] = 14
            elif hex_split[i] == 'F':
                hex_split[i] = 15
            elif hex_split[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                hex_split[i] = int(hex_split[i])
            else:
                print('No valid input, Try again!')
                time.sleep(1000)
        self.hex = hex_split

    def hex_to_bin(self, hex):
        self.hex_to_number(hex)
        self.binary = []
        for i in range(len(self.hex)):
            if self.hex[i] >= 8:
                self.hex[i] -= 8
                self.binary.append(1)
            else:
                self.binary.append(0)

            if self.hex[i] >= 4:
                self.hex[i] -= 4
                self.binary.append(1)
            else:
                self.binary.append(0)

            if self.hex[i] >= 2:
                self.hex[i] -= 2
                self.binary.append(1)
            else:
                self.binary.append(0)

            if self.hex[i] >= 1:
                self.hex[i] -= 1
                self.binary.append(1)
            else:
                self.binary.append(0)

        return self.binary

    def bin_to_dec(self, bin_number):
        self.bin_number = list(reversed(bin_number))
        self.dec_number = 0
        for i in range(len(self.bin_number)):
             self.dec_number += 2**i * self.bin_number[i]

        return self.dec_number

