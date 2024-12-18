import time

def count_numbers():
    """Function to count numbers from 1 to 5."""
    for i in range(1, 6):
        print(f"Number: {i}")
        time.sleep(1)  # Simulate a delay

def print_letters():
    """Function to print letters from A to E."""
    for letter in 'ABCDE':
        print(f"Letter: {letter}")
        time.sleep(1.5)  # Simulate a delay

def main():
    # Perform tasks sequentially
    count_numbers()
    print_letters()

    print("Both tasks have finished.")

if __name__ == "__main__":
    main()
