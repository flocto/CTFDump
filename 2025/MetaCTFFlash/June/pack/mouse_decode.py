#!/usr/bin/env python3
import argparse
from draw import draw_movement


def to_signed_int(n, bitlength):
    if n >= 2 ** (bitlength - 1):
        n -= 2 ** bitlength
    return n


def decode_line(line, bit_lengths):
    nbytes = sum(bit_lengths) // 8
    n = int.from_bytes(line[:nbytes], byteorder='little')

    click = n & (2**bit_lengths[0] - 1)
    n >>= bit_lengths[0]

    x_displacement = to_signed_int(n & (2**bit_lengths[1] - 1), bit_lengths[1])
    n >>= bit_lengths[1]

    y_displacement = to_signed_int(n, bit_lengths[2])

    return click, x_displacement, y_displacement


def decode_mouse_data(raw_data, bit_lengths, offset=0, absolute=False):
    mouse_data = [
        bytes.fromhex(''.join(d.strip().split(':')))[offset:]
        for d in raw_data.split('\n') if d
    ]

    clicks, xs, ys = [], [0], [0]
    for line in mouse_data:
        click, new_x, new_y = decode_line(line, bit_lengths)
        clicks.append(click)

        if not absolute:
            # Relative coordinates
            new_x += xs[-1]
            new_y = ys[-1] - new_y

        xs.append(new_x)
        ys.append(new_y)

    return clicks, xs[1:], ys[1:]


def parse_args():
    parser = argparse.ArgumentParser(
        description='Visualize USB Mouse data',
        epilog='Keyboard commands:\n  <SPACE>: pause/resume animation\n  c: clear screen during animation\n  q: quit', 
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('file', type=argparse.FileType('r'), help='mouse data file')
    parser.add_argument('--offset', type=int, default=0, help='byte offset of data (default: %(default)s)')
    parser.add_argument('-b', '--bit-lengths', type=int, choices=[8, 12, 16], default=[8, 8, 8], nargs='+', help='bit lengths of each data field [click, x, y] (default: 8 8 8)')
    parser.add_argument('-m', '--mode', type=int, choices=range(3), default=1, metavar='0-2', help='''display mode for mouse movement, from less to more verbose (default: %(default)s)
  0: hide mouse movements (use with -c for clicks only)
  1: show mouse movements while any mouse button is held
  2: show all mouse movements''')
    parser.add_argument('-c', '--clicks', action='store_true', help='show mouse clicks explicitly')
    parser.add_argument('-s', '--speed', type=int, choices=range(0, 11), default=0, metavar='0, 1-10', help='animation speed, 0 for no animation (default: %(default)s)')
    parser.add_argument('-a', '--absolute', action='store_true', help='interpret mouse coordinates as absolute')
    return parser.parse_args()


def main():
    args = parse_args()
    if len(args.bit_lengths) == 1:
        args.bit_lengths *= 3
    elif len(args.bit_lengths) != 3:
        print('Please specify a bit length per field (three total) or a single if identical for all fields')
        exit()

    if sum(args.bit_lengths) % 8 != 0:
        print('Total bit length must be a multiple of 8')
        exit()

    args.bit_lengths = [16, 16, 16]

    clicks, xs, ys = decode_mouse_data(args.file.read(), bit_lengths=args.bit_lengths, offset=args.offset, absolute=args.absolute)

    pos = []
    for click, x, y in zip(clicks, xs, ys):
        if click:
            # print(f'Click at ({x}, {y})')
            pos.append((x, y))
    
    # ON SCREEN KEYBOARD, PARSE OUT KEY POSITIONS
    # Define a simple QWERTY keyboard layout with key bounding boxes (x1, y1, x2, y2)
    # These values must be adapted to your screen/keyboard image coordinates
    # Example layout for demonstration (units: pixels)
    # BUTTONS are 75 by 60
    # KEYBOARD_LAYOUT = [
    #     # SHIFT
    #     {'key': 'Shift', 'box': (-660, -180, -600, -120)},
        
    #     # ROW 1
    #     {'key': 'Q', 'box': (-575, -60, -500, 0)},
    #     {'key': 'W', 'box': (-500, -60, -425, 0)},
    #     {'key': 'E', 'box': (-425, -60, -350, 0)},
    #     {'key': 'R', 'box': (-350, -60, -275, 0)},
    #     {'key': 'T', 'box': (-275, -60, -200, 0)},
    #     {'key': 'Y', 'box': (-200, -60, -125, 0)},
    #     {'key': 'U', 'box': (-125, -60, -50, 0)},
    #     {'key': 'I', 'box': (-50, -60, 25, 0)},
    #     {'key': 'O', 'box': (25, -60, 100, 0)},
    #     {'key': 'P', 'box': (100, -60, 175, 0)},

    # ]

    # def get_key_at_position(x, y):
    #     for key_info in KEYBOARD_LAYOUT:
    #         x1, y1, x2, y2 = key_info['box']
    #         if x1 <= x <= x2 and y1 <= y <= y2:
    #             return key_info['key']
    #     return None

    # pressed_keys = []
    # for x, y in pos:
    #     key = get_key_at_position(x, y)
    #     if key:
    #         pressed_keys.append(key)

    # print(pos)
    # print("Keys pressed by mouse clicks:", ','.join(pressed_keys))

    # between_clicks = []
    # prev = 0
    # for i, (click, x, y) in enumerate(zip(clicks, xs, ys)):
    #     if click:
    #         between_clicks.append([clicks[prev:i], xs[prev:i], ys[prev:i]])
    #         prev = i + 1
    #         print(f'Click {i}: {click}, X: {x}, Y: {y}')

    # if prev < len(xs):
    #     between_clicks.append([clicks[prev:], xs[prev:], ys[prev:]])

    click_count = 0
    for i, (click, x, y) in enumerate(zip(clicks, xs, ys)):
        if click:
            click_count += 1
            if click_count == 16: # start at 16th click
                clicks = clicks[i:]
                xs = xs[i:]
                ys = ys[i:]
                break

    draw_movement(clicks, xs, ys, draw_mode=args.mode, draw_clicks=args.clicks, speed=args.speed)

    # for clicks, xs, ys in between_clicks:
    #     draw_movement(clicks, xs, ys, draw_mode=2, draw_clicks=True, speed=args.speed)
    


if __name__ == '__main__':
    main()
