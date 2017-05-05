# This program translates sudoku into exact cover problem and solves it
# by Chen and Ling
# 05052017
from dancing import *

def sudoku2exact_cover(A):
	"""
	A represents the sudoku problem. 
	0s for blank
	"""
	exact_cover_mat = []
	for i in range(N):
		for j in range(N):
			if A[i,j] != 0:
				exact_cover_mat.append(row_generator(A[i,j], i, j))
			else:
				for n in valid_list(A, i, j):
					exact_cover_mat.append(row_generator(n, i, j))
	exact_cover_mat = np.array(exact_cover_mat)
	return exact_cover_mat

def row_generator(n, i, j):
	# i and j start from 0
	row = [0]*4*N*N
	index1 = i*N+j
	index2 = N*N-1 + N*j + n
	index3 = 2*N*N-1 + N*i + n
	index4 = 3*N*N-1 + N*block(i, j) + n
	row[index1] = 1
	row[index2] = 1
	row[index3] = 1
	row[index4] = 1
	return row

def block(i, j):
	# calculates the block index
	# by Xiao Ling
	return int(i/N_sqrt)*int(N_sqrt)\
		+int(j/N_sqrt)

def valid_list(A,i,j):
	# gives all valid values for position i, j
	nonvalid = []
	for x in A[i,:]:
		if x != 0: 
			nonvalid.append(x)
	for x in A[:,j]:
		if x != 0:
			nonvalid.append(x)

	b = block(i, j)
	jb = np.mod(b, N_sqrt) * N_sqrt
	ib = int(b/N_sqrt) * N_sqrt

	all_ii = [ib+x for x in range(N_sqrt)]
	all_jj = [jb+x for x in range(N_sqrt)]
	for ii in all_ii:
		for jj in all_jj:
			nonvalid.append(A[ii,jj])
	return [x for x in range(1,N+1) if x not in nonvalid]

def translateback(row):
	index = row[0]
	i = int(index/N)
	j = np.mod(index, N)
	n = row[1] - N*N+1 - N*j
	return (i, j, index, n)

if __name__ == "__main__":

	Sudoku = np.loadtxt("mediumPuzzle.csv", delimiter=",", dtype=int)
	print(Sudoku)
	N=len(Sudoku) # N*N sudoku
	N_sqrt = int(np.sqrt(N))

	A = sudoku2exact_cover(Sudoku)
	root = mat2linklist(A)
	search(root)

	k=1
	ans = Sudoku[:]
	for row in solutions:
		i,j,index, n = translateback(row)
		ans[i,j]=n
		if np.mod(index+1,N*N) == 0:
			print("====== solution {} ======".format(k))
			k+=1
			print(ans)
		# print("{},{}: {}".format(i+1,j+1,n))
	









