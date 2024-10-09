import json
import os
import sys
from pathlib import Path

from work import do_work

SEQUENCE_LENGTH_DEFAULT = 20
SEQUENCE_LENGTH_MINIMUM = 2
SEQUENCE_F0_DEFAULT = 0
SEQUENCE_F1_DEFAULT = 1

output_folder = Path("/data/outputs/")
output_file_name = "sequence.json"


def main():

    print("Starting fibonacci model")

    # Read values from environment variables but use default values if they don't exist
    sequence_length = os.getenv("SEQUENCE_LENGTH", SEQUENCE_LENGTH_DEFAULT)
    sequence_f0 = os.getenv("SEQUENCE_F0", SEQUENCE_F0_DEFAULT)
    sequence_f1 = os.getenv("SEQUENCE_F1", SEQUENCE_F1_DEFAULT)

    # Check each of the values are in an acceptable format for this model
    if not is_int(sequence_length):
        sys.exit("Error: SEQUENCE_LENGTH must be a whole number")

    sequence_length = int(sequence_length)
    if sequence_length < SEQUENCE_LENGTH_MINIMUM:
        sys.exit(
            f"Error: SEQUENCE_LENGTH must be a minimum of {SEQUENCE_LENGTH_MINIMUM}"
        )

    if not is_int(sequence_f0):
        sys.exit("Error: SEQUENCE_F0 must be whole number")

    if not is_int(sequence_f1):
        sys.exit("Error: SEQUENCE_F1 must be whole number")

    # Call main work
    sequence = do_work(sequence_length, int(sequence_f0), int(sequence_f1))

    # Output the results to a file
    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder.joinpath(
        f"{sequence_length}-{sequence_f0}-{sequence_f1}-{output_file_name}"
    )
    output_file.write_text(json.dumps({"sequence": sequence}))

    print("Finished fibonacci model")


def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    main()
