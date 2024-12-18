import paramiko

def ssh(username, password, ip, port):
    # Create an SSH client instance
    client_ssh = paramiko.SSHClient()
    
    # Automatically add host keys from the server
    client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to the SSH server
        client_ssh.connect(ip, port=port, username=username, password=password)
        
        # Open a new session
        transport = client_ssh.get_transport()
        session = transport.open_session()
        
        if session.active:
            print('[+] Connection established.')
            try:
                while True:
                    # Prompt user for a command
                    command = input("Enter command: ").strip()
                    if command:
                        # Send the command to the server
                        session.send(command)
                        
                        # Check for exit command
                        if command.lower() == "exit":
                            print("Exiting...")
                            break
                        
                        # Receive and print the output from the server
                        output = session.recv(8192).decode()
                        print("Output:", output)
                    else:
                        print("No command entered")
            except KeyboardInterrupt:
                print("\nInterrupted by user")
            finally:
                # Close the session and client connection
                session.close()
                client_ssh.close()
        else:
            print("Session is not active")

    except paramiko.AuthenticationException:
        print("Authentication failed")
    except paramiko.SSHException as e:
        print(f"SSH Exception: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Define server connection details
    username = "lucid"
    password = "@iamlucid669"
    ip = "192.168.1.135"
    port = 2222

    # Call the SSH function to connect and interact with the server
    ssh(username, password, ip, port)
