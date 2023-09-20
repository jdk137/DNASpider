import time
from query import querySingle
 
# 格式化成2016-03-20 11:45:39形式
t = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime()) 
 
# Using readlines()
fileIn = open('input.txt', 'r')
Lines = fileIn.readlines()

# writing to file
fileOut = open('./result/' + t + '.txt', 'w')


count = 0
# Strips the newline character
for line in Lines:
    str = line.split('#')[0].strip();

    if not str:
      continue

    count += 1
    print(count)

    q = querySingle(str)
    fileOut.writelines(q)
    fileOut.writelines('\n\n')
    print('\n\n')

fileOut.close()

