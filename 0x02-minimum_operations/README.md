# 0x02-minimum_operations

## RESOURCES
Dynamic Programming (GeeksforGeeks) => <br>https://www.geeksforgeeks.org/dynamic-programming/<br>
How to optimize Python code => <br>https://stackify.com/how-to-optimize-python-code/<br>
Greedy Algorithms (GeeksforGeeks) => <br>https://www.geeksforgeeks.org/greedy-algorithms/<br>
Python Functions (Python Official Documentation) => <br>https://docs.python.org/3/tutorial/controlflow.html#defining-functions<br>

## 0-minoperations.py
	In a text file, there is a single character H. Your text editor can execute only two operations in this file: Copy All and Paste. Given a number n, write a method that calculates the fewest number of operations needed to result in exactly n H characters in the file.

		- Prototype: def minOperations(n)
		- Returns an integer
		- If n is impossible to achieve, return 0
	Example:

	n = 9

	H => Copy All => Paste => HH => Paste =>HHH => Copy All => Paste => HHHHHH => Paste => HHHHHHHHH

	Number of operations: 6

