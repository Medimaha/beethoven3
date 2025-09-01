salaries=[]
salaries.append(1000)
salaries.append(5000)
salaries.append(6000)
print(salaries)
search=5000
I=0
for salary in salaries:
    if salary==search:
      index=I
      break
    I += 1
print(index)
   