// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.28;

import {Script, console} from "@forge-std-1.9.1/src/Script.sol";

import {Recovery} from "src/Recovery.sol";
import {Deploy} from "script/Deploy.s.sol";

contract Test is Script {
    function setUp() public {}

    function run() public {
        address challenge_addr = 0x472887f79dF39f224388b632d4519D9b79ca555B;
        Recovery challenge = Recovery(payable(challenge_addr));
        console.log(challenge.isSolved());

        // vm.startBroadcast(0x0889f5a98ce0409689100f1c0ac6567a382ec76610c4e29c4b3e59f893da29aa);
        uint8 v = 27;
        bytes32 r = 0xd63fa60c15e211e223be390b06209800137fe4d43a6fe58cc21f864aad4f6ffd;
        bytes32 s = 0x2e23ca8fb85b54da34014c13af249df39d756d067bd955bdbafe24bd79736866;
        bytes32 hsh = 0x06337210da8352e0df042682f2ec9434d4600f60fa8bf00c745473b9c3928485;

        address signer = ecrecover(hsh, v, r, s);
        console.log(signer);

        // Deploy deploy = Deploy(signer);
        // console.log(deploy);

        console.log(challenge.owner());
        console.log(address(this));
        // challenge.changeOwner(v, r, s, hsh, address(this));
        console.log(challenge.owner());
        // vm.stopBroadcast();
        challenge.solve();
        console.log(challenge.isSolved());
        
    }
}
