package main

import (
	"crypto/aes"
	"crypto/cipher"
	"fmt"
	"log"
	"os"
	"runtime"
	"sync"
)

// char* gen_printable(int32_t arg1)

//     int64_t len = sx.q(arg1)
//     int32_t rcx = len.d
//     uint64_t rcx_1 = zx.q(rcx + 1)

//     if (rcx u>= 0xffffffff)
//         rcx_1 = -1

//     char* result = malloc(rcx_1)

//     if (len.d s<= 0)
//         result[len] = 0
//         return result

//     int32_t R_1 = R
//     int64_t i = 0

//     do
//         R_1 = R_1 * 0x343fd + 0x269ec3
//         result[i] = ((R_1 u>> 0x10 & 0x7fff) u% 94).b + 0x20
//         i += 1
//     while (i s< len)

//     R = R_1
//     result[len] = 0
//     return result

func gen_printable(arg1 int32, R uint32) ([]byte, uint32) {
	len := int64(arg1)
	rcx := int32(len)
	rcx_1 := uint64(rcx + 1)
	result := make([]byte, rcx_1)
	if len <= 0 {
		result[len] = 0
		return result, R
	}
	R_1 := R
	i := int64(0)
	for i < len {
		R_1 = R_1*0x343fd + 0x269ec3
		result[i] = byte(((R_1 >> 0x10 & 0x7fff) % 94) + 0x20)
		i += 1
	}
	R = R_1
	result[len] = 0
	return result, R
}

func gen_key_iv(R uint32) (key []byte, iv []byte) {
	key, R = gen_printable(32, R)
	iv, R = gen_printable(16, R)
	// truncate the last byte
	key = key[:len(key)-1]
	iv = iv[:len(iv)-1]
	return key, iv
}

// aes cbc decrypt
func decrypt(enc, key, iv []byte) []byte {
	decryptor, err := aes.NewCipher(key)
	if err != nil {
		log.Fatalf("failed to create decryptor: %v", err)
	}
	decrypted := make([]byte, len(enc))
	mode := cipher.NewCBCDecrypter(decryptor, iv)
	mode.CryptBlocks(decrypted, enc)
	return decrypted
}

// valid if starts with "gctf{"
func isValid(decrypted []byte) bool {
	return string(decrypted[:4]) == "gctf{"
}

func main() {
	// read enc from flag.txt.enc
	enc, err := os.ReadFile("flag.txt.enc")
	if err != nil {
		log.Fatalf("failed to read file: %v", err)
	}
	fmt.Printf("Encrypted data: %x\n", enc)

	results := make(chan []byte)
	found := false
	var wg sync.WaitGroup
	numWorkers := runtime.NumCPU() / 2
	log.Printf("numWorkers: %d", numWorkers)
	work := make(chan uint32, numWorkers)

	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for R := range work {
				key, iv := gen_key_iv(R)
				decrypted := decrypt(enc, key, iv)
				if isValid(decrypted) {
					results <- decrypted
					log.Printf("found key: %s, iv: %s", key, iv)
					found = true
					close(results)
					return
				}
			}
		}()
	}

	go func() {
		for R := uint32(0); R < 0xffffffff; R++ {
			if found {
				break
			}
			work <- R
		}
		close(work)
	}()

	wg.Wait()

	if !found {
		log.Fatal("failed to find the key")
	}

	for result := range results {
		fmt.Printf("Decrypted data: %s\n", result)
		break
	}
	fmt.Println("Done")

}
