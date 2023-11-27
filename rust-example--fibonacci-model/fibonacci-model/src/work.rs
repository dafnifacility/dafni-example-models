use std::vec;
use std::ops;

fn print_sequence( sequence: &Vec<i64> ) {
    print!( "Have: Sequence=");
    for x in sequence {
        print!("{} ", x);
    }
    println!();
}

pub fn get_fibonacci_sequence(length: usize, f0:i64, f1:i64) -> Vec<i64> {

    println!("Generating sequence.");
    let sequence = fibonacci_sequence( length, f0, f1);

    print_sequence(&sequence);

    sequence
}

fn fibonacci_sequence( length: usize, f0:i64, f1:i64) -> Vec<i64> {

    if length == 1 {
        return vec![f0];
    }

    let mut sequence : Vec<i64> = vec![0; length];
    sequence[0] = f0;
    sequence[1] = f1;

    for i in (ops::Range::<usize>{ start: 2, end: length}) {
        sequence[i] = sequence[i-2] + sequence[i-1]
    }

    sequence
}