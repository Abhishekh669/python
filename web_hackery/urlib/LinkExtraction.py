import requests
import argparse 
import sys
import re 
from bs4 import BeautifulSoup

def main():
   print(f"\nSearching Link in :: {url}\n")
   try:
      response = requests.get(url)
      response.raise_for_status() 
      data = response.text
      soup = BeautifulSoup(data, 'html.parser')
      tags = soup('a')
      print("\n")
      for line in tags:
         
         print( "Tag : ", line)
         print("Url : ", line.get("href", None))
         print("\n")

    
    #   links = re.findall(r'href="(http[s]?://.*?)"', data)
    #   for link in links:
    #    print(link)
       
   except:
      print(f"Error in the  processing {url}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
      print(
        '''
            syntax : python3 LinkExtraction.py <url>
            example : python3 LinkExtraction.py "http://google.com"

        ''')
    else:  
        url = sys.argv[1]
        main()
