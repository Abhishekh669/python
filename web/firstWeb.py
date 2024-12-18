# from  urllib.parse import urlsplit # for parseing the url, constructing, manipulating the url 
# import urllib.request #open and intereact with turls for fetching the data from the web

# url='http://www.google.com'
# content = urllib.request.urlopen(url).read()
# print("this is the  data  :: " ,content.decode('utf-8'))


# url2 = 'https://www.jiku-finance.vercel.app/accounts/123453'
# print("\nThis isthe url pase functin : ", urlsplit(url2))



# # sending the loign data to the web page 

# url3="https://jiku-finance.vercel.app/sign-in"
# info ={'email' : "hello@hello.hello", 'password': "hello12345"}
# data = urllib.parse.urlencode(info).encode() #data is now of type bytes 
# req = urllib.request.Request(url3, data)
# content = urllib.request.urlopen(req).read()
# print("\n\nThis is the data after the login :: ",content)




# #using the request 

import requests

url='https://www.jiku-finance.vercel.app'
url2='https://jiku-finance.vercel.app/sign-in'
response = requests.get(url, verify=False) # get 
print("this isthe repsonnse: ",response.text)


data = {'email' : "hello@hello.hello", "password" : "hello12345"}
response = requests.post(url2, data=data)
print("\n\nThis is the next response ",response.text)

