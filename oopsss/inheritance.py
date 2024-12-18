class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def printname(self):
        print(f"Name : {self.name}\nAge : {self.age}\nAddress : {self.address}")



class Student(Person):
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address
x = Student("Kabu",18, "Morang")
x.printname();

