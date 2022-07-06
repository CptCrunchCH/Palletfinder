#use pickle

import pickle
file = open('04_CAN/Data.txt', 'w')
file.write(str(100))
file.close

file = open('04_CAN/Data.txt', 'r')
print(file.read())
file.close
#file.read("04_CAN/Data.txt")
#print()

