// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

// Decompiled by library.dedaub.com
// 2024.12.20 11:01 UTC
// Warning: 53.0% of the contract's code is inferred to be dead code.

contract GasSaver {
    function setOwner(address _owner) public payable { 
        require(msg.sender == STORAGE[CHAINID()]);
        STORAGE[CHAINID()] = _owner;
    }

    function owner() public payable { 
        return STORAGE[CHAINID()];
    }

    // Note: The function selector is not present in the original solidity code.
    // However, we display it for the sake of completeness.

    function __function_selector__(bytes4 function_selector, uint256 varg1) public payable { 
        if (0x8da5cb5b == function_selector >> 224) {
            owner();
        } else {
            if (tx.origin == msg.sender) {
                if (0x7e5f4552091a69125d5dfcb7b8c2659029395bdf != msg.sender) {
                }
            } else {
                assert(msg.value <= 0);
                if (0x7e5f4552091a69125d5dfcb7b8c2659029395bdf == tx.origin) {
                    CALLDATACOPY(12, 132, 20);
                    CALLDATACOPY(44, 152, 20);
                    CALLDATACOPY(94, 172, 2);
                    revert();
                } else if (STORAGE[CHAINID()] != msg.sender) {
                    exit;
                }
            }
            if (0x13af4035 == function_selector >> 224) {
                setOwner(address);
            } else {
                exit;
            }
        }
    }
}