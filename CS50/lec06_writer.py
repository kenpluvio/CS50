import csv
#file = open("phonebook.csv", "a")
with open("phonebook.csv", "a") as file:
  name = input("Name: ")
  number = input("Number: ")

  writer = csv.writer(file)
  writer.writerow([name, number])

#file.close()