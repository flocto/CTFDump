// Decompiled by library.dedaub.com
// 2025.06.21 04:32 UTC
// Compiled using the solidity compiler version 0.8.30





function fallback() public payable { 
    revert();
}

function 0xbb6f4291(bytes varg0) public payable { 
    require(msg.data.length - 4 >= 32);
    require(varg0 <= uint64.max);
    require(msg.data.length > 4 + varg0 + 31);
    require(varg0.length <= uint64.max, Panic(65)); // failed memory allocation (too much memory)
    v0 = new bytes[](varg0.length);
    require(!((v0 + (63 + (0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0 & varg0.length + 31) & 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0) < v0) | (v0 + (63 + (0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0 & varg0.length + 31) & 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0) > uint64.max)), Panic(65)); // failed memory allocation (too much memory)
    require(msg.data.length >= 32 + (varg0.length + (4 + varg0)));
    CALLDATACOPY(v0.data, varg0.data, varg0.length);
    v0[varg0.length] = 0;
    if (44 == v0.length) {
        v1 = v2 = 0;
        while (v1 < 16) {
            v3 = _SafeSub(15, v1);
            v4 = _SafeMul(8, v3);
            v5 = _SafeSub(15, v1);
            v6 = _SafeMul(8, v5);
            require(v1 < v0.length, Panic(50)); // access an out-of-bounds or negative index of bytesN array or slice
            v7 = 0x492(1, uint8(v0[v1] >> 248 ^ uint128(0xc5d71484f8cf9bf4b76f47904730804b) >> v6));
            if (uint8(v7) == uint8(0xa8b576e88daae1c2885f77f57702fa15 >> v4)) {
                v1 = v1 + 1;
            } else {
                v8 = v9 = 0;
            }
        }
        v10 = v11 = 16;
        while (v10 < 32) {
            v12 = _SafeSub(v10, 16);
            v13 = _SafeSub(15, v12);
            v14 = _SafeMul(8, v13);
            v15 = _SafeSub(15, v12);
            v16 = _SafeMul(8, v15);
            require(v10 < v0.length, Panic(50)); // access an out-of-bounds or negative index of bytesN array or slice
            v17 = 0x492(v0[v10] >> 248, uint8(uint128(0x9e3225a9f133b5dea168f4e2851f072f) >> v16));
            if (uint8(v17) == uint8(0x10659bdc6368e83dd4d62a13f3523aa1 >> v14)) {
                v10 = v10 + 1;
            } else {
                v8 = v18 = 0;
            }
        }
        v19 = v20 = 32;
        while (v19 < 44) {
            v21 = _SafeSub(v19, 32);
            v22 = _SafeSub(11, v21);
            v23 = _SafeMul(8, v22);
            v24 = _SafeSub(11, v21);
            v25 = _SafeMul(8, v24);
            require(v19 < v0.length, Panic(50)); // access an out-of-bounds or negative index of bytesN array or slice
            if (uint8(0xff64a39c4c96443e1b4a7098 >> v23) == uint8(v0[v19] >> 248 ^ uint96(0xcc00fcaa7ca62061717a48e5) >> v25)) {
                v19 = v19 + 1;
            } else {
                v8 = v26 = 0;
            }
        }
        require(15 < v0.length, Panic(50)); // access an out-of-bounds or negative index of bytesN array or slice
        require(10 < v0.length, Panic(50)); // access an out-of-bounds or negative index of bytesN array or slice
        require(4 < v0.length, Panic(50)); // access an out-of-bounds or negative index of bytesN array or slice
        v27 = 0x492(v0[4] >> 248, uint8(v0[10] >> 248 << 248 >> 248));
        v28 = 0x492(v27, uint8(v0[15] >> 248 << 248 >> 248));
        if (260 == uint16(v28)) {
            v8 = v29 = 1;
        } else {
            v8 = v30 = 0;
        }
    } else {
        v8 = v31 = 0;
    }
    return bool(v8);
}

function _SafeSub(uint256 varg0, uint256 varg1) private { 
    require(varg0 - varg1 <= varg0, Panic(17)); // arithmetic overflow or underflow
    return varg0 - varg1;
}

function _SafeMul(uint256 varg0, uint256 varg1) private { 
    require((varg1 == varg1 * varg0 / varg0) | !varg0, Panic(17)); // arithmetic overflow or underflow
    return varg1 * varg0;
}

function 0x492(uint16 varg0, uint16 varg1) private { 
    require(varg1 + varg0 <= uint16.max, Panic(17)); // arithmetic overflow or underflow
    return varg1 + varg0;
}

// Note: The function selector is not present in the original solidity code.
// However, we display it for the sake of completeness.

function __function_selector__( function_selector) public payable { 
    MEM[64] = 128;
    require(!msg.value);
    if (msg.data.length >= 4) {
        if (0xbb6f4291 == function_selector >> 224) {
            0xbb6f4291();
        }
    }
    fallback();
}
