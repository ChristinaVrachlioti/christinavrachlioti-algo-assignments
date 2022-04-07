import math
from sys import argv
import hashlib

# Class of bit-array (allows us to handle bits and does the placing for us)
class BitArray:

    def __init__(self):

        # Create the array of bytes
        self.array = bytearray()

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
        shifts = 7-(self.bits%8)

        # Construct the new bitmask for the bit that is provided
        bitmask = bit << shifts

        # Add it to the last byte
        self.array[-1] = self.array[-1] | bitmask

        # Accumulate the number of bits
        self.bits += 1

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

    # Check that exactly one argument is provided
    if len(argv) < 2:
        print("You need to specify a filename")
        return

    # Try to open the file for reading 
    try:
        file = open(argv[1],'r')
        filecontents = file.read()
        file.close()
    except:
        print("Sorry, the file could not be read")
        return

    # Turn the numbers into a list
    num_list = []
    for num in filecontents.split():
        num_list.append(int(num))
    
    # Find the biggest number
    big = num_list[-1]

    # Find the number of tail bits
    l = math.floor(math.log2(big/len(num_list)))
    print("l",l)

    # Create the mask that will get the number tails
    tail_mask = 0
    for i in range(l):
        tail_mask = (tail_mask << 1)+1

    # Construct the L bit array and fill it with the ends of numbers
    # Simulteaneously transform the numbers for the next operation
    L = BitArray()
    for i in range(len(num_list)):

        # Get the part you need
        num_tail = num_list[i] & tail_mask

        # Shrink the number
        num_list[i] = num_list[i] >> l

        # Add the tail to the bitlist
        L.add_number(num_tail,l)

    # Construct the U bit list with the number differences
    U = BitArray()
    last = 0
    for i in range(len(num_list)):

        # Get the number difference
        diff = num_list[i]-last
        last = num_list[i]

        # Add 0 bits as many times as needed
        for j in range(diff):
            U.add_bit(0)

        # Add the final 1 bit
        U.add_bit(1)

    # Display the contents of each list
    print("L")
    L.print_bitlist()
    print("U")
    U.print_bitlist()

    # Print the hash value
    m = hashlib.sha256()
    m.update(L.array)
    m.update(U.array)
    digest = m.hexdigest()
    print(digest)



if __name__ == "__main__":
    
    # Run the main method
    main()