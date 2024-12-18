import paramiko


def ssh_command(ip, port, user, passwd, cmd):
    client  = paramiko.SSHClient() #create the instance of the sshclient
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port= port, username=user, password=passwd)

    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print("----Output----")
        for line in output:
            print(line.strip())


if __name__=="__main__":
    import getpass
    user = input("Username: ")
    password = getpass.getpass()
    ip = input("enter the server ip : ")
    port = input("enter the port : ")
    cmd = input("enter the command : ")
    ssh_command(ip, port, user, password, cmd)

