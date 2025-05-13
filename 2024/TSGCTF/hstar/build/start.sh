#!/bin/sh

cd /home/opam

eval $(opam env) && timeout --foreground -s 9 60s ./chall
