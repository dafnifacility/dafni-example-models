import os
import json
from pathlib import Path
from work import do_work

SEQUENCE_LENGTH_DEFAULT = 20
SEQUENCE_F0_DEFAULT = 0
SEQUENCE_F1_DEFAULT = 1

output_folder = Path("/data/outputs/")


def main():

    print("Starting example model")

    # Read value from environment variable using the default value
    # if it is not specified and convert the value to an integer
    sequence_length = int(os.getenv("SEQUENCE_LENGTH", SEQUENCE_LENGTH_DEFAULT))
    sequence_f0 = int(os.getenv("SEQUENCE_F0", SEQUENCE_F0_DEFAULT))
    sequence_f1 = int(os.getenv("SEQUENCE_F1", SEQUENCE_F1_DEFAULT))

    if sequence_length < 5:
        raise Exception("Sequence_length is below the minimum value")

    # Call main work
    sequence = do_work(sequence_length, sequence_f0, sequence_f1)

    # Output the results to a file
    output_folder.mkdir(parents=True, exist_ok=True)
    output_file = output_folder.joinpath("sequence.json")
    output_file.write_text(json.dumps({"sequence": sequence}))

    print("Finished example model")


def is_int(number):
    """ Check is a real number """
    try:
        int(number)
        return True
    except (ValueError, TypeError):
        pass
    return False


if __name__ == "__main__":
    main()
