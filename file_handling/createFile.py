f = open("newtxt.txt", "r")

print(f.readline())
print(f.readline())


f.close()

f = open("newtxt.txt", "a")
f.write("hello world")
f.close()

newfile = open("kxa.txt","w")
read = open("newtxt.txt", "r")
for line in read:
    newfile.write(line)