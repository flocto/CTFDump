# To ensure correctly formatted answers for the challenge, use 1-indexed values for the output bits.
# For example, if you have an S-Box of 8 bits to 8 bits, the first output bit is 1, the second is 2, and so forth.
# Your ANF expression will have the variables y1, y2, ..., y8.

# Put your S-Boxes here.

example = [0, 1, 0, 0, 0, 1, 1, 1]
example = list(map(int, '10001110'))

sbox1 = [1, 45, 226, 147, 190, 69, 21, 174, 120, 3, 135, 164, 184, 56, 207, 63, 8, 103, 9, 148, 235, 38, 168, 107, 189, 24, 52, 27, 187, 191, 114, 247, 64, 53, 72, 156, 81, 47, 59, 85, 227, 192, 159, 216, 211, 243, 141, 177, 255, 167, 62, 220, 134, 119, 215, 166, 17, 251, 244, 186, 146, 145, 100, 131, 241, 51, 239, 218, 44, 181, 178, 43, 136, 209, 153, 203, 140, 132, 29, 20, 129, 151, 113, 202, 95, 163, 139, 87, 60, 130, 196, 82, 92, 28, 232, 160, 4, 180, 133, 74, 246, 19, 84, 182, 223, 12, 26, 142, 222, 224, 57, 252, 32, 155, 36, 78, 169, 152, 158, 171, 242, 96, 208, 108, 234, 250, 199, 217, 0, 212, 31, 110, 67, 188, 236, 83, 137, 254, 122, 93, 73, 201, 50, 194, 249, 154, 248, 109, 22, 219, 89, 150, 68, 233, 205, 230, 70, 66, 143, 10, 193, 204, 185, 101, 176, 210, 198, 172, 30, 65, 98, 41, 46, 14, 116, 80, 2, 90, 195, 37, 123, 138, 42, 91, 240, 6, 13, 71, 111, 112, 157, 126, 16, 206, 18, 39, 213, 76, 79, 214, 121, 48, 104, 54, 117, 125, 228, 237, 128, 106, 144, 55, 162, 94, 118, 170, 197, 127, 61, 175, 165, 229, 25, 97, 253, 77, 124, 183, 11, 238, 173, 75, 34, 245, 231, 115, 35, 33, 200, 5, 225, 102, 221, 179, 88, 105, 99, 86, 15, 161, 49, 149, 23, 7, 58, 40]
sbox2 = [152, 158, 42, 231, 197, 251, 250, 79, 39, 1, 96, 57, 146, 137, 178, 133, 170, 32, 212, 154, 73, 97, 78, 7, 204, 218, 9, 195, 88, 149, 71, 235, 199, 247, 211, 124, 33, 0, 219, 185, 77, 2, 81, 201, 164, 224, 76, 102, 69, 198, 181, 20, 28, 210, 147, 115, 226, 180, 80, 189, 150, 46, 166, 171, 248, 37, 227, 21, 13, 63, 228, 216, 191, 143, 103, 40, 184, 121, 246, 207, 61, 26, 98, 249, 174, 156, 155, 10, 176, 44, 123, 114, 100, 240, 70, 130, 188, 104, 252, 126, 15, 131, 239, 234, 122, 229, 134, 214, 31, 8, 127, 236, 65, 208, 255, 128, 93, 190, 83, 135, 47, 183, 22, 173, 112, 241, 106, 186, 53, 49, 193, 64, 237, 36, 16, 153, 94, 92, 165, 203, 116, 144, 12, 138, 172, 177, 5, 202, 215, 56, 66, 117, 132, 142, 59, 209, 17, 11, 27, 206, 151, 111, 162, 87, 225, 161, 159, 160, 244, 108, 67, 243, 253, 196, 140, 51, 107, 113, 84, 230, 118, 34, 220, 89, 6, 68, 213, 163, 58, 141, 221, 200, 54, 23, 182, 217, 14, 24, 222, 60, 62, 110, 38, 55, 74, 129, 50, 148, 72, 167, 136, 35, 30, 109, 205, 90, 238, 29, 194, 254, 41, 187, 85, 82, 101, 119, 192, 145, 157, 125, 223, 19, 4, 175, 45, 139, 232, 18, 86, 179, 95, 245, 91, 99, 105, 48, 120, 168, 3, 43, 233, 75, 25, 242, 52, 169]
sbox3 = [99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21, 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115, 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]

# 3 input bits: 000, 001, 010, 011, 100, 101, 110, 111
# Array indexes: 0    1    2    3    4    5    6    7
# f(x1,x2,x3):   0    1    0    0    0    1    1    1

# Customize the following settings to extract specific bits of specific S-Boxes and have a comfortable visualization of terms.

SYMBOL = 'x'
INPUT_BITS = 8
OUTPUT_BITS = 8
SBOX = sbox3
BIT = 6

# Ignore the functions, we've implemented this for you to save your time.
# Don't touch it, it might break and we don't want that, right? ;)

depend = set()

def get_sbox_result(input_int):
    return SBOX[input_int]

def get_term(binary_string):
    term = ""
    i = 1
    for (count,bit) in enumerate(binary_string):
        if bit == "1":
            term += SYMBOL+str(i)+"*"
            depend.add(SYMBOL+str(i))
        i += 1

    if term == "":
        return "1"

    return term[:-1]

def get_poly(inputs, outputs):
    poly = ""
    for v in inputs:
        if outputs[v]:
            poly += get_term(v) + "+"
    return poly[:-1]

def should_sum(u, v, n):
    for i in range(n):
        if u[i] > v[i]:
            return False

    return True

def get_as(vs, f, n):
    a = {}
    for v in vs:
        a[v] = 0
        for u in vs:
            if should_sum(u, v, n):
                a[v] ^= f[u]

    return a

def get_anf(vs, f, n):
    return get_poly(vs, get_as(vs, f, n))

def get_vs_and_fis_from_sbox(which_fi):
    vs = []
    fis = {}
    for input_integer in range(2**INPUT_BITS):
        sbox_output = get_sbox_result(input_integer)
        input_integer_binary = bin(input_integer)[2:].zfill(INPUT_BITS)
        fis[input_integer_binary] = 0
        sbox_output_binary = bin(sbox_output)[2:].zfill(OUTPUT_BITS)

        vs.append(input_integer_binary)
        fis[input_integer_binary] = int(sbox_output_binary[which_fi-1])

    return vs, fis

def get_anf_from_sbox_fi(which_fi):
    vs, fis = get_vs_and_fis_from_sbox(which_fi)
    poly = get_anf(vs, fis, INPUT_BITS)
    return poly

# output = get_anf_from_sbox_fi(BIT)
# print(output)
# print(','.join(sorted(list(depend))))

for i in range(1, 9):
    output = get_anf_from_sbox_fi(i)
    print(f'y{i} = {output}')
    print(','.join(sorted(list(depend))))
    depend.clear()
    print()