#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>

typedef long long ll;
using namespace std;

__device__ ll nextLong(ll seed) {
    ll m = 1L << 52;
    ll c = 4164880461924199L;
    ll a = 2760624790958533L;
    return (a * seed + c) & (m - 1);
}

__global__ void bruteforce(ll low, ll high, ll* result) {
    // ensure each i is unique per thread, then start from low
    ll i = (blockIdx.x * blockDim.x + threadIdx.x) * (blockIdx.y * blockDim.y + threadIdx.y) + low;
    ll stride = blockDim.x * gridDim.x;
    printf("i: %lld\n", i);
    
    for (; i < high; i += stride) {
        ll seed = i;
        for (int j = 0; j < 15; j++) {
            if ((seed = nextLong(seed)) < low) {
                break;
            }
            if (j == 14) {
                printf("found: %lld\n", i);
                *result = i;
                return;
            }
        }
    }
}

int main() {
    ll low = (9 * (1L << 52) / 10L);
    ll high = (1L << 52);

    ll* result;
    cudaMallocManaged(&result, sizeof(ll));

    dim3 threadsPerBlock(16, 16);
    dim3 numBlocks(16, 16);

    bruteforce<<<numBlocks, threadsPerBlock>>>(low, high, result);
    cudaDeviceSynchronize();

    cout << *result << endl;
    cout << "done" << endl;
}