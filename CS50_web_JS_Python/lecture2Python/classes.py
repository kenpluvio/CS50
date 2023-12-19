class Point():
    def __init__(self,input1,input2):
        self.x = input1
        self.y = input2
        self.m = input1 * input2

p = Point(2, 8)
print(p.x)
print(p.y)
print(p.m)

class Flight():
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []
    
    def add_passenger(self, name):
        if not self.open_seats():
            return False
        self.passengers.append(name)
        return True
    
    def open_seats(self):
        return self.capacity - len(self.passengers)

flight = Flight(3)

people = ["Harry", "Ron", "Heroine", "Ginny"]

for person in people:
    if flight.add_passenger(person):
        print(flight.passengers)
    elif flight.add_passenger(person) == False:
        print(f"No more seat for {person}")
        break
    