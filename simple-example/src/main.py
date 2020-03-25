import os
import sys
import json
from pathlib import Path
from work import do_work

SEQUENCE_LENGTH_DEFAULT = 20
SEQUENCE_F0_DEFAULT = 0
SEQUENCE_F1_DEFAULT = 1

output_folder = Path("/data/outputs/")


def main():

    print("Starting example model")

    # Read values from environment variables but use default values if they don't exist
    sequence_length = os.getenv("SEQUENCE_LENGTH", SEQUENCE_LENGTH_DEFAULT)
    sequence_f0 = os.getenv("SEQUENCE_F0", SEQUENCE_F0_DEFAULT)
    sequence_f1 = os.getenv("SEQUENCE_F1", SEQUENCE_F1_DEFAULT)
    
    # Check each of the values are in an acceptable format for this model
    try:
        sequence_length = int( sequence_length )
    except ValueError:
        sys.exit("Error: SEQUENCE_LENGTH must be a whole number")

    if sequence_length <= 0:
        sys.exit("Error: SEQUENCE_LENGTH must be greater than zero")
    
    try:
        sequence_f0 = int(sequence_f0)
        sequence_f1 = int(sequence_f1)
    except ValueError:
        sys.exit("Error: SEQUENCE_F0 and SEQUENCE_F1 must be whole numbers")
    
    # Call main work
    sequence = do_work(sequence_length, sequence_f0, sequence_f1)

    # Output the results to a file
    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder.joinpath("sequence.json")
    output_file.write_text(json.dumps({"sequence": sequence}))


    print("Finished example model")


if __name__ == "__main__":
    main()
