# 0x00-pascal_triangle

## Resources
What is Pascal’s triangle <br>https://www.cuemath.com/algebra/pascals-triangle/<br>

Pascal’s Triangle - Numberphile <br>https://www.youtube.com/watch?feature=shared&v=0iMtlus-afo<br>

What are Python Algorithms <br>https://builtin.com/data-science/python-algorithms<br>

## Additional Resources
Mock Technical Interview <br>https://www.youtube.com/watch?feature=shared&v=1qw5ITr3k9E<br>

# TASKS

## 0-pascal_triangle.py
Create a function def pascal_triangle(n): that returns a list of lists of integers representing the Pascal’s triangle of n:

Returns an empty list if n <= 0
You can assume n will be always an intege

	guillaume@ubuntu:~/0x00$ cat 0-main.py
	#!/usr/bin/python3
	"""
	0-main
	"""
	pascal_triangle = __import__('0-pascal_triangle').pascal_triangle

	def print_triangle(triangle):
	    """
	    Print the triangle
	    """
	    for row in triangle:
		print("[{}]".format(",".join([str(x) for x in row])))


	if __name__ == "__main__":
	    print_triangle(pascal_triangle(5))

	guillaume@ubuntu:~/0x00$ 
	guillaume@ubuntu:~/0x00$ ./0-main.py
	[1]
	[1,1]
	[1,2,1]
	[1,3,3,1]
	[1,4,6,4,1]
	guillaume@ubuntu:~/0x00$ 
