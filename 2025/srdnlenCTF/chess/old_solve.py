from collections import defaultdict
from chess import Board, pgn
import chess
from Crypto.Util.number import bytes_to_long
from io import StringIO
from pwn import *
from z3 import *
set_option("parallel.enable", True)
# from cvc5.pythonic import *
from src.pseudorandom import XorShift128


def string_to_bits(s):
    binary_string = bin(bytes_to_long(s.encode()))[2:]
    padding_length = (8 - len(binary_string) % 8) % 8
    padded_binary_string = binary_string.zfill(len(binary_string) + padding_length)
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
        legal_possible_moves = [ legal_move for legal_move in legal_moves if legal_move[2:4] in possible_moves ]
        
        choice_outputs.append((legal_possible_moves.index(result_moves[i]), len(legal_possible_moves)))
        
        chosen_move = result_moves[i]
        chess_board.push(chess.Move.from_uci(chosen_move))

    return choice_outputs

def solve_xorshift128(outputs):
    s = Solver()

    state0 = BitVec('state0', 64)
    state1 = BitVec('state1', 64)

    for output, length in outputs:
        s1 = state0
        s0 = state1
        new_state0 = s0
        s1 ^= s1 << 23
        # s1 &= (1 << 64) - 1
        # s1 ^= s1 >> 17
        s1 ^= LShR(s1, 17)
        s1 ^= s0
        # s1 ^= s0 >> 26
        s1 ^= LShR(s0, 26)
        new_state1 = s1

        # new_state0 = new_state0 & 0xFFFFFFFFFFFFFFFF
        # new_state1 = new_state1 & 0xFFFFFFFFFFFFFFFF

        next_value = new_state0 + new_state1
        # s.add(next_value % length == output)
        # always mod 4, so just extract both 2 bits
        s.add(next_value & 0b11 == output)

        state0 = new_state0
        state1 = new_state1

    if s.check() == sat:
        model = s.model()
        return model[BitVec('state0', 64)], model[BitVec('state1', 64)]
    else:
        return None

# r = remote('chess.challs.srdnlen.it', 4012)
r = process(['python3', 'main.py'])

pgns = []
for i in range(64 * 8):
    r.recvuntil(b'Enter your choice (1/2/3/4): ')
    r.sendline(b'1')
    r.recvuntil(b'Enter the string to encode (max 300 characters): ')
    r.sendline(b'r')
    r.recvuntil(b'[Result "*"]\n\n')
    pgns.append(r.recvline().decode())

choice_outputs = []
for pgn in pgns:
    game = chess.pgn.read_game(StringIO(pgn))
    board = game.board()
    moves = []
    for move in game.mainline_moves():
        moves.append(str(move))
        board.push(move)
    choice_outputs.extend(get_prng_outputs("r", moves))

print(choice_outputs)
state0, state1 = solve_xorshift128(choice_outputs)
print(state0, state1)
prng = XorShift128(state0.as_long(), state1.as_long())

for output, length in choice_outputs:
    assert output == prng.choice(range(length))

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
    "Wei Yi", "Alireza Firouzja" , "Vladislav Artemiev", "Dmitry Andreikin", 
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
    r.sendline(output)
r.interactive()