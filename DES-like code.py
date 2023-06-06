"""
Giovanny Joseph
This program preforms a simplified DES-type algorithm that implements a product cipher with 5 rounds
"""


class DES:
    def __init__(self, input_bytes: int, master_key: int):
        self.ib = input_bytes
        self.mk = master_key
        # s-boxes
        self.sb1 = ((0b101, 0b010, 0b001, 0b110, 0b011, 0b100, 0b111, 0b000),
                    (0b001, 0b100, 0b110, 0b010, 0b000, 0b111, 0b101, 0b011))
        self.sb2 = ((0b100, 0b000, 0b110, 0b101, 0b111, 0b001, 0b011, 0b010),
                    (0b101, 0b011, 0b000, 0b111, 0b110, 0b010, 0b001, 0b100))

    @staticmethod
    def expander(bytes):
        # store middle bytes to append later
        middle_bytes = (bytes >> 2) & 0b11

        # flip middle bytes
        first_middle = (middle_bytes >> 1) & 0b1
        second_middle = middle_bytes & 0b1
        flipped_middle_bytes = ((0b0 | second_middle) << 1) | first_middle

        # store last 2 bytes
        last_2_bytes = bytes & 0b11

        # take out last 4 bytes and allow 2 more to be added
        extended = bytes >> 4 << 2

        # set last two bytes to the middle, shift to allow two more bytes
        extended = (extended | flipped_middle_bytes) << 2
        extended = (extended | flipped_middle_bytes) << 2

        # return with the last two bytes added back
        return extended | last_2_bytes

    def sub_key(self, rnd):
        # index 1 -> 8
        if rnd == 1:
            return self.mk >> 0b1
        # index 2 -> 9
        elif rnd == 2:
            return self.mk & 0b11111111
        # index 3 -> 9 + 1 bits of master key
        elif rnd == 3:
            return ((self.mk & 0b1111111) << 1) | self.mk >> 8
        # index 4 -> 9 + 2 bits of master key
        elif rnd == 4:
            return ((self.mk & 0b111111) << 2) | self.mk >> 7
        # index 5 -> 9 + 3 bits of master key
        elif rnd == 5:
            return ((self.mk & 0b11111) << 3) | self.mk >> 6

    @staticmethod
    def sbox_results(bits, sbox):
        # most significant bit is the first one which gives us the row
        msb = (bits >> 3) & 0b1
        # last 3 bits are the column
        last_bits = bits & 0b111
        # return them as index of the sbox
        return sbox[msb][last_bits]

    def f_function(self, R0, rnd):
        # extend the bytes to have 8
        R_extended = self.expander(R0)

        # XOR with key
        R_XOR = R_extended ^ self.sub_key(rnd)

        # split R_XOR by 4 bits each side and compare to sboxes
        R_first_4 = R_XOR >> 4
        R_last_4 = R_XOR & 0b1111

        # take comparison from sbox and slap together should be 3 bits
        new_first_3 = self.sbox_results(R_first_4, self.sb1)
        new_last_3 = self.sbox_results(R_last_4, self.sb2)

        # return value combined should be 6 bits
        return (new_first_3 << 3) | new_last_3

    def round(self, x, rnd):
        # get L0 and R0
        L0 = x >> 6
        R0 = x & 0b111111

        # put right side through function
        # xor with left side to get R1
        R1 = self.f_function(R0, rnd) ^ L0

        # R0 is now L1
        L1 = R0

        # combine values to get new number
        return (L1 << 6) | R1

    def encrypt(self):
        # encrypt the plain text in 5 rounds
        for i in range(5):
            self.ib = self.round(self.ib, i + 1)

        # print(hex(self.ib))
        return self.ib

def test():
    des_like = DES(0x726, 0x99)
    # testing if all the functions give desired outputs
    assert des_like.expander(0b110011) == 0b11000011
    assert des_like.sbox_results(0b1001, des_like.sb1) == 0b100
    assert des_like.sbox_results(0b1001, des_like.sb2) == 0b011
    assert des_like.sub_key(4) == 0b01100101
    assert des_like.encrypt() == 0x3f8

    return des_like.ib


if __name__ == "__main__":
    result = DES(0x726, 0x99).encrypt()
 
    if test():
        print(hex(result))


