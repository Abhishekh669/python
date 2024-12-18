import requests
import urllib3
import sys

def login(s, url):
    data = {
        'email': 'hello@hello.hello',
        'password': 'hello'
    }
    r = s.post(url, data, verify=False)
    print("this is the data ", r)
    
    # Check if the response contains the text indicating invalid credentials
    if "Invalid credentials" in r.text:
        print("Login failed: Invalid credentials")
    else:
        print("Login successful or other response")

    # Optionally print additional information for debugging
    print(f"Response Status Code: {r.status_code}")
    print(f"Response URL: {r.url}")
    print("Response Content:")
    print(r.text[:500])  # Print the first 500 characters of the response content for readability

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
    else:
        url = sys.argv[1].strip()
        s = requests.Session()
        
        login(s, url)
