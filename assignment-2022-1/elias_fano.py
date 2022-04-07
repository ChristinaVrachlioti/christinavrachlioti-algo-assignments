import math
from sys import argv
import hashlib

# Class of bit-array (allows us to handle bits and does the placing for us)
class BitArray:

    def __init__(self):

        # Create the array of bytes
        self.array = []

        # Setup counters for bits and bytes
        self.bytes = 0
        self.bits = 0

    def add_number(self, number, bits):
        # Adds a number consisting of specific number of bits to the array

        for i in range(bits):
            
            # Get the number bit
            thebit = (number >> (bits-i-1))&1

            # Add it to the array
            self.add_bit(thebit)

        pass

        

    def add_bit(self,bit):

        # This will add a bit to the array
        if self.bits // 8 == self.bits / 8:
            # If that is so you need to create a new byte
            self.array.append(0)
            self.bytes+=1

        # Get the number of shifts for the new bit
        shifts = 7-self.bits%8

        # Construct the new bitmask for the bit that is provided
        bitmask = bit << shifts

        # Add it to the last byte
        self.array[-1] = self.array[-1] | bitmask

    def print_bitlist(self):
        # This will print all the numbers on the list

        for byte in self.array:
            # Print every byte

            for i in range(8):
                # Do it for every bit

                # Get the appropriate bit
                thebit = (byte >> (7-i)) & 1

                # Print it out
                print(thebit,end = '')

            # Print a newline after every byte
            print("")



def main():
    # The main method

    print(argv)

    pass



if __name__ == "__main__":
    
    # Run the main method
    main()