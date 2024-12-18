import re 

hand = open('passWord')
for line in hand:
    line = line.rstrip()
    x =re.findall('\S+on\S+', line)
    if len(x) > 0: print("This is me : ", x)
    if re.search('^mon*', line):
        print("found it : ", line)