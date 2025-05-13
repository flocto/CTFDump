#include <iostream>
#include <fstream>
#include <vector>
#include <omp.h>

void decrypt(uint32_t* v, const uint32_t* k) {
    uint32_t v0 = v[0], v1 = v[1];
    uint32_t delta = 0x9E3779B9;
    uint32_t sum = 0x13a00000;
    for (int i = 0; i < 10485760; i++) {
        v1 -= ((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >> 5) + k[3]);
        v0 -= ((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >> 5) + k[1]);
        sum -= delta;
    }
    v[0] = v0;
    v[1] = v1;
}

std::vector<uint32_t> readFile(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary);
    std::vector<uint32_t> data;
    uint32_t value;
    while (file.read(reinterpret_cast<char*>(&value), sizeof(value))) {
        data.push_back(value);
    }
    return data;
}

void writeFile(const std::string& filename, const std::vector<uint32_t>& data) {
    std::ofstream file(filename, std::ios::binary);
    for (const auto& value : data) {
        file.write(reinterpret_cast<const char*>(&value), sizeof(value));
    }
}

int main() {
    const std::string inputFilename = "flag_enc_cpp2";
    const std::string outputFilename = "flag_dec_cpp2";
    const uint32_t key[4] = {0xa341316c, 0xc8013ea4, 0x3c6ef372, 0x14292967};

    std::vector<uint32_t> encryptedData = readFile(inputFilename);
    std::vector<uint32_t> decryptedData(encryptedData.size());

    #pragma omp parallel for num_threads(6400)
    for (size_t i = 0; i < encryptedData.size(); i += 2) {
        uint32_t block[2] = {encryptedData[i], encryptedData[i + 1]};
        decrypt(block, key);
        decryptedData[i] = block[0];
        decryptedData[i + 1] = block[1];
    }

    writeFile(outputFilename, decryptedData);

    std::cout << "Decryption complete. Decrypted data written to " << outputFilename << std::endl;

    return 0;
}