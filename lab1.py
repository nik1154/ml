import csv
#!usr/bin/python
#list creatin
hypo=['%','%','%','%','%','%']


with open('Training_examples.csv') as csv_file:
    readcsv = csv.reader(csv_file, delimiter=',')
    print(readcsv)
    data = []
    print("\nThe given training examples are:")
    for row in readcsv:
        print(row)
        if row[len(row)-1].upper() == "YES":
            data.append(row)
print("\nThe positive examples are:")
for x in data:
    print(x)   
print("\n")
print("Data first row is: \n",data[0])
list=[]
for i in range(len(data[0])-1):
    list.append(data[0][i])
print("\nlist:\n",list)
hypo=list
for i in range(len(data)):
    for j in range(len(list)):
        if hypo[j]!=data[i][j]:
            hypo[j]='?'
            j=j+1
        else:
            hypo[j]
    print(hypo)

print("\nThe most specific hypothesis is:\n",hypo)