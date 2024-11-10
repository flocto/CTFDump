const { Web3 } = require("web3");
const fs = require("fs");
// const web3 = new Web3("BINANCE_TESTNET_RPC_URL");
// https://bsc-testnet.public.blastapi.io
const web3 = new Web3("https://bsc-testnet.public.blastapi.io");
const contractAddress = "0x5324EAB94b236D4d1456Edc574363B113CEbf09d";
async function callContractFunction(inputString) {
    try {
        // Set-Variable -Name _body -Value ('{"method":"eth_call","params":[{"to":"$address","data":"0x5c880fcb"}, BLOCK],"id":1,"jsonrpc":"2.0"}')
        const new_methodId = "0x5c880fcb";
        const blockNumber = 43148912;
        const newEncodedData = new_methodId;
        const newData = await web3.eth.call(
            { to: contractAddress, data: newEncodedData },
            blockNumber
        );
        const decodedData = web3.eth.abi.decodeParameter("string", newData);
        console.log("Decoded data:", decodedData);
        const base64DecodedData = Buffer.from(decodedData, "base64");
        console.log("Base64 decoded data:", base64DecodedData.toString());
        const xorKey = Buffer.from("FLAREON24");

        for (let i = 0; i < base64DecodedData.length; i++) {
            base64DecodedData[i] ^= xorKey[i % xorKey.length];
        }

        console.log("Decoded data:", base64DecodedData.toString());
    } catch (error) {
        console.error("Error calling contract function:", error);
    }
}
const inputString = "giV3_M3_p4yL04d!A";
callContractFunction(inputString);
