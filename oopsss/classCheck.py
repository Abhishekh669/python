class Myclass:
    x =5;



class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def __str__(self):
        return f"{self.name}({self.age})"
    
p2 = Person("Kabu", 18);
print(f"this is my name {p2.name}")
print(p2)

p1=Myclass();
print(p1.x)