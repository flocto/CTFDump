pragma solidity ^0.8.28;

import "./Chal.sol";

contract Setup {
    Chal public immutable TARGET;

    constructor() payable {
        TARGET = new Chal();
    }

    function isSolved() public view returns (bool) {
        return TARGET.hasWon();
    }
}