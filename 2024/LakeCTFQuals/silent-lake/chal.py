#!/usr/bin/env python3

import subprocess
import tempfile
import os

def pns(s: str) -> None:
    print(s)

pns("Give me the correct source code.")
source = ""
for line in iter(input, "EOF"):
    source += line + "\n"

codeql_path = './codeql-linux64/codeql/codeql'

with tempfile.TemporaryDirectory() as tmpdirname:
    with open(os.path.join(tmpdirname, "main.c"), "w") as f:
        f.write(source)
    
    print('Compiling...')
    subprocess.run([codeql_path,
                    "database",
                    "create",
                    "--language=c", 
                    "--command=clang -nostdinc -O0 -o " + os.path.join(tmpdirname, "main") + " " + os.path.join(tmpdirname, "main.c"),
                    os.path.join(tmpdirname, "db")],
                    stdout = subprocess.DEVNULL,
                    stderr = subprocess.DEVNULL
                   )
    
    print('Running query...')
    # result = subprocess.run([codeql_path,
    #                 "query",
    #                 "run",
    #                 "vscode-codeql-starter/codeql-custom-queries-cpp/example.ql",
    #                 "-d",
    #                 os.path.join(tmpdirname, "db")],
    #                capture_output = True, text=True)
    
    result = subprocess.run([codeql_path,
                "query",
                "run",
                "vscode-codeql-starter/codeql-custom-queries-cpp/example.ql",
                "-d",
                os.path.join(tmpdirname, "db")],
                capture_output = True, text=True)
    
    print('output:', result.stdout)
    if "correct" in result.stdout:
        try:
            with open("/flag.txt", "r") as f:
                print(f.read())
        except:
            print("EPFL{local_fake_flag}")
