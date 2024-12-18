# import requests
# from io import BytesIO
# from lxml import etree


# url = 'https://jiku-finance.vercel.app'

# response = requests.get(url)
# content = response.content
# parser = etree.HTMLParser()

# content = etree.parse(BytesIO(content), parser=parser)

# print("Result :: ", dir(content))

from bs4 import BeautifulSoup as bs
import requests 
 
url = 'https://jiku-finance.vercel.app'
r = requests.get(url)
tree = bs(r.text, 'html.parser')
print("This is the treee :: ",tree)
for meta in tree.find_all('meta'):
    if 'name' in meta.attrs:
        print(f"{meta.get('name')}: {meta.get('content')}")
    elif 'property' in meta.attrs:
        print(f"{meta.get('property')}: {meta.get('content')}")








