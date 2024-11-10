const { Web3 } = require("web3");
const fs = require("fs");
// const web3 = new Web3("BINANCE_TESTNET_RPC_URL");
// https://bsc-testnet.public.blastapi.io
const web3 = new Web3("https://bsc-testnet.public.blastapi.io");
const contractAddress = "0x9223f0630c598a200f99c5d4746531d10319a569";
async function callContractFunction(inputString) {
    try {
        const methodId = "0x5684cff5";
        const encodedData =
            methodId +
            web3.eth.abi.encodeParameters(["string"], [inputString]).slice(2);
        const result = await web3.eth.call({
            to: contractAddress,
            data: encodedData,
        });
        const targetAddress = web3.eth.abi.decodeParameter("address", result);
        console.log("Decoded data:", targetAddress);
        const filePath = "decoded_output.txt";
        // fs.writeFileSync(filePath, "$address = " + targetAddress + "\n");

        const new_methodId = "0x5c880fcb";
        const blockNumber = 43152014;
        const newEncodedData =
            new_methodId +
            web3.eth.abi
                .encodeParameters(["address"], [targetAddress])
                .slice(2);
        const newData = await web3.eth.call(
            { to: targetAddress, data: newEncodedData },
            blockNumber
        );
        const decodedData = web3.eth.abi.decodeParameter("string", newData);
        console.log("Decoded data:", decodedData);
        const base64DecodedData = Buffer.from(decodedData, "base64").toString(
            "utf-8"
        );
        fs.writeFileSync(filePath, decodedData);
        console.log(`Saved decoded data to:${filePath}`);
    } catch (error) {
        console.error("Error calling contract function:", error);
    }
}
const inputString = "giV3_M3_p4yL04d!A";
callContractFunction(inputString);
