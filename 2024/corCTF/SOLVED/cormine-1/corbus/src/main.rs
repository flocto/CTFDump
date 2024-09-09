use byteorder::ReadBytesExt;
use byteorder::LittleEndian;
use rand_chacha::rand_core::RngCore;
use rand_chacha::rand_core::SeedableRng;
use rand_chacha::ChaCha12Rng;
use std::env;
use std::io::BufReader;
use std::io::Read;

fn read_serialized<R: Read>(reader: &mut R) -> u64 {
    let mut buf = [0; 1];
    let mut result = 0;
    let mut shift = 0;
    let mask = 0xffff_ffff_ffff_ffff;
    loop {
        reader.read_exact(&mut buf).unwrap();
        let byte = buf[0];
        result = result | ((byte & 0x7f) as u64) << shift;
        shift += 7;
        if byte & 0x80 == 0 {
            if byte & 0x40 != 0 {
                result |= (mask << shift) & mask;
            }
            break;
        }
    }
    result
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <file>", args[0]);
        std::process::exit(1);
    }

    let file = std::fs::File::open(&args[1]).unwrap();
    let mut rdr = BufReader::new(file);

    let seed = rdr.read_u32::<LittleEndian>().unwrap() as u64;
    rdr.read_u16::<LittleEndian>().unwrap(); // Not sure what this is used for


    let mut rng = ChaCha12Rng::seed_from_u64(seed);
    let mut tmp = [0u8; 1];

    let mut decrypt = |dat: u64| -> u32 {
        let prng_out = rng.next_u32();
        (dat as u32) ^ prng_out
    };

    loop {
        let x = decrypt(read_serialized(&mut rdr));
        let y = decrypt(read_serialized(&mut rdr));
        let z = decrypt(read_serialized(&mut rdr));
        rdr.read_exact(&mut tmp).unwrap();
        let typ = decrypt(tmp[0] as u64) as u8;

        println!("{}, {}, {}, {}", x as i32, y as i32, z as i32, typ as i32);

        if rdr.read_exact(&mut tmp).is_err() {
            break;
        }
        rdr.seek_relative(-1).unwrap();
    }
}
