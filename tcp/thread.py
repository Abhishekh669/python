import threading
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
        time.sleep(2)  # Simulate a delay

def main():
    # Create threads for counting numbers and printing letters
    number_thread = threading.Thread(target=count_numbers)
    letter_thread = threading.Thread(target=print_letters)
    
    # Start both threads
    number_thread.start()
    letter_thread.start()
    
    # Wait for both threads to finish
    number_thread.join()
    letter_thread.join()

    print("Both threads have finished.")

if __name__ == "__main__":
    main()
