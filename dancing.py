# This program solves exact cover problems via Dancing Links algorithm
# by Chen and Ling
# 05052017

import numpy as np
import string

class Root:
	def __init__(self):
		self.R=None
		self.L=None

class Column:
	def __init__(self):
		self.R=None
		self.L=None
		self.U=None
		self.D=None
		self.S=0
		self.N=""
    
class Node:
	def __init__(self):
		self.R=None
		self.L=None
		self.U=None
		self.D=None
		self.C=None

def mat2linklist(A, column_names=None):
	"""
	A: 0-1 array
	"""
	root = Root()
	tmp1 = root
	r_n,c_n = A.shape 
	nodes = [None] * c_n
	for j in range(c_n):
		column_header = Column()
		if column_names:
			column_header.N = column_names[j]
		else:
			column_header.N = j
		tmp2 = column_header
		tmp1.R = column_header
		column_header.L = tmp1
		tmp1 = column_header
		column = [None] * r_n
		for i in range(r_n):
			if A[i,j] == 1:
				column_header.S += 1
				node = Node()
				column[i] = node
				node.C = column_header
				tmp2.D = node
				node.U = tmp2
				tmp2 = node
		nodes[j] = column             
		tmp2.D = column_header
		column_header.U = tmp2

	tmp1.R=root
	root.L=tmp1
    
	for i in range(r_n):
		for j in range(c_n):
			if A[i,j] == 1:
				tmp = nodes[j][i]
				# keeps searching the next 1 on the right
				for k in range(1, c_n+1):
					if A[i, np.mod(j+k, c_n)]==1:
						node_r = nodes[np.mod(j+k,c_n)][i]
						tmp.R = node_r
						node_r.L = tmp
						tmp = node_r
				break
	return root


O_seq=[] # stack to store temporary solutions
solutions = [] # final solutions

def cover_column(column_header):
	# covers the column header
	column_header.R.L = column_header.L
	column_header.L.R = column_header.R

	i = column_header.D
	while i is not column_header:
		j = i.R
		while j is not i:
			j.D.U = j.U
			j.U.D = j.D
			j.C.S -= 1
			j = j.R
		i = i.D


def uncover_column(column_header):
	# uncovers the column header
	i = column_header.U
	while i is not column_header:
		j = i.L
		while j is not i:
			j.D.U = j
			j.U.D = j
			j.C.S += 1
			j = j.L
		i = i.U
	column_header.R.L = column_header
	column_header.L.R = column_header



def search(root):
	# recursively searches solutions
	global solutions
	if root.R is root:
		for O in O_seq:
			solution = [O.C.N]
			node = O.R
			while node is not O:
				solution.append(node.C.N)
				node = node.R
			solutions.append(solution)
			# print(solution)
		return 0

	c = root.R
	cover_column(c)
	r = c.D
	while r is not c:
		O_seq.append(r)
		j = r.R
		while j is not r:
			cover_column(j.C)
			j = j.R
		search(root)
		r = O_seq.pop()
		c = r.C
		j = r.L
		while j is not r:
			uncover_column(j.C)
			j = j.L
		r = r.D
	uncover_column(c)
	return 1


# test code:
# if __name__ == "__main__":
# 	# A = np.array([[1,0,1,1],
# 	# 	          [1,0,1,0],
# 	# 	          [0,1,0,1]])
# 	A = np.array([[0,0,1,0,1,1,0],
# 				  [1,0,0,1,0,0,1],
# 				  [0,1,1,0,0,1,0],
# 				  [1,0,0,1,0,0,0],
# 				  [0,1,0,0,0,0,1],
# 				  [0,0,0,1,1,0,1]])

# 	root = mat2linklist(A,string.ascii_uppercase[:7])
# 	search(root)
# 	print(solutions)

