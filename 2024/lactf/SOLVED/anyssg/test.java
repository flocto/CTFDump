import java.time.Instant;



public class test {
    public static void main(String[] args) {
        CustomRandom cr = new CustomRandom();
        // long i = 3473400794307473L;
        // System.out.println((9 * (1L << 52)/10L));
        // System.out.println(1L << 52);

        cr.setSeed(12345);
        for (int i = 0; i < 10; i++) {
            System.out.println(cr.nextLong());
        }
        System.out.println("prev");
        for (int i = 0; i < 10; i++) {
            System.out.println(cr.prevLong());
        }
        
    }
}

class CustomRandom {
    private long seed;
    private final long i = 3473400794307473L;

    public CustomRandom() {
        this.seed = Instant.now().getEpochSecond() ^ i;
    }

    public void setSeed(long seed) {
        this.seed = seed ^ i;
    }

    public long nextLong() {
        long m = 1L << 52;
        long c = 4164880461924199L;
        long a = 2760624790958533L;
        seed = (a *seed+ c) & (m -1L);
        return seed;
    }

    public long prevLong() {
        long m = 1L << 52;
        long c = 4164880461924199L;
        long a_inv = 708146206106893L;
        seed = (a_inv * (seed - c)) & (m - 1L);
        long result = this.nextLong();
        seed = (a_inv * (seed - c)) & (m - 1L);
        return result;
    }
}