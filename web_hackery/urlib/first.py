# import urllib.request 
# fhand = urllib.request.urlopen('http://data.pr4e.org/romeo.txt')
# for line in fhand:
#     print(line.decode().strip())

# import requests 
# 
# data = requests.get("http://data.pr4e.org/romeo.txt")
# print("This is the data: ", data.text)
# 
# 



# import urllib.request, urllib.parse, urllib.error
# fhand = urllib.request.urlopen('http://data.pr4e.org/romeo.txt')
# counts = dict()
# for line in fhand:
#     words = line.decode().split()
#     for word in words:
#             counts[word] = counts.get(word, 0) + 1
# print(counts)


import requests
response = requests.get('http://data.pr4e.org/cover3.jpg')
with open('hello.jpg','wb') as f:
    f.write(response.content)

    