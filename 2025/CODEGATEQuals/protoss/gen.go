package main

import (
	"bytes"
	"fmt"
	"math/big"
	"math/rand"
	"os"
	"strconv"
	"strings"
	// protobuf
)

func main() {
	// Read a string from user input
	var input string
	fmt.Print("Enter a string with format 'xxx.yyy' where yyy is a hex number: ")
	fmt.Scanln(&input)

	// Split the string on '.'
	parts := strings.Split(input, ".")

	// Check if we have at least 2 parts
	if len(parts) < 2 {
		fmt.Println("Error: Input must contain at least one '.' character")
		os.Exit(1)
	}

	// Parse the second part as a hex integer
	hexStr := parts[1]
	seed, err := strconv.ParseInt(hexStr, 16, 64)
	if err != nil {
		fmt.Printf("Error parsing '%s' as hex: %v\n", hexStr, err)
		os.Exit(1)
	}

	// Use the parsed value as a random seed
	fmt.Printf("Using seed: %d (0x%x)\n", seed, seed)
	rand.Seed(seed) // Note: In Go 1.20+, use rand.NewSource instead

	// shuffle base58 alphabet
	alphabet := "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
	alphabet = strings.TrimSpace(alphabet)
	// Convert the string to a slice of runes
	runes := []rune(alphabet)
	n := 58

	// Shuffle the alphabet using Fisher-Yates algorithm
	for n > 1 {
		// Generate a random index
		i := rand.Intn(n)
		// Swap the characters at indices i and n-1
		runes[i], runes[n-1] = runes[n-1], runes[i]
		// Decrease n
		n--
	}
	// Print the shuffled alphabet
	alphabet = string(runes)
	fmt.Println("Shuffled alphabet:", alphabet)

	// Decode the data with the alphabet as base58 alphabet
	data := parts[0]
	num := big.NewInt(0)
	for _, c := range data {
		// Find the index of the character in the alphabet
		index := strings.IndexRune(alphabet, c)
		if index == -1 {
			fmt.Printf("Error: Character '%c' not found in alphabet\n", c)
			os.Exit(1)
		}
		// Update the number with the base58 value
		num.Mul(num, big.NewInt(58))
		num.Add(num, big.NewInt(int64(index)))
	}
	// Convert the number to a byte slice
	dbytes := num.Bytes()
	// Print the decoded string
	fmt.Printf("Decoded bytes: %x\n", dbytes)
	decodedString := string(dbytes)
	fmt.Printf("Decoded string: %s\n", decodedString)

	fmt.Print("Enter a string to encode: ")
	var inputString string
	fmt.Scanln(&inputString)
	// Pack as protobuf
	// Prepend \n, length as byte NOT ITOA
	// and append \x10, \x01
	// Convert the string to a byte slice
	inputString = strings.TrimSpace(inputString)

	// Encode the data with the shuffled alphabet
	inputData := make([]byte, len(inputString)+6)
	inputData[0] = 0x0a
	inputData[1] = byte(len(inputString))
	copy(inputData[2:], inputString)
	inputData[len(inputString)+2] = 0x10
	inputData[len(inputString)+3] = 0xad
	inputData[len(inputString)+4] = 0xbd
	inputData[len(inputString)+5] = 0x03

	fmt.Printf("Input data: %x\n", inputData)

	num = big.NewInt(0)
	num.SetBytes(inputData)

	out := bytes.NewBuffer(nil)
	for num.Cmp(big.NewInt(0)) > 0 {
		// Get the remainder when dividing by 58
		remainder := new(big.Int)
		num.DivMod(num, big.NewInt(58), remainder)
		// Append the character at the index of the remainder in the shuffled alphabet
		out.WriteByte(alphabet[remainder.Int64()])
	}
	// Reverse the output buffer
	encoded := out.Bytes()
	for i, j := 0, out.Len()-1; i < j; i, j = i+1, j-1 {
		encoded[i], encoded[j] = encoded[j], encoded[i]
	}
	// Print the encoded string
	fmt.Printf("Encoded string: %s\n", string(encoded))

}
