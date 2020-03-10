def do_work(number, first, second):
    """
    Call the main processing part of the model
    """

    print("Generating Fibonacci sequence.")
    print(f"Using: length={number}, first={first}, second={second}")

    sequence = fibonacci_sequence(number, first, second)

    print("Sequence: ", sequence)

    return sequence


def fibonacci_sequence(length, f0=0, f1=1):
    """
    Simple Fibonacci sequence generator
    """
    sequence = [f0, f1]
    length -= 2
    while length > 0:
        nth = f0 + f1
        sequence.append(nth)

        f0 = f1
        f1 = nth
        length -= 1

    return sequence
