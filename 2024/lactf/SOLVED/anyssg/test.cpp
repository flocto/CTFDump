#include <chrono>
#include <iostream>
// #include <omp.h>
#include <vector>

using namespace std;

typedef long long ll;
static ll I = 3473400794307473L;
class CustomRandom {
   private:
    ll seed;

   public:
    CustomRandom() : seed(chrono::system_clock::now().time_since_epoch().count()) {}

    CustomRandom(ll seed) : seed(seed ^ I) {}

    void setSeed(ll seed) {
        this->seed = seed ^ I;
    }

    ll nextLong() {
        ll m = 1L << 52;
        ll c = 4164880461924199L;
        ll a = 2760624790958533L;
        seed = (a * seed + c) & (m - 1);
        return seed;
    }

    ll prevLong() {
        ll m = 1L << 52;
        ll c = 4164880461924199L;
        ll a_inv = 708146206106893L;
        seed = (a_inv * (seed - c)) & (m - 1);
        ll res = this->nextLong();
        seed = (a_inv * (seed - c)) & (m - 1);
        return res;
    }
};

int main() {
    CustomRandom cr;
    cr.setSeed(12345);

    ll low = (9 * (1L << 52)/10L);
    ll high = (1L << 52);

    auto start = chrono::high_resolution_clock::now();
    vector<ll> v;

    for(ll i = low + 1; i < high; i++) {
        // if((i & 0b11111111111111) == 0) cout << i << endl;
        cr.setSeed(i ^ I);
        for(int j = 0; j < 15; j++){
            if(cr.nextLong() <= low){
                break;
            }
            if(j == 14) v.push_back(i);
        }
    }

    cout << v.size() << endl;
    for(int i = 0; i < v.size(); i++){
        cout << v[i] << endl;
    }
    cout << "done" << endl;
    cout << "took " << chrono::duration_cast<chrono::milliseconds>(chrono::high_resolution_clock::now() - start).count() << "ms" << endl;
}