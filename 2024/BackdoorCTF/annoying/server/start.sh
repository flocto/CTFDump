#!/bin/sh
echo "listenting on port 9035"

socat TCP4-LISTEN:9035,reuseaddr,fork EXEC:"python3 /shell.py",stderr