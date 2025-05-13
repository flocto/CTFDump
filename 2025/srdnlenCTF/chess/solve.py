from sage.all import GF, Matrix, vector
from collections import defaultdict
from chess import Board, pgn
import chess
from Crypto.Util.number import bytes_to_long
from io import StringIO
from pwn import *
from tqdm import trange
from src.pseudorandom import XorShift128


def string_to_bits(s):
    binary_string = bin(bytes_to_long(s.encode()))[2:]
    padding_length = (8 - len(binary_string) % 8) % 8
    padded_binary_string = binary_string.zfill(
        len(binary_string) + padding_length)
    return padded_binary_string


dic_tile_to_bits = {
    f"{chr(col + ord('a'))}{8 - row}": f"{row % 2}{col % 2}"
    for row in range(8)
    for col in range(8)
}

dic_bits_to_tile = defaultdict(list)
for k, v in dic_tile_to_bits.items():
    dic_bits_to_tile[v].append(k)
dic_bits_to_tile = dict(dic_bits_to_tile)


def get_prng_outputs(string_to_encode, result_moves):
    choice_outputs = []
    chess_board = Board()
    bits_to_encode = string_to_bits(string_to_encode)

    for i in range(len(bits_to_encode) // 2):
        current_2bits = bits_to_encode[i * 2:i * 2 + 2]

        legal_moves = list(str(k) for k in chess_board.generate_legal_moves())
        possible_moves = dic_bits_to_tile[current_2bits]
        legal_possible_moves = [
            legal_move for legal_move in legal_moves if legal_move[2:4] in possible_moves]

        # choice_outputs.append((legal_possible_moves.index(result_moves[i]), len(legal_possible_moves)))
        choice_outputs.append(legal_possible_moves.index(result_moves[i]))

        chosen_move = result_moves[i]
        chess_board.push(chess.Move.from_uci(chosen_move))

    return choice_outputs


class BV:
    def __init__(self, data):
        # data is 64-long list of 128 bit ints
        # data[0] is a 128 bit int indicating the mask of bits in s0s1
        #   which are xor-ed together to generate the 0th (LSB) bit of
        #   this state
        # Low 64 bits of s0s1 come from s0, high 64 bits come from s1
        assert (len(data) == 64)
        self.data = data

    def __xor__(self, other):
        return BV([i ^ j for i, j in zip(self.data, other.data)])

    def __lshift__(self, other):
        # After left shift the least significant bits of the state
        # should be empty
        return BV([0] * other + self.data[:-other])

    def __rshift__(self, other):
        # After right shift the most significant bits of the state
        # should be empty
        return BV(self.data[other:] + [0] * other)

    def coef(self, pos):
        # Converts 128 bit mask into list of ints
        coef = f"{self.data[pos]:0128b}"
        coef = [int(i) for i in coef[::-1]]
        return coef

    def eval_one(self, s0s1, pos):
        # From a known s0s1, evalute the bit at one position
        val = sum([i * j for i, j in zip(self.coef(pos), s0s1)]) % 2
        return val

    def eval_all(self, s0s1):
        # From a known s0s1, evalute the bit at all positions and get
        # the u64 output
        vals = [self.eval_one(s0s1, pos) for pos in range(64)]
        vals = "".join([str(i) for i in vals[::-1]])
        vals = int(vals, 2)
        return vals


def xs128p(state0, state1):
    s1 = state0
    s0 = state1

    s1 = s1 ^ (s1 << 23)
    s1 = s1 ^ (s1 >> 17)
    s1 = s1 ^ s0
    s1 = s1 ^ (s0 >> 26)

    state0 = state1
    state1 = s1
    output_state = state0 ^ state1

    return state0, state1, output_state


# Initial symbolic values of s0 and s1
BV.s0 = BV([1 << i for i in range(64)])
BV.s1 = BV([1 << i for i in range(64, 128)])

# r = remote('chess.challs.srdnlen.it', 4012)
r = process(['python3', 'main.py'])

pgns = []
n = 128
for i in trange(n):
    r.recvuntil(b'Enter your choice (1/2/3/4): ')
    r.sendline(b'1')
    r.recvuntil(b'Enter the string to encode (max 300 characters): ')
    r.sendline(b'r')
    r.recvuntil(b'[Result "*"]\n\n')
    pgns.append(r.recvline().decode())

choice_outputs = []
for _pgn in pgns:
    game = chess.pgn.read_game(StringIO(_pgn))
    board = game.board()
    moves = []
    for move in game.mainline_moves():
        moves.append(str(move))
        board.push(move)
    choice_outputs.extend(get_prng_outputs("r", moves))

# print(choice_outputs)

s0, s1 = BV.s0, BV.s1
prng_states = []
for _ in range(n):
    s0, s1, output_state = xs128p(s0, s1)
    prng_states.append(output_state)

mat = []
vec = []
for prng_state, output in zip(prng_states, choice_outputs):
    # we use 1 bit output instead of 2
    # print(prng_state.coef(0), prng_state.coef(1))
    # for idx, bit in enumerate(bin(output)[2:].zfill(2)):
    #     mat.append(prng_state.coef(63 - idx))
    #     vec.append(int(bit))
    mat.append(prng_state.coef(0))
    vec.append(output)

F = GF(2)
mat = Matrix(F, mat)
vec = vector(F, vec)

s0s1 = mat.solve_right(vec)
# print(s0s1)

s0 = s0s1[:64]
s1 = s0s1[64:]
s0 = int("".join([str(i) for i in s0])[::-1], 2)
s1 = int("".join([str(i) for i in s1])[::-1], 2)

prng = XorShift128(s0, s1)
for out in choice_outputs:
    assert (out == prng.next() % 4)

players = [
    "Magnus Carlsen", "Hikaru Nakamura", "Garry Kasparov", "Bobby Fischer",
    "Viswanathan Anand", "Vladimir Kramnik", "Fabiano Caruana", "Ding Liren",
    "Ian Nepomniachtchi", "Anatoly Karpov", "Mikhail Tal", "Alexander Alekhine",
    "Jose Raul Capablanca", "Paul Morphy", "Judith Polgar", "Wesley So",
    "Levon Aronian", "Maxime Vachier-Lagrave", "Sergey Karjakin", "Shakhriyar Mamedyarov",
    "Teimour Radjabov", "Boris Spassky", "Tigran Petrosian", "Veselin Topalov",
    "Peter Svidler", "Anish Giri", "Richard Rapport", "Jan-Krzysztof Duda",
    "Viktor Korchnoi", "Bent Larsen", "David Bronstein", "Samuel Reshevsky",
    "Efim Geller", "Mikhail Botvinnik", "Alexander Grischuk", "Vassily Ivanchuk",
    "Nigel Short", "Michael Adams", "Gata Kamsky", "Ruslan Ponomariov",
    "Vladimir Akopian", "Peter Leko", "Evgeny Bareev", "Alexei Shirov",
    "Vladimir Malakhov", "Boris Gelfand", "Vladimir Fedoseev", "Daniil Dubov",
    "Wei Yi", "Alireza Firouzja", "Vladislav Artemiev", "Dmitry Andreikin",
    "Radoslaw Wojtaszek", "Leinier Dominguez", "Pentala Harikrishna", "Sergey Movsesian",
    "Ernesto Inarkiev", "David Navara", "Vladislav Kovalev", "Jorden Van Foreest",
    "Nihal Sarin", "Vincent Keymer", "Awonder Liang", "Jeffery Xiong",
    "Praggnanandhaa Rameshbabu", "Raunak Sadhwani"
]

trivia_outputs = []
for i in range(50):
    trivia_outputs.append(players[prng.choice(range(66))])

r.recvuntil(b'Enter your choice (1/2/3/4): ')
r.sendline(b'3')
for output in trivia_outputs:
    r.recvuntil(b'Which chess player am I thinking of?\n')
    r.sendline(output.encode())

print(r.recvline_contains(b'Here is the flag').decode())
