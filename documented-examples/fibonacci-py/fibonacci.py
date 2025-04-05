import os
import sys
import json
from pathlib import Path


# constants
SEQUENCE_LENGTH_DEFAULT = 20
SEQUENCE_F0_DEFAULT = 0
SEQUENCE_F1_DEFAULT = 1
# OUTPUT_FOLDER = Path("./outputs/")    # use while running locally
OUTPUT_FOLDER = Path("/data/outputs/")  # use while running in docker


def generate_fibonacci(length, f0=0, f1=1):
    """Generate Fibonacci sequence of given length starting with f0 and f1."""
    sequence = [f0, f1]
    for _ in range(length - 2):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence


def get_env_var(name, default, cast=int):
    """Retrieve environment variable and cast to the specified type."""
    try:
        return cast(os.getenv(name, default))
    except ValueError:
        sys.exit(f"Error: {name} must be a {cast.__name__}")


def main():
    print("Starting Fibonacci model.")

    # retrieve input parameters from environment variables or use defaults
    sequence_length = get_env_var("SEQUENCE_LENGTH", SEQUENCE_LENGTH_DEFAULT)
    sequence_f0 = get_env_var("SEQUENCE_F0", SEQUENCE_F0_DEFAULT)
    sequence_f1 = get_env_var("SEQUENCE_F1", SEQUENCE_F1_DEFAULT)

    # generate Fibonacci sequence
    sequence = generate_fibonacci(sequence_length, sequence_f0, sequence_f1)

    # output results to file
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_FOLDER / "sequence.json"
    output_file.write_text(json.dumps({"sequence": sequence}))

    print(f"Finished Fibonacci model.")
    print(f"Sequence saved to {output_file}")


if __name__ == "__main__":
    main()
