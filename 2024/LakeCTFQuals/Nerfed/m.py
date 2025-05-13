#!/usr/bin/env python3
import numpy as np


class Memory:
    def __init__(self) -> None:
        self.__m = np.load("flag.npz")["flag"]

    def get_hash(self):
        x_m = np.zeros(self.__m.shape[1], dtype=np.int8)
        for i in range(self.__m.shape[0]):
            x_m = x_m ^ self.__m[i]
        x_m.flags.writeable = False
        return x_m

    def s(self):
        mask = self.get_hash()*np.ones(self.__m.shape, dtype=np.int8)
        self.__m = self.__m ^ mask

    def mask(self, mask, offset):
        self.__m = self.__m ^ np.roll(mask, offset, axis=1)

    def get_buf(self):
        return self.__m
# Created by pyminifier (https://github.com/liftoff/pyminifier)
