void ch_fr(const char *cargo) {}
void fr_ch(const char *cargo) {}
// void right(const char *cargo) {}
// void left(const char *cargo) {}

int main(void) {
    fr_ch("Goat"); 
    ch_fr("Nothing");
    fr_ch("Cabbage");
    ch_fr("Goat");
    fr_ch("Wolf");
    ch_fr("Nothing");
    fr_ch("Goat");
    return 0;
}