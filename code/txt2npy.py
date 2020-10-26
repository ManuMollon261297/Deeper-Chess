import numpy as np

# Separate Data in arrays
fB = open('bitStreamPosDataFinalB.txt')
fW = open('bitStreamPosDataFinalW.txt')

for line in fB:
  gamesB = line.split()
for line in fW:
  gamesW = line.split()

fB.close()
fW.close()

print(len(gamesB))
print(len(gamesW))

gamesBarray = np.zeros((len(gamesB),773), dtype=np.int8) 
gamesWarray = np.zeros((len(gamesW),773), dtype=np.int8) 

i = 0
print('gamesB')
for string in gamesB:
  j = 0
  for bit in string:
    gamesBarray[i][j] = bit
    j += 1
  i += 1
  print(i, end="\r")

i = 0
print('gamesW')
for string in gamesW:
  j = 0
  for bit in string:
    gamesWarray[i][j] = bit
    j += 1
  i += 1
  print(i, end="\r")

np.save('bitStreamPosDataFinalB', gamesBarray)
np.save('bitStreamPosDataFinalW', gamesWarray)