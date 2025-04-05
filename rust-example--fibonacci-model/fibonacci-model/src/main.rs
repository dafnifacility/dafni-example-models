mod work;

use std::env;
use std::path::Path;
use std::fs::File;
use std::io::prelude::*;
use chrono::Utc;
use json;

const SEQUENCE_LENGTH_DEFAULT: usize = 20;
const SEQUENCE_LENGTH_MINIMUM: usize = 2;
const SEQUENCE_LENGTH_MAXIMUM: usize = 50;
const SEQUENCE_F0_DEFAULT: i64 = 0;
const SEQUENCE_F1_DEFAULT: i64 = 1;

const MODEL_NAME: &str = "fibonacci-rust-model";
const MODEL_VERSION: &str = "1.0";

const OUTPUT_FOLDER: &str = "/data/outputs/";
const OUTPUT_FILE: &str = "sequence.json";

fn main() {

    let datetime : String = Utc::now().to_string();
    println!("Started fibonacci model.");
    
    let (sequence_length, sequence_f0, sequence_f1) 
        = get_settings();

    let sequence = work::get_fibonacci_sequence( sequence_length, sequence_f0, sequence_f1 );
    
    save_sequence( sequence, sequence_length, sequence_f0, sequence_f1, datetime );
}

fn get_settings() -> (usize, i64, i64) {
    println!("Getting settings.");
    
    let mut sequence_length :usize = SEQUENCE_LENGTH_DEFAULT;
    let sequence_length_env = env::var("SEQUENCE_LENGTH");

    if sequence_length_env.is_ok() {
        sequence_length = sequence_length_env.unwrap().trim().parse()
            .expect("Error: SEQUENCE_LENGTH must be a whole number");

        if sequence_length < SEQUENCE_LENGTH_MINIMUM {
            println!( "Warning: SEQUENCE_LENGTH is less than the minimum {}", SEQUENCE_LENGTH_MINIMUM );
            sequence_length = SEQUENCE_LENGTH_MINIMUM;
        }
        
        if sequence_length > SEQUENCE_LENGTH_MAXIMUM {
            println!( "Warning: SEQUENCE_LENGTH is more than the maximum {}", SEQUENCE_LENGTH_MAXIMUM );
            sequence_length = SEQUENCE_LENGTH_MAXIMUM;
        }
    }

    let mut sequence_f0 = SEQUENCE_F0_DEFAULT;
    let sequence_f0_env = env::var("SEQUENCE_F0");

    if sequence_f0_env.is_ok() {
        sequence_f0 = sequence_f0_env.unwrap().trim().parse()
            .expect("Error: SEQUENCE_F0 must be a whole number");
    }

    let mut sequence_f1 = SEQUENCE_F1_DEFAULT;
    let sequence_f1_env = env::var("SEQUENCE_F1");

    if sequence_f1_env.is_ok() {
        sequence_f1 = sequence_f1_env.unwrap().trim().parse()
            .expect("Error: SEQUENCE_F1 must be a whole number");
    }
    
    println!("Have: length={}, first={}, second={}", sequence_length, sequence_f0, sequence_f1);
    
    (sequence_length, sequence_f0, sequence_f1)
}


fn save_sequence( sequence: Vec<i64>, length: usize, f0:i64, f1:i64, created: String ) {
    
    let mut path = Path::new(OUTPUT_FOLDER);
    if !path.is_dir() {
        println!("Warning: Save folder not available, outputting to working directory instead.");
        path = Path::new("./");
    }
    
    let file = path.join(OUTPUT_FILE);
    println!("Saving file to {}", file.display() );

    let data = json::object!{
        sequence: sequence,
        settings: {
            length: length,
            f0: f0,
            f1: f1,
        },
        model : {
            model: MODEL_NAME,
            version: MODEL_VERSION,
            created: created,
        }
    };
    
    let mut writer = File::create( file )
        .expect("Error: json file failed to be created" );

    writer.write_all( data.dump().as_bytes() )
        .expect("Error: Failed to write file.");
}