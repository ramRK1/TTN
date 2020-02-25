l = int(input("Enter the symbols in one side of the square\n"))
symbol = 'X'
for i in range(l):
	for j in range(l):
		if symbol == 'X':
			print(symbol,end=" ")
			symbol = 'O'
		else:
			print(symbol,end=" ")
			symbol = 'X'
	print("\n",end="")